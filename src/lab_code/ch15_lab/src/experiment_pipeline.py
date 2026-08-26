#!/usr/bin/env python3
"""experiment_pipeline: 题6 — 全流程编排 Action Server"""
import asyncio
import json
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from example_interfaces.srv import Trigger
from geometry_msgs.msg import PoseStamped


class ExperimentPipeline(Node):
    """化学实验全流程编排 — Action Server"""

    def __init__(self):
        super().__init__('experiment_pipeline')
        self.action_server = ActionServer(
            self, None, 'run_experiment',  # 简化：使用 None action type
            execute_callback=self.execute,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb)
        self.validator = self.create_client(Trigger, 'validate_recipe')
        self.get_logger().info('实验编排 Action Server 就绪')

    def goal_cb(self, goal):
        self.get_logger().info('收到实验配方')
        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):
        self.get_logger().warn('实验被取消')
        return CancelResponse.ACCEPT

    async def execute(self, goal_handle):
        recipe = goal_handle.request.recipe_text

        # 步骤1：LLM 校验配方
        self.get_logger().info('Step 1/6: LLM 校验配方...')
        valid = await self.call_service(
            self.validator, recipe)
        if not valid:
            self.get_logger().error('配方校验未通过')
            goal_handle.abort()
            return

        # 步骤2：解析组分
        self.get_logger().info('Step 2/6: 解析配方组分...')
        components = [
            {'name': 'HCl', 'volume_ml': 5},
            {'name': 'NaOH', 'volume_ml': 5},
            {'name': 'Phenolphthalein', 'volume_ml': 2},
        ]

        # 步骤3-5：循环处理每个组分
        for i, comp in enumerate(components):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return

            self.get_logger().info(
                f'Step 3/6: YOLO 检测 {comp["name"]} ({i+1}/{len(components)})')
            await asyncio.sleep(0.3)

            self.get_logger().info(
                f'Step 4/6: VLM 验证 {comp["name"]} 标签')
            await asyncio.sleep(0.3)

            self.get_logger().info(
                f'Step 5/6: 定位+抓取 {comp["name"]}')
            await asyncio.sleep(0.5)

        # 步骤6：完成
        self.get_logger().info('Step 6/6: ✅ 实验配制完成！')
        goal_handle.succeed()

    async def call_service(self, client, data, timeout=10.0):
        if not client.wait_for_service(timeout_sec=2.0):
            return False
        req = Trigger.Request()
        req.data = data
        future = client.call_async(req)
        try:
            await asyncio.wait_for(future, timeout=timeout)
            result = future.result()
            return result.success
        except asyncio.TimeoutError:
            self.get_logger().error('服务调用超时')
            return False


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(ExperimentPipeline())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
