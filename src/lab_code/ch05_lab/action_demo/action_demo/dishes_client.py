"""DoDishes Action Client — 发送洗碗任务并接收进度反馈"""
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from action_demo_interfaces.action import DoDishes


class DoDishesClient(Node):
    def __init__(self):
        super().__init__('do_dishes_client')
        self.client = ActionClient(self, DoDishes, 'do_dishes')

    def send_goal(self, total_dishes):
        self.client.wait_for_server()
        goal = DoDishes.Goal()
        goal.total_dishes = total_dishes
        self.client.send_goal_async(
            goal, feedback_callback=self.feedback_cb
        ).add_done_callback(self.goal_response_cb)

    def goal_response_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('目标被拒绝'); return
        self.get_logger().info('目标已接受')
        goal_handle.get_result_async().add_done_callback(self.result_cb)

    def feedback_cb(self, fb_msg):
        p = fb_msg.feedback.progress
        self.get_logger().info(f'反馈: {p:.0%} (盘子 {fb_msg.feedback.current_dish})')

    def result_cb(self, future):
        r = future.result().result
        self.get_logger().info(f'完成: {r.cleaned_dishes}个, 成功:{r.success}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = DoDishesClient()
    node.send_goal(5)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
