# 第43章 实验代码：行为决策与交通规则

## 代码结构

```
ch43_lab/
├── README.md                       # 本文件
├── fsm_decision.py                 # 有限状态机行为决策
├── traffic_light_detector.py       # 交通灯检测与响应
└── traffic_manager_demo.py         # CARLA Traffic Manager 配置
```

## 文件说明

### fsm_decision.py

基于有限状态机的行为决策节点，包含三种状态：

- **CRUISE** - 车道保持巡航
- **FOLLOW** - 跟车模式
- **STOP** - 停车模式

状态转移逻辑：检测到前车时从 CRUISE → FOLLOW，前车消失时返回 CRUISE；检测到红灯时进入 STOP。

**运行：**

```bash
python fsm_decision.py
```

### traffic_light_detector.py

交通灯检测与响应节点，实现：

- 订阅 CARLA 交通灯状态主题
- 计算车辆到停止线的距离
- 根据灯色和距离输出油门/刹车控制

**运行：**

```bash
python traffic_light_detector.py
```

### traffic_manager_demo.py

CARLA Traffic Manager 配置演示，支持三种驾驶风格：

| 模式 | 特点 |
|------|------|
| normal | 普通驾驶，遵守规则 |
| aggressive | 激进驾驶，闯灯概率20% |
| conservative | 保守驾驶，跟车距离大 |

**运行：**

```bash
python traffic_manager_demo.py --vehicles 20 --mode normal
python traffic_manager_demo.py --vehicles 30 --mode aggressive
python traffic_manager_demo.py --vehicles 50 --mode mixed
```

## 依赖

- Python 3.8+
- carla (pip: `pip install carla`)
- ROS2 Humble (若使用 ROS2 版本)
- rclpy, carla_msgs (ROS2 包)

## 对应实验

- 练习 43.1: `traffic_light_detector.py`
- 练习 43.2: `fsm_decision.py`
- 练习 43.3: `traffic_manager_demo.py`

详细实验步骤见 `lab_manuals/ch43_lab.md`。

---

## 安装与编译

```bash
pip install numpy
# 需本机 CARLA 0.9.13+ 运行中
```

## 运行方法

```bash
python traffic_light_detector.py    # 交通灯检测与停车响应
python fsm_decision.py              # FSM 行为决策(CRUISE/FOLLOW/STOP/AVOID/COMPLETE)
python traffic_manager_demo.py      # 交通管理演示
```

## 测试方法与运行结果

FSM 状态机与交通灯决策逻辑已纳入统一测试(使用 CARLA 对象替身, 无需仿真器):

```text
$ cd src && python -m pytest lab_code/tests/test_ch43_fsm.py -v
lab_code/tests/test_ch43_fsm.py::TestFSM::test_init_to_cruise PASSED
lab_code/tests/test_ch43_fsm.py::TestFSM::test_cruise_keeps_throttle PASSED
lab_code/tests/test_ch43_fsm.py::TestFSM::test_near_lead_transitions_to_follow PASSED
lab_code/tests/test_ch43_fsm.py::TestFSM::test_lead_gone_returns_to_cruise PASSED
lab_code/tests/test_ch43_fsm.py::TestFSM::test_red_light_transitions_to_stop PASSED
lab_code/tests/test_ch43_fsm.py::TestFSM::test_destination_reached_completes PASSED
lab_code/tests/test_ch43_fsm.py::TestTrafficLightDetector::test_green_pass PASSED
lab_code/tests/test_ch43_fsm.py::TestTrafficLightDetector::test_no_light PASSED
lab_code/tests/test_ch43_fsm.py::TestTrafficLightDetector::test_red_within_decel_zone PASSED
lab_code/tests/test_ch43_fsm.py::TestTrafficLightDetector::test_red_far_away PASSED
lab_code/tests/test_ch43_fsm.py::TestTrafficLightDetector::test_already_past_stop_line PASSED
lab_code/tests/test_ch43_fsm.py::TestTrafficLightDetector::test_yellow_close_stops PASSED
lab_code/tests/test_ch43_fsm.py::TestTrafficLightDetector::test_yellow_far_passes PASSED
13 passed in 0.05s
```

> 说明: 本机(Windows)未安装 CARLA/ROS2, 无法截取仿真画面,
> 运行结果以**真实终端输出**代替截图。

## 本次修复记录

`fsm_decision.py` 红灯停车转移条件原为 `have_red_light and lead_distance < 30.0`,
即**无前车时即使红灯也不会进入 STOP 状态(闯红灯缺陷)** → 改为红灯即停
(50m 距离过滤已在感知环节完成), 由回归测试 `test_red_light_transitions_to_stop` 锁定。
