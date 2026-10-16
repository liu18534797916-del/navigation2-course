"""Комплексный запуск: Gazebo (мир) + спавн робота SCOUT + мост топиков."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_gz = get_package_share_directory('scout_gazebo')

    world_path = LaunchConfiguration('world_path')
    verbose = LaunchConfiguration('verbose')
    namespace = LaunchConfiguration('namespace')
    robot_name = LaunchConfiguration('robot_name')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z_rot = LaunchConfiguration('z_rot')

    declare_world_path_cmd = DeclareLaunchArgument(
        name='world_path',
        default_value=os.path.join(pkg_gz, 'worlds', 'empty.world'),
        description='Gazebo world file')
    declare_verbose_cmd = DeclareLaunchArgument(
        name='verbose', default_value='-v4', description='Gazebo verbose level')
    declare_namespace_cmd = DeclareLaunchArgument(
        name='namespace', default_value='scout', description='Robot namespace')
    declare_robot_name_cmd = DeclareLaunchArgument(
        name='robot_name', default_value=namespace, description='Robot name')
    declare_x_cmd = DeclareLaunchArgument(
        name='x', default_value='0.0', description='Robot X axis')
    declare_y_cmd = DeclareLaunchArgument(
        name='y', default_value='0.0', description='Robot Y axis')
    declare_z_rot_cmd = DeclareLaunchArgument(
        name='z_rot', default_value='0.0', description='Robot Z rotation (yaw)')

    gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gz, 'launch', 'gazebo.launch.py')),
        launch_arguments={'world_path': world_path, 'verbose': verbose}.items())
    spawn_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gz, 'launch', 'spawn.launch.py')),
        launch_arguments={'namespace': namespace, 'robot_name': robot_name,
                          'x': x, 'y': y, 'z_rot': z_rot}.items())

    ld = LaunchDescription()
    ld.add_action(declare_world_path_cmd)
    ld.add_action(declare_verbose_cmd)
    ld.add_action(declare_namespace_cmd)
    ld.add_action(declare_robot_name_cmd)
    ld.add_action(declare_x_cmd)
    ld.add_action(declare_y_cmd)
    ld.add_action(declare_z_rot_cmd)
    ld.add_action(gazebo_cmd)
    ld.add_action(spawn_cmd)
    return ld
