# Computer vision on robots (OpenCV + edge AI)

Let a robot see: detect/track objects, follow lines, read markers, estimate pose, then feed the error into control (`pid-control` / `robotics`). Language: Python + **OpenCV**. Platforms: Raspberry Pi (+ Picamera2), NVIDIA **Jetson** (GPU), Coral TPU, ESP32-CAM (basic).

## Capture
```python
import cv2
cap = cv2.VideoCapture(0)                 # USB/webcam; Pi cam -> Picamera2
while True:
    ok, frame = cap.read()
    if not ok: break
    cv2.imshow('view', frame)
    if cv2.waitKey(1) == 27: break        # Esc
```
Pi Camera: use **Picamera2** (`picam2.capture_array()`), then process with OpenCV. Downscale for speed (e.g. 320x240) on a Pi.

## Classic CV building blocks
- **Color tracking** (fast, robust for a colored ball/target):
```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (35,80,80), (85,255,255))     # green range
cnts,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if cnts:
    c = max(cnts, key=cv2.contourArea)
    x,y,w,h = cv2.boundingRect(c); cx = x + w/2
    err = cx - frame.shape[1]/2           # + = target is right of center
```
- **Thresholding/contours** for shapes; **Canny** edges; **Hough** lines (line follower) / circles.
- **Camera calibration** (`cv2.calibrateCamera` with a chessboard) → undistort + real-world scale.
- **Markers**: **ArUco / AprilTag** give ID + **6-DoF pose** (great for docking, localization, pick targets): `cv2.aruco.detectMarkers` + `estimatePoseSingleMarkers`.
- **Optical flow** / trackers (CSRT/KCF) for following a moving object; **background subtraction** for motion.

## Deep learning (objects, people)
- **YOLO** (Ultralytics): `from ultralytics import YOLO; model=YOLO('yolov8n.pt'); results=model(frame)` → boxes+classes; run the nano model on edge.
- **OpenCV DNN** module runs ONNX/Caffe/TF models (MobileNet-SSD) without a heavy framework.
- Edge acceleration: **TensorRT** (Jetson), **TFLite**/**Coral**, **ONNX Runtime**. Quantize to int8 for speed.
- Depth: stereo pairs, or an **RGB-D camera** (RealSense, OAK-D) for distance + 3D.

## Visual servoing (vision -> motion)
Turn a pixel error into motor commands with a PID (see `pid-control`):
```python
steer = pid.compute(0, err, dt)           # err = target x - center
drive(base_speed, steer)                  # differential drive mixing
```
- Center a target: PID on horizontal pixel error -> yaw/steer. Approach: PID on box area/size -> forward speed. For arms, map the detected 3D point through camera->arm calibration then run IK.
- Keep the vision loop fast and at a steady rate; smooth/limit the output; handle "target lost" (search behavior).

## ROS 2 integration (`ros2` skill)
Subscribe to `sensor_msgs/Image`, convert with **cv_bridge**, process, publish results (a `geometry_msgs/Twist` on `/cmd_vel`, or a detection topic):
```python
from cv_bridge import CvBridge
frame = CvBridge().imgmsg_to_cv2(msg, 'bgr8')
# ... detect ... then publish /cmd_vel
```
Use `image_transport` for compressed streams; visualize in **rviz2**.

## Gotchas
- Lighting kills color thresholds — prefer HSV, calibrate ranges, or use markers/DL. 
- Watch FPS: downscale, do heavy detection every N frames, run detection on a thread.
- Camera latency adds control lag — keep the pipeline short; account for it in tuning.
- Always have a "lost target" fallback so the robot doesn't drive blind.

## Checklist
Capture (downscaled) -> detect (color/marker/DL) -> compute pixel/pose error -> PID -> motors (visual servoing) -> handle lost-target -> (optional) wrap as a ROS 2 node with cv_bridge.
