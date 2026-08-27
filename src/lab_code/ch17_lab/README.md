# 第3章 实验代码 — MoveIt2 运动学

本章学习使用 MoveIt2 的 Python API 实现正运动学和逆运动学控制。

## 文件说明

| 文件 | 用途 | 运行方式 |
|------|------|----------|
| `moveit2_fk_demo.py` | 正运动学（FK）演示。使用关节空间控制设置各关节的目标角度，控制机械臂运动 | `python3 moveit2_fk_demo.py` |
| `moveit2_ik_demo.py` | 逆运动学（IK）演示。设置末端执行器目标位姿（位置+姿态），由 MoveIt2 解算 IK 并运动 | `python3 moveit2_ik_demo.py` |
| `test_fk_ik.py` | FK/IK 综合练习题。包含 TODO 填空，完成末端位姿设置、关节空间规划和命名目标控制 | `python3 test_fk_ik.py` |
| `test_rectangle.py` | 笛卡尔路径矩形轨迹规划。沿矩形路径的四个顶点做笛卡尔直线运动 | `python3 test_rectangle.py` |

## 运行说明

所有脚本均需先启动 xarm 机器人仿真环境：

```bash
# 终端1：启动仿真
ros2 launch xarm_moveit_config demo.launch.py

# 终端2：运行实验脚本
cd lab_code/ch03_lab/
python3 moveit2_fk_demo.py
```

### `test_fk_ik.py` TODO 练习

打开 `test_fk_ik.py`，完成以下 TODO：

1. 设置末端执行器目标位姿（位置 x=0.3, y=-0.3, z=0.3，姿态 rpy=0,0,-π/4）
2. 设置机械臂当前状态为初始状态
3. 规划并执行运动到目标位姿
4. 设置六关节角度目标值 `[-0.9, -1.0, 0.2, 0.9, -0.76, 1.5]` 并规划执行
5. 使用命名目标 `Home` 回到初始位置

### `test_rectangle.py` TODO 练习

补全第三个和第四个矩形顶点坐标，完成笛卡尔路径规划。
