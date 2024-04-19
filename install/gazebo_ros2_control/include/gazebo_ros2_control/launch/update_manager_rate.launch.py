from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare the update_rate parameter
    update_rate_arg = DeclareLaunchArgument('update_rate', default_value='50', description='Update rate for the controller manager')

    # Create a node to launch the controller manager
    controller_manager_node = Node(
        package='gazebo_ros2_control',
        executable='controller_manager',
        name='controller_manager_node',
        output='screen',
        parameters=[{'update_rate': LaunchConfiguration('update_rate')}]
    )

    return LaunchDescription([
        update_rate_arg,
        controller_manager_node
    ])
