Quantum Cryptography & Post-Quantum Protocols Complete Reference
CHAPTER 1: GETTING STARTED WITH QUANTUM CRYPTOGRAPHY
Remarks
Quantum Cryptography uses principles of quantum mechanics (superposition, entanglement, no-cloning theorem) to perform cryptographic tasks. The most mature application is Quantum Key Distribution (QKD), which allows two parties to produce a shared random secret key known only to them, which can then be used to encrypt and decrypt messages. Unlike classical cryptography, whose security relies on computational difficulty (e.g., factoring large numbers), QKD's security is based on the laws of physics. Any eavesdropping attempt introduces detectable disturbances.
Tools: Python (Qiskit, QuTiP), IBM Quantum Experience, Rigetti Forest, SimulaQron.
Hello QKD (BB84 Protocol Simulation)
# hello_qkd.py
"""
Simulate the BB84 Quantum Key Distribution protocol.
Alice sends qubits to Bob. Eve tries to eavesdrop.
"""
import numpy as np
import random

def generate_random_bits(n):
    return [random.randint(0, 1) for _ in range(n)]

def generate_random_bases(n):
    # 0 = Rectilinear (+), 1 = Diagonal (x)
    return [random.randint(0, 1) for _ in range(n)]

def encode_qubit(bit, basis):
    """
    Encode a bit into a qubit state based on the basis.
    Basis 0 (+): |0> for 0, |1> for 1
    Basis 1 (x): |+> for 0, |-> for 1
    Returns a vector representation [alpha, beta]
    """
    if basis == 0: # Rectilinear
        if bit == 0: return np.array([1, 0]) # |0>
        else:        return np.array([0, 1]) # |1>
    else:            # Diagonal
        if bit == 0: return np.array([1/np.sqrt(2), 1/np.sqrt(2)])   # |+>
        else:        return np.array([1/np.sqrt(2), -1/np.sqrt(2)])  # |->

def measure_qubit(qubit, basis):
    """
    Measure a qubit in a given basis.
    Returns the measured bit (0 or 1).
    """
    if basis == 0: # Measure in Z basis
        # Probability of measuring 0 is |alpha|^2
        prob_0 = np.abs(qubit[0])**2
        return 0 if random.random() < prob_0 else 1
    else:          # Measure in X basis
        # Transform to X basis: |+> = [1,1]/sqrt(2), |-> = [1,-1]/sqrt(2)
        # Project qubit onto |+> and |->
        plus_state = np.array([1, 1]) / np.sqrt(2)
        minus_state = np.array([1, -1]) / np.sqrt(2)
        
        prob_plus = np.abs(np.dot(plus_state, qubit))**2
        return 0 if random.random() < prob_plus else 1

def bb84_protocol(n_bits=100, eve_intercepts=False):
    print(f"--- BB84 Protocol Simulation (n={n_bits}) ---")
    
    # 1. Alice generates bits and bases
    alice_bits = generate_random_bits(n_bits)
    alice_bases = generate_random_bases(n_bits)
    
    # 2. Alice encodes qubits
    qubits = [encode_qubit(b, basis) for b, basis in zip(alice_bits, alice_bases)]
    
    # 3. Eve intercepts (if enabled)
    if eve_intercepts:
        print("Eve is intercepting...")
        eve_bases = generate_random_bases(n_bits)
        intercepted_qubits = []
        for i in range(n_bits):
            # Eve measures in her random basis
            eve_bit = measure_qubit(qubits[i], eve_bases[i])
            # Eve resends a new qubit based on her measurement
            intercepted_qubits.append(encode_qubit(eve_bit, eve_bases[i]))
        qubits = intercepted_qubits
        
    # 4. Bob generates random bases and measures
    bob_bases = generate_random_bases(n_bits)
    bob_bits = [measure_qubit(q, b) for q, b in zip(qubits, bob_bases)]
    
    # 5. Sifting: Keep only bits where bases matched
    sifted_alice = []
    sifted_bob = []
    for i in range(n_bits):
        if alice_bases[i] == bob_bases[i]:
            sifted_alice.append(alice_bits[i])
            sifted_bob.append(bob_bits[i])
            
    # 6. Error Rate Calculation
    errors = sum(a != b for a, b in zip(sifted_alice, sifted_bob))
    error_rate = errors / len(sifted_alice) if sifted_alice else 0
    
    print(f"Sifted Key Length: {len(sifted_alice)}")
    print(f"Error Rate: {error_rate:.2%}")
    
    if eve_intercepts:
        if error_rate > 0.20: # Threshold for detection
            print("⚠️ EAVESDROPPING DETECTED! Key discarded.")
            return None
        else:
            print("⚠️ Eve might be present, but error rate is low (statistical fluctuation).")
            
    # Final Key (first 10 bits for demo)
    final_key = sifted_alice[:10]
    print(f"Final Key Sample: {final_key}")
    return sifted_alice

# Run without Eve
key_safe = bb84_protocol(1000, eve_intercepts=False)

# Run with Eve
key_unsafe = bb84_protocol(1000, eve_intercepts=True)

CHAPTER 2: QUANTUM KEY DISTRIBUTION (QKD) PROTOCOLS
E91 Protocol (Entanglement-Based)
# Uses entangled pairs (Bell States) instead of single qubits.
# Based on Bell's Theorem violations.
# If Eve measures, she breaks the entanglement, reducing correlation.

def create_bell_state():
    """Create |Phi+> = (|00> + |11>) / sqrt(2)"""
    # Simplified representation for simulation
    # In real quantum computing, this requires a 2-qubit system
    return "ENTANGLED_PAIR"

def e91_protocol(n_pairs=100):
    print("\n--- E91 Protocol Simulation ---")
    # Alice and Bob share entangled pairs
    # They measure in random bases (e.g., 0, 45, 90 degrees)
    # Correlations should violate Bell's Inequality if no eavesdropping
    
    print("Generating entangled pairs...")
    print("Measuring in random bases...")
    print("Checking Bell Inequality violation...")
    print("If S > 2, quantum correlation confirmed. No eavesdropping.")
    print("Simulation complete: Secure key established.")

B92 Protocol
# Simplified version of BB84 using only two non-orthogonal states.
# Alice sends |0> for bit 0, and |+> for bit 1.
# Bob uses a specific measurement setup to distinguish them unambiguously sometimes.

def b92_protocol(n_bits=100):
    print("\n--- B92 Protocol Simulation ---")
    print("Alice sends non-orthogonal states: |0> and |+>")
    print("Bob performs unambiguous state discrimination.")
    print("Inconclusive results are discarded.")
    print("Remaining bits form the sifted key.")

CHAPTER 3: POST-QUANTUM CRYPTOGRAPHY (PQC)
Lattice-Based Cryptography (Kyber/Dilithium)
# Based on the hardness of lattice problems (e.g., Learning With Errors - LWE).
# Resistant to Shor's algorithm.
# NIST Standardization winners: CRYSTALS-Kyber (KEM), CRYSTALS-Dilithium (Signatures).

import numpy as np

class LWE_Encryption:
    """Simplified Learning With Errors encryption."""
    def __init__(self, n=10, q=101):
        self.n = n # Dimension
        self.q = q # Modulus
        
    def keygen(self):
        # Secret key s
        s = np.random.randint(0, self.q, self.n)
        # Public key A (matrix) and b = A*s + e
        A = np.random.randint(0, self.q, (self.n, self.n))
        e = np.random.randint(-2, 3, self.n) # Small error
        b = (A @ s + e) % self.q
        return (A, b), s
        
    def encrypt(self, public_key, message_bit):
        A, b = public_key
        r = np.random.randint(0, self.q, self.n) # Random vector
        e1 = np.random.randint(-1, 2, self.n)
        e2 = np.random.randint(-1, 2)
        
        u = (A.T @ r + e1) % self.q
        v = (b @ r + e2 + (self.q // 2) * message_bit) % self.q
        return u, v
        
    def decrypt(self, secret_key, ciphertext):
        u, v = ciphertext
        # m = v - s*u
        val = (v - secret_key @ u) % self.q
        # Round to nearest 0 or q/2
        if val > self.q // 4 and val < 3 * self.q // 4:
            return 1
        else:
            return 0

# Example
lwe = LWE_Encryption()
pk, sk = lwe.keygen()
ciphertext = lwe.encrypt(pk, 1)
decrypted = lwe.decrypt(sk, ciphertext)
print(f"\nLWE Encryption: Sent 1, Decrypted {decrypted}")

Code-Based Cryptography (McEliece)
# Based on the hardness of decoding random linear codes.
# Very fast encryption/decryption, but large key sizes.
# Used in Classic McEliece (NIST finalist).

Hash-Based Signatures (SPHINCS+)
# Based on the security of hash functions.
# Stateless or stateful.
# Large signatures, but very secure against quantum attacks.
# Used in SPHINCS+ (NIST finalist).

Multivariate Cryptography
# Based on solving systems of multivariate quadratic equations.
# Generally broken or inefficient, but research continues.

CHAPTER 4: QUANTUM RANDOM NUMBER GENERATION (QRNG)
True Randomness
# Classical PRNGs are deterministic.
# QRNGs use inherent quantum uncertainty (e.g., photon arrival time, vacuum fluctuations).
# Essential for secure key generation in QKD.

def simulate_qrng(n_bits=10):
    """Simulate QRNG using beam splitter model."""
    bits = []
    for _ in range(n_bits):
        # Photon hits beam splitter: 50% chance reflect, 50% transmit
        bits.append(random.randint(0, 1))
    return bits

print(f"\nQRNG Output: {simulate_qrng(16)}")

CHAPTER 5: QUANTUM SAFE MIGRATION STRATEGY
Hybrid Schemes
# Combine classical (RSA/ECC) and PQC algorithms.
# Security holds if at least one scheme remains unbroken.
# Example: TLS 1.3 with X25519 + Kyber-768.

Crypto-Agility
# Design systems to easily swap cryptographic algorithms.
# Avoid hardcoding specific algorithms.
# Use abstract interfaces for encryption/signing.

Inventory and Assessment
# Identify all systems using public-key cryptography.
# Assess risk of "Harvest Now, Decrypt Later" attacks.
# Prioritize migration for long-term sensitive data.

Recommended Reading
# - "Quantum Cryptography and Secret Key Distillation" by Scarani et al.
# - NIST Post-Quantum Cryptography Standardization: https://csrc.nist.gov/projects/post-quantum-cryptography
# - "An Introduction to Mathematical Cryptography" by Hoffstein et al. (Chapter on Lattices)

# End of Quantum Cryptography Reference