Advanced Robotics Perception & Sensor Fusion Complete Reference
CHAPTER 1: GETTING STARTED WITH ROBOTICS PERCEPTION
Remarks
Robotics perception is the ability of a robot to interpret sensory data to understand its environment. It bridges raw sensor data (pixels, point clouds, IMU readings) and high-level semantic understanding (objects, maps, poses). Key challenges: noise, occlusion, dynamic environments, real-time constraints, and sensor calibration. Modern approaches combine classical geometry (Kalman Filters, ICP) with deep learning (CNNs, Transformers). Applications: Autonomous driving, warehouse robotics, drone navigation, AR/VR.
Tools: Python/C++, ROS2, OpenCV, PCL (Point Cloud Library), Eigen (linear algebra), PyTorch/TensorFlow, CARLA/Gazebo (simulation).
Hello Perception
# hello_perception.py
"""
First perception program: Simulate a noisy distance sensor and filter it.
"""
import numpy as np
import matplotlib.pyplot as plt

def simulate_lidar(distance, noise_std=0.1, num_samples=100):
    """Simulate LiDAR measurements with Gaussian noise."""
    return distance + np.random.normal(0, noise_std, num_samples)

def moving_average_filter(data, window_size=5):
    """Simple moving average filter."""
    kernel = np.ones(window_size) / window_size
    return np.convolve(data, kernel, mode='valid')

# Simulation
true_dist = 5.0
measurements = simulate_lidar(true_dist, noise_std=0.5, num_samples=200)
filtered = moving_average_filter(measurements, window_size=10)

plt.figure(figsize=(10, 5))
plt.plot(measurements, label='Noisy Measurements', alpha=0.5)
plt.plot(filtered, label='Filtered (Moving Avg)', linewidth=2)
plt.axhline(true_dist, color='r', linestyle='--', label='True Distance')
plt.xlabel('Time Step')
plt.ylabel('Distance (m)')
plt.title('Sensor Noise Filtering')
plt.legend()
plt.grid(True)
plt.show()

Perception Pipeline
# 1. Sensing: Raw data acquisition (Camera, LiDAR, Radar, IMU).
# 2. Preprocessing: Denoising, rectification, synchronization.
# 3. Feature Extraction: Edges, corners, keypoints, clusters.
# 4. Estimation: State estimation (pose, velocity) using filters.
# 5. Interpretation: Object detection, segmentation, mapping.
# 6. Fusion: Combining multiple sensors for robustness.

CHAPTER 2: CAMERA MODELS & CALIBRATION
Pinhole Camera Model
# Projects 3D world points to 2D image plane.
# Intrinsic Matrix K:
# | fx  0   cx |
# | 0   fy  cy |
# | 0   0   1  |
# Extrinsic Matrix [R|t]: Rotation and Translation from World to Camera.

import cv2
import numpy as np

def project_points(world_points, K, R, t):
    """Project 3D points to 2D image coordinates."""
    # Convert to camera coordinates
    pts_cam = (R @ world_points.T) + t.reshape(3, 1)
    
    # Project to image
    pts_img = K @ pts_cam
    
    # Normalize
    u = pts_img[0] / pts_img[2]
    v = pts_img[1] / pts_img[2]
    
    return np.stack([u, v], axis=-1)

# Example
K = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]])
R = np.eye(3)
t = np.array([0, 0, 0])
world_pts = np.array([[1, 1, 5], [-1, -1, 5], [0, 0, 10]]).T

img_pts = project_points(world_pts, K, R, t)
print("Projected Points:", img_pts)

Camera Calibration
# Find intrinsic parameters (K) and distortion coefficients.
# Uses chessboard patterns with known geometry.

def calibrate_camera(images, pattern_size=(9, 6)):
    """Calibrate camera using chessboard images."""
    objp = np.zeros((pattern_size[0]*pattern_size[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
    
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    for img in images:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
        
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)
            
    ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return K, dist

# Undistort an image
def undistort_image(img, K, dist):
    h, w = img.shape[:2]
    new_K, roi = cv2.getOptimalNewCameraMatrix(K, dist, (w,h), 1, (w,h))
    dst = cv2.undistort(img, K, dist, None, new_K)
    return dst

CHAPTER 3: LIDAR PROCESSING
Point Cloud Basics
# LiDAR returns sparse 3D points (x, y, z, intensity).
# Formats: .pcd, .las, .bin.
# Challenges: Large data volume, unstructured nature.

import open3d as o3d

def load_and_visualize_pcd(path):
    """Load and visualize a point cloud."""
    pcd = o3d.io.read_point_cloud(path)
    o3d.visualization.draw_geometries([pcd])

# Downsample point cloud (Voxel Grid)
def voxel_downsample(pcd, voxel_size=0.05):
    """Reduce point cloud density while preserving structure."""
    return pcd.voxel_down_sample(voxel_size)

# Estimate normals
def estimate_normals(pcd, radius=0.1, max_nn=30):
    """Estimate surface normals for each point."""
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius, max_nn=max_nn))
    return pcd

Ground Plane Removal (RANSAC)
# Separate ground points from objects for obstacle detection.

def remove_ground_ransac(pcd, distance_threshold=0.05, ransac_n=3, num_iterations=1000):
    """Remove ground plane using RANSAC."""
    plane_model, inliers = pcd.segment_plane(distance_threshold=distance_threshold, ransac_n=ransac_n, num_iterations=num_iterations)
    ground_cloud = pcd.select_by_index(inliers)
    non_ground_cloud = pcd.select_by_index(inliers, invert=True)
    return non_ground_cloud, ground_cloud

Euclidean Clustering
# Group points into objects based on distance.

def euclidean_clustering(pcd, distance_threshold=0.2, min_cluster_size=10, max_cluster_size=10000):
    """Cluster points into separate objects."""
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        labels = np.array(pcd.cluster_dbscan(eps=distance_threshold, min_points=min_cluster_size))
    
    max_label = labels.max()
    print(f"Found {max_label + 1} clusters.")
    
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0
    pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
    return pcd, labels

CHAPTER 4: VISUAL ODOMETRY & SLAM
Feature-Based Visual Odometry
# Track features between frames to estimate camera motion.
# Steps: Detect features -> Match features -> Estimate Pose (PnP/RANSAC).

def extract_orb_features(img):
    """Extract ORB features from an image."""
    orb = cv2.ORB_create(nfeatures=1000)
    keypoints, descriptors = orb.detectAndCompute(img, None)
    return keypoints, descriptors

def match_features(desc1, desc2):
    """Match descriptors using BFMatcher."""
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc1, desc2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

def estimate_pose(matches, kp1, kp2, K):
    """Estimate relative pose using Essential Matrix."""
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])
    
    E, mask = cv2.findEssentialMat(pts1, pts2, K, method=cv2.RANSAC, prob=0.999, threshold=1.0)
    _, R, t, mask = cv2.recoverPose(E, pts1, pts2, K)
    
    return R, t

Direct Visual Odometry
# Use pixel intensities directly instead of features.
# Minimizes photometric error between frames.
# Examples: DSO, LSD-SLAM.

SLAM (Simultaneous Localization and Mapping)
# Visual SLAM: ORB-SLAM3, DSO, VINS-Mono.
# LiDAR SLAM: LOAM, LeGO-LOAM, LIO-SAM, FAST-LIO.
# Graph SLAM: Optimize pose graph to reduce drift.

# Loop Closure: Detect when robot returns to a previously visited location to correct drift.
# Bag of Words (BoW): Efficient place recognition using visual features.

CHAPTER 5: SENSOR FUSION
Kalman Filter
# Optimal estimator for linear systems with Gaussian noise.
# Predict: Update state estimate based on motion model.
# Update: Correct estimate based on sensor measurement.

class KalmanFilter:
    def __init__(self, F, H, Q, R, P0, x0):
        self.F = F # State transition matrix
        self.H = H # Observation matrix
        self.Q = Q # Process noise covariance
        self.R = R # Measurement noise covariance
        self.P = P0 # Initial error covariance
        self.x = x0 # Initial state
        
    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        
    def update(self, z):
        y = z - self.H @ self.x # Innovation
        S = self.H @ self.P @ self.H.T + self.R # Innovation covariance
        K = self.P @ self.H.T @ np.linalg.inv(S) # Kalman Gain
        
        self.x = self.x + K @ y
        self.P = (np.eye(len(self.x)) - K @ self.H) @ self.P

Extended Kalman Filter (EKF)
# For non-linear systems. Linearizes around current estimate using Jacobians.
# Used in GPS/INS fusion, visual-inertial odometry.

Unscented Kalman Filter (UKF)
# Uses sigma points to capture mean and covariance more accurately than EKF for highly non-linear systems.

Particle Filter
# Represents probability distribution with a set of particles.
# Good for non-Gaussian noise and multi-modal distributions (e.g., global localization).

Multi-Sensor Fusion Architectures
# 1. Loose Coupling: Each sensor processes data independently, then results are fused.
# 2. Tight Coupling: Raw data from multiple sensors is fused jointly (e.g., visual-inertial).
# 3. Centralized vs. Decentralized: Single fusion center vs. distributed fusion.

CHAPTER 6: DEEP LEARNING FOR PERCEPTION
Object Detection (2D/3D)
# 2D: YOLO, Faster R-CNN, SSD.
# 3D: PointPillars, VoxelNet, PV-RCNN (LiDAR), MonoDepth (Camera).

import torch
import torchvision

def load_yolo():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.eval()
    return model

def detect_objects(model, img):
    results = model(img)
    boxes = results.xyxy[0].numpy() # x1, y1, x2, y2, conf, cls
    return boxes

Semantic Segmentation
# Pixel-level classification.
# Architectures: U-Net, DeepLabV3, Mask R-CNN.
# Used for: Drivable area, lane markings, free space.

Instance Segmentation
# Distinguishes between individual objects of the same class.
# Example: Separating two cars.

Panoptic Segmentation
# Combines semantic and instance segmentation.
# Assigns both class label and instance ID to every pixel.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Event-Based Vision
# Dynamic Vision Sensors (DVS) output spikes only when pixel intensity changes.
# Benefits: High temporal resolution, low latency, low power.
# Applications: High-speed tracking, HDR scenes.

Neural Radiance Fields (NeRF)
# Represent scenes as continuous volumetric functions.
# Used for novel view synthesis and 3D reconstruction.
# Recent advances: Instant-NGP, Plenoxels for real-time rendering.

Occupancy Networks
# Implicit representation of 3D geometry.
# Predicts whether a point in space is occupied or free.
# Used for path planning and collision avoidance.

Recommended Reading
# - "Probabilistic Robotics" by Thrun, Burgard, Fox
# - "Multiple View Geometry in Computer Vision" by Hartley & Zisserman
# - "Deep Learning for Autonomous Driving" (Various papers)
# - ORB-SLAM3 Paper: https://arxiv.org/abs/2007.11898
# - LOAM Paper: https://www.roboticsproceedings.org/rss10/p43.pdf

# Online Resources
# - Open3D Documentation: http://www.open3d.org/
# - PCL Documentation: https://pointclouds.org/
# - ROS2 Navigation2: https://navigation.ros.org/
# - KITTI Dataset: http://www.cvlibs.net/datasets/kitti/

# End of Advanced Robotics Perception Reference