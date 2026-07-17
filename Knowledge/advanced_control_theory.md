Advanced Control Theory Complete Reference
CHAPTER 1: GETTING STARTED WITH ADVANCED CONTROL
Remarks
Advanced control theory deals with the behavior of dynamical systems with inputs, and how their behavior can be modified by feedback. While classical control (PID) handles linear, time-invariant systems, advanced control addresses nonlinearities, time-varying parameters, uncertainties, and multi-variable interactions. Key areas: State-Space Analysis, Optimal Control, Robust Control, Adaptive Control, Nonlinear Control, and Model Predictive Control (MPC). Applications: Aerospace, robotics, process control, automotive systems, power grids.
Tools: Python (Control Systems Library, SciPy, CasADi), MATLAB/Simulink, YALMIP, ACADO.
Hello State-Space
# hello_control.py
"""
First advanced control program: Convert Transfer Function to State-Space.
"""
import numpy as np
from scipy import signal

# Transfer Function: G(s) = (2s + 1) / (s^2 + 3s + 2)
num = [2, 1]
den = [1, 3, 2]

# Convert to State-Space (Controllable Canonical Form)
A, B, C, D = signal.tf2ss(num, den)

print("State-Space Representation:")
print(f"A = \n{A}")
print(f"B = \n{B}")
print(f"C = \n{C}")
print(f"D = \n{D}")

# Check Stability (Eigenvalues of A)
eigenvalues = np.linalg.eigvals(A)
print(f"\nEigenvalues: {eigenvalues}")
if np.all(np.real(eigenvalues) < 0):
    print("System is Stable.")
else:
    print("System is Unstable.")

State-Space Representation
# x_dot = Ax + Bu
# y = Cx + Du
# x: State vector (internal variables)
# u: Input vector
# y: Output vector
# A: System matrix
# B: Input matrix
# C: Output matrix
# D: Feedthrough matrix

Controllability & Observability
# Controllability: Can we drive the system from any initial state to any final state?
# Matrix: Co = [B, AB, A^2B, ..., A^(n-1)B]
# Rank(Co) == n -> Controllable.

# Observability: Can we determine the internal state from outputs?
# Matrix: Ob = [C; CA; CA^2; ...; CA^(n-1)]
# Rank(Ob) == n -> Observable.

def check_controllability(A, B):
    n = A.shape[0]
    Co = B
    for i in range(1, n):
        Co = np.hstack((Co, np.linalg.matrix_power(A, i) @ B))
    return np.linalg.matrix_rank(Co) == n

def check_observability(A, C):
    n = A.shape[0]
    Ob = C
    for i in range(1, n):
        Ob = np.vstack((Ob, C @ np.linalg.matrix_power(A, i)))
    return np.linalg.matrix_rank(Ob) == n

CHAPTER 2: OPTIMAL CONTROL
Linear Quadratic Regulator (LQR)
# Minimizes cost function: J = integral(x'Qx + u'Ru)dt
# Q: Penalty on state deviation (positive semi-definite)
# R: Penalty on control effort (positive definite)
# Solution: u = -Kx, where K = R^-1 B' P
# P is solution to Algebraic Riccati Equation (ARE).

from scipy.linalg import solve_continuous_are

def design_lqr(A, B, Q, R):
    """Design LQR controller."""
    P = solve_continuous_are(A, B, Q, R)
    K = np.linalg.inv(R) @ B.T @ P
    return K, P

# Example
A = np.array([[0, 1], [0, 0]]) # Double integrator
B = np.array([[0], [1]])
Q = np.diag([10, 1]) # Penalize position error more
R = np.array([[0.1]]) # Low penalty on control

K, P = design_lqr(A, B, Q, R)
print(f"\nLQR Gain K: {K}")

Linear Quadratic Gaussian (LQG)
# Combines LQR with Kalman Filter.
# Used when states are not directly measurable and noise is present.
# Separation Principle: Design LQR and Kalman Filter independently.

CHAPTER 3: ROBUST CONTROL
H-Infinity Control
# Designs controller to minimize worst-case gain from disturbances to errors.
# Handles model uncertainty explicitly.
# mu-synthesis: Structured uncertainty handling.

Small Gain Theorem
# If ||G||_inf * ||Delta||_inf < 1, the closed-loop system is stable.
# G: Nominal plant
# Delta: Uncertainty block

Robust Stability vs Robust Performance
# Robust Stability: System remains stable for all uncertainties.
# Robust Performance: System meets performance specs for all uncertainties.

CHAPTER 4: ADAPTIVE CONTROL
Model Reference Adaptive Control (MRAC)
# Adjusts controller parameters so plant output follows a reference model.
# Lyapunov stability design ensures convergence.

Self-Tuning Regulators (STR)
# Online parameter estimation (Recursive Least Squares).
# Controller redesign based on estimated parameters.

Gain Scheduling
# Pre-computed controllers for different operating points.
# Interpolate between gains based on scheduling variables (e.g., speed, altitude).
# Common in aerospace (flight control).

CHAPTER 5: NONLINEAR CONTROL
Feedback Linearization
# Transform nonlinear system into linear one via change of coordinates and feedback.
# Exact linearization requires precise model knowledge.

Sliding Mode Control (SMC)
# Forces system state to "slide" along a predefined surface.
# Highly robust to matched uncertainties.
# Chattering: High-frequency oscillation due to discontinuous control law.
# Mitigation: Boundary layer, higher-order SMC.

Lyapunov Stability
# Direct method: Find a Lyapunov function V(x) such that:
# 1. V(x) > 0 for x != 0, V(0) = 0
# 2. dV/dt <= 0
# If such V exists, system is stable.

Backstepping
# Recursive design for strict-feedback systems.
# Stabilizes subsystems step-by-step.

CHAPTER 6: MODEL PREDICTIVE CONTROL (MPC)
Principle
# Solves an optimal control problem over a finite horizon at each time step.
# Uses model to predict future behavior.
# Applies only the first control input, then repeats (Receding Horizon).

Constraints Handling
# MPC explicitly handles constraints on inputs (u_min <= u <= u_max) and states.
# Critical for safety-critical systems.

Optimization Problem
# Minimize: sum(x_k'Qx_k + u_k'Ru_k)
# Subject to:
# x_{k+1} = Ax_k + Bu_k
# y_k = Cx_k
# u_min <= u_k <= u_max
# y_min <= y_k <= y_max

Soft Constraints
# Allow constraint violations with high penalty.
# Prevents infeasibility issues.

Nonlinear MPC (NMPC)
# Uses nonlinear model for prediction.
# Requires non-linear optimization solvers (IPOPT, SNOPT).
# Computationally expensive.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Distributed Control
# Multiple controllers coordinating over a network.
# Consensus algorithms.
# Applications: Drone swarms, smart grids.

Learning-Based Control
# Reinforcement Learning for control policy discovery.
# Safe RL: Ensuring stability during learning.
# Iterative Learning Control (ILC): Improving performance over repeated trials.

Fault-Tolerant Control
# Detects and accommodates actuator/sensor faults.
# Active FTC: Reconfigures controller after fault detection.
# Passive FTC: Designed to be robust to specific faults.

Recommended Reading
# - "Feedback Systems" by Åström and Murray
# - "Robust and Optimal Control" by Zhou, Doyle, and Glover
# - "Nonlinear Systems" by Khalil
# - "Predictive Control" by Maciejowski
# - Python Control Systems Library: https://python-control.readthedocs.io/

# End of Advanced Control Theory Reference