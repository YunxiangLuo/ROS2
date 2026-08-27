# 第2章 实验代码 — URDF 建模与 robot_state_publisher

本章学习如何创建和显示 URDF 机械臂模型。

## 目录结构

```
ch02_lab/
├── README.md
├── arm_urdf/                 # URDF 模型文件
│   ├── urdf/
│   │   ├── arm.urdf          # 机械臂 URDF 模型
│   │   └── arm.xacro         # XACRO 宏定义模型
│   ├── meshes/               # 3D 模型文件（STL/DAE）
│   ├── launch/
│   │   └── display.launch.py # URDF 显示启动文件
│   ├── config/
│   │   └── rviz_config.rviz  # RViz 配置文件
│   └── CMakeLists.txt
└── arm_state_publisher/      # 状态发布器配置
    ├── config/
    │   └── joint_state_publisher.yaml
    ├── launch/
    │   └── state_publisher.launch.py
    └── CMakeLists.txt
```

## 文件说明

| 文件/目录 | 用途 |
|-----------|------|
| `arm_urdf/` | 包含机械臂的 URDF/XACRO 模型定义、3D 网格文件和 RViz 显示配置 |
| `arm_state_publisher/` | 关节状态发布器配置，与 `robot_state_publisher` 配合使用 |

## 运行说明

```bash
# 显示 URDF 模型
cd ch02_lab/arm_urdf
ros2 launch arm_urdf display.launch.py

# 启动状态发布器
ros2 launch arm_state_publisher state_publisher.launch.py
```
