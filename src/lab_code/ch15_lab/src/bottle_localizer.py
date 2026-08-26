#!/usr/bin/env python3
"""bottle_localizer: 题4 — TF 解算试剂瓶 3D 位姿"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from tf2_ros import TransformBroadcaster, Buffer, TransformListener, TransformStamped


class BottleLocalizer(Node):
    def __init__(self):
        super().__init__('bottle_localizer')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.tf_broadcaster = TransformBroadcaster(self)
        # 模拟广播 AR 标签 TF
        self.create_timer(1.0, self.broadcast_markers)
        self.create_timer(2.0, self.localize_bottles)
        self.get_logger().info('TF 空间定位就绪')

    def broadcast_markers(self):
        """广播 4 个试剂瓶 AR 标签的 TF frame"""
        markers = [
            ('ar_marker_hcl',            -0.3, 0.2, 0.1),
            ('ar_marker_naoh',            0.3, -0.2, 0.1),
            ('ar_marker_h2o',             0.5, 0.3, 0.1),
            ('ar_marker_phenolphthalein', -0.5, 0.0, 0.1),
        ]
        for frame_id, x, y, z in markers:
            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = 'base_link'
            t.child_frame_id = frame_id
            t.transform.translation.x = x
            t.transform.translation.y = y
            t.transform.translation.z = z
            t.transform.rotation.w = 1.0
            self.tf_broadcaster.sendTransform(t)

    def localize_bottles(self):
        """查询所有 AR 标签的全局位姿"""
        marker_frames = [
            'ar_marker_hcl', 'ar_marker_naoh',
            'ar_marker_h2o', 'ar_marker_phenolphthalein']
        for fid in marker_frames:
            try:
                t = self.tf_buffer.lookup_transform(
                    'base_link', fid, rclpy.time.Time())
                self.get_logger().info(
                    f'{fid}: x={t.transform.translation.x:.3f}, '
                    f'y={t.transform.translation.y:.3f}, '
                    f'z={t.transform.translation.z:.3f}')
            except Exception as e:
                self.get_logger().debug(f'{fid}: 暂未检测到')


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(BottleLocalizer())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
