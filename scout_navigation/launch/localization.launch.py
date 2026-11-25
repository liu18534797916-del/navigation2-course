"""Локализация SCOUT на известной карте: map_server + AMCL + lifecycle_manager."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    namespace = LaunchConfiguration('namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    map_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')

    declare_namespace_cmd = DeclareLaunchArgument(
        name='namespace', default_value='scout', description='Top-level namespace')
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time', default_value='true', description='Use simulation clock')
    declare_map_file_cmd = DeclareLaunchArgument(
        name='map',
        default_value=os.path.join(
            get_package_share_directory('scout_navigation'), 'maps', 'empty', 'empty.yaml'),
        description='Full path to map yaml file to load')
    declare_params_file_cmd = DeclareLaunchArgument(
        name='params_file',
        default_value=os.path.join(
            get_package_share_directory('scout_navigation'), 'config', 'localization.yaml'),
        description='Localization parameters yaml')

    # Добавление корневого ключа пространства имён ко всем узлам
    configured_params = ParameterFile(
        RewrittenYaml(source_file=params_file, root_key=namespace,
                      param_rewrites={}, convert_types=True),
        allow_substs=True)

    remappings = [('/tf', 'tf'), ('/tf_static', 'tf_static')]

    map_server_cmd = Node(
        package='nav2_map_server', executable='map_server', name='map_server',
        output='screen', namespace=namespace,
        parameters=[configured_params, {'yaml_filename': map_file}],
        remappings=remappings)

    amcl_cmd = Node(
        package='nav2_amcl', executable='amcl', name='amcl',
        output='screen', namespace=namespace,
        parameters=[configured_params], remappings=remappings)

    lifecycle_manager_cmd = Node(
        package='nav2_lifecycle_manager', executable='lifecycle_manager',
        name='lifecycle_manager_localization', output='screen', namespace=namespace,
        parameters=[configured_params])

    ld = LaunchDescription()
    ld.add_action(declare_namespace_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_map_file_cmd)
    ld.add_action(declare_params_file_cmd)
    ld.add_action(map_server_cmd)
    ld.add_action(amcl_cmd)
    ld.add_action(lifecycle_manager_cmd)
    return ld
