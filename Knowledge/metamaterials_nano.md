Metamaterials & Nanotechnology Complete Reference
CHAPTER 1: GETTING STARTED WITH METAMATERIALS
Remarks
Metamaterials are artificial structures engineered to have properties not found in naturally occurring materials. They derive their properties from their structure rather than their composition. Key applications: Negative refraction, invisibility cloaking, superlenses, acoustic insulation, and thermal management. Nanotechnology deals with matter on an atomic, molecular, and supramolecular scale (1-100 nm). Key areas: Nanoparticles, nanotubes, quantum dots, and nanofabrication.
Tools: Python (NumPy, SciPy, Meep for FDTD), Lumerical, COMSOL Multiphysics, MATLAB, Blender (for structure design).
Hello Metamaterials
# hello_meta.py
"""
First metamaterial program: Calculate effective permittivity using Maxwell-Garnett theory.
"""
import numpy as np

def maxwell_garnett(eps_m, eps_i, f):
    """
    Calculate effective permittivity of a composite material.
    eps_m: Permittivity of the matrix (host)
    eps_i: Permittivity of the inclusions
    f: Volume fraction of inclusions
    """
    numerator = eps_i + 2*eps_m + 2*f*(eps_i - eps_m)
    denominator = eps_i + 2*eps_m - f*(eps_i - eps_m)
    return eps_m * (numerator / denominator)

# Example: Silver nanoparticles in glass
eps_glass = 2.25  # Real part
eps_silver = -15 + 1j*0.5  # Complex permittivity at optical frequency
f = 0.1  # 10% volume fraction

eps_eff = maxwell_garnett(eps_glass, eps_silver, f)
print(f"Effective Permittivity: {eps_eff}")
print(f"Refractive Index: {np.sqrt(eps_eff)}")

Negative Refraction
# Snell's Law: n1 sin(theta1) = n2 sin(theta2)
# If n2 is negative, light refracts on the same side of the normal.

def snells_law(n1, n2, theta1_deg):
    theta1 = np.radians(theta1_deg)
    sin_theta2 = (n1 / n2) * np.sin(theta1)
    if np.abs(sin_theta2) > 1:
        return None  # Total internal reflection
    return np.degrees(np.arcsin(sin_theta2))

theta_refracted = snells_law(1.0, -1.5, 30)
print(f"Angle of Refraction (n=-1.5): {theta_refracted:.2f} degrees")

CHAPTER 2: COMPUTATIONAL ELECTROMAGNETICS
Finite-Difference Time-Domain (FDTD)
# Solves Maxwell's equations in time domain.
# Discretizes space and time into a grid.

import matplotlib.pyplot as plt

def simulate_1d_fdtd(steps=200, cells=100):
    """Simple 1D FDTD simulation of a wave hitting a boundary."""
    ez = np.zeros(cells)
    hy = np.zeros(cells)
    
    # Source position
    src_pos = cells // 4
    
    # Boundary position (change in impedance)
    bound_pos = cells // 2
    
    history = []
    
    for t in range(steps):
        # Update electric field
        for i in range(1, cells-1):
            ez[i] += (hy[i] - hy[i-1])
            
        # Add source pulse
        ez[src_pos] += np.exp(-((t-30)/10)**2)
        
        # Update magnetic field
        for i in range(cells-1):
            hy[i] += (ez[i+1] - ez[i])
            
        # Simple absorbing boundary
        ez[0] = 0
        ez[-1] = 0
        
        if t % 10 == 0:
            history.append(ez.copy())
            
    return np.array(history)

data = simulate_1d_fdtd()
plt.figure(figsize=(10, 5))
plt.imshow(data, aspect='auto', cmap='hot')
plt.title("1D FDTD Wave Propagation")
plt.xlabel("Cell Index")
plt.ylabel("Time Step")
plt.colorbar(label="E-field Intensity")
plt.show()

CHAPTER 3: NANOPARTICLE SYNTHESIS & PROPERTIES
Surface Plasmon Resonance
# Collective oscillation of conduction electrons in metal nanoparticles.
# Responsible for vibrant colors in stained glass and gold nanospheres.

def plasmon_resonance_wavelength(radius_nm, metal_type='Au'):
    """Estimate peak plasmon resonance wavelength (simplified)."""
    if metal_type == 'Au':
        # Gold spheres ~520nm, shifts with size
        return 520 + 0.5 * radius_nm
    elif metal_type == 'Ag':
        # Silver spheres ~400nm
        return 400 + 0.3 * radius_nm
    return 500

print(f"Au NP (20nm) Resonance: {plasmon_resonance_wavelength(20)} nm")
print(f"Ag NP (20nm) Resonance: {plasmon_resonance_wavelength(20, 'Ag')} nm")

Quantum Confinement
# When particle size < exciton Bohr radius, bandgap increases.
# E_gap(R) = E_bulk + h^2 / (8*m*R^2)

def quantum_dot_bandgap(r_nm, e_bulk_ev, m_eff):
    """Calculate bandgap of a quantum dot."""
    h = 4.135667696e-15  # eV*s
    c = 3e8
    # Simplified particle in a box model
    delta_e = (h**2) / (8 * m_eff * (r_nm * 1e-9)**2)
    # Convert J to eV roughly for demonstration
    return e_bulk_ev + delta_e * 6.24e18 

print(f"QD Bandgap Shift: {quantum_dot_bandgap(2, 1.4, 9.1e-31)} eV")

CHAPTER 4: NANOFABRICATION TECHNIQUES
Top-Down vs Bottom-Up
# Top-Down: Lithography, Etching, Milling.
# Bottom-Up: Chemical Vapor Deposition (CVD), Self-Assembly, Sol-Gel.

Lithography Resolution Limit
# Rayleigh Criterion: CD = k1 * lambda / NA
# CD: Critical Dimension, lambda: Wavelength, NA: Numerical Aperture

def lithography_limit(wavelength_nm, na, k1=0.25):
    """Calculate minimum feature size."""
    return k1 * wavelength_nm / na

print(f"EUV Lithography (13.5nm, NA=0.33): {lithography_limit(13.5, 0.33):.2f} nm")

CHAPTER 5: CARBON NANOMATERIALS
Graphene Properties
# Single layer of carbon atoms in hexagonal lattice.
# High conductivity, strength, and flexibility.

def graphene_conductivity(carrier_density, mobility):
    """Sigma = n * e * mu"""
    e = 1.602e-19
    return carrier_density * e * mobility

# Typical values
n = 1e12  # cm^-2
mu = 15000  # cm^2/Vs
sigma = graphene_conductivity(n, mu)
print(f"Graphene Conductivity: {sigma:.2e} S/cm")

Carbon Nanotubes (CNTs)
# Chirality determines metallic vs semiconducting behavior.
# (n,m) indices define the roll-up vector.

def is_metallic_cnt(n, m):
    """Metallic if (n-m) is divisible by 3."""
    return (n - m) % 3 == 0

print(f"(5,5) Armchair CNT Metallic? {is_metallic_cnt(5,5)}")
print(f"(10,0) Zigzag CNT Metallic? {is_metallic_cnt(10,0)}")

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Photonic Crystals
# Periodic dielectric structures that affect photon motion like semiconductors affect electrons.
# Photonic Bandgaps: Frequencies where light cannot propagate.

Acoustic Metamaterials
# Structures designed to control sound waves.
# Applications: Sound cloaking, sub-wavelength imaging, vibration isolation.

Thermal Metamaterials
# Control heat flow via transformation thermodynamics.
# Thermal cloaks and concentrators.

Recommended Reading
# - "Principles of Nano-Optics" by Novotny and Hecht
# - "Metamaterials: Theory, Design, and Applications" by Cui et al.
# - "Introduction to Nanoscience and Nanotechnology" by Gabor L. Hornyak
# - Meep Documentation: https://meep.readthedocs.io/

# End of Metamaterials & Nanotechnology Reference