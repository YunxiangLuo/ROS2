import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point


class GpsPublisher(Node):
    """模拟GPS传感器数据发布节点 — 周期发布Point消息"""

    def __init__(self):
        super().__init__('gps_publisher')
        self.publisher = self.create_publisher(
            Point,
            '/gps_position',
            10)
        self.timer = self.create_timer(1.0, self.publish_position)
        self.x = 0.0

    def publish_position(self):
        msg = Point()
        msg.x = self.x
        msg.y = 2 * self.x + 1
        msg.z = 0.0
        self.publisher.publish(msg)
        self.get_logger().info(
            f'发布 GPS 位置: x={msg.x:.2f}, y={msg.y:.2f}')
        self.x += 1.0


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(GpsPublisher())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
