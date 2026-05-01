# Greenswip — Vision to Control
### Perception-to-Action Pipeline for Ackermann Mobile Robot
**Assignment by Revati Technologies Private Limited**

---

## Objective

Design and implement a complete ROS 2 perception-to-action pipeline for an Ackermann-steered robot in Gazebo (Ignition). The robot must visually identify a **Box** among decoy objects (Sphere, Cylinder, Capsule) and navigate toward it — across multiple shuffled object arrangements — without violating Ackermann kinematic constraints.

---

## Demo — Robustness Test (3 Shuffled Arrangements)

| Target: Center | Target: Right | Target: Left |
|---|---|---|
| ![Demo 1](media/demo1.gif) | ![Demo 2](media/demo2.gif) | ![Demo 3](media/demo3.gif) |

The robot successfully identifies and navigates to the Box in all three arrangements, demonstrating robustness of the vision and control pipeline.

---

## System Architecture

```
Gazebo Ignition (Camera Plugin)
        │
        ▼
 /camera/image_raw
        │
        ▼
  ack_perception (Vision Node)
  - OpenCV color/shape masking
  - Centroid calculation
  - Publishes: /target_error (pixel offset from center)
        │
        ▼
  ack_controller (Control Node)
  - Proportional steering from visual error
  - Respects Ackermann turning constraints
  - Publishes: /ackermann_cmd (steering angle + speed)
        │
        ▼
 Gazebo AckermannDrive Plugin → Robot Motion
```

---

## Package Structure

```
assign_ws/
├── src/
│   ├── ack_bringup/            # Launch files
│   │   └── launch/sim.launch.py
│   ├── ack_description/        # Robot model
│   │   ├── urdf/ack.urdf.xacro
│   │   └── worlds/shapes.sdf
│   ├── ack_perception/         # Vision node
│   │   └── ack_perception/vision_node.py
│   └── ack_controller/         # Control node
│       └── ack_controller/control_node.py
└── media/
    ├── demo1.gif               # Target center
    ├── demo2.gif               # Target right
    └── demo3.gif               # Target left
```

---

## Implementation Details

### Perception — `vision_node.py`
- Subscribes to `/camera/image_raw` via `image_transport`
- Applies HSV color masking to isolate the target Box
- Uses OpenCV contour detection and shape filtering to distinguish Box from decoys (Sphere, Cylinder, Capsule)
- Calculates centroid of the detected Box and publishes the horizontal pixel error (centroid_x − image_width/2) to `/target_error`

### Control — `control_node.py`
- Subscribes to `/target_error`
- Computes proportional steering angle: `δ = Kp × error`
- Clamps steering to the robot's minimum turning radius to respect Ackermann constraints
- **Does not stop and spin** — the robot always maintains forward velocity while steering, as required by Ackermann kinematics
- Publishes `AckermannDriveStamped` to `/ackermann_cmd`

### Architecture Setup
- Added `gz_ros2_control` and `ros_gz_bridge` plugins to the barebones URDF
- Configured camera plugin with `ros_gz_image` bridge on `/camera/image_raw`
- Wrote `sim.launch.py` from scratch to spawn robot, launch Gazebo world, and start all bridges

---

## Requirements

- ROS 2 Humble
- Gazebo Ignition (Fortress)
- Python 3.10+
- OpenCV (`cv_bridge`, `image_transport`)
- `ros-humble-ros-gz-bridge`, `ros-humble-ros-gz-image`
- `colcon`

---

## Build & Run

```bash
# Clone
git clone https://github.com/heroshimarobotics22/assign_ws.git
cd assign_ws

# Build
colcon build
source install/setup.bash

# Launch simulation (spawns robot + world + bridges)
ros2 launch ack_bringup sim.launch.py
```

In separate terminals:

```bash
# Terminal 2 — Vision node
source install/setup.bash
ros2 run ack_perception vision_node

# Terminal 3 — Control node
source install/setup.bash
ros2 run ack_controller control_node

# Terminal 4 — Camera node
source ~/assign_ws/install/setup.bash
ros2 run rqt_image_view rqt_image_view /camera/debug_image
```

---

## Evaluation Criteria Addressed

| Criterion | Weight | Implementation |
|---|---|---|
| Ackermann Control Kinematics | 25% | Proportional steering with turning radius clamping; no spin-in-place |
| Architecture Setup & Debugging | 20% | URDF plugins added from scratch; custom launch file and ROS-Gazebo bridges |
| Perception Logic (OpenCV) | 20% | HSV masking + contour shape filter; robust across shuffled arrangements |
| AI & Debugging Log | 20% | See attached PDF report |
| Code Quality & Documentation | 15% | This README + inline comments in nodes |

---

## Submission

**GitHub:** https://github.com/heroshimarobotics22/assign_ws

**Video:** *(add your YouTube/Drive link here)*

**PDF Report:** *(attached to submission email)*

---

## Author

**Nikhilesh Babu Pottepalem** — B.Tech Mechatronics, Hindustan Institute of Technology and Science
*Assignment submitted to Revati Technologies / Greenswip*
