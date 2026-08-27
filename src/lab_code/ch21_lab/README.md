# 第34章 实验代码 — 视觉抓取综合项目

本章综合运用 MoveIt2、TF2 和视觉感知，实现完整的 AR 标签识别与抓取放置系统。

## 文件说明

| 文件 | 用途 | 运行方式 |
|------|------|----------|
| `tf2_camera_broadcaster.py` | 相机 TF 广播器。发布 `camera_link` 到 `base_link` 的静态坐标变换，支持参数或标定文件配置 | `python3 tf2_camera_broadcaster.py` |
| `vision_pickup_pipeline.py` | 检测 ArUco 标签，将位姿转换到 `base_link` 并发布 `/aruco_markers` | `python3 vision_pickup_pipeline.py` |
| `pick_with_ar_server.py` | 订阅 `/aruco_markers`，通过 MoveIt2 Pickup/Place Action 执行多目标抓取放置 | `python3 pick_with_ar_server.py` |

## 运行说明

### 完整抓取流程

```bash
# 终端1：启动机器人仿真
ros2 launch xarm_moveit_config demo.launch.py

# 终端2：启动摄像头 TF 广播
cd lab_code/ch34_lab/
python3 tf2_camera_broadcaster.py --ros-args -p x:=0.3 -p y:=0.0 -p z:=0.1

# 终端3：启动视觉抓取服务
python3 pick_with_ar_server.py

# 调用抓取服务
ros2 service call /xarm_vision_pickup std_srvs/srv/SetBool "{data: true}"
```

### pick_with_ar_server.py

功能流程：
1. 订阅 AR 标签位姿话题 `ar_pose_marker`
2. 将标签物体添加到规划场景中
3. 生成多种抓取姿态（grasps）和放置姿态（places）
4. 循环尝试抓取和放置，直至成功或达到最大尝试次数
5. 清理规划场景并回到 Home

### tf2_camera_broadcaster.py

支持从参数或 YAML 标定文件加载变换：

```bash
# 从参数
python3 tf2_camera_broadcaster.py --ros-args \
  -p x:=0.3 -p y:=0.0 -p z:=0.15 \
  -p roll:=0.0 -p pitch:=0.0 -p yaw:=1.57

# 从标定文件
python3 tf2_camera_broadcaster.py --ros-args \
  -p calibration_file:=/path/to/calib.yaml
```
