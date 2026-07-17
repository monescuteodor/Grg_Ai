High-Energy Physics Simulation Complete Reference
CHAPTER 1: GETTING STARTED WITH HIGH-ENERGY PHYSICS
Remarks
High-Energy Physics (HEP) simulation models the interactions of subatomic particles at high energies, typically in particle accelerators like the LHC. Key areas: Monte Carlo event generation, detector simulation, track reconstruction, and data analysis. Tools: Python (NumPy, SciPy, Matplotlib), C++ (ROOT framework), Geant4, Pythia8, MadGraph. Applications: Discovery of new particles (Higgs boson), testing Standard Model, searching for Dark Matter.
Tools: Python (NumPy, SciPy, ROOT via PyROOT), C++ (Geant4, ROOT), Geant4, Pythia8, MadGraph.
Hello Particle Decay
# hello_hep.py
"""
First HEP program: Simulate simple particle decay.
"""
import numpy as np
import matplotlib.pyplot as plt

def simulate_decay(lifetime, n_particles=1000):
    """Simulate exponential decay of particles."""
    # Time of decay for each particle
    t_decays = np.random.exponential(scale=lifetime, size=n_particles)
    return t_decays

# Example: Muon lifetime ~2.2 microseconds
lifetime = 2.2e-6  # seconds
t_decays = simulate_decay(lifetime, 10000)

plt.figure(figsize=(10, 5))
plt.hist(t_decays * 1e6, bins=50, density=True, alpha=0.7, color='blue', label='Simulated')
# Theoretical curve
t_theory = np.linspace(0, 10, 100)
pdf = (1/lifetime) * np.exp(-t_theory / lifetime)
plt.plot(t_theory * 1e6, pdf * 1e6, 'r-', linewidth=2, label='Theoretical')
plt.xlabel('Time (microseconds)')
plt.ylabel('Probability Density')
plt.title('Muon Decay Simulation')
plt.legend()
plt.grid(True)
plt.show()

Standard Model Particles
# Quarks: Up, Down, Charm, Strange, Top, Bottom.
# Leptons: Electron, Muon, Tau, Neutrinos.
# Bosons: Photon, W/Z, Gluon, Higgs.

Conservation Laws
# Energy, Momentum, Charge, Lepton Number, Baryon Number.
# Used to validate simulated events.

CHAPTER 2: MONTE CARLO EVENT GENERATION
Phase Space Integration
# Calculate probability of final states given initial state.
# Cross-section: Measure of interaction probability.

Importance Sampling
# Generate events more frequently in regions of high cross-section.
# Reduces variance in results.

Parton Distribution Functions (PDFs)
# Describe momentum distribution of quarks/gluons inside protons.
# Essential for proton-proton collisions (LHC).

Pythia8 Interface
# Popular event generator for HEP.
# Simulates hard process, parton shower, hadronization.

# Example Pythia8 usage (conceptual)
# import pythia8
# pythia = pythia8.Pythia()
# pythia.readString("Beams:idA = 2212")  # Proton
# pythia.readString("Beams:idB = 2212")  # Proton
# pythia.readString("Beams:eCM = 13000.") # 13 TeV
# pythia.init()
# pythia.next()
# Get particle info...

CHAPTER 3: DETECTOR SIMULATION WITH GEANT4
Geometry Definition
# Define volumes, materials, and positions.
# World volume, sensitive detectors.

Physics Lists
# Specify which physical processes to simulate.
# Electromagnetic, Hadronic, Decay, Optical.

Tracking
# Step through particle trajectory.
# Calculate energy loss, scattering, secondary production.

Digitization
# Convert energy deposits into electronic signals.
# Simulate noise, resolution, efficiency.

CHAPTER 4: TRACK RECONSTRUCTION
Kalman Filter for Tracking
# Estimate particle trajectory from hit positions.
# Handle measurement errors and material effects.

Pattern Recognition
# Identify tracks from hits in detector layers.
# Hough Transform, Cellular Automata.

Vertex Finding
# Determine origin point of tracks.
# Primary vertex (collision point), Secondary vertices (decays).

CHAPTER 5: DATA ANALYSIS
ROOT Framework
# C++/Python framework for HEP data analysis.
# TTree: Efficient storage of large datasets.
# TH1F/TH2F: Histograms.

Statistical Methods
# Hypothesis testing: Signal vs Background.
# p-value, Significance (Z-score).
# Likelihood fits.

Machine Learning in HEP
# Classification: Signal/Background separation.
# Regression: Energy calibration.
# Anomaly detection: New physics search.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Lattice QCD
# Quantum Chromodynamics on a discrete spacetime lattice.
# Calculate hadron masses, strong coupling constant.
# Computationally intensive (supercomputers).

Neutrino Physics
# Oscillations, mass hierarchy.
# Long-baseline experiments.

Beyond Standard Model
# Supersymmetry, Extra Dimensions, Dark Matter candidates.
# Signature simulation and search strategies.

Recommended Reading
# - "Introduction to High Energy Physics" by Perkins
# - "Monte Carlo Methods in High Energy Physics" by James
# - Geant4 Documentation: https://geant4.web.cern.ch/
# - ROOT Documentation: https://root.cern/

# End of High-Energy Physics Simulation Reference