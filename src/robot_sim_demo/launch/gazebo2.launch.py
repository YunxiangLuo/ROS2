"""Launch the safety inspection robot in the ISCAS Museum Gazebo world."""

import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
    SetEnvironmentVariable,
    TimerAction,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


ROBOT_NAME = "wheeltec_robot"
WORLD_NAME = "default"


def generate_launch_description() -> LaunchDescription:
    share = Path(get_package_share_directory("robot_sim_demo"))
    default_world = share / "worlds" / "museum.sdf"
    robot_sdf = share / "models" / ROBOT_NAME / "model.sdf"
    robot_urdf = share / "wheeltec_robot_urdf" / "urdf" / "mini_akm_robot.urdf"
    bridge_config = share / "config" / "gazebo2_bridge.yaml"
    gui_config = share / "gui" / "museum.gui.config"
    rviz_config = share / "rviz" / "museum.rviz"
    models = share / "models"
    gz_launch = (
        Path(get_package_share_directory("ros_gz_sim"))
        / "launch"
        / "gz_sim.launch.py"
    )

    gui = LaunchConfiguration("gui")
    rviz = LaunchConfiguration("rviz")
    spawn_robot = LaunchConfiguration("spawn_robot")
    drive = LaunchConfiguration("drive")
    drive_linear_speed = LaunchConfiguration("drive_linear_speed")
    drive_angular_speed = LaunchConfiguration("drive_angular_speed")
    drive_loop = LaunchConfiguration("drive_loop")
    drive_duration = LaunchConfiguration("drive_duration")
    gz_partition = LaunchConfiguration("gz_partition")
    world_name = LaunchConfiguration("world_name")
    spawn_x = LaunchConfiguration("spawn_x")
    spawn_y = LaunchConfiguration("spawn_y")
    spawn_z = LaunchConfiguration("spawn_z")
    spawn_yaw = LaunchConfiguration("spawn_yaw")
    use_sim_time = LaunchConfiguration("use_sim_time")
    world_path = LaunchConfiguration("world")

    robot_description = robot_urdf.read_text(encoding="utf-8")

    gazebo_gui = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(str(gz_launch)),
        condition=IfCondition(gui),
        launch_arguments={
            "gz_args": [
                "-r --gui-config ",
                str(gui_config),
                " ",
                 world_path,
            ],
            "on_exit_shutdown": "true",
        }.items(),
    )
    gazebo_headless = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(str(gz_launch)),
        condition=UnlessCondition(gui),
        launch_arguments={
            "gz_args": ["-r -s --headless-rendering ", world_path],
            "on_exit_shutdown": "true",
        }.items(),
    )

    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        condition=IfCondition(spawn_robot),
        output="screen",
        arguments=[
            "-world",
            world_name,
            "-file",
            str(robot_sdf),
            "-name",
            ROBOT_NAME,
            "-x",
            spawn_x,
            "-y",
            spawn_y,
            "-z",
            spawn_z,
            "-Y",
            spawn_yaw,
        ],
    )

    def set_resource_paths(context):
        """Set os.environ so gz_sim.launch.py's OpaqueFunction picks them up."""
        models_dir = str(share / "models")
        urdf_dir = str(share / "wheeltec_robot_urdf")
        existing_gz = os.environ.get("GZ_SIM_RESOURCE_PATH", "")
        os.environ["GZ_SIM_RESOURCE_PATH"] = os.pathsep.join(
            filter(None, [models_dir, urdf_dir, existing_gz])
        )
        existing_ign = os.environ.get("IGN_GAZEBO_RESOURCE_PATH", "")
        os.environ["IGN_GAZEBO_RESOURCE_PATH"] = os.pathsep.join(
            filter(None, [models_dir, urdf_dir, existing_ign])
        )
        return None

    return LaunchDescription(
        [
            DeclareLaunchArgument("gui", default_value="true"),
            DeclareLaunchArgument("rviz", default_value="false"),
            DeclareLaunchArgument("spawn_robot", default_value="true"),
            DeclareLaunchArgument("drive", default_value="true"),
            DeclareLaunchArgument("drive_linear_speed", default_value="0.18"),
            DeclareLaunchArgument("drive_angular_speed", default_value="0.55"),
            DeclareLaunchArgument("drive_loop", default_value="true"),
            DeclareLaunchArgument("drive_duration", default_value="0.0"),
            DeclareLaunchArgument("gz_partition", default_value="robot_sim_demo"),
            DeclareLaunchArgument("world", default_value=str(default_world)),
            DeclareLaunchArgument("world_name", default_value=WORLD_NAME),
            SetEnvironmentVariable(name="GZ_PARTITION", value=gz_partition),
            DeclareLaunchArgument("spawn_x", default_value="0.0"),
            DeclareLaunchArgument("spawn_y", default_value="0.0"),
            DeclareLaunchArgument("spawn_z", default_value="0.03"),
            DeclareLaunchArgument("spawn_yaw", default_value="0.0"),
            DeclareLaunchArgument("use_sim_time", default_value="true"),
            OpaqueFunction(function=set_resource_paths),
            gazebo_gui,
            gazebo_headless,
            Node(
                package="ros_gz_bridge",
                executable="parameter_bridge",
                name="gazebo2_bridge",
                output="screen",
                parameters=[
                    {
                        "config_file": str(bridge_config),
                        "use_sim_time": use_sim_time,
                    }
                ],
            ),
            Node(
                package="ros_gz_image",
                executable="image_bridge",
                name="gazebo2_camera_bridge",
                output="screen",
                arguments=["/camera/image_raw"],
                parameters=[{"use_sim_time": use_sim_time}],
            ),
            Node(
                package="robot_sim_demo",
                executable="camera_info_publisher",
                name="camera_info_publisher",
                output="screen",
                parameters=[{"use_sim_time": False}],
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="gazebo2_robot_state_publisher",
                output="screen",
                parameters=[
                    {
                        "robot_description": robot_description,
                        "use_sim_time": use_sim_time,
                    }
                ],
            ),
            Node(
                package="robot_sim_demo",
                executable="patrol_driver",
                name="patrol_driver",
                condition=IfCondition(drive),
                output="screen",
                parameters=[
                    {"linear_speed": drive_linear_speed},
                    {"angular_speed": drive_angular_speed},
                    {"loop": drive_loop},
                    {"duration": drive_duration},
                ],
            ),
            TimerAction(period=3.0, actions=[spawn]),
            Node(
                package="rviz2",
                executable="rviz2",
                name="museum_rviz",
                condition=IfCondition(rviz),
                output="screen",
                arguments=["-d", str(rviz_config)],
                parameters=[{"use_sim_time": use_sim_time}],
            ),
        ]
    )
