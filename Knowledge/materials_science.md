Advanced Materials Science & Computational Design Complete Reference
CHAPTER 1: GETTING STARTED WITH MATERIALS SCIENCE
Remarks
Materials science studies the relationship between the structure, properties, processing, and performance of materials. Computational materials science uses simulations (DFT, MD, Phase Field) to predict material behavior before synthesis. Key areas: Electronic structure, mechanical properties, phase diagrams, diffusion, corrosion, nanomaterials. Applications: Battery design, aerospace alloys, semiconductors, biomaterials, catalysts.
Tools: Python (ASE, pymatgen, matminer), VASP, Quantum ESPRESSO, LAMMPS, Thermo-Calc, OpenCalphad.
Hello Materials Science
# hello_materials.py
"""
First materials program: Calculate atomic packing factor for FCC crystal.
"""
import numpy as np

def atomic_packing_factor_fcc():
    """
    FCC (Face-Centered Cubic) structure.
    Atoms touch along face diagonal.
    4 atoms per unit cell.
    """
    # In FCC, face diagonal = 4 * radius = sqrt(2) * a
    # So, a = 4 * r / sqrt(2) = 2 * sqrt(2) * r
    
    # Volume of atoms in unit cell
    # 4 atoms * (4/3) * pi * r^3
    # Volume of unit cell = a^3 = (2*sqrt(2)*r)^3 = 16*sqrt(2)*r^3
    
    # APF = Vol_atoms / Vol_cell
    # APF = (4 * 4/3 * pi * r^3) / (16 * sqrt(2) * r^3)
    # APF = (16/3 * pi) / (16 * sqrt(2))
    # APF = pi / (3 * sqrt(2))
    
    apf = np.pi / (3 * np.sqrt(2))
    return apf

print(f"Atomic Packing Factor (FCC): {atomic_packing_factor_fcc():.4f}")
print(f"Theoretical Max: 0.74")

Crystal Structures
# BCC (Body-Centered Cubic): Fe at room temp. APF = 0.68.
# HCP (Hexagonal Close-Packed): Mg, Zn. APF = 0.74.
# Diamond Cubic: Si, Ge. APF = 0.34.

def miller_indices_to_normal(h, k, l):
    """Return normal vector for plane (hkl) in cubic system."""
    return np.array([h, k, l])

# Example: Normal to (111) plane
normal = miller_indices_to_normal(1, 1, 1)
print(f"Normal to (111): {normal}")

CHAPTER 2: ELECTRONIC STRUCTURE THEORY
Density Functional Theory (DFT)
# Solves Schrödinger equation for many-electron systems.
# Hohenberg-Kohn Theorems: Ground state energy is functional of electron density.
# Kohn-Sham Equations: Map interacting system to non-interacting reference system.
# Exchange-Correlation Functionals: LDA, GGA (PBE), Hybrid (B3LYP).

# DFT Workflow:
# 1. Define crystal structure (lattice vectors, atomic positions).
# 2. Choose pseudopotentials (PAW, ultrasoft).
# 3. Set convergence parameters (k-point mesh, energy cutoff).
# 4. Self-consistent field iteration.
# 5. Extract properties (band structure, DOS, forces).

Band Structure Calculation
# Energy bands E(k) vs wave vector k in Brillouin zone.
# Band gap: Difference between valence band maximum and conduction band minimum.
# Direct gap: Same k-point. Indirect gap: Different k-points.

import matplotlib.pyplot as plt

def plot_band_structure_example():
    """Plot hypothetical band structure."""
    k_points = np.linspace(0, 1, 100)
    
    # Valence band
    vb = -2 * np.cos(np.pi * k_points) - 1
    
    # Conduction band
    cb = 2 * np.cos(np.pi * k_points) + 1
    
    plt.figure(figsize=(8, 5))
    plt.plot(k_points, vb, 'b-', label='Valence Band')
    plt.plot(k_points, cb, 'r-', label='Conduction Band')
    plt.axhline(0, color='k', linestyle='--', linewidth=0.5)
    plt.xlabel('Wave Vector k')
    plt.ylabel('Energy (eV)')
    plt.title('Hypothetical Band Structure (Direct Gap)')
    plt.legend()
    plt.grid(True)
    plt.show()

plot_band_structure_example()

Density of States (DOS)
# Number of states per interval of energy.
# Integral of DOS up to Fermi level gives number of electrons.

CHAPTER 3: MECHANICAL PROPERTIES
Stress-Strain Curve
# Elastic Region: Hooke's Law (sigma = E * epsilon).
# Yield Point: Onset of plastic deformation.
# Plastic Region: Permanent deformation.
# Ultimate Tensile Strength: Maximum stress.
# Fracture Point: Material breaks.

def youngs_modulus(stress, strain):
    """Calculate Young's Modulus from linear elastic region."""
    # Assume first 5 points are linear
    coeffs = np.polyfit(strain[:5], stress[:5], 1)
    return coeffs[0]

# Example data
strain = np.array([0.001, 0.002, 0.003, 0.004, 0.005, 0.01, 0.02, 0.05])
stress = np.array([200, 400, 600, 800, 1000, 1100, 1150, 1100]) # MPa

E = youngs_modulus(stress, strain)
print(f"Young's Modulus: {E:.1f} MPa")

Dislocation Theory
# Edge Dislocation: Extra half-plane of atoms.
# Screw Dislocation: Spiral ramp of atoms.
# Slip Systems: Combination of slip plane and slip direction.
# Hall-Petch Relation: Yield strength increases with decreasing grain size.
# sigma_y = sigma_0 + k / sqrt(d)

def hall_petch_yield_strength(sigma_0, k, d):
    """Calculate yield strength based on grain size d."""
    return sigma_0 + k / np.sqrt(d)

sigma_0 = 50 # MPa
k = 0.5 # MPa*m^0.5
d = 10e-6 # 10 micrometers
sigma_y = hall_petch_yield_strength(sigma_0, k, d)
print(f"Yield Strength (d={d*1e6}um): {sigma_y:.1f} MPa")

CHAPTER 4: PHASE DIAGRAMS & THERMODYNAMICS
Gibbs Free Energy
# G = H - TS
# Phase stability determined by minimizing G.
# Chemical potential: mu = dG/dN.

CALPHAD Method
# CALculation of PHAse Diagrams.
# Uses thermodynamic models to describe Gibbs energy of phases.
# Optimizes parameters against experimental data.

# Binary Phase Diagram Types:
# 1. Isomorphous: Complete solubility (Cu-Ni).
# 2. Eutectic: Limited solubility, eutectic point (Pb-Sn).
# 3. Peritectic: Liquid + Solid1 -> Solid2.
# 4. Intermetallic Compounds: Fixed stoichiometry.

def lever_rule(c0, c_alpha, c_beta):
    """
    Calculate fraction of phases in two-phase region.
    c0: Overall composition
    c_alpha: Composition of alpha phase
    c_beta: Composition of beta phase
    """
    f_alpha = (c_beta - c0) / (c_beta - c_alpha)
    f_beta = 1 - f_alpha
    return f_alpha, f_beta

# Example: Pb-Sn alloy at eutectic temperature
c0 = 0.4 # 40% Sn
c_alpha = 0.19 # 19% Sn in alpha
c_beta = 0.97 # 97% Sn in beta

f_alpha, f_beta = lever_rule(c0, c_alpha, c_beta)
print(f"Fraction Alpha: {f_alpha:.2f}")
print(f"Fraction Beta: {f_beta:.2f}")

CHAPTER 5: DIFFUSION & KINETICS
Fick's Laws
# First Law: J = -D * dc/dx (Steady state)
# Second Law: dc/dt = D * d^2c/dx^2 (Non-steady state)

def error_function_solution(x, t, D, Cs, C0):
    """
    Solution for semi-infinite solid with constant surface concentration.
    C(x,t) = Cs - (Cs - C0) * erf(x / (2*sqrt(D*t)))
    """
    from scipy.special import erf
    arg = x / (2 * np.sqrt(D * t))
    return Cs - (Cs - C0) * erf(arg)

# Example: Carbon diffusion into steel
D = 1e-11 # m^2/s
Cs = 1.0 # wt% C at surface
C0 = 0.2 # wt% C initial
x = 1e-3 # 1 mm depth
t = 3600 # 1 hour

C_xt = error_function_solution(x, t, D, Cs, C0)
print(f"Carbon concentration at {x*1000}mm after {t}s: {C_xt:.3f} wt%")

Arrhenius Equation
# D = D0 * exp(-Q / RT)
# Q: Activation energy
# R: Gas constant
# T: Temperature

def diffusion_coefficient(D0, Q, T):
    R = 8.314 # J/(mol*K)
    return D0 * np.exp(-Q / (R * T))

D0 = 2e-5 # m^2/s
Q = 142000 # J/mol
T = 1273 # 1000 C

D_T = diffusion_coefficient(D0, Q, T)
print(f"D at {T-273}C: {D_T:.2e} m^2/s")

CHAPTER 6: COMPUTATIONAL MATERIALS DESIGN
High-Throughput Screening
# Use databases (Materials Project, OQMD) to screen thousands of compounds.
# Filter by stability, band gap, elasticity.

import requests

def get_materials_project_data(api_key, formula):
    """Query Materials Project API."""
    url = "https://www.materialsproject.org/rest/v2/materials/"
    params = {"criteria": json.dumps({"task_id": formula}), "properties": ["formation_energy_per_atom", "band_gap"]}
    headers = {"X-API-KEY": api_key}
    # Note: This is a conceptual example. Actual API usage requires valid key and endpoint.
    pass

Machine Learning for Materials
# Predict properties from composition/structure.
# Features: Atomic number, electronegativity, radius, valence.
# Models: Random Forest, Neural Networks, Graph Neural Networks.

# Example: Predicting formation energy
from sklearn.ensemble import RandomForestRegressor

# Dummy data
features = np.random.rand(100, 5) # 5 features per material
targets = np.random.rand(100) # Formation energy

model = RandomForestRegressor(n_estimators=100)
model.fit(features, targets)

# Predict new material
new_material = np.random.rand(1, 5)
predicted_energy = model.predict(new_material)
print(f"Predicted Formation Energy: {predicted_energy[0]:.3f} eV/atom")

Generative Design
# Use Generative Adversarial Networks (GANs) or Variational Autoencoders (VAEs) to generate new crystal structures.
# Optimize for target properties using reinforcement learning.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Multiscale Modeling
# Linking different scales:
# Electronic (DFT) -> Atomic (MD) -> Microstructural (Phase Field) -> Continuum (FEM).

Topological Materials
# Materials with non-trivial topological order.
# Topological Insulators: Conducting surface, insulating bulk.
# Weyl Semimetals: Linear dispersion, chiral fermions.

2D Materials
# Graphene, MoS2, Black Phosphorus.
# Unique electronic, optical, and mechanical properties.

Recommended Reading
# - "Introduction to Physical Metallurgy" by Sidney Avner
# - "Computational Materials Science" by Richard LeSar
# - "Density Functional Theory: A Practical Introduction" by David Sholl
# - Materials Project: https://materialsproject.org/
# - ASE Documentation: https://wiki.fysik.dtu.dk/ase/

# End of Advanced Materials Science Reference