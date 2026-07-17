Advanced Computer Vision for Robotics Complete Reference
CHAPTER 1: FUNDAMENTALS OF ROBOTIC VISION
Remarks
Robotic vision differs from standard computer vision by requiring real-time performance, robustness to changing lighting/conditions, and tight integration with control loops. Key areas: Camera models, geometric vision, visual odometry, SLAM (Simultaneous Localization and Mapping), object pose estimation, and visual servoing. Applications: Autonomous navigation, manipulation, inspection, augmented reality.
Tools: Python (OpenCV, NumPy, SciPy, PyTorch), C++ (Eigen, OpenCV, PCL, ROS2), CUDA (for acceleration).

1.1 Pinhole Camera Model & Distortion
# Intrinsic Matrix K:
# | fx  0   cx |
# | 0   fy  cy |
# | 0   0   1  |
# Distortion Coefficients (Radial & Tangential): k1, k2, p1, p2, k3
# Undistortion: Map distorted pixel coordinates (u_dist, v_dist) to undistorted (u_undist, v_undist).

import numpy as np
import cv2

def undistort_points(points, K, dist_coeffs):
    """Undistort 2D points using OpenCV."""
    points = np.array(points, dtype=np.float32).reshape(-1, 1, 2)
    undistorted = cv2.undistortPoints(points, K, dist_coeffs)
    return undistorted.reshape(-1, 2)

# Example: Calibrate camera using chessboard images
def calibrate_camera(images, pattern_size=(9, 6)):
    objp = np.zeros((pattern_size[0]*pattern_size[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
    
    objpoints = []
    imgpoints = []
    
    for img in images:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)
            
    ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return K, dist

1.2 Epipolar Geometry
# Fundamental Matrix F: Relates corresponding points in two images.
# x'^T F x = 0
# Essential Matrix E: F for calibrated cameras (K known).
# E = K'^T F K
# Decompose E to get Rotation (R) and Translation (t) up to scale.

def compute_fundamental_matrix(pts1, pts2):
    """Compute Fundamental Matrix using RANSAC."""
    F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)
    return F, mask

def decompose_essential_matrix(E):
    """Decompose Essential Matrix into R and t."""
    U, S, Vt = np.linalg.svd(E)
    W = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    
    R1 = U @ W @ Vt
    R2 = U @ W.T @ Vt
    t = U[:, 2]  # Translation is the last column of U
    
    # Check for valid rotation (det(R) = 1)
    if np.linalg.det(R1) < 0:
        R1 = -R1
    if np.linalg.det(R2) < 0:
        R2 = -R2
        
    return R1, R2, t

CHAPTER 2: VISUAL ODOMETRY & SLAM
2.1 Feature-Based Visual Odometry
# Steps:
# 1. Detect features (ORB, SIFT, AKAZE).
# 2. Match features between frames (BFMatcher, FLANN).
# 3. Estimate motion using PnP or Essential Matrix.
# 4. Integrate motion over time.

class FeatureTracker:
    def __init__(self, K, dist_coeffs):
        self.K = K
        self.dist_coeffs = dist_coeffs
        self.detector = cv2.ORB_create(nfeatures=1000)
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.prev_kps = None
        self.prev_descs = None
        
    def track(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kps, descs = self.detector.detectAndCompute(gray, None)
        
        if self.prev_kps is None:
            self.prev_kps = kps
            self.prev_descs = descs
            return None
            
        matches = self.matcher.match(self.prev_descs, descs)
        matches = sorted(matches, key=lambda x: x.distance)
        
        pts1 = np.float32([self.prev_kps[m.queryIdx].pt for m in matches])
        pts2 = np.float32([kps[m.trainIdx].pt for m in matches])
        
        # Undistort points
        pts1 = undistort_points(pts1, self.K, self.dist_coeffs)
        pts2 = undistort_points(pts2, self.K, self.dist_coeffs)
        
        # Estimate motion
        E, mask = cv2.findEssentialMat(pts1, pts2, self.K, method=cv2.RANSAC, prob=0.999, threshold=1.0)
        R, t = self._recover_pose(E, pts1, pts2, mask)
        
        self.prev_kps = kps
        self.prev_descs = descs
        
        return R, t
        
    def _recover_pose(self, E, pts1, pts2, mask):
        R1, R2, t = decompose_essential_matrix(E)
        # Triangulate points to check for cheirality (positive depth)
        # Choose R, t that gives most points with positive Z
        # Simplified: Return first valid solution
        return R1, t

2.2 Direct Visual Odometry (DVO)
# Minimizes photometric error directly between pixels.
# No feature extraction needed.
# Examples: LSD-SLAM, DSO.
# Cost function: Sum of squared differences (SSD) or Normalized Cross-Correlation (NCC).

def compute_photometric_error(img1, img2, warp_matrix):
    """Warp img2 to align with img1 and compute SSD."""
    h, w = img1.shape[:2]
    warped_img2 = cv2.warpPerspective(img2, warp_matrix, (w, h))
    error = np.sum((img1.astype(float) - warped_img2.astype(float))**2)
    return error

2.3 Visual SLAM Systems
# ORB-SLAM3: Feature-based, supports monocular, stereo, RGB-D.
# DSO: Direct, sparse, optimized for speed.
# VINS-Mono: Visual-Inertial Monocular SLAM.
# Loop Closure: Detect when robot returns to a previously visited location.
# Bag of Words (BoW): Efficient place recognition using visual features.
# Graph Optimization: Minimize error across all poses and landmarks (g2o, Ceres Solver).

CHAPTER 3: OBJECT POSE ESTIMATION
3.1 Perspective-n-Point (PnP)
# Given 3D points and their 2D projections, estimate camera pose.
# Algorithms: EPnP, UPnP, Iterative PnP (Levenberg-Marquardt).

def solve_pnp(object_points, image_points, K, dist_coeffs):
    """Solve PnP problem."""
    success, rvec, tvec = cv2.solvePnP(object_points, image_points, K, dist_coeffs)
    R, _ = cv2.Rodrigues(rvec)
    return R, tvec

3.2 Deep Learning-Based Pose Estimation
# Regression: Directly predict 6D pose (x, y, z, roll, pitch, yaw).
# Detection + PnP: Detect keypoints, then use PnP.
# Dense Fusion: Combine RGB and depth information.
# Models: PoseCNN, DenseFusion, PVNet, YOLO-Pose.

import torch
import torch.nn as nn

class PoseNet(nn.Module):
    def __init__(self):
        super(PoseNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            # ... more layers ...
        )
        self.regression = nn.Sequential(
            nn.Linear(512 * 7 * 7, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(1024, 6)  # 3 for translation, 3 for rotation (quaternion or Euler)
        )
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.regression(x)
        return x

# Training loop would involve minimizing loss between predicted and ground truth pose.
# Loss function: Combination of L1/L2 loss for translation and geodesic loss for rotation.

CHAPTER 4: VISUAL SERVOING
4.1 Image-Based Visual Servoing (IBVS)
# Control robot motion based on image features.
# Error: s - s* (current features vs desired features).
# Interaction Matrix (L_s): Relates feature velocity to camera velocity.
# Control law: v = -lambda * L_s^+ * (s - s*)

def compute_interaction_matrix(features, depth):
    """Compute interaction matrix for point features."""
    L = np.zeros((2*len(features), 6))
    for i, (u, v) in enumerate(features):
        x = (u - cx) / fx
        y = (v - cy) / fy
        Z = depth[i]
        
        L[2*i, 0] = -1/Z
        L[2*i, 1] = 0
        L[2*i, 2] = x/Z
        L[2*i, 3] = x*y
        L[2*i, 4] = -(1 + x*x)
        L[2*i, 5] = y
        
        L[2*i+1, 0] = 0
        L[2*i+1, 1] = -1/Z
        L[2*i+1, 2] = y/Z
        L[2*i+1, 3] = 1 + y*y
        L[2*i+1, 4] = -x*y
        L[2*i+1, 5] = -x
        
    return L

4.2 Position-Based Visual Servoing (PBVS)
# Control based on estimated 3D pose.
# More robust to large motions but requires accurate pose estimation.

CHAPTER 5: DEEP LEARNING FOR ROBOTIC VISION
5.1 Semantic Segmentation for Navigation
# Identify drivable area, obstacles, pedestrians.
# Models: U-Net, DeepLabV3, Mask R-CNN.
# Real-time requirements: Use lightweight models (MobileNet, EfficientNet backbone).

5.2 Object Detection for Manipulation
# Detect objects to grasp.
# Models: YOLO, SSD, Faster R-CNN.
# Output: Bounding boxes, class, confidence.
# Integration: Use detection results to guide grasping algorithms.

5.3 Depth Estimation from Mono Images
# Predict depth map from single RGB image.
# Models: Monodepth2, AdaBins.
# Useful for robots with only monocular cameras.

import torch
from torchvision import transforms

def predict_depth(model, image):
    """Predict depth map from single image."""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        depth_map = model(input_tensor)
    return depth_map.squeeze().cpu().numpy()

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Event-Based Vision
# Dynamic Vision Sensors (DVS) output spikes only when pixel intensity changes.
# High temporal resolution, low latency, low power.
# Applications: High-speed tracking, HDR scenes.

Neural Radiance Fields (NeRF) for Robotics
# Represent scenes as continuous volumetric functions.
# Used for novel view synthesis, 3D reconstruction, and simulation.
# Recent advances: Instant-NGP, Plenoxels for real-time rendering.

Visual Place Recognition (VPR)
# Identify location based on visual appearance.
# Methods: NetVLAD, APGeM, CosPlace.
# Crucial for loop closure in SLAM.

Sim-to-Real Transfer
# Train vision models in simulation (Gazebo, Unity, Unreal Engine).
# Domain Randomization: Vary textures, lighting, camera parameters.
# Fine-tune on real data for better performance.

Recommended Reading
# - "Multiple View Geometry in Computer Vision" by Hartley & Zisserman
# - "Visual SLAM for Autonomous Robots" by Scaramuzza et al.
# - "Deep Learning for Visual Navigation" by Savva et al.
# - OpenCV Documentation: https://docs.opencv.org/
# - ORB-SLAM3 Paper: https://arxiv.org/abs/2007.11898
# - DSO Paper: https://vision.in.tum.de/_media/menue/specializations/computervision/dso.pdf

# End of Advanced Computer Vision for Robotics Reference