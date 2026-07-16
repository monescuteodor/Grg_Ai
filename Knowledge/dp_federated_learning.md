Differential Privacy & Federated Learning Complete Reference
CHAPTER 1: GETTING STARTED WITH PRIVACY-PRESERVING ML
Remarks
As machine learning models are trained on sensitive data (medical records, financial transactions, user behavior), privacy becomes a critical concern. Differential Privacy (DP) provides a mathematical guarantee that the output of an algorithm does not significantly change if any single individual's data is added or removed. Federated Learning (FL) allows models to be trained across multiple decentralized devices holding local data samples, without exchanging the data itself. Combining DP and FL enables secure, private, collaborative AI.
Tools: Python, PyTorch, TensorFlow, Opacus (Facebook/Meta), TensorFlow Privacy, PySyft (OpenMined), Flower (Flwr).
Hello Differential Privacy
# hello_dp.py
"""
First DP program: Add noise to a simple count to preserve privacy.
"""
import numpy as np

def laplace_mechanism(sensitivity, epsilon):
    """Add Laplace noise to a query result."""
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale)
    return noise

def private_count(count, sensitivity=1, epsilon=0.1):
    """Return a differentially private count."""
    noise = laplace_mechanism(sensitivity, epsilon)
    return max(0, count + noise)  # Ensure non-negative

# Example
true_count = 100
private_result = private_count(true_count, epsilon=0.1)
print(f"True Count: {true_count}")
print(f"Private Count (ε=0.1): {private_result:.2f}")

# Lower epsilon = more privacy, more noise
private_result_low_privacy = private_count(true_count, epsilon=1.0)
print(f"Private Count (ε=1.0): {private_result_low_privacy:.2f}")

Hello Federated Learning
# hello_fl.py
"""
First FL program: Simulate federated averaging with two clients.
"""
import numpy as np

class SimpleModel:
    def __init__(self):
        self.weights = np.array([0.5, 0.5])
    
    def predict(self, x):
        return np.dot(x, self.weights)
    
    def update_weights(self, gradient, lr=0.1):
        self.weights -= lr * gradient

def train_local(model, data_x, data_y, epochs=1):
    """Simulate local training on client data."""
    for _ in range(epochs):
        predictions = model.predict(data_x)
        error = predictions - data_y
        gradient = np.mean(error * data_x, axis=0)
        model.update_weights(gradient)
    return model.weights

def federated_average(weights_list):
    """Average weights from multiple clients."""
    return np.mean(weights_list, axis=0)

# Server model
server_model = SimpleModel()

# Client 1 data
c1_x = np.array([[1, 2], [2, 3]])
c1_y = np.array([3, 5])
client1 = SimpleModel()
client1.weights = server_model.weights.copy()
w1 = train_local(client1, c1_x, c1_y)

# Client 2 data
c2_x = np.array([[3, 4], [4, 5]])
c2_y = np.array([7, 9])
client2 = SimpleModel()
client2.weights = server_model.weights.copy()
w2 = train_local(client2, c2_x, c2_y)

# Aggregate
new_weights = federated_average([w1, w2])
server_model.weights = new_weights

print(f"Server Weights after FL round: {server_model.weights}")

CHAPTER 2: DIFFERENTIAL PRIVACY FUNDAMENTALS
Definition of Differential Privacy
# A randomized mechanism M satisfies ε-differential privacy if:
# Pr[M(D1) ∈ S] ≤ e^ε * Pr[M(D2) ∈ S]
# for all datasets D1, D2 differing by one element, and all subsets S of outputs.

# Key parameters:
# ε (epsilon): Privacy budget. Smaller ε = stronger privacy.
# δ (delta): Probability that the privacy guarantee fails. (ε, δ)-DP.

Mechanisms
# 1. Laplace Mechanism: For numeric queries.
#    Noise ~ Laplace(0, Δf/ε)
# 2. Gaussian Mechanism: For numeric queries (allows composition).
#    Noise ~ N(0, σ²), where σ ≥ Δf * √(2 ln(1.25/δ)) / ε
# 3. Exponential Mechanism: For non-numeric outputs (selecting best candidate).

import numpy as np

def gaussian_mechanism(sensitivity, epsilon, delta):
    """Add Gaussian noise for (ε, δ)-DP."""
    sigma = sensitivity * np.sqrt(2 * np.log(1.25 / delta)) / epsilon
    noise = np.random.normal(0, sigma)
    return noise

# Example
sensitivity = 1.0
epsilon = 0.5
delta = 1e-5
noise = gaussian_mechanism(sensitivity, epsilon, delta)
print(f"Gaussian Noise: {noise:.4f}")

Composition Theorems
# Sequential Composition: If M1 is ε1-DP and M2 is ε2-DP, 
# then (M1, M2) is (ε1 + ε2)-DP.
# Parallel Composition: If datasets are disjoint, privacy budget doesn't add up.
# Advanced Composition: Allows tighter bounds for many queries.

CHAPTER 3: DP-SGD (DIFFERENTIALLY PRIVATE STOCHASTIC GRADIENT DESCENT)
Algorithm
# 1. Compute per-sample gradients.
# 2. Clip gradients to bound sensitivity (L2 norm clipping).
# 3. Add Gaussian noise to the average gradient.
# 4. Update model weights.

import torch
import torch.nn as nn
import torch.optim as optim
from opacus import PrivacyEngine

# Define a simple model
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 1)
    
    def forward(self, x):
        return self.fc(x)

model = Net()
optimizer = optim.SGD(model.parameters(), lr=0.05)
privacy_engine = PrivacyEngine()

# Attach privacy engine to optimizer
model, optimizer, data_loader = privacy_engine.make_private(
    module=model,
    optimizer=optimizer,
    data_loader=None,  # In real use, pass your DataLoader
    noise_multiplier=1.0,
    max_grad_norm=1.0,
    epsilon=1.0,
    delta=1e-5,
    epochs=10
)

print("DP-SGD setup complete.")
print(f"Privacy Budget: ε={privacy_engine.get_epsilon(delta=1e-5):.2f}")

Gradient Clipping
# Why clip? To limit the influence of any single sample.
# L2 Clipping: g_clipped = g * min(1, C / ||g||_2)
# Where C is the clipping threshold.

def clip_gradient(grad, max_norm=1.0):
    """Clip gradient to max L2 norm."""
    norm = torch.norm(grad)
    if norm > max_norm:
        grad = grad * (max_norm / norm)
    return grad

CHAPTER 4: FEDERATED LEARNING ARCHITECTURE
Federated Averaging (FedAvg)
# Algorithm:
# 1. Server initializes global model w_global.
# 2. Server selects a subset of K clients.
# 3. Each client k trains locally for E epochs on its data D_k.
# 4. Clients send updated weights w_k to server.
# 5. Server aggregates: w_global = Σ (n_k / n) * w_k.

import numpy as np

class FederatedServer:
    def __init__(self, model_weights):
        self.global_weights = model_weights
    
    def select_clients(self, num_clients, fraction=0.1):
        """Select a random subset of clients."""
        num_selected = max(1, int(num_clients * fraction))
        return np.random.choice(num_clients, num_selected, replace=False)
    
    def aggregate(self, client_weights, client_sizes):
        """Weighted average of client weights."""
        total_size = sum(client_sizes)
        avg_weights = np.zeros_like(self.global_weights)
        for w, size in zip(client_weights, client_sizes):
            avg_weights += (size / total_size) * w
        return avg_weights

class FederatedClient:
    def __init__(self, id, data, model_weights):
        self.id = id
        self.data = data
        self.local_weights = model_weights.copy()
    
    def train_local(self, epochs=1, lr=0.01):
        """Simulate local training."""
        # In real FL, this involves backpropagation on local data
        # Here we just simulate a weight update
        update = np.random.randn(*self.local_weights.shape) * 0.1
        self.local_weights += lr * update
        return self.local_weights

# Simulation
global_weights = np.array([0.5, 0.5])
server = FederatedServer(global_weights)
clients = [FederatedClient(i, None, global_weights) for i in range(10)]

# Round 1
selected_ids = server.select_clients(10, fraction=0.3)
local_weights = []
sizes = []
for cid in selected_ids:
    w = clients[cid].train_local()
    local_weights.append(w)
    sizes.append(100)  # Assume equal size

new_global = server.aggregate(local_weights, sizes)
print(f"New Global Weights: {new_global}")

Communication Efficiency
# Challenges: High latency, limited bandwidth.
# Solutions:
# 1. Compression: Quantization, Sparsification.
# 2. Local Updates: More local epochs (E) reduce communication rounds.
# 3. Federated Dropout: Train only a sub-model.

CHAPTER 5: SECURITY IN FEDERATED LEARNING
Threat Models
# 1. Honest-but-Curious Server: Follows protocol but tries to infer data.
# 2. Malicious Clients: Send poisoned updates to disrupt training.
# 3. Eavesdropper: Intercepts communication.

Attacks
# 1. Membership Inference: Determine if a specific record was in training set.
# 2. Model Inversion: Reconstruct input data from model outputs.
# 3. Poisoning Attack: Inject bad data to corrupt global model.

Defenses
# 1. Secure Aggregation (SecAgg): Cryptographic protocol so server only sees sum.
# 2. Differential Privacy: Add noise to updates.
# 3. Robust Aggregation: Median, Trimmed Mean to ignore outliers.

Secure Aggregation Concept
# Clients encrypt their updates.
# Server can decrypt only the SUM of all updates.
# Individual updates remain hidden.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Personalized Federated Learning
# Global model may not fit all clients well.
# Personalization: Fine-tune global model on local data.
# Methods: FedPer, pFedAvg, Meta-Learning (MAML).

Vertical Federated Learning
# Horizontal FL: Same features, different users (e.g., banks).
# Vertical FL: Same users, different features (e.g., bank + hospital).
# Requires entity alignment and secure multi-party computation.

Split Learning
# Split the neural network between client and server.
# Client runs first layers, sends activations to server.
# Server runs remaining layers, sends gradients back.
# Reduces client compute, but privacy risks remain.

Recommended Reading
# - "The Algorithmic Foundations of Differential Privacy" by Dwork & Roth
# - "Federated Learning: Strategies for Improving Communication Efficiency" by Konečný et al.
# - Opacus Documentation: https://opacus.ai/
# - Flower Framework: https://flower.dev/

# End of Differential Privacy & Federated Learning Reference