# Kinematics & inverse kinematics (robot arms)

Turn a target position into joint angles (IK) and back (FK). Pairs with `robotics` (servos/motors) and `pid-control`.

## Terms
- **Forward kinematics (FK)**: joint angles -> end-effector (gripper) pose. Always one answer.
- **Inverse kinematics (IK)**: desired pose -> joint angles. May have 0, 1, many solutions (elbow-up/down) or none (out of reach).
- **DOF**: degrees of freedom = independent joints. 2-DOF reaches a plane, 6-DOF reaches any position+orientation in space.
- **Workspace**: the set of reachable points. **Singularity**: a pose where the arm loses a DOF (fully stretched) — avoid; gains blow up.

## 2-link planar arm — the analytic case (memorize this)
Links `L1`, `L2`; joint 1 at the origin; target `(x, y)` in the arm's plane.
```
r2 = x*x + y*y
cos2 = (r2 - L1*L1 - L2*L2) / (2*L1*L2)         // clamp to [-1,1]
theta2 = acos(cos2)            // elbow-down; use -acos(cos2) for elbow-up
theta1 = atan2(y, x) - atan2(L2*sin(theta2), L1 + L2*cos(theta2))
```
Reachable only if `|L1 - L2| <= sqrt(r2) <= L1 + L2`. Clamp `cos2` before `acos` to survive rounding at the edge.

## 3-DOF arm in 3D (base yaw + shoulder + elbow) — very common hobby arm
Rotate the base to face the target, then solve the 2-link problem in the vertical plane through the arm:
```
base   = atan2(y, x)                 // yaw
r      = sqrt(x*x + y*y) - GRIP_OFF  // horizontal reach (minus gripper length)
z      = targetZ - BASE_HEIGHT       // height above the shoulder joint
// now 2-link IK in the (r, z) plane:
d2   = r*r + z*z
cosE = (d2 - L1*L1 - L2*L2)/(2*L1*L2); cosE = constrain(cosE,-1,1)
elbow    = acos(cosE)
shoulder = atan2(z, r) - atan2(L2*sin(elbow), L1 + L2*cos(elbow))
```
Then map to servos (below). Add a wrist servo to keep the gripper level: `wrist = -(shoulder + elbow)` (approx).

## General / higher-DOF
- **Analytic** closed-form exists for many 6-DOF arms with a spherical wrist (decouple position + orientation) — fastest, but geometry-specific.
- **Numerical** (works for any chain):
  - **CCD** (Cyclic Coordinate Descent): iterate joints from tip to base, rotating each to point the tip at the target. Simple, great for tentacle/arm on an MCU.
  - **FABRIK**: forward-and-backward reaching, fast and stable, handles chains well.
  - **Jacobian** (transpose or damped least-squares/pseudo-inverse): move joints along dq = J^+ * dx; best for velocity control and 6-DOF with orientation.
- **DH parameters** (a, alpha, d, theta) describe each link; multiply the per-joint transforms for FK. Use them once the arm is >3-DOF.

## Mapping angles -> servos (real hardware)
Servos want microseconds/degrees with per-joint **offset**, **direction**, and **limits** — calibrate each:
```cpp
int toServoUs(float rad, float offsetDeg, int dir, int minUs, int maxUs){
  float deg = degrees(rad) * dir + offsetDeg;
  deg = constrain(deg, 0, 180);
  return map((int)deg, 0, 180, minUs, maxUs);   // e.g. 500..2500
}
```
Account for gear ratios, mirrored joints, and mechanical zero. Move slowly on first run to avoid slamming into limits.

## Trajectories
- **Joint space**: interpolate each joint angle from start to goal (ease in/out) — smooth, but the tip curves.
- **Cartesian**: interpolate the (x,y,z) target and run IK each step — straight-line tip motion (needed for drawing/pick-place). Cap joint velocity; watch singularities.

## Tools (off the MCU)
On a Pi/PC: **ikpy** (Python, URDF chains), **PyBullet** (sim + IK), **ROS2 + MoveIt** (planning, collision, real arms), **Modern Robotics** library. On the MCU, code the analytic 2/3-link math directly (see the `arduino-arm-ik` template).

## Checklist
Measure link lengths + joint zeros -> pick DOF/method (2-3 link = analytic, more = CCD/FABRIK/Jacobian) -> clamp acos inputs + check reachability -> map angles to servos with offset/dir/limits -> interpolate for smooth motion -> test slow, then speed up.
