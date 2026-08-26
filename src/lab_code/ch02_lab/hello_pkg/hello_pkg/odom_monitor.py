#!/usr/bin/env python3
"""odom_monitor: 监听 XBot-U /odom 话题，实时显示机器人位置"""
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry


class OdomMonitor(Node):
    def __init__(self):
        super().__init__('odom_monitor')
        self.sub = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)

    def odom_callback(self, msg):
        pos = msg.pose.pose.position
        orient = msg.pose.pose.orientation
        yaw = 2.0 * orient.z if abs(orient.z) < 1.0 else 0.0
        self.get_logger().info(
            f'XBot-U 位置: x={pos.x:.2f}m, y={pos.y:.2f}m, 航向={yaw:.2f}rad')


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(OdomMonitor())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
