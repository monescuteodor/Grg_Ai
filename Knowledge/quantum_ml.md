Quantum Machine Learning Complete Reference
CHAPTER 1: GETTING STARTED WITH QUANTUM MACHINE LEARNING
Remarks
Quantum Machine Learning (QML) explores the intersection of quantum computing and machine learning. It aims to leverage quantum mechanical phenomena (superposition, entanglement, interference) to speed up ML tasks or create new models. Key areas: Variational Quantum Circuits (VQC), Quantum Kernel Methods, Quantum Neural Networks (QNN), Hybrid Classical-Quantum algorithms. Current hardware is NISQ (Noisy Intermediate-Scale Quantum), so algorithms must be shallow and noise-resilient.
Tools: Python, Qiskit (IBM), PennyLane (Xanadu), Cirq (Google), TensorFlow Quantum, PyTorch Quantum.
Hello QML
# hello_qml.py
"""
First QML program: A simple variational classifier using PennyLane.
"""
import pennylane as qml
from pennylane import numpy as np

# Define a quantum device (simulator)
dev = qml.device("default.qubit", wires=2)

# Define a variational quantum circuit (Ansatz)
@qml.qnode(dev)
def circuit(weights, x):
    # Data encoding (Angle Encoding)
    qml.RX(x[0], wires=0)
    qml.RY(x[1], wires=1)
    
    # Variational layer
    qml.CRY(weights[0], wires=[0, 1])
    qml.CRZ(weights[1], wires=[0, 1])
    
    # Measurement
    return qml.expval(qml.PauliZ(0))

# Random weights
weights = np.array([0.5, 0.5], requires_grad=True)
# Input data
x = np.array([0.1, 0.2])

# Evaluate
result = circuit(weights, x)
print(f"Circuit output: {result}")

# Compute gradient (automatic differentiation)
grad_fn = qml.grad(circuit, argnum=0)
gradients = grad_fn(weights, x)
print(f"Gradients: {gradients}")

CHAPTER 2: DATA ENCODING STRATEGIES
Encoding Classical Data into Quantum States
# Quantum computers process quantum states, so classical data must be encoded.
# Common methods: Basis Encoding, Angle Encoding, Amplitude Encoding.

import pennylane as qml
import numpy as np

def basis_encoding(state, wires):
    """Encode binary data into computational basis states."""
    for i, bit in enumerate(state):
        if bit == 1:
            qml.PauliX(wires=wires[i])

def angle_encoding(features, wires):
    """Encode features as rotation angles."""
    for i, feature in enumerate(features):
        qml.RX(feature, wires=wires[i])
        qml.RY(feature, wires=wires[i])

def amplitude_encoding(state, wires):
    """Encode data into amplitudes of the quantum state."""
    # Normalize input
    norm = np.linalg.norm(state)
    state = state / norm
    qml.AmplitudeEmbedding(state, wires=wires)

# Example
dev = qml.device("default.qubit", wires=3)

@qml.qnode(dev)
def encode_and_measure(encoding_type, data):
    if encoding_type == "basis":
        basis_encoding(data, wires=[0, 1, 2])
    elif encoding_type == "angle":
        angle_encoding(data, wires=[0, 1, 2])
    elif encoding_type == "amplitude":
        amplitude_encoding(data, wires=[0, 1, 2])
    
    return [qml.expval(qml.PauliZ(i)) for i in range(3)]

data_basis = [1, 0, 1]
data_angle = [0.1, 0.2, 0.3]
data_amp = np.array([1, 2, 3, 4, 5, 6, 7, 8]) # Needs 2^3=8 elements for 3 qubits

print("Basis Encoding:", encode_and_measure("basis", data_basis))
print("Angle Encoding:", encode_and_measure("angle", data_angle))
# print("Amplitude Encoding:", encode_and_measure("amplitude", data_amp))

CHAPTER 3: VARIATIONAL QUANTUM CIRCUITS (VQC)
Variational Classifier
# VQC: A hybrid model where a quantum circuit acts as a trainable layer.
# Parameters are optimized using classical optimizers (Adam, SGD).

import pennylane as qml
from pennylane import numpy as np
import matplotlib.pyplot as plt

# Hyperparameters
n_wires = 2
n_layers = 2
n_data = 2

dev = qml.device("default.qubit", wires=n_wires)

# Define the variational ansatz
def layer(weights, wires):
    for i in range(n_wires):
        qml.RX(weights[i, 0], wires=wires[i])
        qml.RY(weights[i, 1], wires=wires[i])
    for i in range(n_wires - 1):
        qml.CNOT(wires=[wires[i], wires[i+1]])
    # Last qubit connects back to first
    qml.CNOT(wires=[wires[-1], wires[0]])

@qml.qnode(dev)
def vqc(weights, x):
    # Encode data
    angle_encoding(x, wires=range(n_wires))
    
    # Apply variational layers
    for l in range(n_layers):
        layer(weights[l], wires=range(n_wires))
        
    # Measure expectation value
    return qml.expval(qml.PauliZ(0))

# Cost function: Mean Squared Error
def cost(weights, X, Y):
    predictions = [vqc(weights, x) for x in X]
    return np.mean((np.array(predictions) - Y)**2)

# Generate dummy dataset (simple classification)
np.random.seed(42)
X = np.random.rand(20, n_data) * np.pi
Y = np.array([1 if x[0] > x[1] else -1 for x in X])

# Initialize weights
init_weights = np.random.rand(n_layers, n_wires, 2)

# Optimization loop
opt = qml.AdamOptimizer(stepsize=0.1)
weights = init_weights

losses = []
for i in range(100):
    weights, loss = opt.step(cost, weights, X, Y)
    losses.append(loss)
    if (i+1) % 20 == 0:
        print(f"Iteration {i+1}: Loss = {loss:.4f}")

plt.plot(losses)
plt.title("VQC Training Loss")
plt.xlabel("Iteration")
plt.ylabel("Loss")
plt.show()

Quantum Neural Network Layers
# QNNs can be built by stacking VQC layers.
# PennyLane integrates with PyTorch and TensorFlow.

import torch
import pennylane as qml

class QLayer(torch.nn.Module):
    def __init__(self, n_wires, n_layers):
        super().__init__()
        self.n_wires = n_wires
        self.n_layers = n_layers
        
        # Random initial weights
        self.weights = torch.nn.Parameter(
            torch.randn(n_layers, n_wires, 2)
        )
        
        self.dev = qml.device("default.qubit", wires=n_wires)
        
        @qml.qnode(self.dev, interface="torch")
        def circuit(weights, x):
            angle_encoding(x, wires=range(n_wires))
            for l in range(n_layers):
                layer(weights[l], wires=range(n_wires))
            return qml.expval(qml.PauliZ(0))
            
        self.circuit = circuit
        
    def forward(self, x):
        return self.circuit(self.weights, x)

# Example usage in a hybrid model
class HybridModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.quantum_layer = QLayer(n_wires=2, n_layers=2)
        self.classical_layer = torch.nn.Linear(1, 1)
        
    def forward(self, x):
        # x shape: (batch_size, 2)
        q_out = self.quantum_layer(x) # Shape: (batch_size,)
        q_out = q_out.unsqueeze(1)    # Shape: (batch_size, 1)
        out = self.classical_layer(q_out)
        return out

model = HybridModel()
print(model)

CHAPTER 4: QUANTUM KERNEL METHODS
Kernel Estimation on Quantum Computers
# Kernel methods map data to high-dimensional feature spaces.
# Quantum computers can implicitly map data to exponentially large Hilbert spaces.
# Kernel function: K(x, x') = |<phi(x)|phi(x')>|^2

import pennylane as qml
from sklearn.svm import SVC
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Quantum kernel function
def quantum_kernel(x1, x2, dev):
    @qml.qnode(dev)
    def circuit(x1, x2):
        # Prepare state |phi(x1)>
        angle_encoding(x1, wires=[0, 1])
        
        # Prepare state |phi(x2)> and measure overlap
        # Inverse of encoding x1
        qml.RY(-x1[1], wires=1)
        qml.RX(-x1[0], wires=0)
        
        # Encode x2
        angle_encoding(x2, wires=[0, 1])
        
        # Probability of measuring |00> is the fidelity
        return qml.probs(wires=[0, 1])[0]
        
    return circuit(x1, x2)

# Generate dataset
X, y = make_circles(n_samples=100, factor=0.1, noise=0.1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Define quantum device
dev = qml.device("default.qubit", wires=2)

# Create kernel matrix for training
def compute_kernel_matrix(X1, X2, dev):
    n1 = len(X1)
    n2 = len(X2)
    K = np.zeros((n1, n2))
    for i in range(n1):
        for j in range(n2):
            K[i, j] = quantum_kernel(X1[i], X2[j], dev)
    return K

# Note: Computing full kernel matrix is expensive. 
# In practice, use PennyLane's built-in kernel functions or approximate methods.

# Using PennyLane's built-in kernel for SVM
from pennylane.kernels import fidelity_kernel

# Train SVM with quantum kernel
# Note: This is computationally intensive for large datasets
# K_train = fidelity_kernel(X_train, X_train, dev)
# K_test = fidelity_kernel(X_test, X_train, dev)

# For demonstration, we use a linear SVM on raw data to show structure
clf = SVC(kernel='linear')
clf.fit(X_train, y_train)
preds = clf.predict(X_test)
print(f"Classical Linear SVM Accuracy: {accuracy_score(y_test, preds):.2f}")

# Quantum kernels often perform better on data that is not linearly separable in classical space
# but becomes separable in the high-dimensional quantum feature space.

CHAPTER 5: QUANTUM GENERATIVE MODELS
Quantum Generative Adversarial Networks (QGANs)
# QGAN: Generator is a quantum circuit, Discriminator can be classical or quantum.
# Goal: Generate samples from a target distribution.

import pennylane as qml
from pennylane import numpy as np

n_wires = 2
dev_gen = qml.device("default.qubit", wires=n_wires)
dev_disc = qml.device("default.qubit", wires=n_wires)

# Generator Circuit
@qml.qnode(dev_gen)
def generator(weights, noise):
    # Noise input
    qml.RX(noise[0], wires=0)
    qml.RY(noise[1], wires=1)
    
    # Trainable layers
    for w in weights:
        qml.RX(w[0], wires=0)
        qml.RY(w[1], wires=1)
        qml.CNOT(wires=[0, 1])
        
    return qml.sample(qml.PauliZ(0)), qml.sample(qml.PauliZ(1))

# Discriminator Circuit (Simple)
@qml.qnode(dev_disc)
def discriminator(weights, data):
    qml.RX(data[0], wires=0)
    qml.RY(data[1], wires=1)
    
    for w in weights:
        qml.RX(w[0], wires=0)
        qml.RY(w[1], wires=1)
        qml.CNOT(wires=[0, 1])
        
    return qml.expval(qml.PauliZ(0))

# Training loop is complex and requires careful balancing of G and D.
# Here we just define the structures.

Quantum Boltzmann Machines
# Quantum version of Restricted Boltzmann Machines (RBMs).
# Uses quantum annealing or variational circuits to sample from energy-based models.

CHAPTER 6: HYBRID ALGORITHMS
QAOA for Optimization
# Quantum Approximate Optimization Algorithm.
# Used for combinatorial optimization problems (e.g., MaxCut).
# Maps problem to Ising Hamiltonian, then finds ground state.

import pennylane as qml
from pennylane import numpy as np

# Problem: MaxCut on a graph with 3 nodes and edges (0,1), (1,2)
# Hamiltonian: H = Z0*Z1 + Z1*Z2
# We want to minimize <H>

n_wires = 3
dev = qml.device("default.qubit", wires=n_wires)

def hamiltonian():
    coeffs = [1.0, 1.0]
    obs = [qml.PauliZ(0) @ qml.PauliZ(1), qml.PauliZ(1) @ qml.PauliZ(2)]
    return qml.Hamiltonian(coeffs, obs)

H = hamiltonian()

@qml.qnode(dev)
def qaoa_circuit(gamma, beta, steps):
    # Initial state: |+>^n
    for i in range(n_wires):
        qml.Hadamard(wires=i)
        
    # QAOA layers
    for step in range(steps):
        # Problem unitary: exp(-i * gamma * H)
        qml.ApproxTimeEvolution(H, time=gamma[step], n=1)
        
        # Mixer unitary: exp(-i * beta * sum(X_i))
        for i in range(n_wires):
            qml.RX(2 * beta[step], wires=i)
            
    return qml.expval(H)

# Optimization
steps = 2
init_gamma = np.random.rand(steps)
init_beta = np.random.rand(steps)

opt = qml.GradientDescentOptimizer(stepsize=0.1)
gamma, beta = init_gamma, init_beta

for i in range(50):
    gamma, beta, energy = opt.step(qaoa_circuit, gamma, beta, steps)
    if (i+1) % 10 == 0:
        print(f"Step {i+1}: Energy = {energy:.4f}")

VQE for Chemistry
# Variational Quantum Eigensolver.
# Finds ground state energy of molecular Hamiltonians.
# Crucial for drug discovery and material science.

from pennylane import qchem

# Define molecule: H2
symbols = ["H", "H"]
coordinates = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.74]) # Angstroms
charge = 0
mult = 1

# Get Hamiltonian
hamiltonian, qubits = qchem.molecular_hamiltonian(symbols, coordinates, charge, mult)

dev = qml.device("default.qubit", wires=qubits)

# Define ansatz (e.g., UCCSD)
# For simplicity, we use a simple hardware-efficient ansatz here
@qml.qnode(dev)
def vqe_circuit(params):
    # Prepare Hartree-Fock state
    qml.BasisState(np.array([1, 1]), wires=[0, 1]) # Simplified for H2
    
    # Variational part
    for i in range(qubits):
        qml.RX(params[i], wires=i)
    qml.CNOT(wires=[0, 1])
    
    return qml.expval(hamiltonian)

# Optimize
params = np.random.rand(qubits)
opt = qml.GradientDescentOptimizer(stepsize=0.1)

for i in range(50):
    params, energy = opt.step(vqe_circuit, params)
    if (i+1) % 10 == 0:
        print(f"VQE Step {i+1}: Energy = {energy:.4f} Ha")

CHAPTER 7: BARREN PLATEAUS AND TRAINING ISSUES
Barren Plateaus
# Problem: Gradients vanish exponentially with number of qubits.
# Makes training deep quantum circuits difficult.
# Causes: Highly entangled states, random initialization.

# Mitigation strategies:
# 1. Local cost functions
# 2. Careful initialization (identity blocks)
# 3. Layer-wise training
# 4. Natural Gradient Descent

def identity_block_init(n_layers, n_wires):
    """Initialize weights to identity to avoid barren plateaus."""
    weights = np.zeros((n_layers, n_wires, 2))
    # Small random perturbation
    weights += np.random.normal(0, 0.01, weights.shape)
    return weights

Noise and Error Mitigation
# NISQ devices are noisy.
# Techniques: Zero-Noise Extrapolation, Probabilistic Error Cancellation, Readout Error Mitigation.

import pennylane as qml

# Simulate noise
dev_noise = qml.device("default.mixed", wires=2)

@qml.qnode(dev_noise)
def noisy_circuit(weights, x):
    angle_encoding(x, wires=[0, 1])
    qml.CRY(weights[0], wires=[0, 1])
    
    # Add depolarizing noise
    qml.DepolarizingChannel(0.01, wires=0)
    qml.DepolarizingChannel(0.01, wires=1)
    
    return qml.expval(qml.PauliZ(0))

# Error mitigation requires running circuits at different noise levels and extrapolating to zero noise.

CHAPTER 8: ADVANCED TOPICS AND RESOURCES
Quantum Natural Language Processing (QNLP)
# DisCoCat model: Maps grammar to quantum circuits.
# Words are states, grammar is entanglement.

Quantum Reinforcement Learning (QRL)
# Agent uses quantum policy or quantum environment.
# Potential for faster convergence in certain environments.

Federated Quantum Learning
# Distributed QML where clients train local quantum models and share updates.

Recommended Reading
# - "Quantum Machine Learning" by Maria Schuld and Francesco Petruccione
# - "Supervised Learning with Quantum Computers" by Maria Schuld
# - PennyLane Documentation: https://pennylane.ai/
# - Qiskit Textbook: https://qiskit.org/textbook/

# Online Resources
# - Xanadu Codebook: https://codebook.xanadu.ai/
# - IBM Quantum Experience: https://quantum-computing.ibm.com/

# End of Quantum Machine Learning Reference