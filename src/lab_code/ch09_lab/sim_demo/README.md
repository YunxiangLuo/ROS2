# sim_demo

第 9 章实验包：Gazebo 仿真练习。

- 包类型：`ament_python`
- ROS 2 Jazzy
- 依赖：`gazebo_ros`（经典 Gazebo）

## 简介

本包用于练习在 Gazebo 中启动机器人仿真。Launch 文件负责启动 Gazebo、spawn xbot 机器人，并可选启动 RViz2。本包无可执行节点。

## Launch 文件

| 文件 | 功能 |
| --- | --- |
| `sim_bringup.launch.py` | 启动 Gazebo + spawn xbot 机器人 + 可选 RViz2 |

### Launch 参数

| 参数 | 说明 |
| --- | --- |
| `use_gazebo` | 是否启动 Gazebo |
| `use_rviz` | 是否启动 RViz2 |
| `world` | Gazebo 世界文件路径 |

## 环境说明

本包依赖经典 Gazebo（`gazebo_ros`），但当前运行环境使用 Gazebo Sim Harmonic。运行前请确认 Gazebo 版本兼容性。

## 构建命令

```bash
cd <workspace>
colcon build --symlink-install --packages-select sim_demo
source /opt/ros/jazzy/setup.bash && source install/setup.bash
```

## 运行步骤

```bash
ros2 launch sim_demo sim_bringup.launch.py
```
