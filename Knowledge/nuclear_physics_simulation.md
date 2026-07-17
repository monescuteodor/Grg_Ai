Advanced Nuclear Physics Simulation Complete Reference
CHAPTER 1: GETTING STARTED WITH NUCLEAR PHYSICS SIMULATION
Remarks
Computational nuclear physics models the behavior of atomic nuclei, nuclear reactions, and radiation transport. Key areas: Neutron transport (Monte Carlo methods), Reactor kinetics, Particle decay chains, Fusion plasma confinement, and Radiation shielding. Applications: Nuclear power plant design, medical isotope production, radiation therapy planning, nuclear waste management, and fundamental research.
Tools: Python (NumPy, SciPy, PyNE), MCNP/OpenMC (Monte Carlo N-Particle), GEANT4, Serpent, FLUKA.
Hello Radioactive Decay
# hello_decay.py
"""
First nuclear program: Simulate radioactive decay chain.
"""
import numpy as np
import matplotlib.pyplot as plt

def simulate_decay(N0, half_life, time_steps, dt):
    """Simulate simple exponential decay."""
    lambda_const = np.log(2) / half_life
    times = np.arange(0, time_steps * dt, dt)
    N = N0 * np.exp(-lambda_const * times)
    return times, N

# Example: Iodine-131 (half-life ~8 days)
t, N = simulate_decay(N0=1000, half_life=8.0, time_steps=50, dt=1.0)

plt.plot(t, N)
plt.title("Radioactive Decay of Iodine-131")
plt.xlabel("Time (days)")
plt.ylabel("Number of Atoms")
plt.grid(True)
plt.show()

Decay Chains
# Parent -> Daughter -> Granddaughter
# Bateman Equations describe the amount of each isotope over time.

def bateman_equation(N0_parent, lambda_p, lambda_d, t):
    """Calculate amount of daughter product at time t."""
    if lambda_p == lambda_d:
        return N0_parent * lambda_p * t * np.exp(-lambda_p * t)
    else:
        term1 = np.exp(-lambda_p * t)
        term2 = np.exp(-lambda_d * t)
        return N0_parent * (lambda_p / (lambda_d - lambda_p)) * (term1 - term2)

CHAPTER 2: MONTE CARLO NEUTRON TRANSPORT
Random Walks
# Neutrons move in straight lines until they interact.
# Interaction types: Scattering, Absorption, Fission.
# Mean Free Path: lambda = 1 / (Sigma_t * rho)

def sample_distance(sigma_t):
    """Sample distance to next collision using inverse transform sampling."""
    xi = np.random.random()
    return -np.log(xi) / sigma_t

def sample_scattering_angle():
    """Isotropic scattering in 3D."""
    cos_theta = 2 * np.random.random() - 1
    phi = 2 * np.pi * np.random.random()
    sin_theta = np.sqrt(1 - cos_theta**2)
    return sin_theta * np.cos(phi), sin_theta * np.sin(phi), cos_theta

Basic Monte Carlo Loop
# 1. Source neutron.
# 2. Sample distance to collision.
# 3. Move neutron.
# 4. Determine interaction type (based on cross-sections).
# 5. If scatter: sample new direction.
# 6. If absorb: kill neutron.
# 7. If fission: create new neutrons.
# 8. Repeat until neutron leaves geometry or is absorbed.

Cross-Sections
# Sigma (σ): Probability of interaction per unit path length.
# Depends on energy (E) and material.
# Data libraries: ENDF/B, JEFF, JENDL.

CHAPTER 3: REACTOR KINETICS
Point Kinetics Equations
# Simplified model for reactor power changes.
# dP/dt = ((rho - beta) / Lambda) * P + sum(lambda_i * C_i)
# dC_i/dt = (beta_i / Lambda) * P - lambda_i * C_i
# P: Power, rho: Reactivity, beta: Delayed neutron fraction, Lambda: Generation time, C_i: Precursor concentration.

def point_kinetics(rho, beta, Lambda, lambdas, betas, P0, C0, time_span, dt):
    """Solve point kinetics equations using Euler method."""
    steps = int(time_span / dt)
    P_hist = [P0]
    C_hist = [C0.copy()]
    
    P = P0
    C = C0.copy()
    
    for _ in range(steps):
        dPdt = ((rho - beta) / Lambda) * P + np.sum(lambdas * C)
        dCdt = (betas / Lambda) * P - lambdas * C
        
        P += dPdt * dt
        C += dCdt * dt
        
        P_hist.append(P)
        C_hist.append(C.copy())
        
    return np.array(P_hist), np.array(C_hist)

# Example parameters for a typical thermal reactor
beta_total = 0.0065
Lambda = 1e-4 # seconds
lambdas = np.array([0.0124, 0.0305, 0.111, 0.301, 1.14, 3.01]) # 1/s
betas_frac = np.array([0.000215, 0.00142, 0.00127, 0.00257, 0.000748, 0.000273])
betas = beta_total * betas_frac / np.sum(betas_frac) # Normalize

rho_step = 0.001 # Step reactivity insertion
P, C = point_kinetics(rho_step, beta_total, Lambda, lambdas, betas, 1.0, np.zeros(6), 10.0, 0.01)

plt.plot(P)
plt.title("Reactor Power Transient (Step Insertion)")
plt.xlabel("Time Step")
plt.ylabel("Relative Power")
plt.grid(True)
plt.show()

Criticality Calculation
# k_eff: Effective multiplication factor.
# k_eff > 1: Supercritical (power increases).
# k_eff = 1: Critical (steady state).
# k_eff < 1: Subcritical (power decreases).
# Calculated via Monte Carlo eigenvalue calculation.

CHAPTER 4: FUSION PLASMA PHYSICS
Magnetohydrodynamics (MHD)
# Describes plasma as a conducting fluid.
# Combines Navier-Stokes equations with Maxwell's equations.
# Important for Tokamak and Stellarator design.

Grad-Shafranov Equation
# Determines equilibrium magnetic field configuration in axisymmetric toroidal plasmas.
# Solved iteratively using finite difference or finite element methods.

Neutron Production in Fusion
# D-T Reaction: Deuterium + Tritium -> Helium-4 + Neutron (14.1 MeV).
# Yield depends on plasma temperature, density, and confinement time (Lawson Criterion).

CHAPTER 5: RADIATION SHIELDING
Attenuation Law
# I(x) = I0 * exp(-mu * x)
# mu: Linear attenuation coefficient.
# Half-Value Layer (HVL): Thickness required to reduce intensity by half.

def calculate_shielding_thickness(I0, I_target, mu):
    """Calculate thickness required to reduce radiation to target level."""
    if I_target <= 0:
        return float('inf')
    return np.log(I0 / I_target) / mu

# Example: Lead shielding for Gamma rays
mu_lead = 0.5 # cm^-1 (approximate for specific energy)
thickness = calculate_shielding_thickness(1000, 1, mu_lead)
print(f"Required Lead Thickness: {thickness:.2f} cm")

Build-up Factor
# Accounts for scattered radiation reaching the detector.
# B(E, x) > 1.
# I_total = B * I_unscattered.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Burnup Calculation
# Tracks change in isotopic composition of fuel over time.
# Coupled with neutron transport code.
# Important for waste management and fuel cycle analysis.

Thermal Hydraulics
# Coupling neutron kinetics with fluid dynamics.
# Coolant flow, heat transfer, boiling phenomena.
# Codes: RELAP, TRACE, CATHARE.

Uncertainty Quantification
# Propagating uncertainties in nuclear data (cross-sections) to system responses.
# Sensitivity analysis.

Recommended Reading
# - "Nuclear Reactor Analysis" by Duderstadt and Gill
# - "Monte Carlo Principles and Neutron Transport Problems" by Spanier and Gelbard
# - "Introduction to Plasma Physics" by Chen
# - OpenMC Documentation: https://docs.openmc.org/
# - GEANT4 Documentation: https://geant4.web.cern.ch/

# End of Advanced Nuclear Physics Reference