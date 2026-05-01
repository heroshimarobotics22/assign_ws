import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro


def generate_launch_description():

    # ── Robot Description ──────────────────────────────────
    desc_pkg    = get_package_share_directory('ack_description')
    xacro_file  = os.path.join(desc_pkg, 'urdf', 'ack.urdf.xacro')
    world_file  = os.path.join(desc_pkg, 'worlds', 'shapes.sdf')
    robot_description = xacro.process_file(xacro_file).toxml()

    # ── Gazebo ─────────────────────────────────────────────
    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('ros_gz_sim'),
            'launch',
            'gz_sim.launch.py'
        ),
        launch_arguments={
            'gz_args': world_file + ' -r',
            'on_exit_shutdown': 'True'
        }.items()
    )

    # ── Robot State Publisher ──────────────────────────────
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )

    # ── Spawn Robot ────────────────────────────────────────
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_robot',
        output='screen',
        arguments=[
            '-name', 'ackermann_robot',
            '-topic', 'robot_description',
            '-x', '-2.0', '-y', '0.0', '-z', '0.1'
        ]
    )

    # ── ROS-GZ Bridge ──────────────────────────────────────
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        output='screen',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/camera/image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
        ],
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        gazebo,
        rsp,
        spawn,
        bridge,
    ])
