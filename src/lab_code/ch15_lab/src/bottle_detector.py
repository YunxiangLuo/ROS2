#!/usr/bin/env python3
"""bottle_detector: 题2 — YOLO 检测 Gazebo 中的试剂瓶 (Topic 节点)"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose
from cv_bridge import CvBridge


class BottleDetector(Node):
    def __init__(self):
        super().__init__('bottle_detector')
        self.bridge = CvBridge()
        self.sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
        self.det_pub = self.create_publisher(
            Detection2DArray, '/bottle_detections', 10)
        self.model = self.load_model()
        self.get_logger().info('YOLO 试剂瓶检测就绪')

    def load_model(self):
        try:
            from ultralytics import YOLO
            self.get_logger().info('加载 YOLOv8n 模型...')
            return YOLO('yolov8n.pt')
        except ImportError:
            self.get_logger().warn('ultralytics 未安装，使用模拟检测')
            return None

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        if self.model is not None:
            results = self.model(cv_image, conf=0.3, classes=[39])  # class 39=bottle
            detections = self.yolo_to_ros(results, msg.header)
        else:
            detections = Detection2DArray()
            detections.header = msg.header

        self.det_pub.publish(detections)

    def yolo_to_ros(self, results, header):
        det_array = Detection2DArray()
        det_array.header = header
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])

                det = Detection2D()
                det.header = header
                det.bbox.center.x = (x1 + x2) / 2.0
                det.bbox.center.y = (y1 + y2) / 2.0
                det.bbox.size_x = float(x2 - x1)
                det.bbox.size_y = float(y2 - y1)

                hyp = ObjectHypothesisWithPose()
                hyp.hypothesis.class_id = 'bottle'
                hyp.hypothesis.score = conf
                det.results.append(hyp)

                det_array.detections.append(det)
                self.get_logger().info(
                    f'检测到试剂瓶: conf={conf:.2f}, '
                    f'中心=({det.bbox.center.x:.0f},{det.bbox.center.y:.0f})')
        return det_array


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(BottleDetector())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
