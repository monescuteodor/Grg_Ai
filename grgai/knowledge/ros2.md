# ROS 2 (Robot Operating System 2)

The standard middleware for real robots: nodes talk over **DDS** with pub/sub, services, actions. Distros (Ubuntu-based, pick the LTS): **Jazzy** (24.04), **Humble** (22.04). Languages: **rclpy** (Python), **rclcpp** (C++).

## Core concepts
- **Node**: a process that does one thing (a sensor driver, a controller).
- **Topic**: async pub/sub stream of typed messages (e.g. `/cmd_vel` = geometry_msgs/Twist, `/scan` = sensor_msgs/LaserScan, `/image_raw` = sensor_msgs/Image).
- **Service**: request/response (sync). **Action**: long goals with feedback + cancel (e.g. "navigate to X").
- **Parameters**: per-node config (set at launch). **QoS**: reliability/durability/history — must match between pub and sub (sensors often use best-effort).
- **Interfaces**: .msg/.srv/.action definitions in a package.

## Minimal Python node (publisher + subscriber)
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.sub = self.create_subscription(String, 'chatter', self.on_msg, 10)
        self.create_timer(0.5, self.tick)
    def tick(self):
        m = String(); m.data = 'hello'; self.pub.publish(m)
    def on_msg(self, msg):
        self.get_logger().info(f'heard: {msg.data}')

def main():
    rclpy.init(); rclpy.spin(Talker()); rclpy.shutdown()
```

## Workspace & build (colcon)
```
ros2_ws/src/my_pkg/           # ament_python: setup.py, package.xml, my_pkg/*.py
cd ros2_ws && colcon build --symlink-install
source install/setup.bash     # every new shell (after sourcing /opt/ros/<distro>/setup.bash)
ros2 run my_pkg talker
```
`package.xml` declares deps; `setup.py` `entry_points={'console_scripts':['talker=my_pkg.talker:main']}` maps the command.

## CLI you use daily
`ros2 run <pkg> <exe>`, `ros2 topic list|echo|pub|hz`, `ros2 node list|info`, `ros2 service call`, `ros2 param set`, `ros2 launch <pkg> <file>`, `ros2 bag record/play` (record+replay data), `rqt_graph`, `rviz2` (3D viz).

## Launch files (Python)
```python
from launch import LaunchDescription
from launch_ros.actions import Node
def generate_launch_description():
    return LaunchDescription([
        Node(package='my_pkg', executable='talker', parameters=[{'rate': 2.0}]),
    ])
```

## The big ecosystem
- **TF2**: coordinate frame transforms (base_link, odom, map, camera). **URDF/xacro**: robot model; `robot_state_publisher` broadcasts joint frames.
- **Nav2**: autonomous navigation (mapping, localization AMCL, path planning, obstacle avoidance) — cmd_vel out.
- **MoveIt 2**: arm motion planning + IK (pairs with `kinematics-ik`).
- **ros2_control**: hardware abstraction for motors/joints (controllers like diff_drive_controller).
- **Sim**: Gazebo/Ignition, or Isaac Sim. **micro-ROS**: run ROS 2 nodes on microcontrollers (ESP32/STM32) — bridge your Arduino robot into ROS 2.
- **Vision**: `cv_bridge` converts sensor_msgs/Image <-> OpenCV (see `robot-vision`).

## Typical robot graph
camera/lidar drivers -> perception nodes -> Nav2/MoveIt -> `/cmd_vel` -> ros2_control -> motors; TF2 ties frames together; rviz2 to visualize; ros2 bag to debug.

## Install & gotchas
`sudo apt install ros-<distro>-desktop`; source `/opt/ros/<distro>/setup.bash` in every shell (add to ~/.bashrc). Match **QoS** or subs get nothing. Set `ROS_DOMAIN_ID` to isolate robots on a LAN. Prefer LTS distros; keep Python deps in the package.xml.
