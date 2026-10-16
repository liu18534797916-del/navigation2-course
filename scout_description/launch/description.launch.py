import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue


def generate_launch_description():
    robot_xacro_path = os.path.join(
        get_package_share_directory('scout_description'),
        'urdf/robots', 'scout.urdf.xacro')

    namespace = LaunchConfiguration('namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_gazebo = LaunchConfiguration('use_gazebo')

    declare_namespace_cmd = DeclareLaunchArgument(
        name='namespace', default_value='scout',
        description='Top-level namespace')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time', default_value='false',
        description='Use simulation (Gazebo) clock if true')

    declare_use_gazebo_cmd = DeclareLaunchArgument(
        name='use_gazebo', default_value='false',
        description='Include Gazebo (ros2_control) plugins in the URDF if true')

    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        namespace=namespace,
        parameters=[
            {'robot_description': ParameterValue(
                Command(['xacro ', robot_xacro_path,
                         ' robot_namespace:=', namespace,
                         ' use_gazebo:=', use_gazebo]),
                value_type=str)},
            {'frame_prefix': [namespace, '/']},
            {'use_sim_time': use_sim_time}]
    )

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_use_gazebo_cmd)
    ld.add_action(declare_namespace_cmd)
    ld.add_action(robot_state_publisher_cmd)
    return ld
