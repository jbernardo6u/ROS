from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gazebo_ros',
            executable='spawn_model',
            name='spawn_model',
            arguments=['-file', '5A Assembly3/urdf/5A Assembly3.urdf', '-urdf', '-model', '5A Assembly3'],
            output='screen'
        ),
        Node(
            package='tf',
            executable='static_transform_publisher',
            name='tf_footprint_base',
            arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'base_footprint', '40']
        ),
        Node(
            package='rostopic',
            executable='rostopic',
            name='fake_joint_calibration',
            arguments=['pub', '/calibrated', 'std_msgs/Bool', 'true']
        )
    ])