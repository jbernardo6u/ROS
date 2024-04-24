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
        'urdf',
        'robot_5a_urdf.xacro.urdf'
    )



    # import re
    # def remove_comments(text):
    #     pattern = r'<!--(.*?)-->'
    #     return re.sub(pattern, '', text, flags=re.DOTALL)
    # xacro_file = remove_comments(xacro_file)

    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    params = {'robot_description':doc.toxml()}

    
    #Define the nodes
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable = 'robot_state_publisher',
        output = 'screen',
        parameters =[params]
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'robot_5a_urdf'],
                    output='screen')
            # Define the gazebo node from the ros gazebo package launch file
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([gazebo_ros_package_path, '/gazebo.launch.py']),
    )

    rviz = Node(
         package='rviz2',
         executable='rviz2',
         arguments=[
             '-d',
             os.path.join(robot_5a_urdf_package_path , 'config/view_robot.rviz'),
         ],
         output='screen'
     )
    
    node_joint_state_publisher = Node(
            name='joint_state_publisher',
            package='joint_state_publisher',
            executable='joint_state_publisher',
            output='screen'
    )

    # Configure the joint state publisher GUI node
    node_joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    
    #Define the loading of joint states and arm controller : the two functions will execute commands to load the controllers
    load_joint_states_controller = ExecuteProcess(
        cmd = ['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
        output='screen'
    )

    load_joint_arm_controller = ExecuteProcess(
        cmd = ['ros2', 'control', 'load_controller', '--set-state', 'active', 'arm_controller'],
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
        node_robot_state_publisher,
        rviz,
        node_joint_state_publisher,
        node_joint_state_publisher_gui,
        spawn_entity
    ])
