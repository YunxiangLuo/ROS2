"""hello_ros2: VS Code 调试示例节点 — LifecyclePublisher + QoS + /cmd_vel"""

import rclpy
from rclpy.lifecycle import LifecycleNode, TransitionCallbackReturn
from geometry_msgs.msg import Twist

from rclpy.qos import (
    QoSProfile,
    HistoryPolicy,
    ReliabilityPolicy,
    DurabilityPolicy,
)


class HelloRos2Node(LifecycleNode):
    def __init__(self):
        super().__init__('hello_ros2_lifecycle')

        self.pub = None
        self.timer = None
        self.count = 0
        self.active = False

        self.get_logger().info('Lifecycle 节点已创建，等待 configure。')

    def on_configure(self, state):
        self.get_logger().info('on_configure: 配置节点资源。')

        cmd_vel_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )
        self.pub = self.create_lifecycle_publisher(
            Twist,
            '/cmd_vel',
            cmd_vel_qos
        )

        self.timer = self.create_timer(0.5, self.timer_callback)

        self.get_logger().info('on_configure: LifecyclePublisher 和定时器创建完成。')

        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state):
        self.get_logger().info('on_activate: 激活节点，允许发布 /cmd_vel。')

        ret = super().on_activate(state)

        if ret == TransitionCallbackReturn.SUCCESS:
            self.active = True
            self.get_logger().info('on_activate: 节点已激活。')

        return ret

    def on_deactivate(self, state):
        self.get_logger().info('on_deactivate: 停用节点，停止发布 /cmd_vel。')

        self.active = False

        ret = super().on_deactivate(state)

        return ret

    def on_cleanup(self, state):
        self.get_logger().info('on_cleanup: 清理节点资源。')

        self.active = False

        if self.timer is not None:
            self.destroy_timer(self.timer)
            self.timer = None

        if self.pub is not None:

            try:
                self.destroy_lifecycle_publisher(self.pub)
            except AttributeError:
                self.destroy_publisher(self.pub)
            self.pub = None

        self.count = 0

        return TransitionCallbackReturn.SUCCESS

    def timer_callback(self):
        if not self.active:
            return

        msg = Twist()
        msg.linear.x = 0.1
        msg.angular.z = 0.0

        self.pub.publish(msg)

        self.count += 1
        self.get_logger().info(
            f'第 {self.count} 次发布 /cmd_vel: '
            f'linear.x={msg.linear.x:.2f}, angular.z={msg.angular.z:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = HelloRos2Node()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('用户中断，节点退出。')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()