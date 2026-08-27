# 第45章 综合项目：城区自动驾驶

基于ROS2与CARLA的城区自动驾驶综合项目。

## 项目概述

在CARLA Town03城区环境中，自车从起点A自动驾驶至终点B，全程约1.8km，需完成6个红绿灯路口、3处人行横道的安全通行，并避让10~20个动态交通参与者。

## 环境要求

- **操作系统**：Ubuntu 20.04 / 22.04
- **ROS2**：Humble / Galactic
- **CARLA**：0.9.13+
- **Python**：3.8+
- **依赖**：见 `requirements.txt`

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 编译工作空间

```bash
cd ~/ros2_autonomous_driving
colcon build --symlink-install
source install/setup.bash
```

### 3. 启动CARLA

```bash
./CarlaUE4.sh -quality-level=Low -prefernvidia
```

### 4. 一键启动演示

```bash
./town_demo.sh
```

### 5. 运行测试

```bash
./run_all_tests.sh
```

## 项目结构

```
lab_code/ch45_lab/
├── README.md                 # 本文件
├── requirements.txt
├── main_pipeline.py          # 主自动驾驶管线节点
├── town_demo.sh              # 一键启动脚本
├── run_all_tests.sh          # 测试套件
├── config/
│   ├── vehicle_params.yaml
│   ├── control_params.yaml
│   ├── perception_params.yaml
│   └── planning_params.yaml
├── launch/
│   └── start_driving.launch.py
├── carla_sensor_driver/
│   ├── __init__.py
│   ├── sensor_driver.py
│   └── sensor_config.py
├── perception_node/
│   ├── __init__.py
│   ├── perception_node.py
│   ├── obstacle_detector.py
│   ├── lane_detector.py
│   └── traffic_light_detector.py
├── localization_node/
│   ├── __init__.py
│   ├── localization_node.py
│   └── ekf_localizer.py
├── planning_node/
│   ├── __init__.py
│   ├── planning_node.py
│   ├── global_planner.py
│   ├── behavior_planner.py
│   ├── motion_planner.py
│   └── traffic_light_planner.py
├── control_node/
│   ├── __init__.py
│   ├── control_node.py
│   ├── pure_pursuit.py
│   └── pid_controller.py
├── safety_monitor_node/
│   ├── __init__.py
│   ├── safety_monitor.py
│   └── collision_predictor.py
└── test/
    ├── test_sensor_driver.py
    ├── test_pure_pursuit.py
    ├── test_pid.py
    ├── test_obstacle_detection.py
    ├── test_behavior_planner.py
    ├── test_traffic_light_detector.py
    ├── test_traffic_light_planner.py
    └── test_integration.py
```

## 模块描述

| 模块 | 包名 | 职责 |
|------|------|------|
| 传感器驱动 | `carla_sensor_driver` | 从CARLA采集传感器数据并发布到ROS2话题 |
| 感知 | `perception_node` | 障碍物检测、车道线检测、交通灯检测 |
| 定位 | `localization_node` | GNSS+IMU融合定位 |
| 规划 | `planning_node` | 全局路径规划、行为规划、运动规划、交通灯规划 |
| 控制 | `control_node` | Pure Pursuit横向控制、PID纵向控制 |
| 安全监控 | `safety_monitor_node` | 碰撞预警、偏离预警、紧急制动 |
| 系统启动 | `autonomous_driving_bringup` | 配置文件、启动文件、可视化配置 |

## 四阶段开发

1. **路径跟踪**：Pure Pursuit + PID，实现A→B基本行驶
2. **避障**：LiDAR聚类、视觉车道线、Frenet轨迹规划
3. **交通灯**：视觉检测、停车/通行决策、精确停车
4. **完整闭环**：集成安全监控、系统诊断、多场景验证

## 验收标准

| 指标 | 阈值 |
|------|------|
| 碰撞次数 | = 0 |
| 红灯停车率 | 100% |
| 路线完成率 | ≥ 95% |
| 平均速度 | ≥ 15 km/h |
| 完成任务时间 | ≤ 10 min |
| 横向跟踪误差 | < 0.5 m |
| 停车位置精度 | < 1.0 m |

---

## 安装与编译

```bash
pip install numpy pyyaml
# ROS2 环境完整编译(引擎子包就位后):
cd <工作空间根目录> && colcon build --symlink-install && source install/setup.bash
```

## 运行方法

```bash
# 一键启动(CARLA + ros-bridge + 管线):
bash town_demo.sh
# 测试套件(需 ROS2/CARLA, test/ 子包就位后):
bash run_all_tests.sh
# 主管线单节点:
python main_pipeline.py
```

## 测试方法与运行结果

主管线模块结构与降级行为已纳入统一测试:

```text
$ cd src && python -m pytest lab_code/tests/test_ch45_pipeline.py -v
lab_code/tests/test_ch45_pipeline.py::test_module_importable PASSED
lab_code/tests/test_ch45_pipeline.py::test_pipeline_states_complete PASSED
lab_code/tests/test_ch45_pipeline.py::test_init_modules_degrades_gracefully PASSED
lab_code/tests/test_ch45_pipeline.py::test_enable_callback_toggles_state PASSED
4 passed in 0.05s
```

> 说明: 本机(Windows)未安装 CARLA/ROS2, 无法截取仿真画面,
> 运行结果以**真实终端输出**代替截图。

## 本次修复记录

1. `main_pipeline.py` 模块级导入 6 个不存在的引擎子包
   (`carla_sensor_driver`/`perception_node`/...) 导致文件无法 import, 且
   `std_srvs.srv` 被使用但未导入 → 子包导入移入 `_init_modules` 延迟加载
   (缺失时进入 FAILED 状态优雅降级), 补充 `import std_srvs.srv`;
2. README 原先描述的 `config/`、`launch/`、`test/` 等目录尚未随代码提交,
   待对应章节实现后补充。
