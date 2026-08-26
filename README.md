# robot_sim_demo

独立的 ROS 2 Gazebo Sim 仿真包：使用 `src/robot_sim_demo/wheeltec_robot_urdf` 中的 Wheeltec Mini AKM 机器人模型，以及 ISCAS_Museum 场景。

## 目录

```text
ROS2/
└── src/robot_sim_demo/
    ├── launch/       Gazebo 启动文件
    ├── config/       ROS-Gazebo 话题桥配置
    ├── gui/          Gazebo GUI 配置
    ├── models/       机器人、博物馆和地面模型及全部材质
    ├── wheeltec_robot_urdf/ Wheeltec URDF 和 STL 资源
    ├── rviz/         可选 RViz 配置（默认不启动）
    ├── urdf/         机器人 TF 模型
    └── worlds/       ISCAS_Museum 世界文件
```

## 环境

建议使用 ROS 2 Jazzy、Gazebo Sim Harmonic 和 WSL2/WSLg。安装至少需要：

```bash
sudo apt install -y ros-jazzy-ros-gz-sim ros-jazzy-ros-gz-bridge \
  ros-jazzy-ros-gz-image ros-jazzy-robot-state-publisher \
  ros-jazzy-rviz2 python3-colcon-common-extensions
```

## 构建

在本目录执行：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select robot_sim_demo
source install/setup.bash
```

## 启动

只启动 Gazebo 的 3D Scene 窗口、机器人和传感器桥；不启动 RViz 或其它可视化窗口，并自动驱动机器人巡航：

```bash
ros2 launch robot_sim_demo gazebo2.launch.py
```

Gazebo 窗口使用深色高对比主题，只保留 3D Scene 视图，并显示激光雷达射线。

常用选项：

```bash
ros2 launch robot_sim_demo gazebo2.launch.py gui:=false rviz:=false
ros2 launch robot_sim_demo gazebo2.launch.py spawn_x:=0.0 spawn_y:=0.0 spawn_z:=0.03 spawn_yaw:=0.0
ros2 launch robot_sim_demo gazebo2.launch.py drive:=false
```

底盘运动接口：

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.15}, angular: {z: 0.0}}"
ros2 topic echo /odom --once
```

## Gazebo 运动演示

![机器人在 ISCAS Museum 中巡检](media/robot_patrol.gif)

启动后可检查：

```bash
ros2 topic echo /clock --once
ros2 topic echo /scan --once
ros2 topic echo /camera/camera_info --once
ros2 topic hz /camera/image_raw
gz model -l
```

该 Wheeltec Mini AKM 机器人现在使用 Gazebo Sim Harmonic 原生 `DiffDrive` 系统，初始位置在博物馆场景中心的开放区域，支持 `/cmd_vel`、`/odom` 和 `/tf`。默认巡航节点发布四段直行与转弯动作；设置 `drive:=false` 后可手动控制。Gazebo Sim 当前只输出相机图像，因此包内的 `camera_info_publisher` 按 SDF 中的 320x180、1.0472 rad 参数发布匹配的 `/camera/camera_info`，并在收到 `/clock` 后使用仿真时间戳。
