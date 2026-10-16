"""Отображение робота SCOUT в RViz (без симуляции).

ВАЖНО: работает БЕЗ пространства имён, чтобы RViz получал TF из глобальных
топиков /tf и /tf_static. Запускает robot_state_publisher +
joint_state_publisher_gui + RViz.
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue


def generate_launch_description():
    pkg_share = get_package_share_directory('scout_description')
    robot_xacro_path = os.path.join(pkg_share, 'urdf/robots', 'scout.urdf.xacro')
    rviz_config = os.path.join(pkg_share, 'rviz', 'view_scout.rviz')

    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time', default_value='false',
        description='Use simulation (Gazebo) clock if true')

    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': ParameterValue(
                Command(['xacro ', robot_xacro_path]), value_type=str)},
            {'use_sim_time': use_sim_time}])

    joint_state_publisher_gui_cmd = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        parameters=[{'use_sim_time': use_sim_time}])

    rviz_cmd = Node(
        package='rviz2', executable='rviz2', name='rviz2', output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-d', rviz_config])

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(joint_state_publisher_gui_cmd)
    ld.add_action(rviz_cmd)
    return ld
