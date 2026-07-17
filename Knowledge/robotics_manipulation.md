Advanced Robotics Manipulation & Dexterous Hands Complete Reference
CHAPTER 1: GETTING STARTED WITH ROBOTIC MANIPULATION
Remarks
Robotic manipulation involves the interaction of a robot with its environment to move, grasp, and modify objects. Key areas: Kinematics (forward/inverse), Dynamics, Grasping theory, Force control, Motion planning for manipulators, and Dexterous manipulation (multi-fingered hands). Applications: Industrial assembly, surgical robotics, household service robots, warehouse automation.
Tools: Python (NumPy, SciPy, PyBullet, MoveIt!), C++ (ROS2, KDL), MuJoCo, Isaac Sim.
Hello Manipulation
# hello_manip.py
"""
First manipulation program: Simple 2-link planar arm inverse kinematics.
"""
import numpy as np

def inverse_kinematics_2link(x, y, l1, l2):
    """
    Solve IK for a 2-link planar arm.
    Returns (theta1, theta2) in radians.
    """
    # Check if target is reachable
    dist = np.sqrt(x**2 + y**2)
    if dist > l1 + l2 or dist < abs(l1 - l2):
        return None, None
    
    # Law of cosines for theta2
    cos_theta2 = (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2)
    # Clamp due to floating point errors
    cos_theta2 = np.clip(cos_theta2, -1.0, 1.0)
    theta2 = np.arccos(cos_theta2)
    
    # Theta1 calculation
    k1 = l1 + l2 * np.cos(theta2)
    k2 = l2 * np.sin(theta2)
    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)
    
    return theta1, theta2

# Example
l1, l2 = 1.0, 1.0
target_x, target_y = 1.5, 0.5

t1, t2 = inverse_kinematics_2link(target_x, target_y, l1, l2)
if t1 is not None:
    print(f"Theta1: {np.degrees(t1):.2f} deg")
    print(f"Theta2: {np.degrees(t2):.2f} deg")
else:
    print("Target unreachable")

Kinematic Chains
# Serial Manipulators: Links connected in series (e.g., PUMA, UR5).
# Parallel Manipulators: Multiple chains connecting base to end-effector (e.g., Stewart platform).
# Degrees of Freedom (DOF): Number of independent joint variables.
# Workspace: The volume of space the end-effector can reach.

CHAPTER 2: GRASPING THEORY
Force Closure
# A grasp achieves force closure if it can resist any external wrench (force/torque).
# Frictional Point Contact: Requires at least 3 fingers for planar, 4 for spatial (with friction).
# Frictionless Point Contact: Requires more contacts.

Grasp Metrics
# Quality measures based on the Grasp Matrix G.
# Volume of the Grasp Wrench Space (GWS).
# Minimum singular value of G.
# Isotropy: Ability to apply forces equally in all directions.

Antipodal Grasps
# Two contact points with normals pointing towards each other.
# Common in parallel-jaw grippers.
# Stable if the line connecting contacts passes through the center of mass.

Soft Finger Contact
# Models contact area rather than a point.
# Can resist torsion about the contact normal.
# Important for dexterous manipulation with soft pads.

CHAPTER 3: FORCE & IMPEDANCE CONTROL
Impedance Control
# Regulates the dynamic relationship between force and position.
# F = M(x_ddot - x_desired_ddot) + B(x_dot - x_desired_dot) + K(x - x_desired)
# M: Mass matrix, B: Damping, K: Stiffness.
# Allows compliance with the environment.

Hybrid Force/Position Control
# Controls position in unconstrained directions and force in constrained directions.
# Selection Matrix S: Defines which axes are force-controlled vs position-controlled.
# Used for tasks like peg-in-hole insertion.

Admittance Control
# Inverse of impedance: Measures force, computes position adjustment.
# Easier to implement on position-controlled robots.
# x_cmd = x_desired + Z_inv * F_measured

CHAPTER 4: DEXTEROUS MANIPULATION
Multi-Fingered Hands
# Examples: Shadow Hand, Allegro Hand, Robotiq Hand-E.
# High DOF (15-20+).
# Challenges: Complex kinematics, underactuation, sensing.

In-Hand Manipulation
# Reorienting an object without placing it down.
# Techniques: Finger gaiting, rolling, sliding.
# Requires precise force control and tactile feedback.

Tactile Sensing
# Technologies: Capacitive, Piezoresistive, Optical (GelSight), Magnetic.
# Provides information about contact location, force distribution, and slip.
# Essential for handling delicate or unknown objects.

CHAPTER 5: MOTION PLANNING FOR MANIPULATORS
Configuration Space (C-Space)
# For an n-DOF arm, C-space is n-dimensional.
# Obstacles in workspace map to C-obstacles.
# Path planning finds a collision-free path in C-space.

RRT-Connect & Bi-RRT
# Bidirectional Rapidly-exploring Random Trees.
# Grows trees from start and goal simultaneously.
# Efficient for high-dimensional spaces.

Trajectory Optimization
# Minimizes cost function (time, energy, jerk) subject to dynamics constraints.
# Methods: CHOMP, STOMP, Direct Collocation.
# Produces smooth, dynamically feasible trajectories.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Learning from Demonstration (LfD)
# Teaching robots by showing them tasks.
# Dynamic Movement Primitives (DMPs).
# Behavior Cloning, Reinforcement Learning from Human Feedback.

Sim-to-Real Transfer
# Training policies in simulation (MuJoCo, Isaac Sim) and deploying on real hardware.
# Domain Randomization: Varying physics parameters in sim to improve robustness.
# System Identification: Calibrating sim to match real robot dynamics.

Soft Robotics Manipulation
# Continuum robots, pneumatic actuators.
# Infinite DOF, compliant, safe for human interaction.
# Modeling challenges: Nonlinear elasticity, hysteresis.

Recommended Reading
# - "Robotics: Modelling, Planning and Control" by Siciliano et al.
# - "Planning Algorithms" by Steven LaValle
# - "Dexterous Robotic Hands" by Antonio Bicchi
# - MoveIt! Documentation: https://moveit.ros.org/
# - PyBullet Documentation: https://pybullet.org/

# End of Advanced Robotics Manipulation Reference