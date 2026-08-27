# 第36章 实验代码 — 自动驾驶概述与CARLA基础

本章学习使用CARLA仿真平台和Python API进行自动驾驶仿真实验。

## 文件说明

| 文件 | 用途 | 运行方式 |
|------|------|----------|
| `install_carla.sh` | CARLA 0.9.15 一键安装脚本 | `bash install_carla.sh` |
| `explore_carla.py` | 连接CARLA并打印世界信息（地图、蓝图、天气等） | `python3 explore_carla.py` |
| `spawn_vehicles.py` | 在CARLA中生成多辆车辆并设置自动驾驶 | `python3 spawn_vehicles.py --num-vehicles 10` |

## 运行说明

### 步骤1：启动CARLA服务器

```bash
cd ~/carla
./CarlaUE4.sh -quality-level=Low
```

### 步骤2：运行Python脚本

```bash
# 终端2：探索CARLA世界信息
cd lab_code/ch36_lab/
python3 explore_carla.py

# 终端2（或新终端）：生成车辆
cd lab_code/ch36_lab/
python3 spawn_vehicles.py --num-vehicles 20
```

### 注意事项

- CARLA服务器至少需要4GB显存和8GB系统内存
- 若使用 `-quality-level=Low` 仍卡顿，可尝试 `-opengl` 参数
- 默认连接地址为 `localhost:2000`，可通过 `--host` 和 `--port` 参数修改
- 首次运行 `explore_carla.py` 前请确保已安装carla Python API

---

## 安装与编译

```bash
# CARLA 0.9.13+ 与 Python 3.8+ 环境
pip install numpy pyyaml
# 或使用本目录脚本自动安装 CARLA egg:
bash install_carla.sh
```

## 运行方法

```bash
# 先启动 CARLA 服务器: ./CarlaUE4.sh -quality-level=Low
python explore_carla.py --host localhost --port 2000   # 地图/生成点/天气探索
python spawn_vehicles.py --count 10                    # 生成背景交通车辆
```

## 运行结果 (本机静态验证)

本机无 CARLA 运行时, 两个脚本通过工作区统一测试套件的语法与导入检查
(下方命令可复现):

```text
$ cd src && python -m pytest lab_code/tests/test_syntax_all.py -q
46 passed in 0.45s
```

> 说明: 本机(Windows)未安装 CARLA/ROS2, 无法截取仿真画面,
> 运行结果以**真实终端输出**代替截图。
