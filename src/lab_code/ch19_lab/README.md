# 第5章 实验代码 — 视觉感知

本章学习使用 OpenCV 和 ROS2 进行图像处理、颜色检测和 AR 标签识别。

## 文件说明

| 文件 | 用途 | 运行方式 |
|------|------|----------|
| `usb_cam_node.py` | USB 摄像头图像查看器。订阅 `/image_raw` 话题，使用 OpenCV 显示图像，按 ESC 退出 | `python3 usb_cam_node.py` |
| `color_detection.py` | 颜色检测节点。在图像中检测指定颜色的物体区域 | `python3 color_detection.py` |
| `ar_tag_detection.py` | AR 标签检测节点。检测 ArUco 标签并估计位姿 | `python3 ar_tag_detection.py` |
| `cv_bridge_demo.py` | cv_bridge 图像转换演示。将 ROS 图像转为 OpenCV 格式，在图像上画矩形，再转回 ROS 图像发布 | `python3 cv_bridge_demo.py` |

## 运行说明

```bash
# 终端1：启动摄像头图像发布
ros2 run usb_cam usb_cam_node_exe

# 终端2：运行视觉脚本
cd lab_code/ch05_lab/
python3 cv_bridge_demo.py
```

或者使用测试图像循环播放：

```bash
ros2 run image_tools cam2image
python3 cv_bridge_demo.py --ros-args -p image_topic:=/image
```

### cv_bridge_demo.py

功能：
1. 订阅 `/camera/color/image_raw` 图像话题
2. 使用 `cv_bridge` 将 ROS 图像转为 OpenCV 格式
3. 在图像上绘制橙色矩形
4. 显示处理后的图像
5. 将 OpenCV 图像转回 ROS 格式发布到 `/image_show`
