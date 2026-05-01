# 🤖 MechaPrime — Autonomous Mobile Robot (ROS2 + Ignition Gazebo)

[![ROS2](https://img.shields.io/badge/ROS2-Humble-blue?logo=ros)](https://docs.ros.org/en/humble/)
[![Gazebo](https://img.shields.io/badge/Gazebo-Ignition%206-orange)](https://gazebosim.org/)
[![Python](https://img.shields.io/badge/Python-3.10-yellow?logo=python)](https://www.python.org/)
[![Nav2](https://img.shields.io/badge/Nav2-Humble-green)](https://navigation.ros.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-robovision2210-black?logo=github)](https://github.com/robovision2210/mechaprime_ws)

> A ROS2 Humble differential drive autonomous mobile robot simulated in Ignition Gazebo 6, featuring full Nav2 autonomous navigation, SLAM-based mapping, AMCL localization, QR-code-guided maze solving, LiDAR obstacle avoidance, IMU feedback, autonomous docking/undocking, and camera-based marker detection.

---

## 🎥 Demos

### 🧠 Autonomous Maze Solver
![MechaPrime Maze Solver Demo](media/mechaprime_maze_solver.gif)

### 🚀 Autonomous Navigation & Docking
![MechaPrime Navigation & Docking Demo](media/mechaprime_navigation_docking.gif)

### 🕹️ Teleoperation
![MechaPrime Teleop Demo](media/mechaprime_demo.gif)

---

## 📸 Screenshots

| QR: Left | QR: Right | QR: Stop |
|----------|-----------|----------|
| ![left](media/qr_left.png) | ![right](media/qr_right.png) | ![stop](media/qr_stop.png) |

| Maze Top View | LiDAR Output | RQT Node Graph |
|---------------|--------------|----------------|
| ![maze](media/maze_topview.png) | ![lidar](media/lidar_output.png) | ![rqt](media/rqt_graph.png) |

| Maze Solver Terminal |
|----------------------|
| ![terminal](media/maze_solver_terminal.png) |

---

## 🧠 Features

- **Full Nav2 Stack** — BehaviorTree-based autonomous navigation with global/local planners, costmap2d, recovery behaviors, and waypoint following
- **SLAM Mapping** — slam_toolbox-based map generation of indoor environments
- **AMCL Localization** — Adaptive Monte Carlo Localization for real-time pose estimation on a pre-built map
- **Autonomous Docking & Undocking** — QR-code-guided precision docking with pre-dock waypoint navigation
- **Docking with Patrolling** — Combined Nav2 waypoint patrol + autonomous docking workflow
- **Battery-aware Docking** — Auto-docking triggered by simulated battery state
- **Autonomous Maze Navigation** — State machine (FORWARD → TURNING → STOPPED) driven by LiDAR + QR codes
- **QR Code Detection** — OpenCV-based QR decoder reads directional commands (`left`, `right`, `stop`)
- **LiDAR Obstacle Avoidance** — 360° LiDAR scan with reactive front threshold detection (0.45m)
- **IMU-based Turning** — Precise 90° turns using yaw feedback from IMU
- **Differential Drive Control** — ros2_control with DiffDriveController via twist_mux priority pipeline
- **Joystick Teleoperation** — Override autonomous mode with PS4/Xbox controller (priority 99)
- **Keyboard Teleoperation** — Manual control via teleop_twist_keyboard

---

## 🏗️ Robot Specifications

| Parameter | Value |
|-----------|-------|
| Drive Type | Differential Drive |
| Wheel Separation | 0.185 m |
| Wheel Radius | 0.034 m |
| Base Mass | 5 kg |
| Max Linear Velocity | 2.0 m/s |
| Max Angular Velocity | 2.5 rad/s |

### Sensors

| Sensor | Type | Topic | Rate |
|--------|------|--------|------|
| LiDAR | 360° GPU Ray | `/scan` | 5 Hz |
| IMU | 6-DOF | `/imu/out` | 100 Hz |
| Camera | RGB 640×480 | `/camera/image_raw` | 10 Hz |

---

## 📦 Package Structure

```
mechaprime_ws/src/
├── mechaprime_description/     # URDF xacro, meshes, Gazebo worlds, dock STL model
├── mechaprime_mapping/         # SLAM toolbox config, slam.launch.py, saved maps
├── mechaprime_localization/    # AMCL config, global_localization.launch.py, RViz config
├── mechaprime_navigation/      # Nav2 full stack — BT, planner, controller, waypoint follower
├── mechaprime_controller/      # ros2_control, DiffDriveController, twist_mux, joystick config
├── mechaprime_bringup/         # Full system bringup launch
└── mechaprime_scripts/         # Python autonomy and sensor nodes
```

---

## 🔧 Dependencies

- ROS2 Humble
- Ignition Gazebo 6 (Harmonic)
- Nav2 (`nav2_bringup`, `nav2_bt_navigator`, `nav2_controller`, `nav2_planner`)
- SLAM Toolbox (`slam_toolbox`)
- Python 3.10
- OpenCV (`cv2`)
- `ros_gz_sim`, `ros_gz_bridge`
- `ros2_control`, `diff_drive_controller`
- `twist_mux`, `joy_teleop`

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/robovision2210/mechaprime_ws.git
cd mechaprime_ws

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build
source install/setup.bash
```

---

## ▶️ Running the Simulation

### Launch Gazebo + Robot

```bash
# Terminal 1 — Full simulation (Gazebo + controllers + twist_mux)
ros2 launch mechaprime_bringup simulated_robot.launch.py
```

---

## 🗺️ Mapping (SLAM)

```bash
# Terminal 1 — Launch simulation
ros2 launch mechaprime_bringup simulated_robot.launch.py

# Terminal 2 — Start SLAM mapping
ros2 launch mechaprime_mapping slam.launch.py

# Terminal 3 — Drive the robot to build the map
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/key_vel

# Save the map when done
ros2 run nav2_map_server map_saver_cli -f ~/mechaprime_ws/src/mechaprime_mapping/maps/small_house/map
```

> A pre-built map of `small_house.world` is already saved in `mechaprime_mapping/maps/small_house/`

---

## 📍 Localization (AMCL)

```bash
# Terminal 1 — Launch simulation
ros2 launch mechaprime_bringup simulated_robot.launch.py

# Terminal 2 — Launch AMCL localization with pre-built map
ros2 launch mechaprime_localization global_localization.launch.py
```

---

## 🧭 Autonomous Navigation (Nav2)

```bash
# Terminal 1 — Launch simulation
ros2 launch mechaprime_bringup simulated_robot.launch.py

# Terminal 2 — Launch localization
ros2 launch mechaprime_localization global_localization.launch.py

# Terminal 3 — Launch Nav2 full stack
ros2 launch mechaprime_navigation navigation.launch.py

# Terminal 4 — Run waypoint follower / goal sender
ros2 run mechaprime_navigation waypoint_following
```

---

## 🔌 Autonomous Docking

### Simple Docking (Nav2 + QR alignment)

```bash
# Terminal 4 — After launching sim + localization + navigation
ros2 run mechaprime_scripts auto_docking_undocking
```

### Docking with Patrolling

```bash
# Patrol waypoints autonomously, then dock at station
ros2 run mechaprime_scripts docking_with_patrolling
```

### Battery-aware Auto Docking

```bash
# Dock automatically when battery drops below threshold
ros2 run mechaprime_scripts auto_docking_with_battery
```

---

## 🧩 Maze Solver (QR Navigation)

```bash
# Terminal 1 — Launch simulation with maze world
ros2 launch mechaprime_bringup simulated_robot.launch.py

# Terminal 2 — Autonomous QR maze navigation
ros2 run mechaprime_scripts maze_solver

# Terminal 3 (optional) — Keyboard override
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/key_vel
```

---

## 🗺️ Available Worlds

| World | Description |
|-------|-------------|
| `empty.world` | Empty world for testing |
| `qr_maze.world` | QR-code guided maze with 3 markers |
| `small_house.world` | Full indoor navigation environment (map pre-built) |

```bash
# Launch with specific world
ros2 launch mechaprime_description gazebo.launch.py world_name:=qr_maze
```

---

## 🐍 Python Nodes

| Node | Description | Topics |
|------|-------------|--------|
| `maze_solver` | Autonomous QR maze navigation state machine | `/scan`, `/imu/out`, `/camera/image_raw` → `/cmd_vel` |
| `auto_docking_undocking` | Nav2-based docking and undocking sequence | Nav2 action client, `/camera/image_raw` |
| `auto_docking_with_battery` | Battery-triggered autonomous docking | Nav2 action client, `/battery_state` |
| `docking_with_patrolling` | Waypoint patrol + autonomous docking | Nav2 action client, `/camera/image_raw` |
| `obstacle_avoidance` | Reactive LiDAR-based obstacle avoidance | `/scan` → `/cmd_vel` |
| `detect_marker` | QR code detection with bounding box visualization | `/camera/image_raw` |
| `read_lidar` | 4-quadrant LiDAR distance reader | `/scan` |
| `read_imu` | Yaw angle and yaw rate from IMU | `/imu/out` |
| `read_camera` | Live camera feed viewer | `/camera/image_raw` |

---

## 🔀 Velocity Pipeline

```
joystick (priority 99) ─┐
navigation (priority 90) ┼─► twist_mux ──► /wheel_controller/cmd_vel_unstamped ──► robot
keyboard   (priority 80) ┘
```

---

## 🏛️ Maze Solver State Machine

```
┌─────────────┐    obstacle detected     ┌─────────────┐
│   FORWARD   │ ──────────────────────► │   TURNING   │
│  (0.15 m/s) │                          │ (0.3 rad/s) │
└─────────────┘ ◄─────────────────────── └─────────────┘
       │           turn complete (IMU)
       │ QR: "stop"
       ▼
┌─────────────┐
│   STOPPED   │
└─────────────┘
```

**QR Commands:**
- `left` → Turn left 90°
- `right` → Turn right 90°
- `stop` → Stop robot permanently

---

## 🔌 Autonomous Docking Pipeline

```
[Patrol Waypoints] ──► [Pre-dock Waypoint] ──► [QR Detection & Alignment] ──► [Docked]
      Nav2                  Nav2 goal              Camera + cmd_vel              STOPPED
```

---

## 📡 Key ROS2 Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/scan` | `sensor_msgs/LaserScan` | LiDAR scan data |
| `/imu/out` | `sensor_msgs/Imu` | IMU data |
| `/camera/image_raw` | `sensor_msgs/Image` | Camera feed |
| `/cmd_vel` | `geometry_msgs/Twist` | Velocity command input |
| `/wheel_controller/cmd_vel_unstamped` | `geometry_msgs/Twist` | Final wheel command |
| `/joint_states` | `sensor_msgs/JointState` | Wheel joint states |
| `/map` | `nav_msgs/OccupancyGrid` | SLAM/AMCL map |
| `/amcl_pose` | `geometry_msgs/PoseWithCovarianceStamped` | Localized robot pose |
| `/navigate_to_pose` | `nav2_msgs/action/NavigateToPose` | Nav2 goal action |

---

## 🕹️ RQT Node Graph

![RQT Graph](media/rqt_graph.png)

---

## 👨‍💻 Author

**Sesha Sai Jagadeswar Patnala**  
Robotics & Mechatronics Engineer | ISRO-NRSC Intern  
[![GitHub](https://img.shields.io/badge/GitHub-robovision2210-black?logo=github)](https://github.com/robovision2210/mechaprime_ws)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
