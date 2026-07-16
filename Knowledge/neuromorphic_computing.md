Neuromorphic Computing & Spiking Neural Networks Complete Reference
CHAPTER 1: GETTING STARTED WITH NEUROMORPHIC COMPUTING
Remarks
Neuromorphic computing mimics the structure and function of the biological brain using specialized hardware (neuromorphic chips) and algorithms (Spiking Neural Networks - SNNs). Unlike traditional von Neumann architectures, neuromorphic systems are event-driven, massively parallel, and energy-efficient. Key concepts: Spikes, Leaky Integrate-and-Fire (LIF) neurons, Synaptic Plasticity (STDP), Event-based vision. Applications: Low-power edge AI, robotics, real-time sensory processing, brain-machine interfaces.
Tools: Python, Brian2 (simulator), NEST (simulator), PyTorch (with snnTorch or Norse), Intel Loihi SDK, SpiNNaker tools.
Hello Neuromorphic
# hello_neuromorphic.py
"""
First neuromorphic program: Simulate a single LIF neuron receiving input.
"""
import numpy as np
import matplotlib.pyplot as plt

class LIFNeuron:
    """Leaky Integrate-and-Fire Neuron model."""
    def __init__(self, tau_m=20.0, v_th=1.0, v_reset=0.0, r_mem=1.0):
        self.tau_m = tau_m      # Membrane time constant (ms)
        self.v_th = v_th        # Threshold voltage
        self.v_reset = v_reset  # Reset voltage
        self.r_mem = r_mem      # Membrane resistance
        self.v = v_reset        # Current membrane potential
        self.spike_times = []   # Record spike times
        
    def step(self, i_input, dt=1.0):
        """
        Update neuron state for one time step.
        i_input: Input current
        dt: Time step (ms)
        Returns: 1 if spiked, 0 otherwise
        """
        # Differential equation: tau_m * dv/dt = -(v - v_reset) + R * I
        # Euler method approximation
        dv = (-(self.v - self.v_reset) + self.r_mem * i_input) * (dt / self.tau_m)
        self.v += dv
        
        spiked = 0
        if self.v >= self.v_th:
            self.v = self.v_reset
            spiked = 1
            self.spike_times.append(len(self.spike_times)) # Simplified time tracking
            
        return spiked

# Simulation
dt = 1.0
duration = 100
neuron = LIFNeuron(tau_m=20.0, v_th=1.0)

# Input current: Step function
i_input = np.zeros(duration)
i_input[20:80] = 0.08 # Inject current from t=20 to t=80

v_record = []
spike_record = []

for t in range(duration):
    spike = neuron.step(i_input[t], dt)
    v_record.append(neuron.v)
    spike_record.append(spike)

# Plot
fig, ax1 = plt.subplots()
ax1.plot(v_record, label='Membrane Potential (V)')
ax1.axhline(1.0, color='r', linestyle='--', label='Threshold')
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Voltage')
ax1.legend(loc='upper left')

ax2 = ax1.twinx()
ax2.eventplot([np.where(spike_record)[0]], colors='black', lineoffsets=1.5, linelengths=0.5)
ax2.set_yticks([])
ax2.set_title('LIF Neuron Response to Step Current')
plt.show()

Biological Inspiration
# 1. Neurons communicate via discrete spikes (action potentials), not continuous values.
# 2. Information is encoded in spike timing (temporal coding) or rate (rate coding).
# 3. Synapses change strength based on activity (Plasticity).
# 4. Massive parallelism and low power consumption.

CHAPTER 2: SPIKING NEURAL NETWORKS (SNNs)
Neuron Models
# 1. Leaky Integrate-and-Fire (LIF): Most common, computationally efficient.
# 2. Integrate-and-Fire (IF): No leak, simpler.
# 3. Hodgkin-Huxley: Biologically accurate, complex.
# 4. Izhikevich: Balance between accuracy and efficiency.

import numpy as np

def lif_update(v, i_input, tau_m, v_th, v_reset, dt):
    dv = (-(v - v_reset) + i_input) * (dt / tau_m)
    v_new = v + dv
    spike = 0
    if v_new >= v_th:
        v_new = v_reset
        spike = 1
    return v_new, spike

Synapse Models
# Static Synapse: Fixed weight.
# Dynamic Synapse: Short-term plasticity (facilitation/depression).

def static_synapse(pre_spike, weight):
    """Generate post-synaptic current."""
    if pre_spike:
        return weight
    else:
        return 0.0

Coding Schemes
# 1. Rate Coding: Frequency of spikes represents intensity.
# 2. Temporal Coding: Precise timing of spikes carries information.
# 3. Population Coding: Distributed representation across many neurons.

def poisson_encoder(rate, duration, dt=1.0):
    """Convert input value to spike train using Poisson process."""
    probs = np.clip(rate * dt, 0, 1)
    spikes = np.random.rand(int(duration/dt)) < probs
    return spikes.astype(int)

# Example
input_val = 50.0 # Hz
spikes = poisson_encoder(input_val/1000.0, 100) # Normalize rate
print(f"Input Rate: {input_val} Hz")
print(f"Generated Spikes: {np.sum(spikes)}")

CHAPTER 3: LEARNING RULES
Hebbian Learning
# "Cells that fire together, wire together."
# Delta w = eta * pre_spike * post_spike

def hebbian_update(w, pre_spike, post_spike, eta=0.01, w_max=1.0):
    dw = eta * pre_spike * post_spike
    w_new = min(w + dw, w_max)
    return w_new

Spike-Timing-Dependent Plasticity (STDP)
# Weight change depends on the relative timing of pre- and post-synaptic spikes.
# If Pre fires before Post -> Potentiation (LTP)
# If Post fires before Pre -> Depression (LTD)

def stdp_update(w, t_pre, t_post, eta_plus=0.01, eta_minus=0.012, tau_stdp=20.0):
    if t_pre is None or t_post is None:
        return w
    
    dt = t_pre - t_post
    
    if dt > 0: # Pre before Post
        dw = eta_plus * np.exp(-dt / tau_stdp)
    elif dt < 0: # Post before Pre
        dw = -eta_minus * np.exp(dt / tau_stdp)
    else:
        dw = 0
        
    return np.clip(w + dw, 0, 1.0)

# Example
w = 0.5
t_pre = 10
t_post = 12 # Post fires 2ms after Pre
w_new = stdp_update(w, t_pre, t_post)
print(f"STDP Update: {w} -> {w_new:.4f} (Potentiation)")

t_post_2 = 8 # Post fires 2ms before Pre
w_new_2 = stdp_update(w, t_pre, t_post_2)
print(f"STDP Update: {w} -> {w_new_2:.4f} (Depression)")

Supervised Learning in SNNs
# 1. SpikeProp: Gradient descent for spike times.
# 2. Surrogate Gradients: Approximate derivative of spike function for backpropagation.
# 3. Conversion: Train ANN, convert weights to SNN.

import torch
import torch.nn as nn

class SurrogateSpike(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        return (input > 0).float()
    
    @staticmethod
    def backward(ctx, grad_output):
        input, = ctx.saved_tensors
        # Approximate derivative using sigmoid or triangular function
        grad_input = grad_output * torch.exp(-input**2) # Gaussian surrogate
        return grad_input

class SNNLayer(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.fc = nn.Linear(input_size, output_size, bias=False)
        
    def forward(self, x):
        # x is spike train (T, B, N)
        v = torch.zeros_like(x[0]) # Initial membrane potential
        spikes_out = []
        
        for t in range(x.shape[0]):
            i_input = self.fc(x[t])
            v = v + i_input - v * 0.1 # Leak
            spike = SurrogateSpike.apply(v - 1.0) # Threshold at 1.0
            v = v * (1 - spike) # Reset
            spikes_out.append(spike)
            
        return torch.stack(spikes_out)

CHAPTER 4: NEUROMORPHIC HARDWARE
Intel Loihi
# Asynchronous, event-driven architecture.
# On-chip learning capabilities.
# Used for: Robotics, sensory processing.

IBM TrueNorth
# Digital neuromorphic chip.
# 1 million neurons, 256 million synapses.
# Low power consumption.

SpiNNaker (University of Manchester)
# Massively parallel multi-core system.
# Uses ARM cores to simulate neurons.
# Scalable to millions of neurons.

BrainScaleS (Heidelberg)
# Mixed-signal (analog/digital) wafer-scale system.
# Accelerated time scale (1000x faster than real-time).

Comparison with GPUs/TPUs
# Feature       | GPU/TPU          | Neuromorphic Chip
# --------------|------------------|-------------------
# Architecture  | Von Neumann      | Event-driven
# Clock         | Synchronous      | Asynchronous
# Power         | High             | Ultra-low
# Precision     | FP16/FP32        | Binary/Integer
# Best For      | Training Large Models | Inference, Edge AI

CHAPTER 5: APPLICATIONS
Event-Based Vision
# Dynamic Vision Sensors (DVS) output spikes only when pixel intensity changes.
# Benefits: High temporal resolution, low latency, low data bandwidth.
# Applications: Object tracking, gesture recognition, autonomous driving.

import numpy as np

def simulate_dvs_frame(prev_frame, curr_frame, threshold=0.1):
    """Generate events from two consecutive frames."""
    diff = curr_frame - prev_frame
    pos_events = diff > threshold
    neg_events = diff < -threshold
    
    events = []
    y_coords, x_coords = np.where(pos_events | neg_events)
    
    for y, x in zip(y_coords, x_coords):
        polarity = 1 if pos_events[y, x] else -1
        events.append((x, y, polarity))
        
    return events

# Example
prev = np.random.rand(10, 10)
curr = prev.copy()
curr[5, 5] += 0.5 # Change one pixel
events = simulate_dvs_frame(prev, curr)
print(f"DVS Events: {events}")

Robotic Control
# SNNs for motor control due to low latency and energy efficiency.
# Reinforcement learning with SNN agents.

Brain-Machine Interfaces (BMI)
# Decoding neural signals for prosthetic control.
# Encoding sensory feedback into spike trains.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Deep Spiking Neural Networks
# Multi-layer SNNs with convolutional layers.
# Frameworks: snnTorch, Norse, SpykeTorch.

Reservoir Computing
# Liquid State Machines (LSM): Fixed random recurrent network, trainable readout.
# Efficient for temporal pattern recognition.

Recommended Reading
# - "Spiking Neural Networks" by Wolfgang Maass
# - "Neuromorphic Engineering" by Giacomo Indiveri
# - Papers from Conference on Neural Information Processing Systems (NeurIPS)
# - Intel Loihi Research: https://www.intel.com/content/www/us/en/research/neuromorphic.html

# Online Resources
# - Brian2 Simulator: https://brian2.readthedocs.io/
# - NEST Simulator: https://www.nest-simulator.org/
# - snnTorch: https://snntorch.readthedocs.io/

# End of Neuromorphic Computing Reference