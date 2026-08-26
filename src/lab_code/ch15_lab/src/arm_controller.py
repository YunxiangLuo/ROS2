#!/usr/bin/env python3
"""arm_controller: 题5 — MoveIt2 机械臂 pick→transfer→pour"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped


class ArmController(Node):
    """机械臂控制器 — pick → transfer → pour 流程"""

    def __init__(self):
        super().__init__('arm_controller')
        self.get_logger().info('机械臂控制器就绪 (模拟模式)')

    def execute_pick_and_place(self, target_pose, material_name):
        self.get_logger().info(f'=== 开始抓取 {material_name} ===')

        # 步骤1：预抓取位姿（目标上方 0.1m）
        pre_grasp = PoseStamped()
        pre_grasp.pose = target_pose.pose
        pre_grasp.pose.position.z += 0.1
        self.plan_move(pre_grasp, f'移动到 {material_name} 上方')

        # 步骤2：下降到抓取位姿
        self.plan_move(target_pose, f'抓取 {material_name}')
        self.close_gripper()

        # 步骤3：转移到倾倒位置（试管上方 0.5, 0, 0.4）
        pour_pose = PoseStamped()
        pour_pose.pose.position.x = 0.5
        pour_pose.pose.position.y = 0.0
        pour_pose.pose.position.z = 0.4
        self.plan_move(pour_pose, '转移到试管上方')

        # 步骤4：执行倾倒（2秒）
        self.pour(duration_sec=2.0)
        self.open_gripper()

        self.get_logger().info(f'✅ {material_name} 加料完成')

    def plan_move(self, pose, description):
        self.get_logger().info(f'规划: {description} → ({pose.pose.position.x:.2f}, {pose.pose.position.y:.2f})')
        # 实际使用 MoveItPy:
        # from moveit_py import MoveItPy
        # moveit = MoveItPy(node=self)
        # result = moveit.plan_and_execute(pose)

    def close_gripper(self):
        self.get_logger().info('闭合夹爪')

    def open_gripper(self):
        self.get_logger().info('打开夹爪')

    def pour(self, duration_sec):
        self.get_logger().info(f'倾倒 {duration_sec}s...')
        import time
        time.sleep(duration_sec)


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(ArmController())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
