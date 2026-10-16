"""Запуск сервера и клиента Gazebo Harmonic с указанным миром."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, IncludeLaunchDescription,
                            SetEnvironmentVariable)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_desc = get_package_share_directory('scout_description')

    world_path = LaunchConfiguration('world_path')
    verbose = LaunchConfiguration('verbose')

    declare_world_path_cmd = DeclareLaunchArgument(
        name='world_path',
        default_value=os.path.join(
            get_package_share_directory('scout_gazebo'), 'worlds', 'empty.world'),
        description='Specify world file')
    declare_verbose_cmd = DeclareLaunchArgument(
        name='verbose', default_value='-v4', description='Gazebo verbose level')

    # Сервер (физика, сенсоры) + клиент (GUI)
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': ['-r -s ', verbose, ' ', world_path],
                          'on_exit_shutdown': 'true'}.items())
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': ['-g ', verbose]}.items())

    ld = LaunchDescription()
    ld.add_action(SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', pkg_desc))
    ld.add_action(declare_world_path_cmd)
    ld.add_action(declare_verbose_cmd)
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    return ld
