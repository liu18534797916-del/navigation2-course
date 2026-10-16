"""Спавн робота SCOUT в Gazebo + мост топиков (scan, clock).

Включает описание робота (robot_state_publisher с плагинами ros2_control)
и создаёт сущность в Gazebo из топика /<ns>/robot_description.
Контроллеры активируются отдельно (scout_control/control.launch.py).
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from nav2_common.launch import ReplaceString


def generate_launch_description():
    namespace = LaunchConfiguration('namespace')
    robot_name = LaunchConfiguration('robot_name')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z_rot = LaunchConfiguration('z_rot')
    bridge_file_path = LaunchConfiguration('bridge_file_path')

    declare_namespace_cmd = DeclareLaunchArgument(
        name='namespace', default_value='scout', description='Top-level namespace')
    declare_robot_name_cmd = DeclareLaunchArgument(
        name='robot_name', default_value=namespace, description='Robot name in Gazebo')
    declare_x_cmd = DeclareLaunchArgument(
        name='x', default_value='0.0', description='Robot position (x)')
    declare_y_cmd = DeclareLaunchArgument(
        name='y', default_value='0.0', description='Robot position (y)')
    declare_z_rot_cmd = DeclareLaunchArgument(
        name='z_rot', default_value='0.0', description='Robot orientation (yaw)')
    declare_bridge_file_path_cmd = DeclareLaunchArgument(
        name='bridge_file_path',
        default_value=os.path.join(
            get_package_share_directory('scout_gazebo'), 'config', 'bridge.yaml'),
        description='Bridge configuration')

    # Описание робота с плагинами ros2_control (use_gazebo:=true)
    robot_description_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('scout_description'),
                         'launch', 'description.launch.py')),
        launch_arguments={'namespace': namespace,
                          'use_sim_time': 'true',
                          'use_gazebo': 'true'}.items())

    # Спавн из топика robot_description в пространстве имён робота.
    # base_footprint — корень, z=0.15 даёт мягкое приземление на колёса.
    spawn_entity_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        name='urdf_spawner',
        output='screen',
        arguments=['-topic', [namespace, '/robot_description'],
                   '-name', robot_name,
                   '-x', x, '-y', y, '-Y', z_rot, '-z', '0.15'])

    # Подстановка пространства имён в bridge.yaml
    namespaced_bridge_file_path = ReplaceString(
        source_file=bridge_file_path,
        replacements={'<robot_namespace>': ('/', namespace)})

    gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        namespace=namespace,
        parameters=[{'config_file': namespaced_bridge_file_path,
                     'use_sim_time': True}])

    ld = LaunchDescription()
    ld.add_action(declare_namespace_cmd)
    ld.add_action(declare_robot_name_cmd)
    ld.add_action(declare_x_cmd)
    ld.add_action(declare_y_cmd)
    ld.add_action(declare_z_rot_cmd)
    ld.add_action(declare_bridge_file_path_cmd)
    ld.add_action(robot_description_cmd)
    ld.add_action(spawn_entity_cmd)
    ld.add_action(gazebo_ros_bridge_cmd)
    return ld
