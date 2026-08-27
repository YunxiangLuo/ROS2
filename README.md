# Ch01 生命周期节点实验

本章把最小 ROS 2 Python 脚本整理为正式的 `lifecycle_demo` 包，演示 `LifecycleNode`、生命周期发布器、QoS 和 `/cmd_vel` 发布。默认启动后节点处于 `unconfigured`，只有完成 `configure` 和 `activate` 后才会发布速度消息。

## 安装

安装 ROS 2 Jazzy，并在每个终端加载 ROS 环境：

```bash
source /opt/ros/jazzy/setup.bash
```

Windows 或其他 ROS 2 发行版请使用本机实际的 ROS 环境，不要把发行版路径写死在工作区配置中。

## 构建

在工作区根目录执行：

```bash
colcon build --symlink-install --packages-select lifecycle_demo
source install/setup.bash
```

## 运行

手动练习生命周期转换：

```bash
ros2 run lifecycle_demo hello_node
ros2 lifecycle get /hello_ros2_lifecycle
ros2 lifecycle set /hello_ros2_lifecycle configure
ros2 lifecycle set /hello_ros2_lifecycle activate
```

一次启动并自动激活：

```bash
ros2 launch lifecycle_demo lifecycle_demo.launch.py autostart:=true
```

## 验证

另开终端查看节点状态和速度消息：

```bash
ros2 lifecycle get /hello_ros2_lifecycle
ros2 topic echo /cmd_vel --once
colcon test --packages-select lifecycle_demo
colcon test-result --verbose
```

预期状态为 `active`，`/cmd_vel` 中的 `linear.x` 为 `0.1`。本章的节点测试不启动 Gazebo 或 RViz。

## 运行结果

实际运行结果截图：

![生命周期节点运行结果](docs/images/result.png)
