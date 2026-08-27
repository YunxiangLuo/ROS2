# 第39章 实验代码：全局路径规划与地图导航

## 文件说明

| 文件名 | 功能 | 依赖 |
|--------|------|------|
| `global_planner.py` | A\* 全局路径规划器，在 CARLA 路网图中搜索最优路径 | carla, numpy, heapq |
| `waypoint_pub.py` | ROS2 节点，通过 CARLA Waypoint API 生成连续路径并发布 | carla, rclpy, nav_msgs |
| `map_visualizer.py` | 可视化 CARLA 地图 OpenDRIVE 路网和拓扑结构 | carla, matplotlib, xml.etree |

## 使用方法

```bash
# 1. 启动 CARLA
./CarlaUE4.sh -quality-level=Low

# 2. 运行地图可视化
python map_visualizer.py

# 3. 运行全局路径规划
python global_planner.py

# 4. 运行 ROS2 Waypoint 节点 (需先 source ROS2)
ros2 run ch39_lab waypoint_pub.py
```

## 依赖安装

```bash
pip install carla matplotlib numpy
# ROS2 依赖 (Humble/Foxy)
sudo apt install ros-humble-nav-msgs ros-humble-geometry-msgs
```

---

## 安装与编译

```bash
pip install numpy matplotlib
```

## 运行方法

```bash
# 纯算法验证(无需 CARLA): 在 CARLA 路网拓扑上运行 A* 全局规划
python global_planner.py --host localhost --port 2000 --start-index 0
python global_planner.py --dijkstra            # Dijkstra 对比
python map_visualizer.py --export              # 导出 OpenDRIVE 并绘制路网图
python waypoint_pub.py                          # 航点发布(需 ROS2)
```

## 测试方法与运行结果

A* 算法(RoadGraph/a_star_search/dijkstra/heuristic)已纳入工作区统一测试:

```text
$ cd src && python -m pytest lab_code/tests/test_ch39_astar.py -v
lab_code/tests/test_ch39_astar.py::test_linear_graph_path PASSED
lab_code/tests/test_ch39_astar.py::test_disconnected_returns_empty PASSED
lab_code/tests/test_ch39_astar.py::test_dijkstra_matches_astar PASSED
lab_code/tests/test_ch39_astar.py::test_heuristic_admissible PASSED
lab_code/tests/test_ch39_astar.py::test_shortcut_prefers_direct_edge PASSED
lab_code/tests/test_ch39_astar.py::test_find_closest_node PASSED
6 passed in 0.09s
```

> 说明: 本机(Windows)未安装 CARLA/ROS2, 无法截取仿真画面,
> 运行结果以**真实终端输出**代替截图。
