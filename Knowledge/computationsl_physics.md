Computational Physics Complete Reference
CHAPTER 1: GETTING STARTED WITH COMPUTATIONAL PHYSICS
Remarks
Computational physics uses numerical methods and algorithms to solve physical problems that cannot be solved analytically. Key areas: numerical integration/differentiation, Monte Carlo simulations, molecular dynamics, finite element methods, computational fluid dynamics, quantum mechanics simulations, optimization algorithms. Applications: astrophysics, materials science, biophysics, climate modeling, particle physics, engineering.
Tools: Python (NumPy, SciPy, Matplotlib), C/C++ (performance-critical), Fortran (legacy HPC), Julia (modern scientific computing), Mathematica (symbolic), MATLAB.
Hello Computational Physics
# hello_physics.py
"""
First computational physics program: simulate projectile motion with air resistance.
"""
import numpy as np
import matplotlib.pyplot as plt

def projectile_motion(v0, angle_deg, dt=0.01, duration=10.0, drag_coeff=0.0):
    """
    Simulate projectile motion with optional air resistance.
    
    v0: initial velocity (m/s)
    angle_deg: launch angle (degrees)
    dt: time step (s)
    duration: simulation time (s)
    drag_coeff: drag coefficient (0 = no drag)
    """
    g = 9.81  # gravitational acceleration (m/s^2)
    angle = np.radians(angle_deg)
    
    # Initial conditions
    x = 0.0
    y = 0.0
    vx = v0 * np.cos(angle)
    vy = v0 * np.sin(angle)
    
    # Store trajectory
    trajectory = [(x, y)]
    
    # Euler integration
    t = 0.0
    while t < duration and y >= 0:
        # Air resistance (proportional to velocity)
        if drag_coeff > 0:
            v = np.sqrt(vx**2 + vy**2)
            ax = -drag_coeff * v * vx
            ay = -g - drag_coeff * v * vy
        else:
            ax = 0.0
            ay = -g
        
        # Update velocities
        vx += ax * dt
        vy += ay * dt
        
        # Update positions
        x += vx * dt
        y += vy * dt
        
        trajectory.append((x, y))
        t += dt
    
    return np.array(trajectory)

# Simulate different scenarios
v0 = 50.0  # m/s
angle = 45.0  # degrees

# No air resistance
traj_no_drag = projectile_motion(v0, angle, drag_coeff=0.0)

# With air resistance
traj_with_drag = projectile_motion(v0, angle, drag_coeff=0.01)

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(traj_no_drag[:, 0], traj_no_drag[:, 1], 'b-', linewidth=2, label='No drag')
plt.plot(traj_with_drag[:, 0], traj_with_drag[:, 1], 'r--', linewidth=2, label='With drag')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.title('Projectile Motion with Air Resistance')
plt.grid(alpha=0.3)
plt.legend()
plt.axhline(0, color='k', linestyle='-', linewidth=0.5)
plt.tight_layout()
plt.savefig('projectile_motion.png', dpi=100)
plt.show()

# Calculate range and max height
print("=== Simulation Results ===")
print(f"Initial velocity: {v0} m/s at {angle}°")
print(f"\nNo drag:")
print(f"  Range: {traj_no_drag[-1, 0]:.2f} m")
print(f"  Max height: {traj_no_drag[:, 1].max():.2f} m")
print(f"  Flight time: {len(traj_no_drag) * 0.01:.2f} s")

print(f"\nWith drag (coeff={0.01}):")
print(f"  Range: {traj_with_drag[-1, 0]:.2f} m")
print(f"  Max height: {traj_with_drag[:, 1].max():.2f} m")
print(f"  Flight time: {len(traj_with_drag) * 0.01:.2f} s")

# Analytical solution (no drag)
theoretical_range = v0**2 * np.sin(2 * np.radians(angle)) / g
theoretical_height = v0**2 * np.sin(np.radians(angle))**2 / (2 * g)
print(f"\nTheoretical (no drag):")
print(f"  Range: {theoretical_range:.2f} m")
print(f"  Max height: {theoretical_height:.2f} m")

Numerical Methods Overview
# Why computational physics?
# 1. Many physical problems have no analytical solution
# 2. Analytical solutions may be too complex
# 3. Need to simulate real-world conditions
# 4. Parameter studies and optimization

# Common numerical methods:
# - Finite difference methods (derivatives)
# - Numerical integration (trapezoidal, Simpson's, Gaussian quadrature)
# - Root finding (Newton-Raphson, bisection)
# - ODE solvers (Euler, Runge-Kutta, Verlet)
# - PDE solvers (finite difference, finite element, spectral methods)
# - Monte Carlo methods (random sampling)
# - Optimization (gradient descent, genetic algorithms)

# Key considerations:
# - Accuracy vs. computational cost
# - Stability of numerical methods
# - Convergence and error analysis
# - Boundary conditions
# - Initial conditions

CHAPTER 2: NUMERICAL METHODS
Numerical Differentiation
# Finite difference approximations for derivatives
# Forward difference: f'(x) ≈ (f(x+h) - f(x)) / h
# Backward difference: f'(x) ≈ (f(x) - f(x-h)) / h
# Central difference: f'(x) ≈ (f(x+h) - f(x-h)) / (2h)

import numpy as np

def numerical_derivative(f, x, h=1e-5, method='central'):
    """
    Compute numerical derivative of function f at point x.
    
    f: function to differentiate
    x: point(s) at which to compute derivative
    h: step size
    method: 'forward', 'backward', or 'central'
    """
    if method == 'forward':
        return (f(x + h) - f(x)) / h
    elif method == 'backward':
        return (f(x) - f(x - h)) / h
    elif method == 'central':
        return (f(x + h) - f(x - h)) / (2 * h)
    else:
        raise ValueError(f"Unknown method: {method}")

# Example: derivative of sin(x)
x_values = np.linspace(0, 2*np.pi, 100)
f = np.sin
f_prime_analytical = np.cos(x_values)
f_prime_numerical = numerical_derivative(f, x_values, h=1e-5)

print("=== Numerical Differentiation ===")
print(f"Max error: {np.max(np.abs(f_prime_analytical - f_prime_numerical)):.2e}")

# Second derivative
def numerical_second_derivative(f, x, h=1e-5):
    """Compute second derivative using central difference."""
    return (f(x + h) - 2*f(x) + f(x - h)) / h**2

f_double_prime_analytical = -np.sin(x_values)
f_double_prime_numerical = numerical_second_derivative(f, x_values, h=1e-4)

print(f"Second derivative max error: {np.max(np.abs(f_double_prime_analytical - f_double_prime_numerical)):.2e}")

Numerical Integration
# Methods for computing definite integrals
# 1. Rectangle rule (left, right, midpoint)
# 2. Trapezoidal rule
# 3. Simpson's rule
# 4. Gaussian quadrature

def integrate_rectangle(f, a, b, n=1000, method='midpoint'):
    """Integrate using rectangle rule."""
    dx = (b - a) / n
    x = np.linspace(a, b, n, endpoint=False)
    
    if method == 'left':
        return np.sum(f(x)) * dx
    elif method == 'right':
        return np.sum(f(x + dx)) * dx
    elif method == 'midpoint':
        return np.sum(f(x + dx/2)) * dx
    else:
        raise ValueError(f"Unknown method: {method}")

def integrate_trapezoidal(f, a, b, n=1000):
    """Integrate using trapezoidal rule."""
    dx = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return dx * (np.sum(y) - 0.5 * (y[0] + y[-1]))

def integrate_simpson(f, a, b, n=1000):
    """Integrate using Simpson's rule (n must be even)."""
    if n % 2 != 0:
        n += 1
    
    dx = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    
    return dx / 3 * (y[0] + y[-1] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-2:2]))

# Example: integrate sin(x) from 0 to pi
f = np.sin
a, b = 0, np.pi
analytical = 2.0  # ∫₀^π sin(x) dx = 2

print("\n=== Numerical Integration ===")
print(f"Analytical: {analytical:.6f}")

for n in [10, 100, 1000, 10000]:
    rect = integrate_rectangle(f, a, b, n)
    trap = integrate_trapezoidal(f, a, b, n)
    simp = integrate_simpson(f, a, b, n)
    
    print(f"\nn = {n}:")
    print(f"  Rectangle:  {rect:.6f} (error: {abs(rect - analytical):.2e})")
    print(f"  Trapezoid:  {trap:.6f} (error: {abs(trap - analytical):.2e})")
    print(f"  Simpson:    {simp:.6f} (error: {abs(simp - analytical):.2e})")

Runge-Kutta Methods for ODEs
# Solve ordinary differential equations: dy/dt = f(t, y)
# Euler method: y_{n+1} = y_n + h * f(t_n, y_n)
# RK4: 4th order Runge-Kutta (most common)

def euler_method(f, t0, y0, t_end, h):
    """
    Solve ODE using Euler method.
    
    f: function f(t, y) returning dy/dt
    t0: initial time
    y0: initial condition
    t_end: final time
    h: step size
    """
    t_values = [t0]
    y_values = [y0]
    
    t = t0
    y = y0
    
    while t < t_end:
        y = y + h * f(t, y)
        t = t + h
        t_values.append(t)
        y_values.append(y)
    
    return np.array(t_values), np.array(y_values)

def runge_kutta_4(f, t0, y0, t_end, h):
    """
    Solve ODE using 4th order Runge-Kutta method.
    
    More accurate than Euler: O(h^4) vs O(h)
    """
    t_values = [t0]
    y_values = [y0]
    
    t = t0
    y = y0
    
    while t < t_end:
        k1 = h * f(t, y)
        k2 = h * f(t + h/2, y + k1/2)
        k3 = h * f(t + h/2, y + k2/2)
        k4 = h * f(t + h, y + k3)
        
        y = y + (k1 + 2*k2 + 2*k3 + k4) / 6
        t = t + h
        
        t_values.append(t)
        y_values.append(y)
    
    return np.array(t_values), np.array(y_values)

# Example: Simple harmonic oscillator
# d²x/dt² = -ω²x  →  dx/dt = v, dv/dt = -ω²x
def harmonic_oscillator(t, state, omega=1.0):
    """State = [x, v]"""
    x, v = state
    return np.array([v, -omega**2 * x])

# Solve
t0, tf = 0, 10
h = 0.01
y0 = np.array([1.0, 0.0])  # x(0)=1, v(0)=0

t_euler, y_euler = euler_method(harmonic_oscillator, t0, y0, tf, h)
t_rk4, y_rk4 = runge_kutta_4(harmonic_oscillator, t0, y0, tf, h)

# Analytical solution
t_analytical = np.linspace(t0, tf, 1000)
x_analytical = np.cos(t_analytical)

# Plot
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(t_analytical, x_analytical, 'k-', linewidth=2, label='Analytical')
plt.plot(t_euler, y_euler[:, 0], 'b--', label='Euler')
plt.plot(t_rk4, y_rk4[:, 0], 'r-.', label='RK4')
plt.xlabel('Time')
plt.ylabel('Position')
plt.title('Simple Harmonic Oscillator')
plt.legend()
plt.grid(alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(t_euler, np.abs(y_euler[:, 0] - np.cos(t_euler)), 'b-', label='Euler error')
plt.plot(t_rk4, np.abs(y_rk4[:, 0] - np.cos(t_rk4)), 'r-', label='RK4 error')
plt.xlabel('Time')
plt.ylabel('Absolute Error')
plt.title('Error Comparison')
plt.yscale('log')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('ode_solvers.png', dpi=100)
plt.show()

print(f"\n=== ODE Solver Comparison ===")
print(f"Euler max error: {np.max(np.abs(y_euler[:, 0] - np.cos(t_euler))):.2e}")
print(f"RK4 max error: {np.max(np.abs(y_rk4[:, 0] - np.cos(t_rk4))):.2e}")

Root Finding
# Find x such that f(x) = 0
# Methods: bisection, Newton-Raphson, secant

def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Find root using bisection method.
    Requires f(a) and f(b) to have opposite signs.
    """
    if f(a) * f(b) > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    
    for i in range(max_iter):
        c = (a + b) / 2
        
        if abs(f(c)) < tol:
            return c
        
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2

def newton_raphson(f, f_prime, x0, tol=1e-6, max_iter=100):
    """
    Find root using Newton-Raphson method.
    Requires derivative f'(x).
    """
    x = x0
    
    for i in range(max_iter):
        fx = f(x)
        
        if abs(fx) < tol:
            return x
        
        fpx = f_prime(x)
        if fpx == 0:
            raise ValueError("Derivative is zero")
        
        x = x - fx / fpx
    
    return x

# Example: find root of x^3 - 2x - 5
f = lambda x: x**3 - 2*x - 5
f_prime = lambda x: 3*x**2 - 2

root_bisect = bisection(f, 2, 3)
root_newton = newton_raphson(f, f_prime, 2.0)

print(f"\n=== Root Finding ===")
print(f"Bisection: x = {root_bisect:.6f}, f(x) = {f(root_bisect):.2e}")
print(f"Newton-Raphson: x = {root_newton:.6f}, f(x) = {f(root_newton):.2e}")

CHAPTER 3: MONTE CARLO METHODS
Monte Carlo Integration
# Estimate integrals using random sampling
# ∫f(x)dx ≈ (b-a) * (1/N) * Σf(x_i) where x_i ~ Uniform(a,b)

def monte_carlo_integrate(f, a, b, n_samples=100000):
    """
    Estimate integral using Monte Carlo method.
    
    f: function to integrate
    a, b: integration bounds
    n_samples: number of random samples
    """
    x_random = np.random.uniform(a, b, n_samples)
    f_values = f(x_random)
    
    integral = (b - a) * np.mean(f_values)
    error = (b - a) * np.std(f_values) / np.sqrt(n_samples)
    
    return integral, error

# Example: integrate sin(x) from 0 to pi
f = np.sin
a, b = 0, np.pi
analytical = 2.0

print("=== Monte Carlo Integration ===")
for n in [100, 1000, 10000, 100000, 1000000]:
    integral, error = monte_carlo_integrate(f, a, b, n)
    print(f"N = {n:7d}: {integral:.6f} ± {error:.6f} (true: {analytical:.6f})")

# Multi-dimensional integration
def monte_carlo_integrate_nd(f, bounds, n_samples=100000):
    """
    Monte Carlo integration in N dimensions.
    
    f: function f(x) where x is array of shape (n_samples, n_dims)
    bounds: list of (min, max) for each dimension
    """
    n_dims = len(bounds)
    
    # Generate random points
    x_random = np.random.uniform(
        [b[0] for b in bounds],
        [b[1] for b in bounds],
        (n_samples, n_dims)
    )
    
    f_values = f(x_random)
    
    # Volume of integration region
    volume = np.prod([b[1] - b[0] for b in bounds])
    
    integral = volume * np.mean(f_values)
    error = volume * np.std(f_values) / np.sqrt(n_samples)
    
    return integral, error

# Example: integrate x^2 + y^2 over unit square [0,1] x [0,1]
f_2d = lambda x: x[:, 0]**2 + x[:, 1]**2
bounds = [(0, 1), (0, 1)]
analytical_2d = 2/3  # ∫₀¹∫₀¹ (x²+y²) dx dy = 2/3

integral_2d, error_2d = monte_carlo_integrate_nd(f_2d, bounds, 1000000)
print(f"\n2D integral: {integral_2d:.6f} ± {error_2d:.6f} (true: {analytical_2d:.6f})")

Monte Carlo Simulation: Random Walk
# Simulate random walk (Brownian motion)
# Used for: diffusion, stock prices, polymer physics

def random_walk_2d(n_steps=1000, step_size=1.0, n_walkers=100):
    """
    Simulate 2D random walk.
    
    n_steps: number of steps per walker
    step_size: length of each step
    n_walkers: number of independent walkers
    """
    # Random directions
    angles = np.random.uniform(0, 2*np.pi, (n_walkers, n_steps))
    dx = step_size * np.cos(angles)
    dy = step_size * np.sin(angles)
    
    # Cumulative sum to get positions
    x = np.cumsum(dx, axis=1)
    y = np.cumsum(dy, axis=1)
    
    # Add starting point (0, 0)
    x = np.hstack([np.zeros((n_walkers, 1)), x])
    y = np.hstack([np.zeros((n_walkers, 1)), y])
    
    return x, y

# Simulate and visualize
x, y = random_walk_2d(n_steps=500, n_walkers=50)

plt.figure(figsize=(12, 5))

# Plot individual walks
plt.subplot(1, 2, 1)
for i in range(min(10, len(x))):  # Plot first 10 walks
    plt.plot(x[i], y[i], alpha=0.5, linewidth=1)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Random Walk Trajectories')
plt.grid(alpha=0.3)
plt.axis('equal')

# Plot mean squared displacement
plt.subplot(1, 2, 2)
r_squared = x**2 + y**2
mean_r_squared = np.mean(r_squared, axis=0)
steps = np.arange(len(mean_r_squared))

plt.plot(steps, mean_r_squared, 'b-', linewidth=2, label='Simulated')
plt.plot(steps, steps, 'r--', linewidth=2, label='Theoretical (⟨r²⟩ = n)')
plt.xlabel('Number of Steps')
plt.ylabel('Mean Squared Displacement ⟨r²⟩')
plt.title('Random Walk Statistics')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('random_walk.png', dpi=100)
plt.show()

print(f"\n=== Random Walk Statistics ===")
print(f"Number of walkers: {len(x)}")
print(f"Steps per walker: {len(x[0])-1}")
print(f"Final mean squared displacement: {mean_r_squared[-1]:.2f}")
print(f"Theoretical: {len(x[0])-1:.2f}")

Monte Carlo: Pi Estimation
# Estimate π using random sampling
# Generate random points in unit square, count those in unit circle

def estimate_pi(n_samples=1000000):
    """
    Estimate π using Monte Carlo method.
    
    Generate random points in [0,1]×[0,1] and count
    how many fall within the unit circle (x²+y² ≤ 1).
    """
    # Generate random points
    x = np.random.uniform(0, 1, n_samples)
    y = np.random.uniform(0, 1, n_samples)
    
    # Check if inside unit circle
    inside = (x**2 + y**2) <= 1
    
    # Estimate π
    pi_estimate = 4 * np.sum(inside) / n_samples
    error = 4 * np.sqrt(np.sum(inside) * (n_samples - np.sum(inside))) / (n_samples * np.sqrt(n_samples))
    
    return pi_estimate, error

print("\n=== Monte Carlo Pi Estimation ===")
for n in [100, 1000, 10000, 100000, 1000000]:
    pi_est, error = estimate_pi(n)
    print(f"N = {n:7d}: π ≈ {pi_est:.6f} ± {error:.6f} (true: {np.pi:.6f})")

Metropolis-Hastings Algorithm
# Generate samples from complex probability distributions
# Used for: statistical mechanics, Bayesian inference

def metropolis_hastings(target_log_pdf, x0, n_samples=10000, proposal_std=1.0):
    """
    Metropolis-Hastings MCMC sampler.
    
    target_log_pdf: log of target probability density function
    x0: initial state
    n_samples: number of samples to generate
    proposal_std: standard deviation of Gaussian proposal
    """
    samples = [x0]
    accepted = 0
    
    x_current = x0
    log_p_current = target_log_pdf(x_current)
    
    for i in range(n_samples):
        # Propose new state
        x_proposal = x_current + np.random.normal(0, proposal_std, size=len(x0))
        log_p_proposal = target_log_pdf(x_proposal)
        
        # Acceptance probability
        log_alpha = log_p_proposal - log_p_current
        alpha = min(1.0, np.exp(log_alpha))
        
        # Accept or reject
        if np.random.random() < alpha:
            x_current = x_proposal
            log_p_current = log_p_proposal
            accepted += 1
        
        samples.append(x_current)
    
    acceptance_rate = accepted / n_samples
    return np.array(samples), acceptance_rate

# Example: sample from 2D Gaussian mixture
def gaussian_mixture_log_pdf(x):
    """Log PDF of mixture of two Gaussians."""
    mu1 = np.array([2.0, 2.0])
    mu2 = np.array([-2.0, -2.0])
    sigma = 1.0
    
    p1 = np.exp(-0.5 * np.sum((x - mu1)**2) / sigma**2)
    p2 = np.exp(-0.5 * np.sum((x - mu2)**2) / sigma**2)
    
    return np.log(0.5 * p1 + 0.5 * p2)

# Sample
samples, acceptance_rate = metropolis_hastings(
    gaussian_mixture_log_pdf,
    x0=np.array([0.0, 0.0]),
    n_samples=10000,
    proposal_std=0.5
)

print(f"\n=== Metropolis-Hastings ===")
print(f"Acceptance rate: {acceptance_rate:.2%}")
print(f"Samples generated: {len(samples)}")

# Plot
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.scatter(samples[:, 0], samples[:, 1], alpha=0.3, s=5)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('MCMC Samples')
plt.grid(alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(samples[:, 0], samples[:, 1], alpha=0.5, linewidth=0.5)
plt.plot(samples[0, 0], samples[0, 1], 'go', markersize=10, label='Start')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('MCMC Trajectory')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('mcmc.png', dpi=100)
plt.show()

CHAPTER 4: MOLECULAR DYNAMICS
Lennard-Jones Potential
# Model interatomic interactions
# V(r) = 4ε[(σ/r)^12 - (σ/r)^6]
# ε: depth of potential well
# σ: distance where V=0

def lennard_jones_potential(r, epsilon=1.0, sigma=1.0):
    """
    Lennard-Jones potential.
    
    r: distance(s) between particles
    epsilon: depth of potential well
    sigma: distance where potential is zero
    """
    r6 = (sigma / r)**6
    r12 = r6**2
    return 4 * epsilon * (r12 - r6)

def lennard_jones_force(r, epsilon=1.0, sigma=1.0):
    """
    Force from Lennard-Jones potential.
    F = -dV/dr = 24ε/r * [2(σ/r)^12 - (σ/r)^6]
    """
    r6 = (sigma / r)**6
    r12 = r6**2
    return 24 * epsilon / r * (2 * r12 - r6)

# Plot potential
r = np.linspace(0.9, 3.0, 500)
V = lennard_jones_potential(r)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(r, V, 'b-', linewidth=2)
plt.axhline(0, color='k', linestyle='--', linewidth=0.5)
plt.axvline(1.0, color='r', linestyle='--', label='σ (V=0)')
plt.axvline(2**(1/6), color='g', linestyle='--', label='r_min (V=-ε)')
plt.xlabel('Distance r')
plt.ylabel('Potential V(r)')
plt.title('Lennard-Jones Potential')
plt.legend()
plt.grid(alpha=0.3)
plt.xlim(0.9, 3.0)
plt.ylim(-1.5, 10)

plt.subplot(1, 2, 2)
F = lennard_jones_force(r)
plt.plot(r, F, 'r-', linewidth=2)
plt.axhline(0, color='k', linestyle='--', linewidth=0.5)
plt.xlabel('Distance r')
plt.ylabel('Force F(r)')
plt.title('Lennard-Jones Force')
plt.grid(alpha=0.3)
plt.xlim(0.9, 3.0)
plt.ylim(-50, 50)

plt.tight_layout()
plt.savefig('lj_potential.png', dpi=100)
plt.show()

Molecular Dynamics Simulation
# Simulate N particles interacting via Lennard-Jones potential
# Use Velocity Verlet integration (symplectic, time-reversible)

class MolecularDynamics:
    """2D molecular dynamics simulation."""
    
    def __init__(self, n_particles=100, box_size=10.0, temperature=1.0):
        self.n_particles = n_particles
        self.box_size = box_size
        self.temperature = temperature
        
        # Lennard-Jones parameters
        self.epsilon = 1.0
        self.sigma = 1.0
        self.cutoff = 2.5 * self.sigma  # Cutoff distance
        
        # Particle properties
        self.positions = None
        self.velocities = None
        self.forces = None
        
        # Initialize
        self._initialize_positions()
        self._initialize_velocities()
    
    def _initialize_positions(self):
        """Initialize positions on a grid."""
        n_side = int(np.ceil(np.sqrt(self.n_particles)))
        spacing = self.box_size / n_side
        
        positions = []
        for i in range(n_side):
            for j in range(n_side):
                if len(positions) < self.n_particles:
                    positions.append([
                        (i + 0.5) * spacing,
                        (j + 0.5) * spacing
                    ])
        
        self.positions = np.array(positions)
    
    def _initialize_velocities(self):
        """Initialize velocities from Maxwell-Boltzmann distribution."""
        # Random velocities
        self.velocities = np.random.randn(self.n_particles, 2)
        
        # Remove center of mass motion
        self.velocities -= np.mean(self.velocities, axis=0)
        
        # Scale to desired temperature
        # <KE> = (1/2) m <v²> = (d/2) k_B T
        # For d=2: <v²> = 2 k_B T / m
        kinetic_energy = 0.5 * np.sum(self.velocities**2)
        target_energy = self.n_particles * self.temperature  # k_B = 1, m = 1
        scale = np.sqrt(target_energy / kinetic_energy)
        self.velocities *= scale
    
    def _compute_forces(self):
        """Compute forces between all particle pairs."""
        self.forces = np.zeros_like(self.positions)
        potential_energy = 0.0
        
        for i in range(self.n_particles):
            for j in range(i + 1, self.n_particles):
                # Distance vector
                rij = self.positions[j] - self.positions[i]
                
                # Minimum image convention (periodic boundary)
                rij = rij - self.box_size * np.round(rij / self.box_size)
                
                r = np.linalg.norm(rij)
                
                if r < self.cutoff:
                    # Lennard-Jones force
                    force_magnitude = lennard_jones_force(r, self.epsilon, self.sigma)
                    force_vector = force_magnitude * rij / r
                    
                    self.forces[i] += force_vector
                    self.forces[j] -= force_vector
                    
                    # Potential energy
                    potential_energy += lennard_jones_potential(r, self.epsilon, self.sigma)
        
        return potential_energy
    
    def step(self, dt=0.001):
        """
        Perform one Velocity Verlet integration step.
        
        1. x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt²
        2. Compute forces F(t+dt)
        3. v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt
        """
        # Current accelerations (a = F/m, m=1)
        accelerations = self.forces.copy()
        
        # Update positions
        self.positions += self.velocities * dt + 0.5 * accelerations * dt**2
        
        # Apply periodic boundary conditions
        self.positions = self.positions % self.box_size
        
        # Compute new forces
        potential_energy = self._compute_forces()
        
        # New accelerations
        new_accelerations = self.forces.copy()
        
        # Update velocities
        self.velocities += 0.5 * (accelerations + new_accelerations) * dt
        
        # Compute kinetic energy
        kinetic_energy = 0.5 * np.sum(self.velocities**2)
        
        return kinetic_energy, potential_energy
    
    def run(self, n_steps=1000, dt=0.001, output_freq=10):
        """Run simulation for n_steps."""
        # Initial forces
        self._compute_forces()
        
        energies = []
        
        for step in range(n_steps):
            ke, pe = self.step(dt)
            
            if step % output_freq == 0:
                total_energy = ke + pe
                energies.append((step, ke, pe, total_energy))
                
                if step % (output_freq * 10) == 0:
                    print(f"Step {step:5d}: KE={ke:.3f}, PE={pe:.3f}, Total={total_energy:.3f}")
        
        return np.array(energies)
    
    def get_temperature(self):
        """Compute instantaneous temperature."""
        kinetic_energy = 0.5 * np.sum(self.velocities**2)
        # T = 2 * KE / (N * k_B * d)
        return 2 * kinetic_energy / (self.n_particles * 2)  # d=2

# Run simulation
md = MolecularDynamics(n_particles=64, box_size=8.0, temperature=1.0)
energies = md.run(n_steps=1000, dt=0.001, output_freq=10)

# Plot energies
plt.figure(figsize=(12, 4))
plt.plot(energies[:, 0], energies[:, 1], 'r-', label='Kinetic')
plt.plot(energies[:, 0], energies[:, 2], 'b-', label='Potential')
plt.plot(energies[:, 0], energies[:, 3], 'k-', linewidth=2, label='Total')
plt.xlabel('Step')
plt.ylabel('Energy')
plt.title('Molecular Dynamics Energy Conservation')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('md_energies.png', dpi=100)
plt.show()

print(f"\nFinal temperature: {md.get_temperature():.3f}")
print(f"Energy drift: {energies[-1, 3] - energies[0, 3]:.3f}")

CHAPTER 5: FINITE ELEMENT METHOD
1D Finite Element Method
# Solve differential equations by discretizing domain into elements
# Approximate solution as linear combination of basis functions

def solve_poisson_1d(n_elements=100, f=lambda x: 1.0):
    """
    Solve -u''(x) = f(x) on [0,1] with u(0)=u(1)=0
    using finite element method.
    """
    # Mesh
    n_nodes = n_elements + 1
    x = np.linspace(0, 1, n_nodes)
    h = x[1] - x[0]  # Element size
    
    # Assemble stiffness matrix K and load vector F
    K = np.zeros((n_nodes, n_nodes))
    F = np.zeros(n_nodes)
    
    for e in range(n_elements):
        # Element nodes
        i, j = e, e + 1
        
        # Element stiffness matrix (linear elements)
        ke = (1.0 / h) * np.array([[1, -1], [-1, 1]])
        
        # Element load vector (midpoint rule)
        x_mid = (x[i] + x[j]) / 2
        fe = f(x_mid) * h / 2 * np.array([1, 1])
        
        # Assemble
        K[i:i+2, i:i+2] += ke
        F[i:i+2] += fe
    
    # Apply boundary conditions (u(0)=u(1)=0)
    K[0, :] = 0
    K[0, 0] = 1
    F[0] = 0
    
    K[-1, :] = 0
    K[-1, -1] = 1
    F[-1] = 0
    
    # Solve system
    u = np.linalg.solve(K, F)
    
    return x, u

# Example: solve -u'' = 1 (parabolic solution)
x, u = solve_poisson_1d(n_elements=50)

# Analytical solution: u(x) = x(1-x)/2
u_analytical = x * (1 - x) / 2

plt.figure(figsize=(10, 5))
plt.plot(x, u, 'b-o', linewidth=2, markersize=4, label='FEM')
plt.plot(x, u_analytical, 'r--', linewidth=2, label='Analytical')
plt.xlabel('x')
plt.ylabel('u(x)')
plt.title('1D Poisson Equation: -u\'\' = 1')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('fem_1d.png', dpi=100)
plt.show()

print(f"Max error: {np.max(np.abs(u - u_analytical)):.2e}")

2D Finite Element Method (Conceptual)
# For 2D problems, use triangular or quadrilateral elements
# Solve: -∇²u = f on domain Ω

def fem_2d_conceptual():
    """Demonstrate FEM concepts for 2D problems."""
    print("=== 2D Finite Element Method ===")
    print("\nSteps:")
    print("1. Discretize domain into elements (triangles/quads)")
    print("2. Define basis functions (linear, quadratic)")
    print("3. Assemble global stiffness matrix K")
    print("4. Assemble load vector F")
    print("5. Apply boundary conditions")
    print("6. Solve Ku = F")
    print("\nCommon applications:")
    print("- Structural mechanics (stress, strain)")
    print("- Heat transfer")
    print("- Fluid flow")
    print("- Electromagnetics")

fem_2d_conceptual()

CHAPTER 6: COMPUTATIONAL FLUID DYNAMICS
Navier-Stokes Equations (2D)
# Incompressible flow:
# ∂u/∂t + (u·∇)u = -∇p/ρ + ν∇²u  (momentum)
# ∇·u = 0  (continuity)

def simulate_cavity_flow(nx=50, ny=50, reynolds=100, n_steps=1000):
    """
    Simulate 2D lid-driven cavity flow using simple finite difference.
    
    nx, ny: grid size
    reynolds: Reynolds number
    n_steps: number of time steps
    """
    # Grid
    dx = 1.0 / (nx - 1)
    dy = 1.0 / (ny - 1)
    
    # Time step (CFL condition)
    dt = 0.01
    
    # Viscosity
    nu = 1.0 / reynolds
    
    # Initialize velocity and pressure
    u = np.zeros((ny, nx))
    v = np.zeros((ny, nx))
    p = np.zeros((ny, nx))
    
    # Boundary conditions (lid-driven cavity)
    # Top wall moves with u=1
    u[-1, :] = 1.0
    
    # Pressure and velocity arrays for iteration
    b = np.zeros((ny, nx))
    
    print("Simulating lid-driven cavity flow...")
    print(f"Grid: {nx}×{ny}, Re={reynolds}")
    
    for step in range(n_steps):
        # Compute divergence
        b[1:-1, 1:-1] = (
            (u[1:-1, 2:] - u[1:-1, :-2]) / (2 * dx) +
            (v[2:, 1:-1] - v[:-2, 1:-1]) / (2 * dy)
        )
        
        # Pressure Poisson equation (simplified)
        for _ in range(50):  # Iterative solver
            p[1:-1, 1:-1] = (
                (p[1:-1, 2:] + p[1:-1, :-2]) * dy**2 +
                (p[2:, 1:-1] + p[:-2, 1:-1]) * dx**2
            ) / (2 * (dx**2 + dy**2))
            p[1:-1, 1:-1] -= dx**2 * dy**2 * b[1:-1, 1:-1] / (2 * (dx**2 + dy**2))
        
        # Update velocities
        u[1:-1, 1:-1] = (
            u[1:-1, 1:-1] -
            dt * (u[1:-1, 1:-1] * (u[1:-1, 2:] - u[1:-1, :-2]) / (2 * dx) +
                  v[1:-1, 1:-1] * (u[2:, 1:-1] - u[:-2, 1:-1]) / (2 * dy)) -
            dt / dx * (p[1:-1, 2:] - p[1:-1, :-2]) / 2 +
            nu * dt * (
                (u[1:-1, 2:] - 2*u[1:-1, 1:-1] + u[1:-1, :-2]) / dx**2 +
                (u[2:, 1:-1] - 2*u[1:-1, 1:-1] + u[:-2, 1:-1]) / dy**2
            )
        )
        
        v[1:-1, 1:-1] = (
            v[1:-1, 1:-1] -
            dt * (u[1:-1, 1:-1] * (v[1:-1, 2:] - v[1:-1, :-2]) / (2 * dx) +
                  v[1:-1, 1:-1] * (v[2:, 1:-1] - v[:-2, 1:-1]) / (2 * dy)) -
            dt / dy * (p[2:, 1:-1] - p[:-2, 1:-1]) / 2 +
            nu * dt * (
                (v[1:-1, 2:] - 2*v[1:-1, 1:-1] + v[1:-1, :-2]) / dx**2 +
                (v[2:, 1:-1] - 2*v[1:-1, 1:-1] + v[:-2, 1:-1]) / dy**2
            )
        )
        
        # Reapply boundary conditions
        u[-1, :] = 1.0  # Lid
        u[0, :] = 0.0   # Bottom
        u[:, 0] = 0.0   # Left
        u[:, -1] = 0.0  # Right
        
        v[0, :] = 0.0
        v[-1, :] = 0.0
        v[:, 0] = 0.0
        v[:, -1] = 0.0
        
        if step % 100 == 0:
            print(f"  Step {step}/{n_steps}")
    
    return u, v, p

# Run simulation (smaller grid for speed)
u, v, p = simulate_cavity_flow(nx=30, ny=30, reynolds=100, n_steps=200)

# Plot velocity field
x = np.linspace(0, 1, u.shape[1])
y = np.linspace(0, 1, u.shape[0])
X, Y = np.meshgrid(x, y)

plt.figure(figsize=(10, 8))
speed = np.sqrt(u**2 + v**2)
plt.contourf(X, Y, speed, levels=20, cmap='viridis')
plt.colorbar(label='Speed')
plt.quiver(X[::3, ::3], Y[::3, ::3], u[::3, ::3], v[::3, ::3], 
           speed[::3, ::3], cmap='viridis', alpha=0.7)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Lid-Driven Cavity Flow (Re=100)')
plt.tight_layout()
plt.savefig('cavity_flow.png', dpi=100)
plt.show()

CHAPTER 7: QUANTUM MECHANICS SIMULATION
Schrödinger Equation (1D)
# Time-independent: -ℏ²/(2m) * d²ψ/dx² + V(x)ψ = Eψ
# Time-dependent: iℏ * ∂ψ/∂t = -ℏ²/(2m) * ∂²ψ/∂x² + V(x)ψ

def solve_schrodinger_1d(V, x, n_states=5):
    """
    Solve 1D time-independent Schrödinger equation using finite difference.
    
    V: potential energy function V(x)
    x: position grid
    n_states: number of energy levels to compute
    """
    # Constants (atomic units: ℏ = m = 1)
    hbar = 1.0
    m = 1.0
    
    # Grid spacing
    dx = x[1] - x[0]
    n_points = len(x)
    
    # Build Hamiltonian matrix
    H = np.zeros((n_points, n_points))
    
    # Kinetic energy (finite difference)
    coeff = -hbar**2 / (2 * m * dx**2)
    for i in range(n_points):
        H[i, i] = -2 * coeff + V[i]
        if i > 0:
            H[i, i-1] = coeff
        if i < n_points - 1:
            H[i, i+1] = coeff
    
    # Solve eigenvalue problem
    eigenvalues, eigenvectors = np.linalg.eigh(H)
    
    # Return lowest n_states
    energies = eigenvalues[:n_states]
    wavefunctions = eigenvectors[:, :n_states]
    
    return energies, wavefunctions

# Example: Quantum harmonic oscillator
# V(x) = (1/2) * m * ω² * x²
omega = 1.0
x = np.linspace(-5, 5, 500)
V = 0.5 * omega**2 * x**2

energies, wavefunctions = solve_schrodinger_1d(V, x, n_states=5)

# Analytical energies: E_n = ℏω(n + 1/2)
energies_analytical = omega * (np.arange(5) + 0.5)

print("=== Quantum Harmonic Oscillator ===")
print("Energy levels:")
for n in range(5):
    print(f"  n={n}: E={energies[n]:.4f} (analytical: {energies_analytical[n]:.4f})")

# Plot
plt.figure(figsize=(12, 8))

# Plot potential and wavefunctions
plt.subplot(2, 1, 1)
plt.plot(x, V, 'k-', linewidth=2, label='Potential V(x)')
for n in range(5):
    # Scale wavefunctions for visibility
    psi_scaled = wavefunctions[:, n] * 2 + energies[n]
    plt.plot(x, psi_scaled, linewidth=2, label=f'n={n}, E={energies[n]:.2f}')
    plt.axhline(energies[n], color='gray', linestyle='--', alpha=0.5)

plt.xlabel('Position x')
plt.ylabel('Energy / Wavefunction')
plt.title('Quantum Harmonic Oscillator')
plt.legend()
plt.grid(alpha=0.3)
plt.xlim(-5, 5)

# Plot probability densities
plt.subplot(2, 1, 2)
for n in range(5):
    prob_density = np.abs(wavefunctions[:, n])**2
    plt.plot(x, prob_density, linewidth=2, label=f'n={n}')

plt.xlabel('Position x')
plt.ylabel('Probability Density |ψ(x)|²')
plt.title('Probability Densities')
plt.legend()
plt.grid(alpha=0.3)
plt.xlim(-5, 5)

plt.tight_layout()
plt.savefig('quantum_oscillator.png', dpi=100)
plt.show()

Time-Dependent Schrödinger Equation
# Simulate wave packet evolution

def simulate_wave_packet(x, V, psi0, dt=0.001, n_steps=100):
    """
    Simulate time-dependent Schrödinger equation.
    iℏ ∂ψ/∂t = Hψ
    
    Using split-operator method.
    """
    hbar = 1.0
    m = 1.0
    n_points = len(x)
    dx = x[1] - x[0]
    
    # Kinetic energy operator in momentum space
    k = 2 * np.pi * np.fft.fftfreq(n_points, dx)
    K_op = hbar**2 * k**2 / (2 * m)
    
    # Potential energy operator
    V_op = V
    
    # Time evolution operators
    exp_K = np.exp(-1j * K_op * dt / hbar)
    exp_V = np.exp(-1j * V_op * dt / (2 * hbar))
    
    psi = psi0.copy()
    probabilities = [np.abs(psi)**2]
    
    for step in range(n_steps):
        # Split-operator method: exp(-iHt/ℏ) ≈ exp(-iVt/2ℏ) exp(-iKt/ℏ) exp(-iVt/2ℏ)
        
        # Half step in position space
        psi = exp_V * psi
        
        # Full step in momentum space
        psi_k = np.fft.fft(psi)
        psi_k = exp_K * psi_k
        psi = np.fft.ifft(psi_k)
        
        # Half step in position space
        psi = exp_V * psi
        
        probabilities.append(np.abs(psi)**2)
    
    return psi, np.array(probabilities)

# Example: Gaussian wave packet in harmonic potential
x = np.linspace(-10, 10, 512)
V = 0.5 * x**2  # Harmonic oscillator

# Initial Gaussian wave packet
x0 = -3.0  # Initial position
k0 = 2.0   # Initial momentum
sigma = 0.5  # Width

psi0 = (1 / (np.pi * sigma**2))**0.25 * np.exp(-(x - x0)**2 / (2 * sigma**2)) * np.exp(1j * k0 * x)

# Normalize
psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * (x[1] - x[0]))

# Simulate
psi_final, probabilities = simulate_wave_packet(x, V, psi0, dt=0.01, n_steps=200)

# Plot
plt.figure(figsize=(12, 8))

# Initial state
plt.subplot(2, 2, 1)
plt.plot(x, np.abs(psi0)**2, 'b-', linewidth=2)
plt.plot(x, V / 10, 'k--', linewidth=1, alpha=0.5)
plt.xlabel('x')
plt.ylabel('|ψ(x)|²')
plt.title('Initial State')
plt.grid(alpha=0.3)

# Final state
plt.subplot(2, 2, 2)
plt.plot(x, np.abs(psi_final)**2, 'r-', linewidth=2)
plt.plot(x, V / 10, 'k--', linewidth=1, alpha=0.5)
plt.xlabel('x')
plt.ylabel('|ψ(x)|²')
plt.title('Final State')
plt.grid(alpha=0.3)

# Time evolution
plt.subplot(2, 1, 2)
plt.imshow(probabilities.T, aspect='auto', origin='lower',
           extent=[x[0], x[-1], 0, len(probabilities)-1],
           cmap='viridis')
plt.xlabel('Position x')
plt.ylabel('Time step')
plt.title('Wave Packet Evolution')
plt.colorbar(label='|ψ(x,t)|²')

plt.tight_layout()
plt.savefig('wave_packet.png', dpi=100)
plt.show()

CHAPTER 8: OPTIMIZATION ALGORITHMS
Gradient Descent
# Find minimum of function f(x)
# x_{n+1} = x_n - α * ∇f(x_n)

def gradient_descent(f, grad_f, x0, learning_rate=0.01, n_iterations=1000, tol=1e-6):
    """
    Minimize function using gradient descent.
    
    f: objective function
    grad_f: gradient of f
    x0: initial point
    learning_rate: step size
    n_iterations: maximum iterations
    tol: convergence tolerance
    """
    x = x0.copy()
    history = [x.copy()]
    
    for i in range(n_iterations):
        gradient = grad_f(x)
        
        # Check convergence
        if np.linalg.norm(gradient) < tol:
            print(f"Converged at iteration {i}")
            break
        
        # Update
        x = x - learning_rate * gradient
        history.append(x.copy())
    
    return x, f(x), np.array(history)

# Example: Rosenbrock function
# f(x, y) = (a - x)² + b(y - x²)²
# Minimum at (a, a²)
def rosenbrock(x):
    a, b = 1.0, 100.0
    return (a - x[0])**2 + b * (x[1] - x[0]**2)**2

def rosenbrock_gradient(x):
    a, b = 1.0, 100.0
    df_dx = -2 * (a - x[0]) - 4 * b * x[0] * (x[1] - x[0]**2)
    df_dy = 2 * b * (x[1] - x[0]**2)
    return np.array([df_dx, df_dy])

# Optimize
x0 = np.array([-1.0, 1.0])
x_opt, f_opt, history = gradient_descent(
    rosenbrock, rosenbrock_gradient, x0,
    learning_rate=0.001, n_iterations=10000
)

print(f"\n=== Gradient Descent ===")
print(f"Initial: x={x0}, f={rosenbrock(x0):.2f}")
print(f"Optimal: x={x_opt}, f={f_opt:.6f}")
print(f"Theoretical minimum: x=[1, 1], f=0")

# Plot optimization path
x_grid = np.linspace(-2, 2, 100)
y_grid = np.linspace(-1, 3, 100)
X, Y = np.meshgrid(x_grid, y_grid)
Z = (1 - X)**2 + 100 * (Y - X**2)**2

plt.figure(figsize=(10, 8))
plt.contour(X, Y, Z, levels=50, cmap='viridis')
plt.plot(history[:, 0], history[:, 1], 'r.-', markersize=3, linewidth=1, label='Path')
plt.plot(x0[0], x0[1], 'go', markersize=10, label='Start')
plt.plot(x_opt[0], x_opt[1], 'r*', markersize=15, label='Minimum')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Rosenbrock Function Optimization')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('gradient_descent.png', dpi=100)
plt.show()

Simulated Annealing
# Global optimization algorithm inspired by metallurgy
# Accept worse solutions with probability exp(-ΔE/T)

def simulated_annealing(f, x0, temperature_initial=1.0, temperature_final=1e-6,
                        cooling_rate=0.99, n_iterations=10000):
    """
    Minimize function using simulated annealing.
    
    f: objective function
    x0: initial point
    temperature_initial: starting temperature
    temperature_final: ending temperature
    cooling_rate: temperature reduction factor
    n_iterations: maximum iterations
    """
    x_current = x0.copy()
    f_current = f(x_current)
    
    x_best = x_current.copy()
    f_best = f_current
    
    temperature = temperature_initial
    
    history = [f_current]
    
    for i in range(n_iterations):
        # Generate neighbor
        x_neighbor = x_current + np.random.normal(0, 0.1, size=len(x0))
        f_neighbor = f(x_neighbor)
        
        # Acceptance probability
        delta_f = f_neighbor - f_current
        
        if delta_f < 0 or np.random.random() < np.exp(-delta_f / temperature):
            x_current = x_neighbor
            f_current = f_neighbor
            
            # Update best
            if f_current < f_best:
                x_best = x_current.copy()
                f_best = f_current
        
        # Cool down
        temperature *= cooling_rate
        
        history.append(f_current)
        
        # Check termination
        if temperature < temperature_final:
            print(f"Converged at iteration {i}")
            break
    
    return x_best, f_best, np.array(history)

# Optimize Rosenbrock with simulated annealing
x0 = np.array([-1.0, 1.0])
x_opt_sa, f_opt_sa, history_sa = simulated_annealing(
    rosenbrock, x0,
    temperature_initial=10.0,
    cooling_rate=0.995,
    n_iterations=50000
)

print(f"\n=== Simulated Annealing ===")
print(f"Optimal: x={x_opt_sa}, f={f_opt_sa:.6f}")

# Plot convergence
plt.figure(figsize=(10, 5))
plt.plot(history_sa)
plt.xlabel('Iteration')
plt.ylabel('Objective Function')
plt.title('Simulated Annealing Convergence')
plt.yscale('log')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('simulated_annealing.png', dpi=100)
plt.show()

Genetic Algorithm
# Evolutionary optimization algorithm
# Population → Selection → Crossover → Mutation → New population

def genetic_algorithm(f, bounds, population_size=100, n_generations=100,
                      mutation_rate=0.1, crossover_rate=0.8):
    """
    Minimize function using genetic algorithm.
    
    f: objective function
    bounds: list of (min, max) for each dimension
    population_size: number of individuals
    n_generations: number of generations
    mutation_rate: probability of mutation
    crossover_rate: probability of crossover
    """
    n_dims = len(bounds)
    
    # Initialize population
    population = np.random.uniform(
        [b[0] for b in bounds],
        [b[1] for b in bounds],
        (population_size, n_dims)
    )
    
    best_history = []
    
    for gen in range(n_generations):
        # Evaluate fitness
        fitness = np.array([f(ind) for ind in population])
        
        # Track best
        best_idx = np.argmin(fitness)
        best_history.append(fitness[best_idx])
        
        # Selection (tournament)
        new_population = []
        for _ in range(population_size):
            # Tournament selection
            idx1, idx2 = np.random.choice(population_size, 2, replace=False)
            if fitness[idx1] < fitness[idx2]:
                parent1 = population[idx1].copy()
            else:
                parent1 = population[idx2].copy()
            
            idx1, idx2 = np.random.choice(population_size, 2, replace=False)
            if fitness[idx1] < fitness[idx2]:
                parent2 = population[idx1].copy()
            else:
                parent2 = population[idx2].copy()
            
            # Crossover
            if np.random.random() < crossover_rate:
                alpha = np.random.random()
                child = alpha * parent1 + (1 - alpha) * parent2
            else:
                child = parent1.copy()
            
            # Mutation
            for d in range(n_dims):
                if np.random.random() < mutation_rate:
                    child[d] += np.random.normal(0, 0.1)
                    # Clip to bounds
                    child[d] = np.clip(child[d], bounds[d][0], bounds[d][1])
            
            new_population.append(child)
        
        population = np.array(new_population)
        
        if gen % 10 == 0:
            print(f"Generation {gen}: Best fitness = {best_history[-1]:.6f}")
    
    # Final evaluation
    fitness = np.array([f(ind) for ind in population])
    best_idx = np.argmin(fitness)
    
    return population[best_idx], fitness[best_idx], np.array(best_history)

# Optimize Rosenbrock with genetic algorithm
bounds = [(-2, 2), (-1, 3)]
x_opt_ga, f_opt_ga, history_ga = genetic_algorithm(
    rosenbrock, bounds,
    population_size=100,
    n_generations=200
)

print(f"\n=== Genetic Algorithm ===")
print(f"Optimal: x={x_opt_ga}, f={f_opt_ga:.6f}")

# Plot convergence
plt.figure(figsize=(10, 5))
plt.plot(history_ga)
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.title('Genetic Algorithm Convergence')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('genetic_algorithm.png', dpi=100)
plt.show()

CHAPTER 9: VISUALIZATION AND ANALYSIS
Phase Space Plots
# Visualize dynamical systems in phase space

def lorenz_system(state, t, sigma=10.0, rho=28.0, beta=8/3):
    """Lorenz attractor equations."""
    x, y, z = state
    return np.array([
        sigma * (y - x),
        x * (rho - z) - y,
        x * y - beta * z
    ])

# Solve Lorenz system
from scipy.integrate import odeint

t = np.linspace(0, 50, 10000)
state0 = [1.0, 1.0, 1.0]
solution = odeint(lorenz_system, state0, t)

# Plot phase space
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(solution[:, 0], solution[:, 1], solution[:, 2], 
        linewidth=0.5, alpha=0.7)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Lorenz Attractor')
plt.tight_layout()
plt.savefig('lorenz_attractor.png', dpi=100)
plt.show()

Poincaré Sections
# Analyze periodic/quasi-periodic systems

def pendulum_system(state, t, omega0=1.0, F=0.5, omega_d=2/3):
    """Driven damped pendulum."""
    theta, theta_dot = state
    return np.array([
        theta_dot,
        -omega0**2 * np.sin(theta) - 0.1 * theta_dot + F * np.cos(omega_d * t)
    ])

# Solve for long time
t_long = np.linspace(0, 1000, 50000)
state0 = [0.1, 0.0]
solution_long = odeint(pendulum_system, state0, t_long)

# Poincaré section (sample at driving frequency)
omega_d = 2/3
period = 2 * np.pi / omega_d
indices = np.arange(0, len(t_long), int(period / (t_long[1] - t_long[0])))

theta_section = solution_long[indices, 0] % (2 * np.pi)
theta_dot_section = solution_long[indices, 1]

plt.figure(figsize=(10, 5))
plt.scatter(theta_section, theta_dot_section, s=1, alpha=0.5)
plt.xlabel('θ (mod 2π)')
plt.ylabel('dθ/dt')
plt.title('Poincaré Section of Driven Pendulum')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('poincare_section.png', dpi=100)
plt.show()

Lyapunov Exponents
# Measure sensitivity to initial conditions (chaos indicator)

def compute_lyapunov_exponent(f, state0, t, dt=0.01, epsilon=1e-8):
    """
    Compute largest Lyapunov exponent.
    
    f: system function f(state, t)
    state0: initial state
    t: time array
    dt: time step
    epsilon: initial perturbation
    """
    # Two nearby trajectories
    state1 = state0.copy()
    state2 = state0.copy() + np.array([epsilon, 0, 0])
    
    lyapunov_sum = 0
    n_steps = len(t)
    
    for i in range(n_steps):
        # Evolve both trajectories
        state1 = state1 + f(state1, t[i]) * dt
        state2 = state2 + f(state2, t[i]) * dt
        
        # Distance
        distance = np.linalg.norm(state2 - state1)
        
        if distance > 0:
            # Lyapunov exponent contribution
            lyapunov_sum += np.log(distance / epsilon)
            
            # Renormalize
            state2 = state1 + epsilon * (state2 - state1) / distance
    
    return lyapunov_sum / (n_steps * dt)

# Compute for Lorenz system
lyap_exp = compute_lyapunov_exponent(lorenz_system, [1.0, 1.0, 1.0], 
                                      np.linspace(0, 100, 10000))

print(f"\n=== Lyapunov Exponent ===")
print(f"Largest Lyapunov exponent: {lyap_exp:.4f}")
if lyap_exp > 0:
    print("→ System is CHAOTIC (positive Lyapunov exponent)")
else:
    print("→ System is NOT chaotic")

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Advanced Numerical Methods
# - Spectral methods (high accuracy for smooth problems)
# - Multigrid methods (fast PDE solvers)
# - Adaptive mesh refinement (AMR)
# - Boundary element methods (BEM)
# - Smoothed particle hydrodynamics (SPH)

# High-performance computing:
# - Parallel computing (MPI, OpenMP)
# - GPU acceleration (CUDA, OpenCL)
# - Distributed computing
# - Cloud computing for simulations

Software and Libraries
# Python:
# - NumPy/SciPy: numerical computing
# - Matplotlib: visualization
# - FEniCS: finite element method
# - FiPy: finite volume PDEs
# - ASE: atomic simulation environment
# - LAMMPS: molecular dynamics
# - GROMACS: biomolecular simulation

# C/C++:
# - deal.II: finite element library
# - PETSc: scalable solvers
# - Trilinos: scientific computing

# Julia:
# - DifferentialEquations.jl: ODE/PDE solvers
# - JuMP: optimization
# - CLIMA: climate modeling

Applications
# Astrophysics: N-body simulations, galaxy formation
# Materials science: crystal structure, phase transitions
# Biophysics: protein folding, molecular dynamics
# Climate modeling: weather prediction, climate change
# Particle physics: Monte Carlo simulations (Geant4)
# Engineering: structural analysis, fluid dynamics
# Quantum chemistry: electronic structure calculations

Recommended Reading
# - "Numerical Recipes" by Press et al.
# - "Computational Physics" by Giordano & Nakanishi
# - "Understanding Molecular Simulation" by Frenkel & Smit
# - "The
