Autonomous Systems & Sensor Fusion Complete Reference
CHAPTER 1: GETTING STARTED WITH AUTONOMOUS SYSTEMS
Remarks
Autonomous systems perceive their environment, make decisions, and act without human intervention. Key domains: Self-driving cars (SDV), Unmanned Aerial Vehicles (UAVs/Drones), Mobile Robotics, Marine Autonomy. Core stack: Perception (Sensors → Objects), Localization (Where am I?), Planning (Path/Behavior), Control (Actuation).
Tools: Python/C++, ROS2 (Robot Operating System), CARLA (Simulator), Gazebo, AirSim, OpenCV, PCL (Point Cloud Library), TensorFlow/PyTorch.
Hello Autonomous
# hello_autonomous.py
"""
First autonomous program: Simple PID controller for lane keeping.
"""
import numpy as np
import matplotlib.pyplot as plt

class Vehicle:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0 # Heading angle
        self.v = 10.0    # Velocity (m/s)
        
    def step(self, steering_angle, dt=0.1):
        # Bicycle model kinematics
        L = 2.5 # Wheelbase
        self.x += self.v * np.cos(self.theta) * dt
        self.y += self.v * np.sin(self.theta) * dt
        self.theta += (self.v / L) * np.tan(steering_angle) * dt
        
        # Wrap angle
        self.theta = np.arctan2(np.sin(self.theta), np.cos(self.theta))

class Lane:
    def __init__(self):
        self.width = 4.0
        
    def get_cross_track_error(self, x, y, theta):
        # Simplified: Error is just y-distance from center line y=0
        return y

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0
        
    def compute(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return np.clip(output, -0.5, 0.5) # Limit steering

# Simulation
car = Vehicle()
lane = Lane()
pid = PIDController(kp=1.0, ki=0.01, kd=0.5)

trajectory_x = []
trajectory_y = []

for i in range(1000):
    cte = lane.get_cross_track_error(car.x, car.y, car.theta)
    steering = pid.compute(cte, dt=0.1)
    car.step(steering)
    
    trajectory_x.append(car.x)
    trajectory_y.append(car.y)

plt.plot(trajectory_x, trajectory_y)
plt.axhline(0, color='r', linestyle='--')
plt.title("PID Lane Keeping")
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.axis('equal')
plt.show()

CHAPTER 2: SENSOR MODELS & CALIBRATION
LiDAR Point Clouds
# LiDAR returns (x, y, z, intensity) points.
# Sparse, accurate depth, robust to lighting.
# Challenges: Noise, occlusion, large data volume.

import open3d as o3d

def visualize_lidar(points):
    """Visualize raw LiDAR point cloud."""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.visualization.draw_geometries([pcd])

# Ground Plane Removal (RANSAC)
def remove_ground(pcd):
    plane_model, inliers = pcd.segment_plane(distance_threshold=0.05, ransac_n=3, num_iterations=1000)
    ground_cloud = pcd.select_by_index(inliers)
    non_ground_cloud = pcd.select_by_index(inliers, invert=True)
    return non_ground_cloud

Camera Model (Pinhole)
# Intrinsic Matrix K:
# | fx  0   cx |
# | 0   fy  cy |
# | 0   0   1  |
# Extrinsic Matrix [R|t]: Rotation and Translation from World to Camera.

import cv2

def project_points(world_points, K, R, t):
    """Project 3D world points to 2D image plane."""
    # Convert to camera coordinates
    pts_cam = (R @ world_points.T) + t.reshape(3, 1)
    
    # Project to image
    pts_img = K @ pts_cam
    
    # Normalize
    u = pts_img[0] / pts_img[2]
    v = pts_img[1] / pts_img[2]
    
    return np.stack([u, v], axis=-1)

Sensor Calibration
# Intrinsic Calibration: Find K (focal length, principal point) using Chessboard.
# Extrinsic Calibration: Find R, t between sensors (e.g., LiDAR ↔ Camera).
# Tools: Kalibr, MATLAB Camera Calibrator, OpenCV calibrateCamera.

CHAPTER 3: PERCEPTION PIPELINE
Object Detection (2D)
# CNN-based detectors: YOLO, SSD, Faster R-CNN.
# Output: Bounding Boxes (x, y, w, h), Class, Confidence.

import torch
import torchvision

def load_yolo():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.eval()
    return model

def detect_objects(model, image):
    results = model(image)
    boxes = results.xyxy[0].numpy() # x1, y1, x2, y2, conf, cls
    return boxes

3D Object Detection
# Methods:
# 1. Point-based: PointNet, PointRCNN (operate directly on points).
# 2. Voxel-based: VoxelNet, SECOND (convert points to voxels).
# 3. Projection-based: Project points to BEV (Bird's Eye View) or Image.

Semantic Segmentation
# Pixel-level classification.
# Architectures: U-Net, DeepLabV3, Mask R-CNN.
# Used for: Drivable area detection, lane marking identification.

CHAPTER 4: LOCALIZATION
GPS/INS Fusion
# GPS: Global position, low frequency (1-10Hz), noisy.
# IMU (Inertial Measurement Unit): Acceleration/Angular velocity, high frequency (100-1000Hz), drifts.
# Fusion: Kalman Filter (EKF) combines them.

class ExtendedKalmanFilter:
    def __init__(self, x0, P0, Q, R):
        self.x = x0 # State vector [x, y, vx, vy, theta]
        self.P = P0 # Covariance matrix
        self.Q = Q  # Process noise
        self.R = R  # Measurement noise
        
    def predict(self, u, dt):
        # Motion model f(x, u)
        self.x[0] += self.x[2] * dt
        self.x[1] += self.x[3] * dt
        self.x[2] += u[0] * dt # ax
        self.x[3] += u[1] * dt # ay
        self.x[4] += u[2] * dt # omega
        
        # Jacobian F
        F = np.eye(5)
        F[0, 2] = dt
        F[1, 3] = dt
        
        self.P = F @ self.P @ F.T + self.Q
        
    def update(self, z, H):
        # Innovation
        y = z - H @ self.x
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)
        
        self.x = self.x + K @ y
        self.P = (np.eye(5) - K @ H) @ self.P

SLAM (Simultaneous Localization and Mapping)
# Visual SLAM: ORB-SLAM3, DSO.
# LiDAR SLAM: LOAM, LeGO-LOAM, LIO-SAM.
# Graph SLAM: Pose graph optimization (g2o, Ceres Solver).

CHAPTER 5: PATH PLANNING
Global Planning (Graph Search)
# A* Algorithm: Heuristic search on grid/graph.
# Dijkstra: Shortest path, no heuristic.
# Hybrid A*: For non-holonomic vehicles (cars).

import heapq

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]
            
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            neighbor = (current[0]+dx, current[1]+dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] == 0:
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + abs(neighbor[0]-goal[0]) + abs(neighbor[1]-goal[1])
                    heapq.heappush(open_set, (f_score, neighbor))
    return []

Local Planning (Reactive)
# Dynamic Window Approach (DWA): Sample velocities, simulate trajectories, pick best.
# Artificial Potential Fields: Attractive force to goal, repulsive from obstacles.
# MPC (Model Predictive Control): Optimize control inputs over horizon.

CHAPTER 6: CONTROL SYSTEMS
Pure Pursuit Controller
# Geometric controller for path following.
# Steer towards a lookahead point on the path.

def pure_pursuit(current_pose, path, lookahead_dist):
    # Find closest point on path
    min_dist = float('inf')
    target_idx = 0
    for i, pt in enumerate(path):
        dist = np.linalg.norm(np.array(pt) - np.array([current_pose.x, current_pose.y]))
        if dist < min_dist:
            min_dist = dist
            target_idx = i
            
    # Find lookahead point
    lookahead_point = None
    for i in range(target_idx, len(path)):
        dist = np.linalg.norm(np.array(path[i]) - np.array([current_pose.x, current_pose.y]))
        if dist >= lookahead_dist:
            lookahead_point = path[i]
            break
            
    if lookahead_point is None:
        return 0
        
    # Calculate steering angle
    alpha = np.arctan2(lookahead_point[1] - current_pose.y, lookahead_point[0] - current_pose.x) - current_pose.theta
    steering = np.arctan2(2 * 2.5 * np.sin(alpha), lookahead_dist) # L=2.5
    return steering

Stanley Controller
# Used in DARPA Grand Challenge.
# Minimizes cross-track error and heading error.

def stanley_controller(cte, heading_error, k):
    return heading_error + np.arctan2(k * cte, velocity)

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
End-to-End Learning
# Input: Sensors → Output: Steering/Throttle.
# Models: CNNs, LSTMs, Transformers.
# Pros: Simple pipeline. Cons: Black box, hard to verify safety.

V2X Communication
# Vehicle-to-Everything: Share intent/state with other cars/infrastructure.
# Standards: DSRC, C-V2X.
# Benefits: Non-line-of-sight perception, cooperative planning.

Safety & Verification
# ISO 26262: Functional Safety for Road Vehicles.
# SOTIF (ISO 21448): Safety of Intended Functionality.
# Formal Methods: Verify planning algorithms mathematically.

Recommended Reading
# - "Probabilistic Robotics" by Thrun, Burgard, Fox
# - "Planning Algorithms" by LaValle
# - "Deep Learning for Autonomous Driving" (Various papers)
# - CARLA Documentation: https://carla.org/

# End of Autonomous Systems Reference