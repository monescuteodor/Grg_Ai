Computational Neuroscience Complete Reference
CHAPTER 1: GETTING STARTED WITH COMPUTATIONAL NEUROSCIENCE
Remarks
Computational Neuroscience uses mathematical models, computer simulations, and theoretical analysis to understand the principles governing the development, structure, physiology, and cognitive abilities of the nervous system. Key areas: Single neuron modeling (Hodgkin-Huxley, Integrate-and-Fire), Neural coding, Synaptic plasticity, Network dynamics, Brain-Computer Interfaces (BCI).
Tools: Python (NumPy, SciPy, Brian2, Neuron, NEST), MATLAB, GENESIS.
Hello Computational Neuroscience
# hello_neuro.py
"""
First neuro program: Simulate a Leaky Integrate-and-Fire (LIF) neuron.
"""
import numpy as np
import matplotlib.pyplot as plt

def simulate_lif_neuron(I_ext=1.5, tau_m=20.0, v_rest=-70.0, v_th=-55.0, v_reset=-70.0, dt=0.1, duration=100):
    """
    Simulate a LIF neuron receiving constant current.
    
    I_ext: External input current (nA)
    tau_m: Membrane time constant (ms)
    v_rest: Resting potential (mV)
    v_th: Threshold potential (mV)
    v_reset: Reset potential after spike (mV)
    dt: Time step (ms)
    duration: Simulation duration (ms)
    """
    t = np.arange(0, duration, dt)
    v = np.zeros_like(t)
    v[0] = v_rest
    spikes = []
    
    for i in range(1, len(t)):
        # Differential equation: tau_m * dv/dt = -(v - v_rest) + R*I
        # Simplified: dv = (-(v - v_rest) + I_ext) * (dt / tau_m)
        # Assuming R=1 for simplicity
        dv = (-(v[i-1] - v_rest) + I_ext) * (dt / tau_m)
        v[i] = v[i-1] + dv
        
        if v[i] >= v_th:
            spikes.append(t[i])
            v[i] = v_reset
            
    return t, v, spikes

# Simulation
t, v, spikes = simulate_lif_neuron(I_ext=1.5)

plt.figure(figsize=(12, 4))
plt.plot(t, v, label='Membrane Potential')
plt.axhline(-55, color='r', linestyle='--', label='Threshold')
plt.axhline(-70, color='k', linestyle=':', label='Rest/Reset')
for s in spikes:
    plt.axvline(s, color='g', alpha=0.3)
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
plt.title('Leaky Integrate-and-Fire Neuron')
plt.legend()
plt.grid(True)
plt.show()

print(f"Number of spikes: {len(spikes)}")
print(f"Firing rate: {len(spikes) / (max(t)/1000):.2f} Hz")

Neural Coding
# Rate Coding: Information encoded in firing frequency.
# Temporal Coding: Information encoded in precise spike timing.
# Population Coding: Information distributed across many neurons.

CHAPTER 2: SINGLE NEURON MODELS
Hodgkin-Huxley Model
# Biophysically accurate model of action potential generation.
# Uses voltage-gated Na+ and K+ channels.
# Four differential equations: V, m, h, n.

def hodgkin_huxley(I_ext=10.0, duration=50.0, dt=0.01):
    """Simulate Hodgkin-Huxley neuron."""
    # Parameters
    C_m = 1.0     # uF/cm^2
    g_Na = 120.0  # mS/cm^2
    g_K = 36.0    # mS/cm^2
    g_L = 0.3     # mS/cm^2
    E_Na = 50.0   # mV
    E_K = -77.0   # mV
    E_L = -54.387 # mV
    
    t = np.arange(0, duration, dt)
    V = np.zeros_like(t)
    m = np.zeros_like(t)
    h = np.zeros_like(t)
    n = np.zeros_like(t)
    
    # Initial conditions
    V[0] = -65.0
    m[0] = 0.05
    h[0] = 0.60
    n[0] = 0.32
    
    def alpha_m(v): return 0.1 * (v + 40) / (1 - np.exp(-(v + 40) / 10))
    def beta_m(v): return 4.0 * np.exp(-(v + 65) / 18)
    def alpha_h(v): return 0.07 * np.exp(-(v + 65) / 20)
    def beta_h(v): return 1.0 / (1 + np.exp(-(v + 35) / 10))
    def alpha_n(v): return 0.01 * (v + 55) / (1 - np.exp(-(v + 55) / 10))
    def beta_n(v): return 0.125 * np.exp(-(v + 65) / 80)
    
    for i in range(len(t) - 1):
        v = V[i]
        
        # Update gating variables
        dm = (alpha_m(v) * (1 - m[i]) - beta_m(v) * m[i]) * dt
        dh = (alpha_h(v) * (1 - h[i]) - beta_h(v) * h[i]) * dt
        dn = (alpha_n(v) * (1 - n[i]) - beta_n(v) * n[i]) * dt
        
        m[i+1] = m[i] + dm
        h[i+1] = h[i] + dh
        n[i+1] = n[i] + dn
        
        # Conductances
        g_na = g_Na * m[i+1]**3 * h[i+1]
        g_k = g_K * n[i+1]**4
        
        # Currents
        I_Na = g_na * (v - E_Na)
        I_K = g_k * (v - E_K)
        I_L = g_L * (v - E_L)
        
        # Update Voltage
        dV = (I_ext - I_Na - I_K - I_L) / C_m * dt
        V[i+1] = v + dV
        
    return t, V

t, V = hodgkin_huxley(I_ext=10.0)
plt.figure(figsize=(10, 4))
plt.plot(t, V)
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
plt.title('Hodgkin-Huxley Action Potential')
plt.grid(True)
plt.show()

Integrate-and-Fire Variants
# 1. LIF (Leaky): Standard linear leak.
# 2. QIF (Quadratic): Non-linear leak, captures spike initiation better.
# 3. EIF (Exponential): Exponential leak, captures sharp spike onset.
# 4. AdEx (Adaptive Exponential): Includes adaptation current for spike frequency adaptation.

CHAPTER 3: SYNAPTIC PLASTICITY
Hebbian Learning Rule
# "Cells that fire together, wire together."
# Delta w = eta * pre_spike * post_spike

def hebbian_update(w, pre_spike, post_spike, eta=0.01, w_max=1.0):
    dw = eta * pre_spike * post_spike
    return min(w + dw, w_max)

Spike-Timing-Dependent Plasticity (STDP)
# Weight change depends on relative timing of pre- and post-synaptic spikes.
# Pre before Post -> Potentiation (LTP)
# Post before Pre -> Depression (LTD)

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
print(f"STDP Update (LTP): {w} -> {w_new:.4f}")

t_post_2 = 8 # Post fires 2ms before Pre
w_new_2 = stdp_update(w, t_pre, t_post_2)
print(f"STDP Update (LTD): {w} -> {w_new_2:.4f}")

Oja's Rule
# Normalized Hebbian learning.
# Prevents weights from growing infinitely.
# Delta w = eta * y * (x - y * w)

CHAPTER 4: NEURAL NETWORK DYNAMICS
Hopfield Networks
# Recurrent network with symmetric weights.
# Acts as content-addressable memory.
# Energy function decreases over time until stable state.

class HopfieldNetwork:
    def __init__(self, n_neurons):
        self.n = n_neurons
        self.weights = np.zeros((n_neurons, n_neurons))
        
    def train(self, patterns):
        """Store patterns using Hebbian rule."""
        for p in patterns:
            p_vec = np.array(p)
            # Outer product
            self.weights += np.outer(p_vec, p_vec)
        # Zero diagonal
        np.fill_diagonal(self.weights, 0)
        self.weights /= len(patterns)
        
    def recall(self, initial_state, steps=10):
        """Recall pattern from noisy initial state."""
        state = np.array(initial_state)
        for _ in range(steps):
            # Update all neurons synchronously
            h = self.weights @ state
            state = np.sign(h)
        return state

# Example
patterns = [
    [1, 1, -1, -1],
    [-1, -1, 1, 1]
]
net = HopfieldNetwork(4)
net.train(patterns)

noisy_input = [1, -1, -1, -1] # Noisy version of first pattern
recalled = net.recall(noisy_input)
print(f"Noisy Input: {noisy_input}")
print(f"Recalled:    {recalled}")

Wilson-Cowan Model
# Mean-field model of excitatory and inhibitory populations.
# Describes oscillations, bistability, and wave propagation.

def wilson_cowan(E0=0.1, I0=0.1, tau_E=10.0, tau_I=10.0, w_EE=10.0, w_EI=10.0, w_IE=10.0, w_II=10.0, duration=100.0, dt=0.1):
    t = np.arange(0, duration, dt)
    E = np.zeros_like(t)
    I = np.zeros_like(t)
    
    E[0] = E0
    I[0] = I0
    
    def sigmoid(x): return 1.0 / (1.0 + np.exp(-x))
    
    for i in range(len(t) - 1):
        dE = (-E[i] + sigmoid(w_EE * E[i] - w_EI * I[i])) / tau_E * dt
        dI = (-I[i] + sigmoid(w_IE * E[i] - w_II * I[i])) / tau_I * dt
        
        E[i+1] = E[i] + dE
        I[i+1] = I[i] + dI
        
    return t, E, I

t, E, I = wilson_cowan()
plt.figure(figsize=(10, 4))
plt.plot(t, E, label='Excitatory')
plt.plot(t, I, label='Inhibitory')
plt.xlabel('Time')
plt.ylabel('Activity')
plt.title('Wilson-Cowan Oscillations')
plt.legend()
plt.grid(True)
plt.show()

CHAPTER 5: BRAIN-COMPUTER INTERFACES (BCI)
Signal Processing for EEG
# EEG signals are noisy and non-stationary.
# Preprocessing: Filtering (Bandpass 0.5-40 Hz), Artifact Removal (ICA), Feature Extraction.

def bandpass_filter(signal, lowcut, highcut, fs, order=5):
    """Simple Butterworth bandpass filter."""
    from scipy.signal import butter, filtfilt
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)

# Example: Extract Alpha Band (8-12 Hz)
fs = 256 # Sampling frequency
t_eeg = np.linspace(0, 10, 10*fs)
eeg_signal = np.random.randn(len(t_eeg)) # Noise
alpha_component = 0.5 * np.sin(2 * np.pi * 10 * t_eeg) # 10 Hz alpha
mixed_signal = eeg_signal + alpha_component

filtered_alpha = bandpass_filter(mixed_signal, 8, 12, fs)

plt.figure(figsize=(10, 4))
plt.plot(t_eeg[:500], mixed_signal[:500], label='Raw EEG')
plt.plot(t_eeg[:500], filtered_alpha[:500], label='Alpha Band (8-12 Hz)')
plt.legend()
plt.title('EEG Alpha Band Extraction')
plt.show()

Common Spatial Patterns (CSP)
# Spatial filtering technique to maximize variance difference between classes.
# Used in Motor Imagery BCIs.

Classification Algorithms
# LDA (Linear Discriminant Analysis): Simple, fast, effective for CSP features.
# SVM (Support Vector Machine): Robust to high-dimensional data.
# CNN (Convolutional Neural Networks): End-to-end learning from raw EEG.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Connectomics
# Mapping neural connections at scale.
# Graph theory applied to brain networks.
# Small-world properties, hub nodes.

Neuromorphic Computing
# Hardware implementation of spiking neural networks.
# Low power, event-driven processing.
# Intel Loihi, IBM TrueNorth.

Whole-Brain Simulation
# Projects like Blue Brain Project.
# Simulating millions of neurons with biophysical detail.
# Challenges: Computational cost, parameter tuning.

Recommended Reading
# - "Theoretical Neuroscience" by Dayan and Abbott
# - "Neuronal Dynamics" by Gerstner et al.
# - "Spiking Neuron Models" by Gerstner and Kistler
# - Brian2 Documentation: https://brian2.readthedocs.io/
# - NEURON Simulator: https://neuron.yale.edu/

# End of Computational Neuroscience Reference