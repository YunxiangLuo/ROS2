# robot_sim_demo

ISCAS Museum Gazebo Sim 仿真包：使用 Wheeltec Mini AKM 机器人模型在 ISCAS Museum 场景中进行安全巡检仿真。

## 目录结构

```text
src/robot_sim_demo/
├── launch/                    Gazebo 启动文件
│   └── gazebo2.launch.py      主启动入口
├── config/
│   └── gazebo2_bridge.yaml    ROS-Gazebo 话题桥配置
├── gui/
│   └── museum.gui.config      Gazebo GUI 配置（顶视 3D Scene）
├── models/
│   ├── wheeltec_robot/         Wheeltec Mini AKM 机器人 SDF 模型
│   ├── ISCAS_Museum/           博物馆场景模型（含 DAE 网格和纹理）
│   ├── ISCAS_groundplane/      地面模型
│   └── campus_patrol_robot/    备用巡逻机器人模型
├── wheeltec_robot_urdf/        Wheeltec URDF 和 STL 网格资源
├── worlds/
│   └── museum.sdf             ISCAS Museum 世界文件
├── rviz/
│   └── museum.rviz            RViz 配置（默认不启动）
├── urdf/
│   └── campus_patrol_robot.urdf
└── robot_sim_demo/
    ├── camera_info_publisher.py  相机内参发布节点
    └── patrol_driver.py          巡航驱动节点
```

## 环境

- ROS 2 Jazzy
- Gazebo Sim Harmonic (v8)
- WSL2 / WSLg

```bash
sudo apt install -y ros-jazzy-ros-gz-sim ros-jazzy-ros-gz-bridge \
  ros-jazzy-ros-gz-image ros-jazzy-robot-state-publisher \
  ros-jazzy-rviz2 python3-colcon-common-extensions
```

## 构建

```bash
cd robot_sim_demo
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select robot_sim_demo
source install/setup.bash
```

## 启动

### 默认启动（GUI + 自动巡航）

```bash
ros2 launch robot_sim_demo gazebo2.launch.py
```

启动 Gazebo 3D Scene 窗口、Wheeltec 机器人、传感器桥和自动巡航。

### 常用选项

```bash
# 无 GUI（headless）
ros2 launch robot_sim_demo gazebo2.launch.py gui:=false

# 不启动 RViz（默认已关闭）
ros2 launch robot_sim_demo gazebo2.launch.py rviz:=false

# 不自动巡航（手动控制 /cmd_vel）
ros2 launch robot_sim_demo gazebo2.launch.py drive:=false

# 自定义生成位置
ros2 launch robot_sim_demo gazebo2.launch.py spawn_x:=0.0 spawn_y:=0.0 spawn_z:=0.03 spawn_yaw:=0.0

# 自定义巡航速度
ros2 launch robot_sim_demo gazebo2.launch.py drive_linear_speed:=0.18 drive_angular_speed:=0.55
```

### Launch 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `gui` | `true` | 启动 Gazebo GUI |
| `rviz` | `false` | 启动 RViz2 |
| `spawn_robot` | `true` | 在场景中生成机器人 |
| `drive` | `true` | 启动自动巡航节点 |
| `drive_linear_speed` | `0.18` | 巡航线速度 (m/s) |
| `drive_angular_speed` | `0.55` | 巡航角速度 (rad/s) |
| `drive_loop` | `true` | 循环巡航 |
| `world` | `museum.sdf` | 世界文件路径 |
| `spawn_x/y/z/yaw` | `0/0/0.03/0` | 机器人生成位姿 |
| `use_sim_time` | `true` | 使用仿真时钟 |
| `gz_partition` | `robot_sim_demo` | Gazebo 分区名 |

## 话题接口

| 话题 | 类型 | 方向 | 说明 |
|------|------|------|------|
| `/cmd_vel` | `geometry_msgs/Twist` | ROS→Gazebo | 底盘速度命令 |
| `/odom` | `nav_msgs/Odometry` | Gazebo→ROS | 里程计 |
| `/scan` | `sensor_msgs/LaserScan` | Gazebo→ROS | 激光雷达 |
| `/tf` | `tf2_msgs/TFMessage` | 双向 | 坐标变换 |
| `/clock` | `rosgraph_msgs/Clock` | Gazebo→ROS | 仿真时钟 |
| `/camera/image_raw` | `sensor_msgs/Image` | Gazebo→ROS | 相机图像 |
| `/camera/camera_info` | `sensor_msgs/CameraInfo` | ROS 节点 | 相机内参（320x180, FOV 60°） |

## 手动控制

```bash
# 启动仿真（不自动巡航）
ros2 launch robot_sim_demo gazebo2.launch.py drive:=false

# 发送速度命令
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.15}, angular: {z: 0.0}}"

# 查看里程计
ros2 topic echo /odom --once
```

## 验证

```bash
ros2 topic echo /clock --once
ros2 topic echo /scan --once
ros2 topic echo /camera/camera_info --once
ros2 topic hz /camera/image_raw
```

## 测试

```bash
cd src/robot_sim_demo
python3 -m pytest test/ -v
```

7 项测试全部通过：检查必需文件存在性、SDF/URDF 格式正确性、世界文件引用、Launch 引用、相机内参匹配、DiffDrive 插件配置和 Wheeltec 模型网格引用。

## 截图录制

```bash
# 录制 Gazebo 3D Scene 帧（需 Gazebo GUI 运行中）
bash tools/record_gazebo_scene.sh <时长秒> <帧率> <输出目录> <分区名>

# 示例：录制 16 秒，6 FPS
bash tools/record_gazebo_scene.sh 16 6
```

## 机器人模型

Wheeltec Mini AKM 机器人使用 Gazebo Sim Harmonic 原生 `DiffDrive` 系统：
- 初始位置：场景中心开放区域 `(0, 0, 0.03)`
- 坐标系：`base_link`（底盘）→ `laser_link`（激光雷达）→ `camera_link`（相机）
- 配色：石墨黑车体、黑色轮胎、银色轮毂/RGB-D 外壳、青色状态环、安全橙前部
- 两个原始门洞已用与相邻墙面对齐的墙体封闭
