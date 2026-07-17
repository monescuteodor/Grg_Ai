Advanced Astrophysics & Cosmological Simulation Complete Reference
CHAPTER 1: GETTING STARTED WITH ASTROPHYSICS SIMULATION
Remarks
Computational astrophysics uses numerical methods to model celestial phenomena, from star formation to galaxy evolution and the large-scale structure of the universe. Key areas: N-body simulations (gravity), Hydrodynamics (gas dynamics), Radiative Transfer, Magnetohydrodynamics (MHD), and Cosmic Microwave Background (CMB) analysis. Applications: Understanding dark matter, black hole accretion, supernova explosions, and cosmic web formation.
Tools: Python (Astropy, NumPy, SciPy, yt), GADGET-2/4, ENZO, RAMSES, AREPO, FLASH.
Hello N-Body
# hello_nbody.py
"""
First astrophysics program: Simple N-body gravity simulation.
"""
import numpy as np
import matplotlib.pyplot as plt

class Particle:
    def __init__(self, mass, pos, vel):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.acc = np.zeros(3)

def compute_accelerations(particles, G=1.0, softening=0.1):
    """Compute gravitational accelerations for all particles."""
    N = len(particles)
    for i in range(N):
        particles[i].acc *= 0 # Reset acceleration
        for j in range(N):
            if i == j: continue
            r_vec = particles[j].pos - particles[i].pos
            r_dist = np.linalg.norm(r_vec)
            # Softening prevents singularity at r=0
            force_mag = G * particles[j].mass / (r_dist**2 + softening**2)**1.5
            particles[i].acc += force_mag * r_vec

def leapfrog_integrate(particles, dt):
    """Leapfrog integration scheme (symplectic, good for energy conservation)."""
    # Half-step velocity
    for p in particles:
        p.vel += 0.5 * p.acc * dt
    
    # Full-step position
    for p in particles:
        p.pos += p.vel * dt
        
    # Recompute accelerations
    compute_accelerations(particles)
    
    # Half-step velocity
    for p in particles:
        p.vel += 0.5 * p.acc * dt

# Initial conditions: Random cluster
N = 50
particles = []
for _ in range(N):
    m = np.random.uniform(0.5, 1.5)
    pos = np.random.randn(3) * 5
    vel = np.random.randn(3) * 0.1
    particles.append(Particle(m, pos, vel))

compute_accelerations(particles)

# Simulation loop
dt = 0.01
steps = 1000
history_pos = []

for i in range(steps):
    leapfrog_integrate(particles, dt)
    if i % 100 == 0:
        history_pos.append(np.array([p.pos for p in particles]))

# Plot final state
final_pos = np.array([p.pos for p in particles])
plt.figure(figsize=(8, 8))
plt.scatter(final_pos[:, 0], final_pos[:, 1], c='black', s=10)
plt.title("N-Body Simulation Final State")
plt.xlabel("X")
plt.ylabel("Y")
plt.axis('equal')
plt.grid(True)
plt.show()

Gravitational Softening
# In N-body simulations, point masses lead to infinite forces at close approach.
# Softening length epsilon modifies the potential: Phi = -GM / sqrt(r^2 + epsilon^2).
# This mimics the finite size of stars or resolution limits.

CHAPTER 2: HYDRODYNAMICS IN ASTROPHYSICS
Smoothed Particle Hydrodynamics (SPH)
# Mesh-free method where fluid is represented by particles.
# Each particle carries mass, density, pressure, energy.
# Density estimated by kernel smoothing: rho_i = sum_j m_j W(r_ij, h).

def sph_density(particle_i, particles, h_smooth):
    """Estimate density using Gaussian kernel."""
    rho = 0
    for p in particles:
        r = np.linalg.norm(particle_i.pos - p.pos)
        # Gaussian kernel
        W = (1 / (h_smooth * np.sqrt(np.pi))**3) * np.exp(-(r/h_smooth)**2)
        rho += p.mass * W
    return rho

Grid-Based Methods (Eulerian)
# Finite Volume Method: Conserves mass, momentum, energy across cell interfaces.
# Riemann Solvers: Resolve shocks and discontinuities (e.g., HLLC, Roe).
# Used in codes like ENZO, FLASH, RAMSES.

Equation of State (EOS)
# Relates pressure, density, and temperature.
# Ideal Gas: P = (gamma - 1) * rho * u
# Polytropic: P = K * rho^gamma

CHAPTER 3: COSMOLOGICAL SIMULATIONS
Lambda-CDM Model
# Standard model of cosmology.
# Components: Dark Energy (Lambda), Cold Dark Matter (CDM), Baryonic Matter.
# Parameters: H0 (Hubble constant), Omega_m (matter density), Omega_lambda (dark energy density).

Expansion of the Universe
# Scale factor a(t): Describes how distances expand over time.
# Friedmann Equation: (da/dt / a)^2 = H0^2 * (Omega_m/a^3 + Omega_lambda + Omega_r/a^4)

def scale_factor_derivative(a, Omega_m=0.3, Omega_l=0.7, H0=70):
    """Derivative of scale factor da/dt."""
    # Simplified units where c=1, H0 in appropriate units
    term_m = Omega_m / a**3
    term_l = Omega_l
    return H0 * np.sqrt(term_m + term_l)

Initial Conditions
# Generated from Power Spectrum P(k) derived from CMB data (Planck satellite).
# Zeldovich Approximation: Displace particles from grid based on density field.

Dark Matter Halos
# Formed via hierarchical clustering.
# Profile: Navarro-Frenk-White (NFW) profile.
# rho(r) = rho_0 / ((r/rs) * (1 + r/rs)^2)

CHAPTER 4: STELLAR EVOLUTION & SUPERNOVAE
Stellar Structure Equations
# 1. Mass Conservation: dM/dr = 4*pi*r^2*rho
# 2. Hydrostatic Equilibrium: dP/dr = -G*M*rho/r^2
# 3. Energy Transport: dT/dr depends on radiation/convection.
# 4. Energy Generation: dL/dr = 4*pi*r^2*rho*epsilon_nuclear

Nuclear Reaction Networks
# Simulates fusion chains (pp-chain, CNO cycle, triple-alpha).
# Rate equations: dY_i/dt = sum(reactions producing i) - sum(reactions consuming i).

Supernova Explosion Mechanisms
# Core-Collapse (Type II): Iron core collapses to neutron star/black hole.
# Thermonuclear (Type Ia): White dwarf exceeds Chandrasekhar limit.
# Simulations require neutrino transport and complex EOS.

CHAPTER 5: GALAXY FORMATION & MERGERS
Merger Trees
# Track progenitor halos over time.
# Used to study galaxy assembly history.

Feedback Processes
# Star Formation Feedback: Supernovae inject energy/metallicity into ISM.
# AGN Feedback: Black hole jets heat surrounding gas, suppressing star formation.
# Crucial for matching observed galaxy masses (preventing "overcooling").

Radiative Cooling
# Gas loses energy via emission lines (H, He, metals).
# Cooling function Lambda(T, Z): Depends on temperature and metallicity.
# Allows gas to condense into stars.

CHAPTER 6: OBSERVATIONAL COMPARISON
Synthetic Observations
# Convert simulation data into mock images/spectra.
# Ray Tracing: Compute light propagation through simulated volume.
# SED (Spectral Energy Distribution): Predict flux at different wavelengths.

Power Spectrum Analysis
# P(k): Statistical measure of structure clustering.
# Compare simulation P(k) with galaxy survey data (SDSS, Euclid).

Two-Point Correlation Function
# xi(r): Probability of finding two galaxies separated by distance r.
# Measures clustering strength.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Magnetohydrodynamics (MHD)
# Coupling magnetic fields with fluid dynamics.
# Important for jet formation, accretion disks, star formation.
# Constrained Transport (CT) scheme preserves div(B)=0.

Cosmic Rays
# High-energy particles accelerated by shocks.
# Transport equation includes diffusion, advection, and losses.

Gravitational Waves
# Numerical Relativity: Solve Einstein's field equations directly.
# Used for binary black hole/neutron star mergers.
# Codes: Einstein Toolkit, SpEC.

Recommended Reading
# - "Galactic Dynamics" by Binney and Tremaine
# - "Numerical Recipes in Fortran/C++" (Chapters on ODEs/PDEs)
# - "Cosmological Physics" by John Peacock
# - GADGET Documentation: https://wwwmpa.mpa-garching.mpg.de/gadget/
# - Astropy Documentation: https://docs.astropy.org/

# End of Advanced Astrophysics Reference