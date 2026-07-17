Computational Chemistry & Molecular Modeling Complete Reference
CHAPTER 1: GETTING STARTED WITH COMPUTATIONAL CHEMISTRY
Remarks
Computational chemistry uses computer simulation to help solve chemical problems. It uses methods of theoretical chemistry, incorporated into efficient computer programs, to calculate the structures and properties of molecules and solids. Key areas: Quantum Chemistry (electronic structure), Molecular Mechanics (force fields), Molecular Dynamics (time evolution), and Docking (drug discovery).
Tools: Python (NumPy, SciPy, ASE, RDKit), Gaussian, ORCA, GROMACS, LAMMPS, PyMOL, VMD.
Hello Computational Chemistry
# hello_chem.py
"""
First chem program: Calculate bond length from coordinates.
"""
import numpy as np

def calculate_distance(atom1, atom2):
    """Calculate Euclidean distance between two atoms."""
    return np.linalg.norm(np.array(atom1) - np.array(atom2))

# Water molecule coordinates (Angstroms)
O = [0.0000, 0.0000, 0.1173]
H1 = [0.0000, 0.7572, -0.4692]
H2 = [0.0000, -0.7572, -0.4692]

dist_OH1 = calculate_distance(O, H1)
dist_OH2 = calculate_distance(O, H2)
dist_HH = calculate_distance(H1, H2)

print("=== Water Molecule Geometry ===")
print(f"O-H1 Bond Length: {dist_OH1:.4f} Å")
print(f"O-H2 Bond Length: {dist_OH2:.4f} Å")
print(f"H-H Distance:     {dist_HH:.4f} Å")

# Calculate angle H-O-H using dot product
def calculate_angle(p1, p2, p3):
    """Calculate angle at p2 formed by p1-p2-p3."""
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)
    
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    # Clip to avoid numerical errors outside [-1, 1]
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    return np.degrees(np.arccos(cos_angle))

angle = calculate_angle(H1, O, H2)
print(f"H-O-H Angle:      {angle:.2f}°")

Molecular File Formats
# XYZ Format: Simple coordinate list.
# PDB Format: Protein Data Bank (complex, includes connectivity).
# SDF/MOL: MDL Molfile (includes bonds and properties).
# SMILES: Simplified Molecular Input Line Entry System (string representation).

def parse_xyz(filename):
    """Parse a simple XYZ file."""
    atoms = []
    coords = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        n_atoms = int(lines[0])
        # Comment line ignored
        for line in lines[2:2+n_atoms]:
            parts = line.split()
            atoms.append(parts[0])
            coords.append([float(x) for x in parts[1:]])
    return atoms, np.array(coords)

# Example XYZ content for Methane (CH4)
xyz_content = """5
Methane
C    0.0000    0.0000    0.0000
H    0.6287    0.6287    0.6287
H   -0.6287   -0.6287    0.6287
H   -0.6287    0.6287   -0.6287
H    0.6287   -0.6287   -0.6287
"""

with open('methane.xyz', 'w') as f:
    f.write(xyz_content)

atoms, coords = parse_xyz('methane.xyz')
print(f"\nParsed {len(atoms)} atoms from XYZ.")
print(f"Coordinates shape: {coords.shape}")

CHAPTER 2: MOLECULAR MECHANICS (FORCE FIELDS)
Potential Energy Surface
# Molecular Mechanics approximates potential energy using classical physics.
# E_total = E_bond + E_angle + E_dihedral + E_vdW + E_electrostatic

# 1. Bond Stretching (Harmonic Oscillator)
# E_bond = k_b * (r - r0)^2

# 2. Angle Bending
# E_angle = k_theta * (theta - theta0)^2

# 3. Torsion (Dihedral)
# E_dihedral = k_phi * [1 + cos(n*phi - delta)]

# 4. Van der Waals (Lennard-Jones)
# E_vdW = 4*epsilon * [(sigma/r)^12 - (sigma/r)^6]

# 5. Electrostatics (Coulomb)
# E_coulomb = (q1 * q2) / (4*pi*epsilon0 * r)

import numpy as np

def harmonic_bond(r, r0, k_b):
    """Bond stretching energy."""
    return k_b * (r - r0)**2

def lennard_jones(r, epsilon, sigma):
    """Van der Waals interaction."""
    sr6 = (sigma / r)**6
    return 4 * epsilon * (sr6**2 - sr6)

def coulomb(q1, q2, r, epsilon_r=1.0):
    """Electrostatic interaction (simplified units)."""
    ke = 332.06  # kcal·Å/(mol·e²)
    return (ke * q1 * q2) / (epsilon_r * r)

# Example: Interaction between two Argon atoms
r_range = np.linspace(2.5, 10, 100)
epsilon = 0.238  # kcal/mol
sigma = 3.405    # Angstroms

energies = [lennard_jones(r, epsilon, sigma) for r in r_range]

import matplotlib.pyplot as plt
plt.figure(figsize=(8, 5))
plt.plot(r_range, energies)
plt.axhline(0, color='k', linestyle='--', linewidth=0.5)
plt.xlabel("Distance (Å)")
plt.ylabel("Potential Energy (kcal/mol)")
plt.title("Lennard-Jones Potential for Argon")
plt.grid(True)
plt.show()

Force Fields
# Popular Force Fields:
# - AMBER: Biomolecules (proteins, DNA).
# - CHARMM: Biomolecules and materials.
# - OPLS: Organic liquids and proteins.
# - UFF: Universal Force Field (inorganic/organic).

CHAPTER 3: QUANTUM CHEMISTRY BASICS
Hartree-Fock Method
# Approximates the many-electron wavefunction as a single Slater determinant.
# Solves the Schrödinger equation iteratively (Self-Consistent Field - SCF).
# Ignores electron correlation (dynamic correlation).

# Basis Sets:
# STO-3G: Minimal basis set (fast, low accuracy).
# 6-31G*: Split-valence with polarization (standard).
# cc-pVTZ: Correlation-consistent triple-zeta (high accuracy).

def simple_huckel(alpha, beta, n_atoms):
    """
    Simple Hückel method for pi-electron systems.
    alpha: Coulomb integral
    beta: Resonance integral
    n_atoms: Number of conjugated atoms
    """
    # Construct Hamiltonian matrix
    H = np.zeros((n_atoms, n_atoms))
    for i in range(n_atoms):
        H[i, i] = alpha
        if i < n_atoms - 1:
            H[i, i+1] = beta
            H[i+1, i] = beta
            
    # Solve eigenvalue problem
    energies, coefficients = np.linalg.eigh(H)
    return energies, coefficients

# Butadiene (4 carbons)
alpha = 0.0  # Reference energy
beta = -1.0  # Negative value
energies, coeffs = simple_huckel(alpha, beta, 4)

print("\n=== Hückel MO Energies (Butadiene) ===")
for i, e in enumerate(energies):
    print(f"MO {i+1}: E = {e:.2f} beta")

Density Functional Theory (DFT)
# Uses electron density rho(r) instead of wavefunction.
# Hohenberg-Kohn Theorems: Ground state properties are determined by rho(r).
# Kohn-Sham Equations: Map interacting system to non-interacting reference system.
# Functionals: LDA, GGA (PBE), Hybrid (B3LYP, PBE0).

CHAPTER 4: MOLECULAR DYNAMICS (MD)
Verlet Integration
# Solves Newton's equations of motion: F = ma
# Positions updated based on forces derived from potential energy.

class Particle:
    def __init__(self, mass, pos, vel):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.force = np.zeros(3)

def verlet_step(particles, dt, potential_func):
    """Velocity Verlet integration step."""
    # 1. Update positions
    for p in particles:
        p.pos += p.vel * dt + 0.5 * (p.force / p.mass) * dt**2
    
    # 2. Compute new forces
    compute_forces(particles, potential_func)
    
    # 3. Update velocities
    for p in particles:
        p.vel += 0.5 * (p.force / p.mass) * dt

def compute_forces(particles, potential_func):
    """Compute pairwise forces."""
    for p in particles:
        p.force = np.zeros(3)
        
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            r_vec = particles[j].pos - particles[i].pos
            r_dist = np.linalg.norm(r_vec)
            if r_dist < 0.01: continue # Avoid singularity
            
            # Force magnitude from Lennard-Jones derivative
            # F = -dV/dr
            eps = 1.0
            sig = 1.0
            sr6 = (sig/r_dist)**6
            force_mag = 24 * eps * (2 * sr6**2 - sr6) / r_dist
            
            f_vec = force_mag * (r_vec / r_dist)
            
            particles[i].force += f_vec
            particles[j].force -= f_vec

# Simple MD Simulation
p1 = Particle(1.0, [0, 0, 0], [0, 0, 0])
p2 = Particle(1.0, [1.5, 0, 0], [0, 0, 0])
particles = [p1, p2]

dt = 0.001
steps = 1000
trajectory = []

compute_forces(particles, None) # Initial forces

for _ in range(steps):
    verlet_step(particles, dt, None)
    if _ % 100 == 0:
        dist = np.linalg.norm(p1.pos - p2.pos)
        trajectory.append(dist)

plt.figure(figsize=(8, 4))
plt.plot(trajectory)
plt.xlabel("Step (x100)")
plt.ylabel("Interatomic Distance (Å)")
plt.title("MD Simulation of Two Atoms")
plt.grid(True)
plt.show()

Thermostats and Barostats
# Thermostat: Controls temperature (kinetic energy).
# - Berendsen Thermostat: Weak coupling.
# - Nosé-Hoover Thermostat: Extended Lagrangian.

# Barostat: Controls pressure.
# - Parrinello-Rahman: Allows box shape change.

CHAPTER 5: CHEMINFORMATICS
SMILES Parsing
# SMILES: String representation of molecular structure.
# Example: Ethanol -> "CCO", Benzene -> "c1ccccc1"

try:
    from rdkit import Chem
    from rdkit.Chem import Draw
    
    def smiles_to_mol(smiles):
        return Chem.MolFromSmiles(smiles)
    
    def mol_to_image(mol, filename="mol.png"):
        img = Draw.MolToImage(mol)
        img.save(filename)
        return filename
        
    ethanol = smiles_to_mol("CCO")
    benzene = smiles_to_mol("c1ccccc1")
    
    print("\n=== RDKit Cheminformatics ===")
    print(f"Ethanol Atoms: {ethanol.GetNumAtoms()}")
    print(f"Benzene Atoms: {benzene.GetNumAtoms()}")
    
    # mol_to_image(benzene)
except ImportError:
    print("RDKit not installed. Install with: conda install -c conda-forge rdkit")

Molecular Descriptors
# Properties calculated from structure:
# - Molecular Weight
# - LogP (Lipophilicity)
# - TPSA (Topological Polar Surface Area)
# - H-Bond Donors/Acceptors

def calculate_molecular_weight(mol):
    from rdkit.Chem import Descriptors
    return Descriptors.MolWt(mol)

if 'ethanol' in locals():
    mw = calculate_molecular_weight(ethanol)
    print(f"Ethanol MW: {mw:.2f} g/mol")

QSAR (Quantitative Structure-Activity Relationship)
# Statistical model linking descriptors to biological activity.
# Activity = f(Descriptors)
# Used in drug discovery to predict potency/toxicity.

CHAPTER 6: DOCKING AND DRUG DISCOVERY
Protein-Ligand Docking
# Predicts preferred orientation of ligand bound to protein.
# Scoring functions estimate binding affinity.
# Methods: Rigid docking, Flexible docking, Induced fit.

# Steps:
# 1. Prepare Protein (add hydrogens, assign charges).
# 2. Prepare Ligand (generate conformers).
# 3. Search Algorithm (Genetic Algorithm, Monte Carlo).
# 4. Scoring (Van der Waals, H-bonds, Electrostatics).

def simple_scoring(ligand_pos, protein_sites):
    """Dummy scoring function based on distance."""
    score = 0
    for site in protein_sites:
        dist = np.linalg.norm(ligand_pos - site)
        if dist < 3.0:
            score -= 1.0 # Favorable contact
    return score

# Virtual Screening
# Screening large libraries of compounds against a target.
# High-Throughput Virtual Screening (HTVS).

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Ab Initio vs Semi-Empirical
# Ab Initio: First principles (HF, MP2, CCSD(T)). Accurate but expensive.
# Semi-Empirical: Parameters from experiment (PM6, AM1). Fast, less accurate.

Machine Learning in Chemistry
# Predicting properties without solving Schrödinger equation.
# Graph Neural Networks (GNNs) for molecular graphs.
# AlphaFold for protein structure prediction.

Recommended Reading
# - "Modern Quantum Chemistry" by Szabo and Ostlund
# - "Understanding Molecular Simulation" by Frenkel and Smit
# - "Chemoinformatics" by Gasteiger
# - RDKit Documentation: https://www.rdkit.org/docs/
# - ASE (Atomic Simulation Environment): https://wiki.fysik.dtu.dk/ase/

# End of Computational Chemistry Reference