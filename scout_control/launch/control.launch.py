"""Активация контроллеров ros2_control для SCOUT (spawner'ы controller_manager).

Запускается ПОСЛЕ спавна робота в Gazebo (scout_gazebo). Поднимает
joint_state_broadcaster и diff_drive_controller в пространстве имён робота.
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    namespace = LaunchConfiguration('namespace')

    declare_namespace_cmd = DeclareLaunchArgument(
        name='namespace', default_value='scout', description='Top-level namespace')

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['--controller-manager-timeout', '100',
                   '-c', [namespace, '/controller_manager'],
                   'joint_state_broadcaster'],
        output='screen')

    diff_drive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['--controller-manager-timeout', '100',
                   '-c', [namespace, '/controller_manager'],
                   'diff_drive_controller'],
        output='screen')

    ld = LaunchDescription()
    ld.add_action(declare_namespace_cmd)
    ld.add_action(joint_state_broadcaster_spawner)
    ld.add_action(diff_drive_controller_spawner)
    return ld
