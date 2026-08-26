import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_path = get_package_share_directory('sim_demo')
    world_path = LaunchConfiguration('world', default=os.path.join(pkg_path, 'worlds', 'empty.world'))
    use_gazebo = LaunchConfiguration('use_gazebo', default='true')
    use_rviz = LaunchConfiguration('use_rviz', default='false')

    return LaunchDescription([
        DeclareLaunchArgument('use_gazebo', default_value='true',
                              description='是否启动 Gazebo'),
        DeclareLaunchArgument('use_rviz', default_value='false',
                              description='是否启动 RViz2'),
        DeclareLaunchArgument('world', default_value=os.path.join(pkg_path, 'worlds', 'empty.world'),
                              description='Gazebo 世界文件路径'),

        # 启动 Gazebo 仿真
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                get_package_share_directory('gazebo_ros'),
                '/launch/gazebo.launch.py'
            ]),
            condition=IfCondition(use_gazebo),
            launch_arguments={'world': world_path}.items(),
        ),

        # Spawn 机器人模型
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', 'xbot',
                '-topic', 'robot_description',
                '-x', '0.0', '-y', '0.0', '-z', '0.1',
            ],
            output='screen',
            condition=IfCondition(use_gazebo),
        ),

        # RViz2 (可选)
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            condition=IfCondition(use_rviz),
            output='screen',
        ),
    ])