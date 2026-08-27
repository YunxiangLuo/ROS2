# 第1章 实验代码 — ROS2 基础与 URDF 模型

本章实验围绕 ROS2 节点创建、话题通信和 URDF 模型展示展开。

## 文件说明

| 文件 | 用途 | 运行方式 |
|------|------|----------|
| `hello_arm_node.py` | ROS2 节点基础示例。创建 `JointState` 发布器，模拟关节运动并发布到 `/joint_states` 话题 | `python3 hello_arm_node.py` |
| `arm_joints_pub1.py` | 关节状态发布器。发布 8 个关节的 `JointState` 消息，让 `arm_2_joint` 在 ±1.5 rad 范围内往复摆动 | `python3 arm_joints_pub1.py` |
| `arm_gripper.py` | 机械臂+手爪联动演示。关节 1、4 和手爪关节循环往复运动 | `python3 arm_gripper.py` |
| `gripper_open_close.py` | 手爪张开/闭合演示。`gripper_1_joint` 和 `gripper_2_joint` 同步开合 | `python3 gripper_open_close.py` |
| `checker3` | 串口设备检测工具。检测激光雷达、机械臂、PCB 板等 USB 串口设备，自动写入 udev 端口映射规则 | 详见 `README.md` |

## 运行说明

启动机器人状态发布器（在另一个终端）：

```bash
# 如果有 URDF 模型
ros2 launch robot_state_publisher robot_state_publisher.launch.py
```

运行关节发布脚本：

```bash
cd lab_code/ch01_lab/
python3 arm_joints_pub1.py

# 在 RViz2 中添加 /joint_states 话题查看关节运动
# 或使用命令行查看：
ros2 topic echo /joint_states
```

## checker3 使用说明

`checker3` 是 Linux 下的串口检测脚本，用于自动检测和配置连接到开发板的 USB 串口设备。详见 `checker3` 目录下的 README。
