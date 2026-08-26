# service_demo

第 4 章实验包：服务通信练习。

- 包类型：`ament_python`
- ROS 2 Jazzy

## 简介

本包用于练习 ROS 2 服务通信。提供 `example_interfaces/srv/AddTwoInts` 服务实现一个简单的两整数相加示例。

## 节点 / 可执行说明

| 节点 | 角色 | 服务 | 类型 |
| --- | --- | --- | --- |
| `server` | 服务端 | `/add_two_ints` | `example_interfaces/srv/AddTwoInts` |
| `client` | 客户端 | `/add_two_ints` | `example_interfaces/srv/AddTwoInts` |

## 构建命令

```bash
cd <workspace>
colcon build --symlink-install --packages-select service_demo
source /opt/ros/jazzy/setup.bash && source install/setup.bash
```

## 运行步骤

```bash
# 终端 1：启动服务端
ros2 run service_demo server

# 终端 2：启动客户端
ros2 run service_demo client

# 验证（任一终端）
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 3, b: 4}"
```
