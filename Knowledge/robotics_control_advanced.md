Advanced Robotics Control & Motion Planning Complete Reference
CHAPTER 1: GETTING STARTED WITH ROBOTICS CONTROL
Remarks
Robotics control involves designing algorithms to make robots move and interact with their environment safely and efficiently. Key areas: Kinematics (position/velocity), Dynamics (forces/torques), Feedback Control (PID, State-Space), Optimal Control (LQR, MPC), and Motion Planning (path finding, trajectory generation). Applications: Industrial manipulators, mobile robots, drones, humanoid robots, autonomous vehicles.
Tools: Python (NumPy, SciPy, Control Systems Library), MATLAB/Simulink, ROS2, CoppeliaSim, Gazebo, Pinocchio (rigid body dynamics).
Hello Control Theory
# hello_control.py
"""
First control program: Simulate a simple mass-spring-damper system.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def mass_spring_damper(state, t, m, c, k):
    """
    Differential equations for mass-spring-damper.
    state = [position, velocity]
    m: mass, c: damping coefficient, k: spring constant
    """
    x, v = state
    dxdt = v
    dvdt = -(c/m)*v - (k/m)*x
    return [dxdt, dvdt]

# Parameters
m = 1.0  # kg
c = 0.5  # Ns/m
k = 10.0 # N/m

# Initial conditions: displaced by 1m, zero velocity
x0 = 1.0
v0 = 0.0
state0 = [x0, v0]

# Time vector
t = np.linspace(0, 10, 1000)

# Solve ODE
solution = odeint(mass_spring_damper, state0, t, args=(m, c, k))
x = solution[:, 0]
v = solution[:, 1]

plt.figure(figsize=(10, 5))
plt.plot(t, x, label='Position')
plt.plot(t, v, label='Velocity')
plt.xlabel('Time (s)')
plt.ylabel('State')
plt.title('Mass-Spring-Damper Response')
plt.legend()
plt.grid(True)
plt.show()

Control System Types
# Open-Loop: No feedback. Output does not affect input. (e.g., toaster)
# Closed-Loop (Feedback): Output is measured and compared to reference. Error drives correction. (e.g., cruise control)

CHAPTER 2: CLASSICAL CONTROL
PID Controller
# Proportional-Integral-Derivative controller.
# u(t) = Kp*e(t) + Ki*∫e(t)dt + Kd*de(t)/dt
# Most common industrial controller.

class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint=0.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        
        self.integral = 0.0
        self.prev_error = 0.0
        
    def compute(self, measurement, dt):
        error = self.setpoint - measurement
        
        # Proportional term
        P = self.Kp * error
        
        # Integral term (with anti-windup)
        self.integral += error * dt
        I = self.Ki * self.integral
        
        # Derivative term
        D = self.Kd * (error - self.prev_error) / dt if dt > 0 else 0
        
        self.prev_error = error
        
        output = P + I + D
        return output
    
    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0

# Example: Control a simple integrator plant (dx/dt = u)
def simulate_pid(Kp, Ki, Kd, target=1.0, duration=10.0, dt=0.01):
    pid = PIDController(Kp, Ki, Kd, setpoint=target)
    
    x = 0.0  # Initial position
    history_x = []
    history_t = []
    
    t = 0.0
    while t < duration:
        u = pid.compute(x, dt)
        
        # Plant dynamics: dx = u * dt
        x += u * dt
        
        history_x.append(x)
        history_t.append(t)
        
        t += dt
        
    return history_t, history_x

t, x = simulate_pid(Kp=2.0, Ki=0.1, Kd=0.5)
plt.plot(t, x)
plt.axhline(1.0, color='r', linestyle='--')
plt.title("PID Control of Integrator")
plt.xlabel("Time")
plt.ylabel("Position")
plt.grid(True)
plt.show()

Tuning Methods
# Ziegler-Nichols: Experimental method based on step response.
# Cohen-Coon: Analytical method for first-order plus dead time models.
# Manual Tuning: Increase Kp until oscillation, then add Kd to dampen, then Ki to remove steady-state error.

Transfer Functions
# Representation in Laplace domain: G(s) = Y(s)/U(s)
# Used for stability analysis (Bode plots, Nyquist criterion).

import control as ctrl

# Define a transfer function: G(s) = 1 / (s^2 + 0.5s + 10)
num = [1]
den = [1, 0.5, 10]
sys = ctrl.TransferFunction(num, den)

# Step response
t, y = ctrl.step_response(sys)
plt.plot(t, y)
plt.title("Step Response of Second Order System")
plt.grid(True)
plt.show()

CHAPTER 3: MODERN CONTROL STATE-SPACE
State-Space Representation
# x_dot = Ax + Bu
# y = Cx + Du
# x: state vector, u: input, y: output
# A: system matrix, B: input matrix, C: output matrix, D: feedthrough matrix

# Example: Inverted Pendulum (linearized)
# States: [theta, theta_dot]
# Input: Torque

A = np.array([[0, 1],
              [10, 0]])  # Unstable system
B = np.array([[0],
              [1]])
C = np.array([[1, 0]])
D = np.array([[0]])

# Check controllability
Co = np.hstack([B, A @ B])
rank_Co = np.linalg.matrix_rank(Co)
print(f"Controllability Rank: {rank_Co} (Full rank: {A.shape[0]})")

Observability
# Can we estimate the full state from outputs?
# Observability Matrix: Ob = [C; CA; CA^2; ...]

Ob = np.vstack([C, C @ A])
rank_Ob = np.linalg.matrix_rank(Ob)
print(f"Observability Rank: {rank_Ob}")

Kalman Filter
# Optimal estimator for linear systems with Gaussian noise.
# Combines prediction (model) and update (measurement).

class KalmanFilter:
    def __init__(self, A, B, H, Q, R, P0, x0):
        self.A = A  # State transition
        self.B = B  # Control input
        self.H = H  # Observation model
        self.Q = Q  # Process noise covariance
        self.R = R  # Measurement noise covariance
        self.P = P0 # Error covariance
        self.x = x0 # State estimate
        
    def predict(self, u):
        # Prediction step
        self.x = self.A @ self.x + self.B @ u
        self.P = self.A @ self.P @ self.A.T + self.Q
        
    def update(self, z):
        # Update step
        y = z - self.H @ self.x  # Innovation
        S = self.H @ self.P @ self.H.T + self.R  # Innovation covariance
        K = self.P @ self.H.T @ np.linalg.inv(S)  # Kalman Gain
        
        self.x = self.x + K @ y
        self.P = (np.eye(len(self.x)) - K @ self.H) @ self.P

# Example usage would involve simulating a system with noise and measurements

Linear Quadratic Regulator (LQR)
# Optimal control law: u = -Kx
# Minimizes cost function: J = ∫(x'Qx + u'Ru)dt

# Solve Algebraic Riccati Equation (ARE)
# A'P + PA - PBR^-1B'P + Q = 0
# K = R^-1B'P

from scipy.linalg import solve_continuous_are

Q = np.diag([10, 1])  # Penalize angle more than velocity
R = np.array([[0.1]]) # Penalize control effort

P = solve_continuous_are(A, B, Q, R)
K = np.linalg.inv(R) @ B.T @ P

print(f"LQR Gain K: {K}")

# Closed loop system: A_cl = A - BK
A_cl = A - B @ K
eigenvalues = np.linalg.eigvals(A_cl)
print(f"Closed-loop eigenvalues: {eigenvalues}")  # Should have negative real parts

CHAPTER 4: NONLINEAR CONTROL
Feedback Linearization
# Transform nonlinear system into linear one via change of variables and feedback.
# Example: Computed Torque Control for robot arms.

Sliding Mode Control
# Robust control method for uncertain systems.
# Forces system state to "slide" along a predefined surface.
# Chattering is a common issue.

Adaptive Control
# Adjusts controller parameters online to handle changing system dynamics.
# Model Reference Adaptive Control (MRAC).

CHAPTER 5: MOTION PLANNING
Configuration Space (C-Space)
# Space of all possible configurations of the robot.
# Obstacles in workspace become C-Obsacles in C-Space.

Sampling-Based Planning
# Probabilistic Roadmap (PRM): Build a graph of free space, then search.
# Rapidly-exploring Random Tree (RRT): Grow a tree from start towards goal.

class RRTPlanner:
    def __init__(self, xmin, xmax, ymin, ymax, obstacle_list):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.obstacles = obstacle_list  # List of (x, y, radius)
        self.nodes = []  # List of (x, y, parent_index)
        
    def is_collision_free(self, x, y):
        for ox, oy, r in self.obstacles:
            if (x - ox)**2 + (y - oy)**2 < r**2:
                return False
        return True
        
    def sample_random(self):
        return np.random.uniform(self.xmin, self.xmax), np.random.uniform(self.ymin, self.ymax)
        
    def nearest_node(self, x, y):
        min_dist = float('inf')
        nearest_idx = -1
        for i, (nx, ny, _) in enumerate(self.nodes):
            dist = (x - nx)**2 + (y - ny)**2
            if dist < min_dist:
                min_dist = dist
                nearest_idx = i
        return nearest_idx
        
    def steer(self, x_from, y_from, x_to, y_to, step_size=0.5):
        theta = np.arctan2(y_to - y_from, x_to - x_from)
        x_new = x_from + step_size * np.cos(theta)
        y_new = y_from + step_size * np.sin(theta)
        return x_new, y_new
        
    def plan(self, start, goal, max_iter=1000, step_size=0.5):
        self.nodes = [(start[0], start[1], -1)]
        
        for _ in range(max_iter):
            x_rand, y_rand = self.sample_random()
            idx_nearest = self.nearest_node(x_rand, y_rand)
            x_near, y_near, _ = self.nodes[idx_nearest]
            
            x_new, y_new = self.steer(x_near, y_near, x_rand, y_rand, step_size)
            
            if self.is_collision_free(x_new, y_new):
                new_idx = len(self.nodes)
                self.nodes.append((x_new, y_new, idx_nearest))
                
                # Check if close to goal
                dist_to_goal = (x_new - goal[0])**2 + (y_new - goal[1])**2
                if dist_to_goal < step_size**2:
                    # Reconstruct path
                    path = []
                    curr_idx = new_idx
                    while curr_idx != -1:
                        x, y, parent = self.nodes[curr_idx]
                        path.append((x, y))
                        curr_idx = parent
                    path.reverse()
                    return path
                    
        return None  # Failed to find path

# Example
obstacles = [(2, 2, 0.5), (3, 3, 0.8)]
rrt = RRTPlanner(0, 5, 0, 5, obstacles)
path = rrt.plan(start=(0, 0), goal=(4, 4))

if path:
    path = np.array(path)
    plt.plot(path[:, 0], path[:, 1], 'b-', label='Path')
    for ox, oy, r in obstacles:
        circle = plt.Circle((ox, oy), r, color='r')
        plt.gca().add_patch(circle)
    plt.scatter([0, 4], [0, 4], c=['g', 'orange'], s=100, label=['Start', 'Goal'])
    plt.axis('equal')
    plt.legend()
    plt.title("RRT Path Planning")
    plt.show()
else:
    print("No path found.")

Optimization-Based Planning
# Trajectory optimization: Minimize cost (time, energy, jerk) subject to constraints.
# Methods: CHOMP, STOMP, Direct Collocation.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Model Predictive Control (MPC)
# Solves an optimal control problem over a finite horizon at each time step.
# Handles constraints explicitly.
# Computationally expensive but powerful.

Reinforcement Learning for Control
# Learn control policies through trial and error.
# Deep Deterministic Policy Gradient (DDPG), Soft Actor-Critic (SAC).
# Useful for complex, high-dimensional systems where modeling is difficult.

Soft Robotics Control
# Control of flexible, deformable materials.
# Challenges: Nonlinear dynamics, hysteresis, sensing.

Recommended Reading
# - "Modern Control Engineering" by Ogata
# - "Robotics: Modelling, Planning and Control" by Siciliano et al.
# - "Probabilistic Robotics" by Thrun, Burgard, Fox
# - "Underactuated Robotics" by Russ Tedrake (MIT OpenCourseWare)

# Online Resources
# - Python Control Systems Library: https://python-control.readthedocs.io/
# - MoveIt! (ROS Motion Planning): https://moveit.ros.org/
# - OMPL (Open Motion Planning Library): https://ompl.kavrakilab.org/

# End of Advanced Robotics Control Reference