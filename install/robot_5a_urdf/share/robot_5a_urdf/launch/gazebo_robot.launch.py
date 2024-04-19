import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import (OnProcessStart, OnProcessExit)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro
#from moveit_configs_utils import MoveItConfigusBuilder


def generate_launch_description():

    
    
    #Define the packages path
    robot_5a_urdf_package_path =os.path.join(
        get_package_share_directory('robot_5a_urdf')
    )
    gazebo_ros_package_path = os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch'
                )
    
    #Define the xacro file to be opened, parsed, processed and overloaded
    xacro_file =os.path.join(robot_5a_urdf_package_path,
        'description',
        'robot_5a_urdf.urdf.xacro'
    )

    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    params = {'robot_description':doc.toxml()}

    
    #Define the nodes
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable = 'robot_state_publisher',
        output = 'screen',
        parameters =[params]
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', '/robot_description',
                                '-entity', 'robot_5a_urdf'],
                    output='screen')
            # Define the gazebo node from the ros gazebo package launch file
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([gazebo_ros_package_path, '/gazebo.launch.py']),
    )
    
    #Define the loading of joint states and arm controller
    load_joint_states_controller = ExecuteProcess(
        cmd = ['ros2', 'control', 'load_controller', '--set-state', 'start', 'joint_state_broadcaster'],
        output='screen'
    )

    load_joint_arm_controller = ExecuteProcess(
        cmd = ['ros2', 'control', 'load_controller', '--set-state', 'start', 'arm_controller'],
        output='screen'
    )

    return LaunchDescription([
        RegisterEventHandler(
            event_handler= OnProcessExit(
                target_action=spawn_entity,
                on_exit=[load_joint_arm_controller],
            )
        ),
        RegisterEventHandler(
            event_handler= OnProcessExit(
                target_action=load_joint_states_controller,
                on_exit=[load_joint_arm_controller],
            )
        ),
        gazebo,
        robot_state_publisher,
        spawn_entity,
    ])
