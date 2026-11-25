"""Автономная навигация Nav2 для SCOUT: bt_navigator, planner, controller, behavior, lifecycle.

cmd_vel контроллера и поведения ремаппится в
<scout>/diff_drive_controller/cmd_vel (TwistStamped, enable_stamped_cmd_vel: true)."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import RewrittenYaml, ReplaceString


def generate_launch_description():
    namespace = LaunchConfiguration('namespace')
    params_file = LaunchConfiguration('params_file')

    declare_namespace_cmd = DeclareLaunchArgument(
        name='namespace', default_value='scout', description='Top-level namespace')
    declare_params_file_cmd = DeclareLaunchArgument(
        name='params_file',
        default_value=os.path.join(
            get_package_share_directory('scout_navigation'), 'config', 'navigation.yaml'),
        description='Navigation parameters yaml')

    # Сначала подставляем <robot_namespace> -> /scout, затем корневой ключ ns
    remapped_params = ReplaceString(
        source_file=params_file,
        replacements={'<robot_namespace>': ('/', namespace)})
    configured_params = ParameterFile(
        RewrittenYaml(source_file=remapped_params, root_key=namespace,
                      param_rewrites={}, convert_types=True),
        allow_substs=True)

    remappings = [('/tf', 'tf'), ('/tf_static', 'tf_static')]
    cmd_remappings = remappings + [('cmd_vel', 'diff_drive_controller/cmd_vel')]

    bt_navigator_cmd = Node(
        package='nav2_bt_navigator', executable='bt_navigator', name='bt_navigator',
        output='screen', namespace=namespace, parameters=[configured_params],
        remappings=remappings)

    planner_cmd = Node(
        package='nav2_planner', executable='planner_server', name='planner_server',
        output='screen', namespace=namespace, parameters=[configured_params],
        remappings=remappings)

    controller_cmd = Node(
        package='nav2_controller', executable='controller_server', name='controller_server',
        output='screen', namespace=namespace, parameters=[configured_params],
        remappings=cmd_remappings)

    behavior_cmd = Node(
        package='nav2_behaviors', executable='behavior_server', name='behavior_server',
        output='screen', namespace=namespace, parameters=[configured_params],
        remappings=cmd_remappings)

    lifecycle_manager_cmd = Node(
        package='nav2_lifecycle_manager', executable='lifecycle_manager',
        name='lifecycle_manager_navigation', output='screen', namespace=namespace,
        parameters=[configured_params])

    ld = LaunchDescription()
    ld.add_action(declare_namespace_cmd)
    ld.add_action(declare_params_file_cmd)
    ld.add_action(bt_navigator_cmd)
    ld.add_action(planner_cmd)
    ld.add_action(controller_cmd)
    ld.add_action(behavior_cmd)
    ld.add_action(lifecycle_manager_cmd)
    return ld
