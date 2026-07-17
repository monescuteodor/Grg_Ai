Advanced Fluid Dynamics & Computational Fluid Dynamics (CFD) Complete Reference
CHAPTER 1: GETTING STARTED WITH FLUID DYNAMICS
Remarks
Fluid dynamics studies the motion of liquids and gases. Computational Fluid Dynamics (CFD) uses numerical analysis and data structures to solve and analyze problems that involve fluid flows. Key concepts: Conservation laws (mass, momentum, energy), Navier-Stokes equations, turbulence modeling, boundary layers, multiphase flow. Applications: Aerodynamics (aircraft, cars), HVAC systems, weather prediction, blood flow, chemical reactor design.
Tools: Python (NumPy, SciPy, PyFoam, FiPy), OpenFOAM, ANSYS Fluent, COMSOL, Lattice Boltzmann Method (LBM) codes.
Hello Fluid Dynamics
# hello_cfd.py
"""
First CFD program: 1D Linear Convection Equation.
du/dt + c * du/dx = 0
"""
import numpy as np
import matplotlib.pyplot as plt

def linear_convection_1d(nx=41, nt=25, dx=2.0/(nx-1), dt=0.025, c=1.0):
    """Solve 1D linear convection using finite difference."""
    x = np.linspace(0, 2, nx)
    u = np.ones(nx)      # Initialize u to 1 everywhere
    u[int(0.5/dx):int(1/dx)+1] = 2  # Set initial hat function
    
    un = np.ones(nx)     # Helper array
    
    for n in range(nt):
        un = u.copy()    # Copy current values to helper array
        for i in range(1, nx):
            # Forward difference in space, forward in time (FTFS)
            # Note: For stability, usually upwind scheme is used if c > 0
            u[i] = un[i] - c * dt / dx * (un[i] - un[i-1])
            
    return x, u

x, u = linear_convection_1d()

plt.figure(figsize=(8, 4))
plt.plot(x, u, 'r-', label='Numerical Solution')
plt.xlabel('Position (x)')
plt.ylabel('Velocity (u)')
plt.title('1D Linear Convection (Hat Function Transport)')
plt.legend()
plt.grid(True)
plt.ylim([0.5, 2.5])
plt.show()

Governing Equations
# 1. Continuity Equation (Mass Conservation):
#    ∂ρ/∂t + ∇·(ρu) = 0
# 2. Momentum Equation (Navier-Stokes):
#    ρ(∂u/∂t + u·∇u) = -∇p + μ∇²u + f
# 3. Energy Equation:
#    ρCp(∂T/∂t + u·∇T) = k∇²T + Φ

Where:
ρ = density
u = velocity vector
p = pressure
μ = dynamic viscosity
f = body forces (gravity)
T = temperature
k = thermal conductivity

CHAPTER 2: DISCRETIZATION METHODS
Finite Difference Method (FDM)
# Approximates derivatives using Taylor series expansions.
# Grid-based (structured grids).
# Simple to implement, hard for complex geometries.

# Derivatives:
# Forward: (u_{i+1} - u_i) / dx
# Backward: (u_i - u_{i-1}) / dx
# Central: (u_{i+1} - u_{i-1}) / (2*dx)

Finite Volume Method (FVM)
# Integrates governing equations over control volumes.
# Conserves mass/momentum exactly within each cell.
# Standard for commercial CFD codes (OpenFOAM, Fluent).
# Handles unstructured grids well.

Finite Element Method (FEM)
# Uses variational formulation and basis functions.
# Common in structural mechanics, increasingly used in CFD (COMSOL).
# Good for complex boundaries and adaptive meshing.

Lattice Boltzmann Method (LBM)
# Mesoscopic approach: simulates particle distribution functions on a lattice.
# Recovers Navier-Stokes at macroscopic limit.
# Highly parallelizable, good for multiphase and porous media.

CHAPTER 3: TURBULENCE MODELING
Reynolds Number
# Re = (ρ * U * L) / μ
# Low Re (< 2300 pipe): Laminar flow (smooth, orderly).
# High Re (> 4000 pipe): Turbulent flow (chaotic, mixing).

RANS (Reynolds-Averaged Navier-Stokes)
# Decomposes variables into mean and fluctuating parts: u = U + u'
# Solves for mean flow, models turbulence effects via Reynolds Stress Tensor.
# Models:
# - k-epsilon: Robust, standard for industrial flows.
# - k-omega: Better for near-wall treatment, adverse pressure gradients.
# - Spalart-Allmaras: One-equation model, popular in aerospace.

LES (Large Eddy Simulation)
# Resolves large turbulent eddies directly.
# Models only small-scale subgrid scales.
# More accurate than RANS, but computationally expensive.

DNS (Direct Numerical Simulation)
# Resolves all scales of turbulence down to Kolmogorov scale.
# No modeling required.
# Extremely expensive (Re^3 cost), limited to low Re or small domains.

CHAPTER 4: BOUNDARY CONDITIONS & MESHING
Boundary Conditions
# Inlet: Velocity profile, mass flow rate, total pressure.
# Outlet: Static pressure, outflow.
# Wall: No-slip (u=0), slip (du/dn=0), moving wall.
# Symmetry: Zero normal gradient.
# Periodic: Flow repeats across boundary.

Meshing Strategies
# Structured Mesh: Regular grid (i,j,k). Easy to generate, hard for complex shapes.
# Unstructured Mesh: Triangles/tetrahedra. Flexible, harder to converge.
# Hybrid Mesh: Structured near walls (boundary layer), unstructured elsewhere.
# Mesh Quality Metrics: Aspect ratio, skewness, orthogonality.

Boundary Layer Resolution
# y+ (y-plus): Non-dimensional distance from wall.
# y+ < 1: Required for resolving viscous sublayer (low-Re models).
# y+ ~ 30-300: Used with wall functions (high-Re models).

CHAPTER 5: MULTIPHASE FLOW
VOF (Volume of Fluid)
# Tracks interface between immiscible fluids (e.g., air-water).
# Uses volume fraction α (0 to 1).
# Captures surface tension effects.

Eulerian-Eulerian
# Treats each phase as interpenetrating continua.
# Used for fluid-fluid (bubbles) or fluid-solid (particles) flows.
# Solves separate momentum equations for each phase.

Discrete Phase Model (DPM)
# Tracks individual particles/droplets in a continuous fluid.
# One-way coupling (fluid affects particles) or two-way coupling.
# Used for sprays, sedimentation, cyclones.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Compressible Flow
# Mach number Ma = U / a (speed of sound).
# Ma < 0.3: Incompressible assumption valid.
# Ma > 0.3: Density changes significant.
# Shock waves: Discontinuities in pressure, temperature, density.
# Requires density-based solvers.

Heat Transfer Coupling
# Conjugate Heat Transfer (CHT): Couples fluid flow with solid conduction.
# Important for heat exchangers, electronics cooling.

Reacting Flows
# Combustion modeling: Finite-rate chemistry, eddy dissipation concept.
# Species transport: Advection-diffusion-reaction equations.

Recommended Reading
# - "Computational Fluid Dynamics: The Basics with Applications" by John D. Anderson
# - "Turbulence Modeling for CFD" by David C. Wilcox
# - "An Introduction to Computational Fluid Dynamics" by H.K. Versteeg
# - OpenFOAM User Guide: https://openfoam.com/guides/
# - NASA CFD Vision 2030 Study

# End of Advanced Fluid Dynamics Reference