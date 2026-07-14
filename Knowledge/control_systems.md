Robotics & Control Systems Complete Reference
CHAPTER 1: GETTING STARTED WITH ROBOTICS
Remarks
Robotics combines mechanical engineering, electrical engineering, and computer science to design machines that can sense, decide, and act. Key areas: kinematics (motion without forces), dynamics (motion with forces), control systems (stability and tracking), state estimation (sensor fusion), SLAM (mapping unknown environments), path planning (navigation), computer vision (perception). Modern frameworks: ROS/ROS2 (Robot Operating System), Gazebo (simulation), OpenCV (vision), MoveIt (motion planning).
Tools: Python (NumPy, SciPy, Matplotlib), ROS/ROS2, Gazebo, Arduino/Raspberry Pi (hardware), MATLAB/Simulink (control design).
Hello Robotics
# hello_robotics.py
"""
First robotics program: simulate a differential drive robot.
"""
import numpy as np
import matplotlib.pyplot as plt

class DifferentialDriveRobot:
    """Simple 2-wheel differential drive robot."""
    
    def __init__(self, x=0.0, y=0.0, theta=0.0, wheel_base=0.5):
        """
        x, y: position (meters)
        theta: orientation (radians)
        wheel_base: distance between wheels (meters)
        """
        self.x = x
        self.y = y
        self.theta = theta
        self.wheel_base = wheel_base
        self.trajectory = [(x, y)]
    
    def move(self, v_left, v_right, dt):
        """
        Update robot position given wheel velocities.
        v_left, v_right: wheel velocities (m/s)
        dt: time step (seconds)
        """
        # Linear and angular velocity
        v = (v_right + v_left) / 2.0
        omega = (v_right - v_left) / self.wheel_base
        
        # Update pose (Euler integration)
        self.x += v * np.cos(self.theta) * dt
        self.y += v * np.sin(self.theta) * dt
        self.theta += omega * dt
        
        # Normalize angle to [-pi, pi]
        self.theta = np.arctan2(np.sin(self.theta), np.cos(self.theta))
        
        self.trajectory.append((self.x, self.y))
    
    def get_pose(self):
        """Return current pose [x, y, theta]."""
        return np.array([self.x, self.y, self.theta])

# Example: drive in a circle
robot = DifferentialDriveRobot(x=0, y=0, theta=0, wheel_base=0.5)

# Constant velocities: left wheel slower than right → turn left
v_left = 0.3   # m/s
v_right = 0.5  # m/s
dt = 0.1       # 10 Hz
duration = 10  # seconds

for _ in range(int(duration / dt)):
    robot.move(v_left, v_right, dt)

print(f"Final pose: x={robot.x:.2f}, y={robot.y:.2f}, theta={np.degrees(robot.theta):.1f}°")

# Plot trajectory
traj = np.array(robot.trajectory)
plt.figure(figsize=(8, 8))
plt.plot(traj[:, 0], traj[:, 1], 'b-', linewidth=2, label='Trajectory')
plt.plot(traj[0, 0], traj[0, 1], 'go', markersize=10, label='Start')
plt.plot(traj[-1, 0], traj[-1, 1], 'rs', markersize=10, label='End')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('Differential Drive Robot Trajectory')
plt.grid(alpha=0.3)
plt.axis('equal')
plt.legend()
plt.tight_layout()
plt.savefig('robot_trajectory.png', dpi=100)
plt.show()

CHAPTER 2: KINEMATICS
Forward Kinematics
# Forward kinematics: given joint angles, compute end-effector position.
# For a robotic arm: use Denavit-Hartenberg (DH) parameters.

import numpy as np

def rotation_matrix_z(theta):
    """Rotation matrix around Z-axis."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ])

def translation_matrix(x, y, z):
    """Translation matrix."""
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])

def dh_transform(a, alpha, d, theta):
    """
    Denavit-Hartenberg transformation matrix.
    a: link length
    alpha: link twist
    d: link offset
    theta: joint angle
    """
    c_theta = np.cos(theta)
    s_theta = np.sin(theta)
    c_alpha = np.cos(alpha)
    s_alpha = np.sin(alpha)
    
    return np.array([
        [c_theta, -s_theta * c_alpha,  s_theta * s_alpha, a * c_theta],
        [s_theta,  c_theta * c_alpha, -c_theta * s_alpha, a * s_theta],
        [0,        s_alpha,            c_alpha,            d          ],
        [0,        0,                  0,                  1          ]
    ])

class RoboticArm:
    """N-link robotic arm using DH parameters."""
    
    def __init__(self, dh_params):
        """
        dh_params: list of (a, alpha, d, theta) for each joint
        """
        self.dh_params = dh_params
        self.n_joints = len(dh_params)
    
    def forward_kinematics(self, joint_angles):
        """
        Compute end-effector position given joint angles.
        joint_angles: list of joint angles (radians)
        Returns: 4x4 transformation matrix
        """
        if len(joint_angles) != self.n_joints:
            raise ValueError(f"Expected {self.n_joints} joint angles")
        
        T = np.eye(4)
        
        for i, (a, alpha, d, _) in enumerate(self.dh_params):
            theta = joint_angles[i]
            T_i = dh_transform(a, alpha, d, theta)
            T = T @ T_i
        
        return T
    
    def get_position(self, joint_angles):
        """Get end-effector position [x, y, z]."""
        T = self.forward_kinematics(joint_angles)
        return T[:3, 3]

# Example: 2-link planar arm
# Link 1: length=1m, Link 2: length=1m
arm_2link = RoboticArm([
    (1.0, 0, 0, 0),  # Link 1
    (1.0, 0, 0, 0),  # Link 2
])

# Joint angles: 45° and 90°
angles = [np.radians(45), np.radians(90)]
position = arm_2link.get_position(angles)
print(f"2-link arm end-effector: x={position[0]:.3f}, y={position[1]:.3f}")

# Example: 3-link arm (like a simple robotic arm)
arm_3link = RoboticArm([
    (0.0, np.pi/2, 0.5, 0),   # Base rotation
    (1.0, 0, 0, 0),           # Link 1
    (1.0, 0, 0, 0),           # Link 2
])

angles_3link = [np.radians(30), np.radians(45), np.radians(-20)]
position_3link = arm_3link.get_position(angles_3link)
print(f"3-link arm end-effector: x={position_3link[0]:.3f}, y={position_3link[1]:.3f}, z={position_3link[2]:.3f}")

Inverse Kinematics
# Inverse kinematics: given end-effector position, compute joint angles.
# Methods: analytical (closed-form), numerical (Jacobian-based), optimization.

def inverse_kinematics_2link(x, y, L1, L2):
    """
    Analytical inverse kinematics for 2-link planar arm.
    x, y: target position
    L1, L2: link lengths
    Returns: (theta1, theta2) or None if unreachable
    """
    # Check if reachable
    dist = np.sqrt(x**2 + y**2)
    if dist > L1 + L2 or dist < abs(L1 - L2):
        return None
    
    # Law of cosines for theta2
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_theta2 = np.clip(cos_theta2, -1, 1)  # Numerical stability
    theta2 = np.arccos(cos_theta2)  # Elbow-up configuration
    
    # Theta1
    k1 = L1 + L2 * np.cos(theta2)
    k2 = L2 * np.sin(theta2)
    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)
    
    return theta1, theta2

# Example: reach target (1.5, 0.5)
target_x, target_y = 1.5, 0.5
L1, L2 = 1.0, 1.0

result = inverse_kinematics_2link(target_x, target_y, L1, L2)
if result:
    theta1, theta2 = result
    print(f"Joint angles: theta1={np.degrees(theta1):.1f}°, theta2={np.degrees(theta2):.1f}°")
    
    # Verify with forward kinematics
    arm = RoboticArm([(L1, 0, 0, 0), (L2, 0, 0, 0)])
    pos = arm.get_position([theta1, theta2])
    print(f"Verification: x={pos[0]:.3f}, y={pos[1]:.3f}")
else:
    print("Target unreachable")

# Numerical IK using Jacobian
def jacobian_2link(theta1, theta2, L1, L2):
    """Compute Jacobian matrix for 2-link arm."""
    J = np.array([
        [-L1*np.sin(theta1) - L2*np.sin(theta1+theta2), -L2*np.sin(theta1+theta2)],
        [ L1*np.cos(theta1) + L2*np.cos(theta1+theta2),  L2*np.cos(theta1+theta2)]
    ])
    return J

def numerical_ik(target, initial_guess, L1, L2, max_iter=100, tol=1e-3):
    """
    Numerical inverse kinematics using Jacobian transpose method.
    target: [x, y]
    initial_guess: [theta1, theta2]
    """
    theta = np.array(initial_guess)
    
    for i in range(max_iter):
        # Current position
        x = L1 * np.cos(theta[0]) + L2 * np.cos(theta[0] + theta[1])
        y = L1 * np.sin(theta[0]) + L2 * np.sin(theta[0] + theta[1])
        current = np.array([x, y])
        
        # Error
        error = target - current
        if np.linalg.norm(error) < tol:
            break
        
        # Jacobian
        J = jacobian_2link(theta[0], theta[1], L1, L2)
        
        # Update (Jacobian transpose method)
        alpha = 0.5  # Step size
        theta += alpha * J.T @ error
    
    return theta

# Example
target = np.array([1.2, 0.8])
initial = [0.5, 0.5]
solution = numerical_ik(target, initial, L1, L2)
print(f"\nNumerical IK solution: theta1={np.degrees(solution[0]):.1f}°, theta2={np.degrees(solution[1]):.1f}°")

CHAPTER 3: DYNAMICS AND FORCES
Rigid Body Dynamics
# Newton-Euler equations for rigid body motion.
# F = m*a (linear), T = I*alpha (rotational)

import numpy as np

class RigidBody:
    """2D rigid body with mass and inertia."""
    
    def __init__(self, mass, inertia, x=0, y=0, theta=0):
        self.mass = mass          # kg
        self.inertia = inertia    # kg*m^2
        self.x = x                # position
        self.y = y
        self.theta = theta        # orientation
        self.vx = 0               # linear velocity
        self.vy = 0
        self.omega = 0            # angular velocity
    
    def apply_force(self, fx, fy, torque, dt):
        """Apply force and torque for time step dt."""
        # Linear acceleration
        ax = fx / self.mass
        ay = fy / self.mass
        
        # Angular acceleration
        alpha = torque / self.inertia
        
        # Update velocities
        self.vx += ax * dt
        self.vy += ay * dt
        self.omega += alpha * dt
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.theta += self.omega * dt
        
        # Normalize angle
        self.theta = np.arctan2(np.sin(self.theta), np.cos(self.theta))
    
    def get_state(self):
        """Return state vector [x, y, theta, vx, vy, omega]."""
        return np.array([self.x, self.y, self.theta, self.vx, self.vy, self.omega])

# Example: apply constant force
body = RigidBody(mass=2.0, inertia=0.5)
body.apply_force(fx=10, fy=0, torque=0, dt=0.1)
print(f"After 0.1s: x={body.x:.2f}, vx={body.vx:.2f}")

Gravity and Contact Forces
def simulate_projectile(v0, angle_deg, dt=0.01, duration=5.0):
    """Simulate projectile motion with gravity."""
    g = 9.81  # m/s^2
    angle = np.radians(angle_deg)
    
    vx = v0 * np.cos(angle)
    vy = v0 * np.sin(angle)
    
    x, y = 0, 0
    trajectory = [(x, y)]
    
    t = 0
    while t < duration and y >= 0:
        # Update position
        x += vx * dt
        y += vy * dt
        
        # Update velocity (gravity)
        vy -= g * dt
        
        trajectory.append((x, y))
        t += dt
    
    return np.array(trajectory)

# Example: launch at 45°, 20 m/s
traj = simulate_projectile(v0=20, angle_deg=45)
print(f"Max height: {traj[:, 1].max():.2f} m")
print(f"Range: {traj[-1, 0]:.2f} m")

# Plot
plt.figure(figsize=(10, 5))
plt.plot(traj[:, 0], traj[:, 1], 'b-', linewidth=2)
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.title('Projectile Motion')
plt.grid(alpha=0.3)
plt.axhline(0, color='k', linestyle='--')
plt.tight_layout()
plt.show()

Lagrangian Mechanics
# Lagrangian: L = T - V (kinetic - potential energy)
# Euler-Lagrange equation: d/dt(∂L/∂q̇) - ∂L/∂q = 0

def lagrangian_2link(theta1, theta2, theta1_dot, theta2_dot, m1, m2, L1, L2, g=9.81):
    """
    Compute Lagrangian for 2-link planar arm.
    Returns kinetic energy T and potential energy V.
    """
    # Positions of centers of mass (assuming uniform links)
    x1 = (L1/2) * np.cos(theta1)
    y1 = (L1/2) * np.sin(theta1)
    
    x2 = L1 * np.cos(theta1) + (L2/2) * np.cos(theta1 + theta2)
    y2 = L1 * np.sin(theta1) + (L2/2) * np.sin(theta1 + theta2)
    
    # Velocities
    vx1 = -(L1/2) * np.sin(theta1) * theta1_dot
    vy1 = (L1/2) * np.cos(theta1) * theta1_dot
    
    vx2 = -L1 * np.sin(theta1) * theta1_dot - (L2/2) * np.sin(theta1 + theta2) * (theta1_dot + theta2_dot)
    vy2 = L1 * np.cos(theta1) * theta1_dot + (L2/2) * np.cos(theta1 + theta2) * (theta1_dot + theta2_dot)
    
    # Kinetic energy
    T1 = 0.5 * m1 * (vx1**2 + vy1**2)
    T2 = 0.5 * m2 * (vx2**2 + vy2**2)
    T = T1 + T2
    
    # Potential energy
    V1 = m1 * g * y1
    V2 = m2 * g * y2
    V = V1 + V2
    
    return T, V, T - V

# Example
m1, m2 = 1.0, 1.0
L1, L2 = 1.0, 1.0
theta1, theta2 = np.radians(30), np.radians(45)
theta1_dot, theta2_dot = 0.5, -0.3

T, V, L = lagrangian_2link(theta1, theta2, theta1_dot, theta2_dot, m1, m2, L1, L2)
print(f"Kinetic energy: {T:.3f} J")
print(f"Potential energy: {V:.3f} J")
print(f"Lagrangian: {L:.3f} J")

CHAPTER 4: CONTROL SYSTEMS
PID Controller
# PID: Proportional-Integral-Derivative controller
# u(t) = Kp*e(t) + Ki*∫e(τ)dτ + Kd*de/dt

import numpy as np
import matplotlib.pyplot as plt

class PIDController:
    """PID controller implementation."""
    
    def __init__(self, Kp, Ki, Kd, setpoint=0.0):
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.Kd = Kd  # Derivative gain
        self.setpoint = setpoint
        
        self.integral = 0.0
        self.prev_error = 0.0
    
    def compute(self, measurement, dt):
        """
        Compute control output.
        measurement: current process value
        dt: time step
        Returns: control signal
        """
        error = self.setpoint - measurement
        
        # Proportional
        P = self.Kp * error
        
        # Integral (with anti-windup)
        self.integral += error * dt
        self.integral = np.clip(self.integral, -100, 100)  # Anti-windup
        I = self.Ki * self.integral
        
        # Derivative
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        D = self.Kd * derivative
        
        self.prev_error = error
        
        return P + I + D
    
    def reset(self):
        """Reset controller state."""
        self.integral = 0.0
        self.prev_error = 0.0

# Example: temperature control
def simulate_temperature_control(Kp, Ki, Kd, target_temp=100, duration=50):
    """Simulate PID control of a heating system."""
    pid = PIDController(Kp, Ki, Kd, setpoint=target_temp)
    
    # System parameters
    ambient_temp = 20
    heating_power = 0.5  # degrees per unit control
    cooling_rate = 0.01  # natural cooling
    
    current_temp = ambient_temp
    dt = 0.1
    
    time_log = []
    temp_log = []
    control_log = []
    
    t = 0
    while t < duration:
        # PID control
        control = pid.compute(current_temp, dt)
        control = np.clip(control, 0, 100)  # 0-100% heater
        
        # System dynamics
        heating = control * heating_power
        cooling = cooling_rate * (current_temp - ambient_temp)
        current_temp += (heating - cooling) * dt
        
        # Log
        time_log.append(t)
        temp_log.append(current_temp)
        control_log.append(control)
        
        t += dt
    
    return np.array(time_log), np.array(temp_log), np.array(control_log)

# Test different gains
plt.figure(figsize=(14, 5))

# Underdamped (oscillatory)
t1, temp1, ctrl1 = simulate_temperature_control(Kp=2.0, Ki=0.1, Kd=0.5)
plt.subplot(1, 3, 1)
plt.plot(t1, temp1, 'b-', linewidth=2)
plt.axhline(100, color='r', linestyle='--', label='Setpoint')
plt.title('Underdamped (Kp=2.0)')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.grid(alpha=0.3)
plt.legend()

# Critically damped (optimal)
t2, temp2, ctrl2 = simulate_temperature_control(Kp=1.0, Ki=0.05, Kd=1.0)
plt.subplot(1, 3, 2)
plt.plot(t2, temp2, 'g-', linewidth=2)
plt.axhline(100, color='r', linestyle='--', label='Setpoint')
plt.title('Critically Damped (Kp=1.0, Kd=1.0)')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.grid(alpha=0.3)
plt.legend()

# Overdamped (slow)
t3, temp3, ctrl3 = simulate_temperature_control(Kp=0.5, Ki=0.01, Kd=2.0)
plt.subplot(1, 3, 3)
plt.plot(t3, temp3, 'orange', linewidth=2)
plt.axhline(100, color='r', linestyle='--', label='Setpoint')
plt.title('Overdamped (Kp=0.5, Kd=2.0)')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig('pid_response.png', dpi=100)
plt.show()

State-Space Control
# State-space representation: ẋ = Ax + Bu, y = Cx + Du
# Used for multi-input multi-output (MIMO) systems.

import numpy as np
from scipy.linalg import expm

class StateSpaceSystem:
    """Linear time-invariant state-space system."""
    
    def __init__(self, A, B, C, D=None):
        """
        A: state matrix (n×n)
        B: input matrix (n×m)
        C: output matrix (p×n)
        D: feedthrough matrix (p×m), default zeros
        """
        self.A = np.array(A)
        self.B = np.array(B)
        self.C = np.array(C)
        self.D = np.array(D) if D is not None else np.zeros((C.shape[0], B.shape[1]))
        
        self.n = A.shape[0]  # Number of states
        self.m = B.shape[1]  # Number of inputs
        self.p = C.shape[0]  # Number of outputs
    
    def simulate(self, x0, u_func, dt, duration):
        """
        Simulate system response.
        x0: initial state
        u_func: function u(t) returning input vector
        dt: time step
        duration: simulation time
        """
        n_steps = int(duration / dt)
        x = np.array(x0)
        
        t_log = []
        x_log = []
        y_log = []
        u_log = []
        
        t = 0
        for _ in range(n_steps):
            u = u_func(t)
            y = self.C @ x + self.D @ u
            
            t_log.append(t)
            x_log.append(x.copy())
            y_log.append(y.copy())
            u_log.append(u.copy())
            
            # State update (Euler integration)
            x_dot = self.A @ x + self.B @ u
            x = x + x_dot * dt
            t += dt
        
        return np.array(t_log), np.array(x_log), np.array(y_log), np.array(u_log)

# Example: mass-spring-damper system
# m*x'' + c*x' + k*x = F
# State: [x, x']
# A = [[0, 1], [-k/m, -c/m]]
# B = [[0], [1/m]]
# C = [[1, 0]] (position output)

m = 1.0  # mass
k = 10.0  # spring constant
c = 2.0   # damping

A = [[0, 1], [-k/m, -c/m]]
B = [[0], [1/m]]
C = [[1, 0]]

system = StateSpaceSystem(A, B, C)

# Step response: apply unit force at t=0
def step_input(t):
    return np.array([1.0]) if t >= 0 else np.array([0.0])

t, x, y, u = system.simulate(x0=[0, 0], u_func=step_input, dt=0.01, duration=10)

plt.figure(figsize=(10, 5))
plt.plot(t, y[:, 0], 'b-', linewidth=2, label='Position')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Mass-Spring-Damper Step Response')
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

LQR (Linear Quadratic Regulator)
# LQR: optimal control for linear systems
# Minimizes: J = ∫(x'Qx + u'Ru) dt
# Solution: u = -K*x where K = R^(-1) * B' * P
# P solves Riccati equation: A'P + PA - PBR^(-1)B'P + Q = 0

from scipy.linalg import solve_continuous_are

def lqr(A, B, Q, R):
    """
    Compute LQR gain matrix.
    A, B: system matrices
    Q: state cost matrix (positive semi-definite)
    R: control cost matrix (positive definite)
    Returns: K gain matrix
    """
    # Solve continuous-time algebraic Riccati equation
    P = solve_continuous_are(A, B, Q, R)
    
    # Compute optimal gain
    K = np.linalg.inv(R) @ B.T @ P
    
    return K

# Example: stabilize inverted pendulum (linearized)
# State: [position, velocity, angle, angular_velocity]
# Simplified model:
g = 9.81
L = 1.0  # pendulum length
m = 0.5  # pendulum mass
M = 1.0  # cart mass

# Linearized state-space (around upright position)
A = [
    [0, 1, 0, 0],
    [0, 0, -m*g/M, 0],
    [0, 0, 0, 1],
    [0, 0, (M+m)*g/(M*L), 0]
]

B = [
    [0],
    [1/M],
    [0],
    [-1/(M*L)]
]

A = np.array(A)
B = np.array(B)

# Cost matrices
Q = np.diag([10, 1, 100, 1])  # Penalize position and angle heavily
R = np.array([[0.01]])         # Allow large control effort

K = lqr(A, B, Q, R)
print(f"LQR gain matrix K:\n{K}")

# Simulate closed-loop system
A_cl = A - B @ K
system_cl = StateSpaceSystem(A_cl, B, np.eye(4))

# Initial condition: pendulum slightly tilted
x0 = [0, 0, 0.1, 0]  # 0.1 rad tilt

def zero_input(t):
    return np.array([0.0])

t, x, y, u = system_cl.simulate(x0, zero_input, dt=0.01, duration=5)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(t, x[:, 0], label='Position')
plt.plot(t, x[:, 2], label='Angle')
plt.xlabel('Time (s)')
plt.ylabel('State')
plt.title('LQR Stabilization')
plt.legend()
plt.grid(alpha=0.3)

plt.subplot(1, 2, 2)
u_control = -K @ x.T
plt.plot(t, u_control[0, :], 'r-', label='Control Force')
plt.xlabel('Time (s)')
plt.ylabel('Force (N)')
plt.title('Control Input')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

CHAPTER 5: STATE ESTIMATION
Kalman Filter
# Kalman filter: optimal state estimator for linear systems with Gaussian noise.
# Predict: x̂_k = F*x̂_{k-1} + B*u_k, P_k = F*P_{k-1}*F' + Q
# Update: K = P_k*H'*(H*P_k*H' + R)^(-1), x̂_k = x̂_k + K*(z_k - H*x̂_k)

import numpy as np

class KalmanFilter:
    """Linear Kalman filter."""
    
    def __init__(self, F, H, Q, R, B=None):
        """
        F: state transition matrix
        H: observation matrix
        Q: process noise covariance
        R: measurement noise covariance
        B: control input matrix (optional)
        """
        self.F = np.array(F)
        self.H = np.array(H)
        self.Q = np.array(Q)
        self.R = np.array(R)
        self.B = np.array(B) if B is not None else None
        
        self.n = F.shape[0]  # State dimension
        self.m = H.shape[0]  # Measurement dimension
        
        # Initialize state and covariance
        self.x = np.zeros((self.n, 1))
        self.P = np.eye(self.n)
    
    def predict(self, u=None):
        """Predict step (time update)."""
        # State prediction
        if self.B is not None and u is not None:
            self.x = self.F @ self.x + self.B @ u
        else:
            self.x = self.F @ self.x
        
        # Covariance prediction
        self.P = self.F @ self.P @ self.F.T + self.Q
        
        return self.x
    
    def update(self, z):
        """Update step (measurement update)."""
        z = np.array(z).reshape(-1, 1)
        
        # Innovation (measurement residual)
        y = z - self.H @ self.x
        
        # Innovation covariance
        S = self.H @ self.P @ self.H.T + self.R
        
        # Kalman gain
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # State update
        self.x = self.x + K @ y
        
        # Covariance update (Joseph form for numerical stability)
        I = np.eye(self.n)
        self.P = (I - K @ self.H) @ self.P
        
        return self.x
    
    def filter(self, measurements, controls=None):
        """Run Kalman filter on sequence of measurements."""
        n_steps = len(measurements)
        x_log = []
        P_log = []
        
        for i in range(n_steps):
            u = controls[i] if controls is not None else None
            self.predict(u)
            self.update(measurements[i])
            
            x_log.append(self.x.copy())
            P_log.append(self.P.copy())
        
        return np.array(x_log), np.array(P_log)

# Example: track a moving object with noisy measurements
np.random.seed(42)

# System: constant velocity model
# State: [x, y, vx, vy]
dt = 0.1
F = [
    [1, 0, dt, 0],
    [0, 1, 0, dt],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

# Measurement: only position
H = [
    [1, 0, 0, 0],
    [0, 1, 0, 0]
]

# Process noise
Q = np.eye(4) * 0.1

# Measurement noise
R = np.eye(2) * 2.0

kf = KalmanFilter(F, H, Q, R)

# True trajectory: circular motion
t = np.arange(0, 10, dt)
true_x = 5 * np.cos(0.5 * t)
true_y = 5 * np.sin(0.5 * t)
true_vx = -2.5 * np.sin(0.5 * t)
true_vy = 2.5 * np.cos(0.5 * t)

# Noisy measurements
meas_x = true_x + np.random.randn(len(t)) * np.sqrt(R[0, 0])
meas_y = true_y + np.random.randn(len(t)) * np.sqrt(R[1, 1])
measurements = [np.array([meas_x[i], meas_y[i]]) for i in range(len(t))]

# Run Kalman filter
x_est, P_est = kf.filter(measurements)

# Plot results
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(true_x, true_y, 'g-', linewidth=2, label='True')
plt.plot(meas_x, meas_y, 'b.', alpha=0.3, label='Measurements')
plt.plot(x_est[:, 0], x_est[:, 1], 'r-', linewidth=2, label='Kalman Estimate')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('2D Tracking')
plt.legend()
plt.grid(alpha=0.3)
plt.axis('equal')

plt.subplot(1, 2, 2)
plt.plot(t, true_x, 'g-', linewidth=2, label='True X')
plt.plot(t, meas_x, 'b.', alpha=0.3, label='Measurements')
plt.plot(t, x_est[:, 0], 'r-', linewidth=2, label='Kalman')
plt.fill_between(t, 
                 x_est[:, 0] - 2*np.sqrt(P_est[:, 0, 0]),
                 x_est[:, 0] + 2*np.sqrt(P_est[:, 0, 0]),
                 alpha=0.2, color='r', label='95% Confidence')
plt.xlabel('Time (s)')
plt.ylabel('X Position (m)')
plt.title('X Position with Uncertainty')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('kalman_tracking.png', dpi=100)
plt.show()

Extended Kalman Filter (EKF)
# EKF: Kalman filter for nonlinear systems
# Linearizes system around current estimate using Jacobians

class ExtendedKalmanFilter:
    """Extended Kalman filter for nonlinear systems."""
    
    def __init__(self, f, h, Q, R, n, m):
        """
        f: state transition function f(x, u)
        h: measurement function h(x)
        Q: process noise covariance
        R: measurement noise covariance
        n: state dimension
        m: measurement dimension
        """
        self.f = f
        self.h = h
        self.Q = Q
        self.R = R
        self.n = n
        self.m = m
        
        self.x = np.zeros((n, 1))
        self.P = np.eye(n)
    
    def jacobian_f(self, x, u, eps=1e-6):
        """Compute Jacobian of f numerically."""
        F = np.zeros((self.n, self.n))
        for i in range(self.n):
            x_plus = x.copy()
            x_plus[i, 0] += eps
            F[:, i] = ((self.f(x_plus, u) - self.f(x, u)) / eps).flatten()
        return F
    
    def jacobian_h(self, x, eps=1e-6):
        """Compute Jacobian of h numerically."""
        H = np.zeros((self.m, self.n))
        for i in range(self.n):
            x_plus = x.copy()
            x_plus[i, 0] += eps
            H[:, i] = ((self.h(x_plus) - self.h(x)) / eps).flatten()
        return H
    
    def predict(self, u=None):
        """Predict step."""
        self.x = self.f(self.x, u)
        F = self.jacobian_f(self.x, u)
        self.P = F @ self.P @ F.T + self.Q
        return self.x
    
    def update(self, z):
        """Update step."""
        z = np.array(z).reshape(-1, 1)
        H = self.jacobian_h(self.x)
        
        y = z - self.h(self.x)
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)
        
        self.x = self.x + K @ y
        I = np.eye(self.n)
        self.P = (I - K @ H) @ self.P
        
        return self.x

# Example: track object with range-bearing measurements
# State: [x, y, vx, vy]
# Measurement: [range, bearing] from origin

def f_nonlinear(x, u):
    """Constant velocity model."""
    dt = 0.1
    F = np.array([
        [1, 0, dt, 0],
        [0, 1, 0, dt],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    return F @ x

def h_polar(x):
    """Convert Cartesian to polar (range, bearing)."""
    px, py = x[0, 0], x[1, 0]
    range_meas = np.sqrt(px**2 + py**2)
    bearing = np.arctan2(py, px)
    return np.array([[range_meas], [bearing]])

# Initialize EKF
Q = np.eye(4) * 0.1
R = np.diag([1.0, 0.05])  # 1m range noise, 0.05 rad bearing noise
ekf = ExtendedKalmanFilter(f_nonlinear, h_polar, Q, R, n=4, m=2)

# Simulate
np.random.seed(42)
t = np.arange(0, 10, 0.1)
true_x = 3 * t * np.cos(0.3 * t)
true_y = 3 * t * np.sin(0.3 * t)

measurements = []
for i in range(len(t)):
    px, py = true_x[i], true_y[i]
    range_true = np.sqrt(px**2 + py**2)
    bearing_true = np.arctan2(py, px)
    
    range_noisy = range_true + np.random.randn() * np.sqrt(R[0, 0])
    bearing_noisy = bearing_true + np.random.randn() * np.sqrt(R[1, 1])
    measurements.append(np.array([range_noisy, bearing_noisy]))

# Run EKF
x_est = []
for z in measurements:
    ekf.predict()
    ekf.update(z)
    x_est.append(ekf.x.copy())

x_est = np.array(x_est).reshape(-1, 4)

plt.figure(figsize=(10, 8))
plt.plot(true_x, true_y, 'g-', linewidth=2, label='True')
plt.plot(x_est[:, 0], x_est[:, 1], 'r-', linewidth=2, label='EKF Estimate')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('EKF Tracking with Polar Measurements')
plt.legend()
plt.grid(alpha=0.3)
plt.axis('equal')
plt.tight_layout()
plt.show()

Particle Filter
# Particle filter: Monte Carlo approximation of posterior
# Represents distribution with weighted samples (particles)
# Steps: predict (move particles), update (weight by likelihood), resample

import numpy as np

class ParticleFilter:
    """Particle filter for nonlinear, non-Gaussian systems."""
    
    def __init__(self, n_particles, state_dim, process_noise, measurement_noise):
        self.n_particles = n_particles
        self.state_dim = state_dim
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise
        
        # Initialize particles uniformly
        self.particles = np.random.randn(n_particles, state_dim)
        self.weights = np.ones(n_particles) / n_particles
    
    def predict(self, motion_model):
        """
        Predict step: move particles according to motion model.
        motion_model: function(x) -> x_next
        """
        for i in range(self.n_particles):
            # Apply motion model
            self.particles[i] = motion_model(self.particles[i])
            
            # Add process noise
            self.particles[i] += np.random.randn(self.state_dim) * self.process_noise
    
    def update(self, measurement, measurement_model):
        """
        Update step: weight particles by likelihood.
        measurement: observed measurement
        measurement_model: function(x) -> expected_measurement
        """
        for i in range(self.n_particles):
            expected = measurement_model(self.particles[i])
            error = measurement - expected
            likelihood = np.exp(-0.5 * np.sum(error**2) / self.measurement_noise**2)
            self.weights[i] *= likelihood
        
        # Normalize weights
        self.weights += 1e-300  # Avoid zero
        self.weights /= np.sum(self.weights)
    
    def resample(self):
        """Resample particles based on weights (systematic resampling)."""
        positions = (np.arange(self.n_particles) + np.random.rand()) / self.n_particles
        cumulative = np.cumsum(self.weights)
        indices = np.searchsorted(cumulative, positions)
        
        self.particles = self.particles[indices]
        self.weights = np.ones(self.n_particles) / self.n_particles
    
    def estimate(self):
        """Return weighted mean of particles."""
        return np.average(self.particles, weights=self.weights, axis=0)

# Example: 1D localization with landmarks
np.random.seed(42)

# True position
true_x = 0.0
true_v = 1.0  # velocity

# Landmarks
landmarks = [2.0, 5.0, 8.0]

# Particle filter
pf = ParticleFilter(n_particles=500, state_dim=2, process_noise=0.1, measurement_noise=0.5)

# Initialize particles around true position
pf.particles[:, 0] = true_x + np.random.randn(500) * 0.5
pf.particles[:, 1] = true_v + np.random.randn(500) * 0.1

def motion_model(x):
    """Constant velocity model."""
    dt = 0.1
    x_next = x.copy()
    x_next[0] += x[1] * dt  # position += velocity * dt
    return x_next

def measurement_model(x):
    """Measure distance to nearest landmark."""
    pos = x[0]
    distances = [abs(pos - lm) for lm in landmarks]
    return min(distances)

# Simulate
estimates = []
for t in range(100):
    # True motion
    true_x += true_v * 0.1
    
    # Measurement (distance to nearest landmark)
    distances = [abs(true_x - lm) for lm in landmarks]
    measurement = min(distances) + np.random.randn() * 0.5
    
    # Particle filter steps
    pf.predict(motion_model)
    pf.update(measurement, measurement_model)
    pf.resample()
    
    estimates.append(pf.estimate()[0])

# Plot
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(pf.particles[:, 0], np.zeros_like(pf.particles[:, 0]), 'b.', alpha=0.3, label='Particles')
plt.plot(true_x, 0, 'go', markersize=10, label='True Position')
plt.plot(estimates[-1], 0, 'rs', markersize=10, label='PF Estimate')
for lm in landmarks:
    plt.plot(lm, 0, 'k^', markersize=10, label='Landmark' if lm == landmarks[0] else "")
plt.xlabel('X Position')
plt.title('Particle Distribution')
plt.legend()
plt.grid(alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(estimates, 'r-', linewidth=2, label='PF Estimate')
plt.axhline(true_x, color='g', linestyle='--', label='True')
plt.xlabel('Time Step')
plt.ylabel('Position')
plt.title('Position Estimate Over Time')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

CHAPTER 6: SLAM (SIMULTANEOUS LOCALIZATION AND MAPPING)
...