# hello_pkg

第 2 章实验包：节点与日志练习。

- 包类型：`ament_python`
- ROS 2 Jazzy

## 简介

本包用于练习 ROS 2 节点的创建、定时器使用与日志 API。包含三个示例节点：基础定时输出、日志分级演示、里程计话题监听。

## 节点 / 可执行说明

| 节点 | 功能 |
| --- | --- |
| `hello_node` | 每秒输出 `"Hello ROS 2!"` 并附带计数 |
| `logger_demo` | 展示 DEBUG / INFO / WARN / ERROR 分级日志、节流日志与一次性输出 |
| `odom_monitor` | 订阅 `/odom` 话题，显示机器人位置 |

## 构建命令

```bash
cd <workspace>
colcon build --symlink-install --packages-select hello_pkg
source /opt/ros/jazzy/setup.bash && source install/setup.bash
```

## 运行步骤

```bash
# 基础节点
ros2 run hello_pkg hello_node

# 日志分级演示
ros2 run hello_pkg logger_demo

# 里程计监听（需先启动 Gazebo 仿真）
ros2 run hello_pkg odom_monitor
```
