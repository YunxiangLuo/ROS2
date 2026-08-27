# ch44_lab — 安全验证与系统集成实验代码

## 文件结构

```
ch44_lab/
├── README.md              # 本文件
├── safety_monitor.py      # 安全监控节点：碰撞检测 + 偏离检测 + AEB
├── fault_injector.py      # 故障注入器：丢帧/噪声/偏置/延迟/失效
├── integration_test.py    # 集成测试框架：端到端自动化测试
└── eval_metrics.py        # 性能评估工具：指标计算与报告生成
```

## 依赖

```bash
pip install numpy matplotlib pandas scipy
```

ROS2包依赖：
- `rclpy`
- `std_msgs`, `geometry_msgs`, `nav_msgs`
- `visualization_msgs`
- `autoware_auto_perception_msgs`（可选，可用自定义消息替代）

## 快速开始

```bash
# 1. 启动CARLA仿真
./CarlaUE4.sh -quality-level=Low

# 2. 启动ROS2桥接
ros2 launch carla_ros_bridge carla_ros_bridge.launch.py town:=Town01

# 3. 启动安全监控
python safety_monitor.py

# 4. 启动故障注入
python fault_injector.py --faults lidar_drop --drop-rate 0.05

# 5. 运行集成测试
python integration_test.py --scenario straight_lane --duration 120

# 6. 评估结果
python eval_metrics.py --log-dir results/run_001 --output report.md
```

## 话题接口

| 话题 | 类型 | 说明 |
|------|------|------|
| `/perception/objects` | `DetectedObjects` | 感知目标列表 |
| `/planning/trajectory` | `Trajectory` | 规划轨迹 |
| `/vehicle/odometry` | `Odometry` | 车辆里程计 |
| `/vehicle/status` | `VehicleStatus` | 车辆状态 |
| `/control/cmd` | `ControlCommand` | 控制指令 |
| `/safety/collision_warning` | `Bool` | 碰撞预警 |
| `/safety/deviation` | `Float32` | 偏离量 |
| `/safety/aeb_command` | `ControlCommand` | AEB制动指令 |
| `/fault_injector/status` | `String` | 故障注入状态 |
| `/fault_injector/active_faults` | `String[]` | 活跃故障列表 |

---

## 安装与编译

```bash
pip install numpy matplotlib
```

## 运行方法

```bash
python eval_metrics.py --log-dir results/ch44_eval --summary   # 汇总评估
python eval_metrics.py --log-dir results/ch44_eval             # 生成 md/json 报告
python safety_monitor.py        # 安全监控节点(需 ROS2)
python fault_injector.py        # 故障注入(需 ROS2)
python integration_test.py      # 集成测试(需 ROS2)
```

## 测试方法与运行结果

评估指标计算(安全/舒适/效率/实时/精度/综合报告)已纳入统一测试:

```text
$ cd src && python -m pytest lab_code/tests/test_ch44_eval_metrics.py -q
13 passed in 0.07s
```

> 说明: 本机(Windows)未安装 CARLA/ROS2, 无法截取仿真画面,
> 运行结果以**真实终端输出**代替截图。

## 本次修复记录

`eval_metrics.py` 使用 numpy 2.x 已移除的 `np.trapz`(触发 AttributeError)
→ 改为 `np.trapezoid`; 并添加 Windows 控制台 UTF-8 输出兼容块。
