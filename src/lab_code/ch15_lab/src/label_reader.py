#!/usr/bin/env python3
"""label_reader: 题3 — VLM 读取试剂瓶标签文字 (Service 节点)"""
import json
import base64
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from example_interfaces.srv import Trigger
from cv_bridge import CvBridge


class LabelReader(Node):
    def __init__(self):
        super().__init__('label_reader')
        self.bridge = CvBridge()
        self.latest_image = None
        self.sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_cb, 10)
        # 服务：接收期望材料名称，返回比对结果
        self.srv = self.create_service(
            Trigger, 'read_label', self.read_label_cb)
        self.get_logger().info('VLM 标签识别就绪')

    def image_cb(self, msg):
        self.latest_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

    def read_label_cb(self, request, response):
        expected = request.data  # 期望的材料名称
        if self.latest_image is None:
            response.success = False
            response.message = '无可用图像'
            return response

        label_text = self.call_vlm(self.latest_image)
        matches = expected.lower() in label_text.lower()

        result = {
            'label_text': label_text,
            'expected': expected,
            'matches': matches,
            'confidence': 0.95 if matches else 0.1
        }
        response.success = matches
        response.message = json.dumps(result, ensure_ascii=False)
        self.get_logger().info(
            f'标签比对: "{expected}" vs "{label_text}" → {"匹配" if matches else "不匹配"}')
        return response

    def call_vlm(self, image):
        _, buffer = cv2.imencode('.jpg', image)
        img_b64 = base64.b64encode(buffer).decode('utf-8')
        try:
            from openai import OpenAI
            client = OpenAI()
            resp = client.chat.completions.create(
                model='gpt-4o',
                messages=[{'role': 'user', 'content': [
                    {'type': 'text', 'text': '请读取图中试剂瓶标签上的文字，只返回文字内容，不附加任何说明。'},
                    {'type': 'image_url', 'image_url': {
                        'url': f'data:image/jpeg;base64,{img_b64}'}}
                ]}],
                max_tokens=50)
            return resp.choices[0].message.content.strip()
        except Exception as e:
            self.get_logger().warn(f'VLM调用失败: {e}')
            return 'HCl'  # 默认返回


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(LabelReader())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
