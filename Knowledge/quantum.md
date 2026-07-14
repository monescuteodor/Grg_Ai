Quantum Computing Complete Reference
CHAPTER 1: GETTING STARTED WITH QUANTUM COMPUTING
Remarks
Quantum computing is a model of computation that exploits quantum-mechanical phenomena—superposition, entanglement, and interference—to perform calculations that are intractable for classical computers. Unlike classical bits (0 or 1), quantum bits (qubits) exist in linear combinations of basis states. Quantum algorithms such as Shor's (factoring), Grover's (search), and VQE (chemistry) achieve exponential or quadratic speedups.
Tools: Qiskit (IBM), Cirq (Google), PennyLane (Xanadu), Q#, QuTiP, Stim (stabilizer simulation).
Hello Quantum
# hello_quantum.py
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

# Create a 1-qubit circuit
qc = QuantumCircuit(1, 1)
qc.h(0)                 # Hadamard → superposition (|0⟩ + |1⟩)/√2
qc.measure(0, 0)

# Simulate
backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend, shots=1024).result()
counts = result.get_counts()
print("Measurement outcomes:", counts)
# Expected: ~512 '0' and ~512 '1'

CHAPTER 2: LINEAR ALGEBRA FOR QUANTUM MECHANICS
State Vectors and Dirac Notation
import numpy as np

# Basis states |0⟩ and |1⟩
ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

# Superposition: |ψ⟩ = α|0⟩ + β|1⟩, with |α|² + |β|² = 1
alpha = 1 / np.sqrt(2)
beta  = 1j / np.sqrt(2)
psi = alpha * ket_0 + beta * ket_1
print("State |ψ⟩:", psi)
print("Probabilities:", np.abs(psi)**2)  # [0.5, 0.5]

# Inner product ⟨φ|ψ⟩
phi = np.array([1, 1]) / np.sqrt(2)
inner = np.vdot(phi, psi)   # conjugate-linear in first argument
print("⟨φ|ψ⟩ =", inner)

# Outer product |ψ⟩⟨φ| (density-matrix-like operator)
outer = np.outer(psi, phi.conj())
print("Outer product shape:", outer.shape)

Tensor Products and Multi-Qubit States
# Two-qubit basis: |00⟩, |01⟩, |10⟩, |11⟩
ket_00 = np.kron(ket_0, ket_0)
ket_11 = np.kron(ket_1, ket_1)

# Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
bell_phi_plus = (ket_00 + ket_11) / np.sqrt(2)
print("Bell state |Φ⁺⟩:", bell_phi_plus)

# Verify entanglement: reduced density matrix is maximally mixed
rho = np.outer(bell_phi_plus, bell_phi_plus.conj())
rho_A = np.trace(rho.reshape(2,2,2,2), axis1=1, axis2=3)
print("Reduced ρ_A (should be I/2):\n", rho_A)

Pauli Matrices and Observables
# Pauli matrices σ_x, σ_y, σ_z
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
I       = np.eye(2, dtype=complex)

# Expectation value ⟨ψ|σ_z|ψ⟩
exp_z = psi.conj().T @ sigma_z @ psi
print("⟨σ_z⟩ =", exp_z.real)

# Commutator [σ_x, σ_y] = 2i σ_z
comm = sigma_x @ sigma_y - sigma_y @ sigma_x
print("[σ_x, σ_y] == 2iσ_z?", np.allclose(comm, 2j * sigma_z))

CHAPTER 3: QUANTUM GATES AND CIRCUITS
Single-Qubit Gates
from qiskit import QuantumCircuit
import numpy as np

qc = QuantumCircuit(1)

# Pauli gates
qc.x(0)     # NOT / bit-flip: |0⟩ → |1⟩
qc.y(0)     # σ_y
qc.z(0)     # Phase flip: |1⟩ → -|1⟩

# Hadamard: creates superposition
qc.h(0)     # |0⟩ → (|0⟩+|1⟩)/√2

# Phase gates
qc.s(0)     # S = √Z, phase π/2
qc.t(0)     # T = √S, phase π/4 (universal for fault-tolerance)

# Rotation gates
qc.rx(np.pi/4, 0)   # rotation around X by π/4
qc.ry(np.pi/3, 0)   # rotation around Y
qc.rz(np.pi/6, 0)   # rotation around Z

# U3 (general single-qubit unitary)
qc.u(np.pi/2, np.pi/4, np.pi/8, 0)
print(qc.draw())

Two-Qubit Gates and Entanglement
qc2 = QuantumCircuit(2)

# CNOT (controlled-X): the entangling gate
qc2.cx(0, 1)          # control=0, target=1
# |00⟩→|00⟩, |01⟩→|01⟩, |10⟩→|11⟩, |11⟩→|10⟩

# Create Bell state
qc_bell = QuantumCircuit(2)
qc_bell.h(0)
qc_bell.cx(0, 1)
print("Bell circuit:\n", qc_bell.draw())

# CZ (controlled-Z), SWAP, iSWAP
qc2.cz(0, 1)
qc2.swap(0, 1)

# Toffoli (CCX) — 3-qubit universal classical gate
qc3 = QuantumCircuit(3)
qc3.ccx(0, 1, 2)

# Fredkin (CSWAP)
qc3.cswap(0, 1, 2)

Universal Gate Sets
# {H, T, CNOT} is universal for quantum computation
# Any n-qubit unitary can be approximated to ε using O(4ⁿ log(1/ε)) gates
# Solovay-Kitaev theorem guarantees efficient decomposition

from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller
from qiskit.circuit.library import HGate, TGate, CXGate

# Decompose arbitrary circuit into {H, T, CX}
pm = PassManager(Unroller(['h', 't', 'cx']))
# pm.run(qc) → equivalent circuit over universal basis

CHAPTER 4: GROVER'S SEARCH ALGORITHM
Theory
# Grover's algorithm finds a marked item in an unstructured database
# of N items in O(√N) queries (quadratic speedup over classical O(N))

import numpy as np
from qiskit import QuantumCircuit

def grover_oracle(n, marked_state):
    """Phase oracle: flips sign of |marked_state⟩."""
    qc = QuantumCircuit(n)
    # X gates on qubits where marked_state has 0
    for i, bit in enumerate(reversed(bin(marked_state)[2:].zfill(n))):
        if bit == '0':
            qc.x(i)
    # Multi-controlled Z = H · MCX · H
    qc.h(n-1)
    if n == 2:
        qc.cx(0, 1)
    else:
        qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    for i, bit in enumerate(reversed(bin(marked_state)[2:].zfill(n))):
        if bit == '0':
            qc.x(i)
    return qc

def diffusion_operator(n):
    """Grover diffusion: 2|s⟩⟨s| - I."""
    qc = QuantumCircuit(n)
    for i in range(n):
        qc.h(i)
        qc.x(i)
    qc.h(n-1)
    if n == 2:
        qc.cx(0, 1)
    else:
        qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    for i in range(n):
        qc.x(i)
        qc.h(i)
    return qc

def grover_search(n, marked_state):
    N = 2**n
    iterations = int(np.floor(np.pi/4 * np.sqrt(N)))
    qc = QuantumCircuit(n, n)
    # Initial superposition
    for i in range(n):
        qc.h(i)
    # Iterate
    for _ in range(iterations):
        qc.compose(grover_oracle(n, marked_state), inplace=True)
        qc.compose(diffusion_operator(n), inplace=True)
    qc.measure(range(n), range(n))
    return qc

# Search for state |101⟩ = 5 in 3-qubit space (N=8)
qc = grover_search(3, 5)
print(qc.draw())
# After ~2 iterations, measurement yields '101' with >94% probability

CHAPTER 5: SHOR'S FACTORING ALGORITHM
Overview
# Shor's algorithm factors N in O((log N)³) time — exponential speedup
# Steps:
#   1. Reduce factoring to order-finding: find r such that a^r ≡ 1 (mod N)
#   2. Use Quantum Phase Estimation (QPE) to find r
#   3. Compute gcd(a^{r/2} ± 1, N)

import numpy as np
from qiskit import QuantumCircuit
from math import gcd

def classical_order(a, N):
    """Find smallest r > 0 such that a^r ≡ 1 (mod N)."""
    r = 1
    val = a % N
    while val != 1:
        val = (val * a) % N
        r += 1
        if r > N: return None
    return r

def controlled_modular_exp(a, N, n_target):
    """Controlled-U where U|x⟩ = |a·x mod N⟩.
    Implemented via repeated controlled multiplications."""
    # Simplified: for real Shor, use reversible arithmetic circuits
    # Here we show the conceptual structure
    qc = QuantumCircuit(n_target)
    # Build modular exponentiation circuit
    # (full implementation requires ~O(n³) gates)
    return qc

def quantum_phase_estimation(U_circuit, n_counting, n_state):
    """QPE: estimates eigenvalue phase θ of U where U|u⟩ = e^{2πiθ}|u⟩."""
    qc = QuantumCircuit(n_counting + n_state, n_counting)
    # 1. Hadamard on counting register
    for i in range(n_counting):
        qc.h(i)
    # 2. Controlled-U^{2^k} operations
    for k in range(n_counting):
        # Apply controlled-U^(2^k)
        pass  # U_circuit controlled by qubit k, raised to 2^k
    # 3. Inverse QFT on counting register
    for i in range(n_counting // 2):
        qc.swap(i, n_counting - 1 - i)
    for i in range(n_counting):
        for j in range(i):
            qc.cp(-np.pi / (2**(i-j)), j, i)
        qc.h(i)
    # 4. Measure counting register
    for i in range(n_counting):
        qc.measure(i, i)
    return qc

def shor_factor(N, a=2):
    """Conceptual Shor: returns non-trivial factor of N."""
    if N % 2 == 0: return 2
    r = classical_order(a, N)
    if r % 2 != 0:
        return None  # odd order, retry with different a
    x = pow(a, r // 2, N)
    if x == N - 1:
        return None  # trivial factor
    p = gcd(x - 1, N)
    q = gcd(x + 1, N)
    return p if 1 < p < N else q

print("Factor of 15:", shor_factor(15, a=7))  # → 3 or 5

CHAPTER 6: VARIATIONAL QUANTUM EIGENSOLVER (VQE)
Hybrid Quantum-Classical Algorithm
# VQE finds the ground-state energy of a Hamiltonian H
# by minimizing ⟨ψ(θ)|H|ψ(θ)⟩ over parameters θ

import numpy as np
from qiskit import QuantumCircuit
from qiskit.opflow import PauliSumOp
from scipy.optimize import minimize

# Molecular Hamiltonian (H₂ at 0.735 Å, STO-3G basis, Jordan-Wigner)
# H = -1.05 II + 0.39 ZI - 0.39 IZ - 0.03 ZZ + 0.18 XX + 0.18 YY
H = PauliSumOp.from_list([
    ("II", -1.0523),
    ("ZI",  0.3979),
    ("IZ", -0.3979),
    ("ZZ", -0.0112),
    ("XX",  0.1809),
    ("YY",  0.1809),
])

def ansatz(theta):
    """Hardware-efficient ansatz with 2 qubits, 1 layer."""
    qc = QuantumCircuit(2)
    qc.ry(theta[0], 0)
    qc.ry(theta[1], 1)
    qc.cx(0, 1)
    qc.ry(theta[2], 0)
    qc.ry(theta[3], 1)
    return qc

def energy(theta):
    """Compute ⟨ψ(θ)|H|ψ(θ)⟩ via Pauli expectation values."""
    qc = ansatz(theta)
    E = 0.0
    for pauli, coeff in H.to_list():
        # Measure ⟨pauli⟩ by rotating basis
        meas_qc = qc.copy()
        if pauli[0] == 'X': meas_qc.h(0)
        if pauli[1] == 'X': meas_qc.h(1)
        if pauli[0] == 'Y': meas_qc.sdg(0); meas_qc.h(0)
        if pauli[1] == 'Y': meas_qc.sdg(1); meas_qc.h(1)
        meas_qc.measure_all()
        # Simulate
        from qiskit import Aer, execute
        result = execute(meas_qc, Aer.get_backend('qasm_simulator'),
                        shots=8192).result()
        counts = result.get_counts()
        # Compute expectation from parity
        exp = 0.0
        for bitstring, count in counts.items():
            bits = bitstring.replace(' ', '')
            parity = bits.count('1') % 2
            exp += ((-1)**parity) * count / 8192
        E += coeff * exp
    return E

# Optimize
theta0 = np.random.uniform(0, 2*np.pi, 4)
result = minimize(energy, theta0, method='COBYLA',
                 options={'maxiter': 100})
print("Ground-state energy:", result.fun)
print("Exact (full diag):", -1.8573)  # reference

CHAPTER 7: QUANTUM ERROR CORRECTION
The 3-Qubit Bit-Flip Code
from qiskit import QuantumCircuit

def encode_bit_flip(qc, data=0, ancilla_start=1):
    """Encode |ψ⟩ = α|0⟩+β|1⟩ into α|000⟩+β|111⟩."""
    qc.cx(data, ancilla_start)
    qc.cx(data, ancilla_start + 1)

def detect_bit_flip(qc, data_start=0, syndrome_start=3):
    """Measure syndromes to locate single bit-flip error."""
    # Syndrome 1: compare qubits 0 and 1
    qc.cx(data_start, syndrome_start)
    qc.cx(data_start + 1, syndrome_start)
    # Syndrome 2: compare qubits 1 and 2
    qc.cx(data_start + 1, syndrome_start + 1)
    qc.cx(data_start + 2, syndrome_start + 1)

def correct_bit_flip(qc, data_start=0, syndrome_start=3):
    """Apply correction based on syndrome (classical feed-forward)."""
    # Syndrome 00: no error
    # Syndrome 01: error on qubit 2
    # Syndrome 10: error on qubit 0
    # Syndrome 11: error on qubit 1
    # Implemented via conditional X gates (requires measurement first)
    pass

# Full circuit
qc = QuantumCircuit(5, 2)
# Prepare state to encode
qc.h(0)
# Encode
encode_bit_flip(qc, 0, 1)
# Simulate error: bit-flip on qubit 1
qc.x(1)
# Detect
detect_bit_flip(qc, 0, 3)
# Measure syndromes
qc.measure(3, 0)
qc.measure(4, 1)
print(qc.draw())

The 9-Qubit Shor Code
# Combines bit-flip and phase-flip correction
# Encodes 1 logical qubit into 9 physical qubits
# Distance d=3: corrects any single-qubit error

# Logical |0⟩_L = (|000⟩+|111⟩)⊗³ / 2√2
# Logical |1⟩_L = (|000⟩-|111⟩)⊗³ / 2√2

def shor_encode(qc, data=0):
    """Encode into 9-qubit Shor code."""
    ancillas = list(range(1, 9))
    # Phase-flip encoding (3 blocks)
    for block in range(3):
        base = block * 3
        qc.h(data if block == 0 else ancillas[base-1])
        for i in range(1, 3):
            qc.cx(data if block == 0 and i == 1 else ancillas[base+i-2],
                 ancillas[base+i-1] if not (block==0 and i==1) else data)
    # Bit-flip encoding within each block
    for block in range(3):
        base = block * 3
        qc.cx(base, base + 1)
        qc.cx(base, base + 2)

Surface Codes (Topological QEC)
# Surface code: 2D lattice of data and ancilla qubits
# Threshold error rate ~1%
# Logical error rate scales as (p/p_th)^{(d+1)/2}
# d = code distance (odd integer)
# Requires O(d²) physical qubits per logical qubit

# Stabilizers:
# - X-stabilizers (plaquettes): 4-body XX XX measurements
# - Z-stabilizers (stars): 4-body ZZ ZZ measurements
# Syndrome extraction via ancilla measurements

CHAPTER 8: QUANTUM KEY DISTRIBUTION (BB84)
from qiskit import QuantumCircuit, Aer, execute
import numpy as np

def bb84_protocol(n_bits=100):
    """Simulate BB84 QKD protocol."""
    np.random.seed(42)
    # Alice's random bits and bases
    alice_bits  = np.random.randint(0, 2, n_bits)
    alice_bases = np.random.randint(0, 2, n_bits)  # 0=Z, 1=X

    # Prepare and send qubits
    sent_states = []
    for b, basis in zip(alice_bits, alice_bases):
        qc = QuantumCircuit(1)
        if b == 1:
            qc.x(0)
        if basis == 1:  # X basis
            qc.h(0)
        sent_states.append(qc)

    # Eve's eavesdropping (intercept-resend attack)
    eve_bases = np.random.randint(0, 2, n_bits)
    eve_measured_bits = []
    eve_resend = []
    for qc, eve_basis in zip(sent_states, eve_bases):
        meas_qc = qc.copy()
        if eve_basis == 1:
            meas_qc.h(0)
        meas_qc.measure_all()
        result = execute(meas_qc, Aer.get_backend('qasm_simulator'),
                        shots=1).result()
        bit = int(list(result.get_counts().keys())[0])
        eve_measured_bits.append(bit)
        # Eve resends in her basis
        resend = QuantumCircuit(1)
        if bit == 1:
            resend.x(0)
        if eve_basis == 1:
            resend.h(0)
        eve_resend.append(resend)

    # Bob measures in random bases
    bob_bases = np.random.randint(0, 2, n_bits)
    bob_bits = []
    for qc, bob_basis in zip(eve_resend, bob_bases):
        meas_qc = qc.copy()
        if bob_basis == 1:
            meas_qc.h(0)
        meas_qc.measure_all()
        result = execute(meas_qc, Aer.get_backend('qasm_simulator'),
                        shots=1).result()
        bit = int(list(result.get_counts().keys())[0])
        bob_bits.append(bit)

    # Sifting: keep only bits where Alice and Bob used same basis
    sifted_alice, sifted_bob = [], []
    for i in range(n_bits):
        if alice_bases[i] == bob_bases[i]:
            sifted_alice.append(alice_bits[i])
            sifted_bob.append(bob_bits[i])

    # Error rate (due to Eve)
    errors = sum(1 for a, b in zip(sifted_alice, sifted_bob) if a != b)
    error_rate = errors / len(sifted_alice) if sifted_alice else 0

    print(f"Sifted key length: {len(sifted_alice)}")
    print(f"Error rate (Eve detected): {error_rate:.2%}")
    if error_rate > 0.11:  # ~11% threshold for BB84
        print("⚠ Eavesdropping detected! Abort.")
    else:
        print("✓ Key secure. First 10 bits:", sifted_alice[:10])
    return sifted_alice, sifted_bob

bb84_protocol(200)

CHAPTER 9: QUANTUM MACHINE LEARNING
Quantum Neural Networks with PennyLane
import pennylane as qml
from pennylane import numpy as np

# Quantum device: 4 qubits, analytic mode
dev = qml.device("default.qubit", wires=4)

@qml.qnode(dev)
def quantum_layer(inputs, weights):
    """Single quantum layer: angle encoding + variational rotations + entanglement."""
    # Encode classical data
    for i in range(4):
        qml.RX(inputs[i], wires=i)
    # Variational block
    for i in range(4):
        qml.RY(weights[i, 0], wires=i)
        qml.RZ(weights[i, 1], wires=i)
    # Entanglement (circular)
    for i in range(4):
        qml.CNOT(wires=[i, (i+1) % 4])
    # Measurement
    return [qml.expval(qml.PauliZ(i)) for i in range(4)]

def quantum_model(inputs, all_weights):
    """Stack multiple quantum layers."""
    x = inputs
    for weights in all_weights:
        x = quantum_layer(x, weights)
    return np.array(x)

# Random dataset: 4D inputs, binary labels
np.random.seed(0)
X_data = np.random.randn(50, 4)
Y_data = np.random.randint(0, 2, 50)

# Training
n_layers = 3
weights = np.random.randn(n_layers, 4, 2, requires_grad=True)
opt = qml.AdamOptimizer(stepsize=0.1)

for epoch in range(20):
    for x, y in zip(X_data, Y_data):
        def cost(w):
            pred = quantum_model(x, w)
            # Binary cross-entropy-like loss
            target = 2*y - 1  # map {0,1} → {-1,+1}
            return -target * pred[0]
        weights, loss = opt.step_and_cost(cost, weights)
    if (epoch+1) % 5 == 0:
        print(f"Epoch {epoch+1}, loss: {loss:.4f}")

Quantum Kernel Methods
from sklearn.svm import SVC
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

# Quantum kernel: K(x, x') = |⟨φ(x)|φ(x')⟩|²
def quantum_kernel(x1, x2):
    """Fidelity kernel via quantum circuit."""
    @qml.qnode(dev)
    def circuit():
        for i in range(4):
            qml.RX(x1[i], wires=i)
            qml.RY(x1[i]**2, wires=i)
        for i in range(4):
            qml.RX(-x2[i], wires=i)
            qml.RY(-x2[i]**2, wires=i)
        return qml.probs(wires=range(4))
    probs = circuit()
    # Fidelity = |⟨0|U†(x2)U(x1)|0⟩|²
    return probs[0]  # probability of |0000⟩

# Build kernel matrix
X, y = make_moons(100, noise=0.1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Pad to 4 features
def pad(x):
    return np.array([x[0], x[1], 0.0, 0.0])

K_train = np.array([[quantum_kernel(pad(xi), pad(xj))
                    for xi in X_train] for xj in X_train])
K_test  = np.array([[quantum_kernel(pad(xi), pad(xj))
                    for xi in X_train] for xj in X_test])

svm = SVC(kernel='precomputed', C=1.0)
svm.fit(K_train, y_train)
print("QKM accuracy:", svm.score(K_test, y_test))

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Quantum Supremacy and Complexity
# BQP (Bounded-error Quantum Polynomial time):
#   class of problems efficiently solvable by quantum computers
# BPP ⊆ BQP ⊆ PSPACE
# Believed: BQP ⊄ BPP (quantum > classical)
# Factoring ∈ BQP (Shor), but factoring ∉ P (believed)

# Quantum supremacy experiments:
# - Google Sycamore (2019): random circuit sampling, 53 qubits
# - Jiuzhang (2020): Gaussian boson sampling, 76 photons
# These demonstrate tasks intractable for classical supercomputers

Hardware Platforms (2026 State-of-the-Art)
# Superconducting (IBM, Google): ~1000+ qubits, coherence ~100μs
# Trapped ions (Quantinuum, IonQ): ~50 qubits, all-to-all connectivity
# Photonic (PsiQuantum, Xanadu): room-temperature, boson sampling
# Neutral atoms (QuEra, Pasqal): 256+ qubits, Rydberg blockade
# Topological (Microsoft): Majorana-based, fault-tolerant by design

Recommended Reading
# - Nielsen & Chuang: "Quantum Computation and Quantum Information"
# - Preskill's lecture notes: http://www.theory.caltech.edu/~preskill/ph219/
# - Qiskit Textbook: https://qiskit.org/learn
# - "Quantum Computer Science" by N. David Mermin
# - arXiv quant-ph for cutting-edge research

# End of Quantum Computing Reference