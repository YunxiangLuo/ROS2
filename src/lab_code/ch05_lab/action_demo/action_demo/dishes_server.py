"""DoDishes Action Server — 模拟洗碗任务，支持进度反馈和取消"""
import asyncio
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from action_demo_interfaces.action import DoDishes


class DoDishesServer(Node):
    def __init__(self):
        super().__init__('do_dishes_server')
        self.action_server = ActionServer(
            self, DoDishes, 'do_dishes',
            execute_callback=self.execute,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)

    def goal_callback(self, goal_request):
        self.get_logger().info(f'收到目标: {goal_request.total_dishes} 个盘子')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('收到取消请求')
        return CancelResponse.ACCEPT

    async def execute(self, goal_handle):
        total = goal_handle.request.total_dishes
        fb = DoDishes.Feedback()
        for i in range(1, total + 1):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result = DoDishes.Result()
                result.cleaned_dishes = i - 1
                result.success = False
                return result
            await asyncio.sleep(1.0)
            fb.progress = i / total
            fb.current_dish = i
            goal_handle.publish_feedback(fb)
            self.get_logger().info(f'进度: {fb.progress:.0%} ({i}/{total})')
        goal_handle.succeed()
        result = DoDishes.Result()
        result.cleaned_dishes = total
        result.success = True
        return result


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(DoDishesServer())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
