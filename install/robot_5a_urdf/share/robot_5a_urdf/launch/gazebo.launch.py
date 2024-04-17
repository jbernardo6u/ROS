from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_urdf_model',
            arguments=['-entity', 'robot_5a_urdf', '-file', 'package://robot_5a_urdf/description/robot_5a_urdf.xacro.urdf'],
            output='screen'
        )
    ])
