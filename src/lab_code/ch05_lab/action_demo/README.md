# action_demo

第 5 章实验包：动作通信练习。

- 包类型：`ament_python`
- ROS 2 Jazzy
- 依赖：`action_demo_interfaces`

## 简介

本包演示 ROS 2 Action 通信。服务端提供 `/do_dishes` 动作，使用异步执行回调，每秒反馈进度；客户端发送目标并接收结果。

## 节点 / 可执行说明

| 节点 | 角色 | Action | 说明 |
| --- | --- | --- | --- |
| `server` | 服务端 | `/do_dishes` | 异步 `execute` 回调，每秒发布 feedback |
| `client` | 客户端 | `/do_dishes` | 发送目标，等待结果 |

## 已知问题

本包中 action 的字段名与 `action_demo_interfaces` 中 `DoDishes.action` 的定义不完全匹配，可能需要根据接口定义调整源码后再编译运行。

## 构建命令

```bash
cd <workspace>
colcon build --symlink-install --packages-select action_demo_interfaces action_demo
source /opt/ros/jazzy/setup.bash && source install/setup.bash
```

## 运行步骤

```bash
# 终端 1：启动服务端
ros2 run action_demo server

# 终端 2：启动客户端
ros2 run action_demo client
```
