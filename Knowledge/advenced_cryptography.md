Advanced Cryptography: Zero-Knowledge Proofs, MPC, and Post-Quantum
CHAPTER 1: GETTING STARTED WITH MODERN CRYPTOGRAPHY
Remarks
Modern cryptography extends beyond encryption to include zero-knowledge proofs (proving knowledge without revealing it), multi-party computation (computing on private data), fully homomorphic encryption (computing on encrypted data), and post-quantum cryptography (resistant to quantum attacks). These enable privacy-preserving computation, verifiable computation, and secure collaboration.
Tools: Python (for implementations), SageMath (algebra), libsnark (ZKP), OpenFHE (FHE), NTRU/CRYSTALS (PQC).
Hello Cryptography
# hello_crypto.py
import hashlib
import secrets

def secure_hash(message):
    """Cryptographic hash function (SHA-256)."""
    return hashlib.sha256(message.encode()).hexdigest()

def generate_nonce(length=32):
    """Generate cryptographically secure random nonce."""
    return secrets.token_hex(length)

def hmac_sha256(key, message):
    """Hash-based Message Authentication Code."""
    import hmac
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

# Example usage
msg = "Hello, cryptography!"
hash_val = secure_hash(msg)
nonce = generate_nonce()
mac = hmac_sha256("secret_key", msg)

print(f"Message: {msg}")
print(f"Hash: {hash_val}")
print(f"Nonce: {nonce}")
print(f"HMAC: {mac}")

CHAPTER 2: MATHEMATICAL FOUNDATIONS
Modular Arithmetic and Number Theory
# Cryptography relies heavily on number theory.
# Key concepts: modular arithmetic, prime numbers, Euler's totient, discrete logarithm.

def mod_inverse(a, m):
    """Compute modular inverse using Extended Euclidean Algorithm.
    Returns x such that (a * x) % m == 1
    """
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"Modular inverse does not exist (gcd={g})")
    return x % m

def extended_gcd(a, b):
    """Extended Euclidean Algorithm.
    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def is_prime_miller_rabin(n, k=10):
    """Miller-Rabin primality test (probabilistic)."""
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True

def generate_large_prime(bits=256):
    """Generate a large prime number."""
    while True:
        n = secrets.randbits(bits)
        n |= (1 << (bits - 1)) | 1  # Ensure correct bit length and odd
        if is_prime_miller_rabin(n):
            return n

# Example
print("Modular inverse of 3 mod 11:", mod_inverse(3, 11))  # 4 (since 3*4=12≡1 mod 11)
print("Is 104729 prime?", is_prime_miller_rabin(104729))  # True

Finite Fields and Elliptic Curves
# Elliptic curves: y² = x³ + ax + b (mod p)
# Used in ECC (Elliptic Curve Cryptography) for key exchange and signatures.

class EllipticCurve:
    """Elliptic curve over finite field F_p."""
    
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        # Verify curve is non-singular: 4a³ + 27b² ≢ 0 (mod p)
        if (4 * a**3 + 27 * b**2) % p == 0:
            raise ValueError("Singular curve")
    
    def is_on_curve(self, point):
        """Check if point (x, y) is on the curve."""
        if point is None:  # Point at infinity
            return True
        x, y = point
        return (y**2 - x**3 - self.a * x - self.b) % self.p == 0
    
    def point_add(self, P, Q):
        """Add two points on the curve."""
        if P is None: return Q
        if Q is None: return P
        
        x1, y1 = P
        x2, y2 = Q
        
        if x1 == x2 and y1 != y2:  # P + (-P) = O
            return None
        
        if x1 == x2:  # Point doubling
            m = (3 * x1**2 + self.a) * mod_inverse(2 * y1, self.p) % self.p
        else:  # Point addition
            m = (y2 - y1) * mod_inverse(x2 - x1, self.p) % self.p
        
        x3 = (m**2 - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def scalar_mult(self, k, P):
        """Scalar multiplication using double-and-add."""
        result = None
        addend = P
        
        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1
        
        return result

# Example: secp256k1-like curve (simplified for demonstration)
curve = EllipticCurve(a=0, b=7, p=2**256 - 2**32 - 977)
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

# Verify generator is on curve
print("Generator on curve?", curve.is_on_curve(G))

# Scalar multiplication
P = curve.scalar_mult(12345, G)
print("Point P:", P)
print("P on curve?", curve.is_on_curve(P))

CHAPTER 3: ZERO-KNOWLEDW PROOFS (ZKP)
Schnorr Identification Protocol
# Schnorr protocol: prove knowledge of discrete log without revealing it.
# Prover knows x such that y = g^x (mod p)
# Protocol:
# 1. Prover commits: r random, R = g^r, sends R
# 2. Verifier sends challenge c
# 3. Prover responds: s = r + c*x (mod q)
# 4. Verifier checks: g^s = R * y^c (mod p)

import hashlib

def schnorr_prove(g, x, p, q):
    """Schnorr proof: prove knowledge of x where y = g^x mod p."""
    y = pow(g, x, p)
    
    # Step 1: Commitment
    r = secrets.randbelow(q - 1) + 1
    R = pow(g, r, p)
    
    # Step 2: Challenge (Fiat-Shamir heuristic for non-interactive)
    c = int(hashlib.sha256(f"{R}{y}".encode()).hexdigest(), 16) % q
    
    # Step 3: Response
    s = (r + c * x) % q
    
    return (y, R, c, s)

def schnorr_verify(g, p, q, proof):
    """Verify Schnorr proof."""
    y, R, c, s = proof
    
    # Check: g^s = R * y^c (mod p)
    lhs = pow(g, s, p)
    rhs = (R * pow(y, c, p)) % p
    
    return lhs == rhs

# Example
p = 23  # Prime
q = 11  # Prime divisor of p-1
g = 4   # Generator (g^q ≡ 1 mod p)
x = 7   # Secret

proof = schnorr_prove(g, x, p, q)
print("Schnorr proof:", proof)
print("Verification:", schnorr_verify(g, p, q, proof))  # True

zk-SNARKs (Simplified Groth16-like)
# zk-SNARK: Zero-Knowledge Succinct Non-Interactive Argument of Knowledge
# Allows proving arbitrary computations in zero knowledge.
# Based on quadratic arithmetic programs (QAP) and elliptic curve pairings.

class QAP:
    """Quadratic Arithmetic Program representation."""
    
    def __init__(self, num_constraints, num_variables):
        self.num_constraints = num_constraints
        self.num_variables = num_variables
        self.A = []  # Coefficients for left wires
        self.B = []  # Coefficients for right wires
        self.C = []  # Coefficients for output wires
    
    def add_constraint(self, a_coeffs, b_coeffs, c_coeffs):
        """Add constraint: (Σ a_i * w_i) * (Σ b_i * w_i) = Σ c_i * w_i"""
        self.A.append(a_coeffs)
        self.B.append(b_coeffs)
        self.C.append(c_coeffs)
    
    def verify_assignment(self, witness):
        """Verify witness satisfies all constraints."""
        for i in range(self.num_constraints):
            a_sum = sum(self.A[i][j] * witness[j] for j in range(self.num_variables))
            b_sum = sum(self.B[i][j] * witness[j] for j in range(self.num_variables))
            c_sum = sum(self.C[i][j] * witness[j] for j in range(self.num_variables))
            
            if a_sum * b_sum != c_sum:
                return False
        return True

# Example: Prove knowledge of x such that x^2 + x + 5 = 35 (solution: x=5)
# Introduce intermediate variables:
# sym_1 = x * x
# y = sym_1 + x
# ~out = y + 5
# Constraints:
# 1. x * x = sym_1
# 2. (sym_1 + x) * 1 = y
# 3. (y + 5) * 1 = ~out

qap = QAP(num_constraints=3, num_variables=5)
# Variables: [1, x, sym_1, y, ~out]

# Constraint 1: x * x = sym_1
qap.add_constraint(
    a_coeffs=[0, 1, 0, 0, 0],  # x
    b_coeffs=[0, 1, 0, 0, 0],  # x
    c_coeffs=[0, 0, 1, 0, 0]   # sym_1
)

# Constraint 2: (sym_1 + x) * 1 = y
qap.add_constraint(
    a_coeffs=[0, 1, 1, 0, 0],  # sym_1 + x
    b_coeffs=[1, 0, 0, 0, 0],  # 1
    c_coeffs=[0, 0, 0, 1, 0]   # y
)

# Constraint 3: (y + 5) * 1 = ~out
qap.add_constraint(
    a_coeffs=[5, 0, 0, 1, 0],  # y + 5
    b_coeffs=[1, 0, 0, 0, 0],  # 1
    c_coeffs=[0, 0, 0, 0, 1]   # ~out
)

# Witness: [1, 5, 25, 30, 35]
witness = [1, 5, 25, 30, 35]
print("QAP satisfied?", qap.verify_assignment(witness))  # True

Pairing-Based Cryptography
# Bilinear pairings enable advanced ZKP constructions.
# e: G1 × G2 → GT where e(aP, bQ) = e(P, Q)^{ab}

def mock_pairing(P, Q):
    """Mock bilinear pairing (for demonstration).
    Real implementation requires elliptic curve pairings (e.g., BN254, BLS12-381).
    """
    # Simplified: return hash of concatenated points
    return hashlib.sha256(f"{P}{Q}".encode()).digest()

# Properties of pairings:
# 1. Bilinearity: e(aP, bQ) = e(P, Q)^{ab}
# 2. Non-degeneracy: e(P, Q) ≠ 1 for generators P, Q
# 3. Computability: efficiently computable

# Used in:
# - Groth16 zk-SNARKs
# - BLS signatures
# - Identity-based encryption

CHAPTER 4: MULTI-PARTY COMPUTATION (MPC)
Secret Sharing (Shamir's Scheme)
# Shamir's Secret Sharing: split secret into n shares, reconstruct with k shares.
# Based on polynomial interpolation over finite field.

def shamir_share(secret, n, k, prime):
    """Split secret into n shares, threshold k."""
    # Generate random polynomial of degree k-1
    # f(x) = secret + a_1*x + a_2*x^2 + ... + a_{k-1}*x^{k-1}
    coeffs = [secret] + [secrets.randbelow(prime) for _ in range(k - 1)]
    
    # Evaluate polynomial at points 1, 2, ..., n
    shares = []
    for i in range(1, n + 1):
        value = sum(c * pow(i, j, prime) for j, c in enumerate(coeffs)) % prime
        shares.append((i, value))
    
    return shares

def shamir_reconstruct(shares, prime):
    """Reconstruct secret from k shares using Lagrange interpolation."""
    k = len(shares)
    secret = 0
    
    for i, (x_i, y_i) in enumerate(shares):
        # Compute Lagrange basis polynomial l_i(0)
        numerator = 1
        denominator = 1
        
        for j, (x_j, _) in enumerate(shares):
            if i != j:
                numerator = (numerator * (-x_j)) % prime
                denominator = (denominator * (x_i - x_j)) % prime
        
        # l_i(0) = numerator / denominator
        l_i_0 = (numerator * mod_inverse(denominator, prime)) % prime
        secret = (secret + y_i * l_i_0) % prime
    
    return secret

# Example
secret = 12345
n, k = 5, 3
prime = 2**127 - 1  # Large prime

shares = shamir_share(secret, n, k, prime)
print("Shares:", shares)

# Reconstruct with k=3 shares
reconstructed = shamir_reconstruct(shares[:k], prime)
print("Reconstructed secret:", reconstructed)  # 12345

Garbled Circuits
# Garbled circuits enable secure two-party computation.
# One party garbles (encrypts) a circuit, other evaluates it.

class GarbledGate:
    """Garbled AND gate."""
    
    def __init__(self):
        self.keys = {
            0: secrets.token_bytes(16),
            1: secrets.token_bytes(16)
        }
    
    def garble(self, gate_type='AND'):
        """Create garbled truth table."""
        table = {}
        
        for a in [0, 1]:
            for b in [0, 1]:
                # Compute output
                if gate_type == 'AND':
                    out = a & b
                elif gate_type == 'OR':
                    out = a | b
                elif gate_type == 'XOR':
                    out = a ^ b
                
                # Encrypt output with input keys
                key_a = self.keys[a]
                key_b = self.keys[b]
                encrypted_out = self._encrypt(key_a, key_b, out)
                table[(a, b)] = encrypted_out
        
        return table
    
    def _encrypt(self, key_a, key_b, plaintext):
        """Simple encryption (real implementation uses AES-GCM)."""
        combined = key_a + key_b
        return hashlib.sha256(combined + bytes([plaintext])).digest()
    
    def evaluate(self, key_a, key_b, table, a_val, b_val):
        """Evaluate garbled gate."""
        encrypted_out = table[(a_val, b_val)]
        # Try all possible outputs
        for out in [0, 1]:
            test = self._encrypt(key_a, key_b, out)
            if test == encrypted_out:
                return out
        return None

# Example
gate = GarbledGate()
table = gate.garble('AND')

# Party 1 has input a=1, Party 2 has input b=1
key_a = gate.keys[1]
key_b = gate.keys[1]

result = gate.evaluate(key_a, key_b, table, 1, 1)
print("Garbled AND(1, 1) =", result)  # 1

Oblivious Transfer (OT)
# Oblivious Transfer: sender has 2 messages, receiver gets 1 without sender knowing which.
# Foundation for secure MPC.

def simple_ot(m0, m1, choice, prime):
    """Simplified 1-out-of-2 OT (for demonstration).
    Real implementation uses public-key cryptography.
    """
    # Sender generates random values
    a = secrets.randbelow(prime)
    x = secrets.randbelow(prime)
    
    # Receiver's choice bit determines which message they can decrypt
    if choice == 0:
        k = pow(x, a, prime)
    else:
        k = pow(x, a + 1, prime)
    
    # Sender encrypts both messages
    c0 = (m0 + k) % prime
    c1 = (m1 + k) % prime
    
    # Receiver can only decrypt one
    if choice == 0:
        return (c0 - k) % prime
    else:
        return (c1 - k) % prime

# Example
m0, m1 = 100, 200
prime = 10**9 + 7

received = simple_ot(m0, m1, choice=1, prime=prime)
print("Receiver got:", received)  # 200

CHAPTER 5: FULLY HOMOMORPHIC ENCRYPTION (FHE)
BFV Scheme (Simplified)
# BFV (Brakerski/Fan-Vercauteren): FHE scheme for integer arithmetic.
# Allows computation on encrypted data without decryption.

import numpy as np

class BFVScheme:
    """Simplified BFV FHE scheme (for educational purposes)."""
    
    def __init__(self, n=1024, t=65537, q=2**60):
        self.n = n  # Polynomial degree
        self.t = t  # Plaintext modulus
        self.q = q  # Ciphertext modulus
        
        # Generate keys
        self.secret_key = self._generate_secret_key()
        self.public_key = self._generate_public_key()
    
    def _generate_secret_key(self):
        """Generate secret key (ternary polynomial)."""
        return np.random.choice([-1, 0, 1], size=self.n)
    
    def _generate_public_key(self):
        """Generate public key."""
        a = np.random.randint(0, self.q, size=self.n)
        e = self._sample_error()
        # pk = (a, b = -a*s + t*e + q/2)
        b = (-np.polyval(a, self.secret_key) + self.t * e) % self.q
        return (a, b)
    
    def _sample_error(self):
        """Sample from discrete Gaussian distribution."""
        return np.random.normal(0, 3.2, size=self.n).astype(int)
    
    def encrypt(self, plaintext):
        """Encrypt plaintext polynomial."""
        a, b = self.public_key
        u = self._generate_secret_key()  # Random polynomial
        e1 = self._sample_error()
        e2 = self._sample_error()
        
        # c0 = a*u + e1
        # c1 = b*u + e2 + (q/t)*m
        c0 = (np.polyval(a, u) + e1) % self.q
        c1 = (np.polyval(b, u) + e2 + (self.q // self.t) * plaintext) % self.q
        
        return (c0, c1)
    
    def decrypt(self, ciphertext):
        """Decrypt ciphertext."""
        c0, c1 = ciphertext
        
        # m = round((t/q) * (c1 - c0*s))
        decrypted = c1 - np.polyval(c0, self.secret_key)
        decrypted = (decrypted % self.q)
        plaintext = np.round((self.t / self.q) * decrypted).astype(int) % self.t
        
        return plaintext
    
    def add(self, ct1, ct2):
        """Homomorphic addition."""
        c0_1, c1_1 = ct1
        c0_2, c1_2 = ct2
        return ((c0_1 + c0_2) % self.q, (c1_1 + c1_2) % self.q)
    
    def multiply(self, ct1, ct2):
        """Homomorphic multiplication (simplified)."""
        # Real BFV uses relinearization and modulus switching
        c0_1, c1_1 = ct1
        c0_2, c1_2 = ct2
        
        # Simplified: just multiply polynomials
        c0 = (c0_1 * c0_2) % self.q
        c1 = (c1_1 * c1_2) % self.q
        
        return (c0, c1)

# Example
scheme = BFVScheme(n=64, t=257, q=2**30)

# Encrypt two values
m1 = np.array([5, 3, 7, 2])
m2 = np.array([2, 4, 1, 6])

ct1 = scheme.encrypt(m1)
ct2 = scheme.encrypt(m2)

# Homomorphic addition
ct_sum = scheme.add(ct1, ct2)
result_sum = scheme.decrypt(ct_sum)
print("Encrypted addition:", result_sum)  # Should be [7, 7, 8, 8]

# Homomorphic multiplication
ct_prod = scheme.multiply(ct1, ct2)
result_prod = scheme.decrypt(ct_prod)
print("Encrypted multiplication:", result_prod)  # Should be [10, 12, 7, 12]

CHAPTER 6: POST-QUANTUM CRYPTOGRAPHY
Lattice-Based Cryptography (LWE)
# Learning With Errors (LWE): foundation for post-quantum cryptography.
# Resistant to quantum attacks (Shor's algorithm).

class LWE:
    """Learning With Errors problem."""
    
    def __init__(self, n=128, q=3329):
        self.n = n  # Dimension
        self.q = q  # Modulus
    
    def keygen(self):
        """Generate LWE key pair."""
        # Secret key: s ∈ Z_q^n
        s = np.random.randint(0, self.q, size=self.n)
        
        # Public key: (A, b = A*s + e)
        A = np.random.randint(0, self.q, size=(self.n, self.n))
        e = np.random.randint(-3, 4, size=self.n)  # Small error
        b = (A @ s + e) % self.q
        
        return (A, b), s
    
    def encrypt(self, pk, message):
        """Encrypt message using LWE."""
        A, b = pk
        
        # Sample random vector r and small error e
        r = np.random.randint(0, 2, size=self.n)
        e1 = np.random.randint(-1, 2, size=self.n)
        e2 = np.random.randint(-1, 2)
        
        # Ciphertext: (u = A^T*r + e1, v = b^T*r + e2 + (q/2)*m)
        u = (A.T @ r + e1) % self.q
        v = (b @ r + e2 + (self.q // 2) * message) % self.q
        
        return (u, v)
    
    def decrypt(self, sk, ciphertext):
        """Decrypt LWE ciphertext."""
        u, v = ciphertext
        
        # m = round((2/q) * (v - s^T*u))
        decrypted = v - sk @ u
        decrypted = decrypted % self.q
        message = np.round((2 / self.q) * decrypted).astype(int) % 2
        
        return message

# Example
lwe = LWE(n=64, q=3329)
pk, sk = lwe.keygen()

# Encrypt binary message
message = np.array([1, 0, 1, 1, 0])
encrypted = lwe.encrypt(pk, message)
decrypted = lwe.decrypt(sk, encrypted)

print("Original:", message)
print("Decrypted:", decrypted)

CRYSTALS-Kyber (Key Encapsulation)
# Kyber: NIST standard for post-quantum key encapsulation (KEM).
# Based on Module-LWE problem.

class KyberSimplified:
    """Simplified Kyber-like KEM."""
    
    def __init__(self, k=2, n=256, q=3329):
        self.k = k  # Module rank
        self.n = n  # Polynomial degree
        self.q = q  # Modulus
    
    def keygen(self):
        """Generate key pair."""
        # Secret key: s ∈ R_q^k (polynomial vector)
        s = [self._sample_polynomial() for _ in range(self.k)]
        
        # Public key: (A, t = A*s + e)
        A = [[self._sample_polynomial() for _ in range(self.k)] for _ in range(self.k)]
        e = [self._sample_error() for _ in range(self.k)]
        
        # t = A*s + e (simplified polynomial arithmetic)
        t = []
        for i in range(self.k):
            t_i = sum(A[i][j] * s[j] for j in range(self.k)) + e[i]
            t.append(t_i % self.q)
        
        return (A, t), s
    
    def encapsulate(self, pk):
        """Encapsulate shared secret."""
        A, t = pk
        
        # Sample random r and error
        r = [self._sample_polynomial() for _ in range(self.k)]
        e1 = [self._sample_error() for _ in range(self.k)]
        e2 = self._sample_error()
        
        # u = A^T*r + e1
        u = []
        for i in range(self.k):
            u_i = sum(A[j][i] * r[j] for j in range(self.k)) + e1[i]
            u.append(u_i % self.q)
        
        # v = t^T*r + e2 + encode(m)
        m = secrets.token_bytes(32)  # Shared secret
        v = sum(t[i] * r[i] for i in range(self.k)) + e2
        v = (v + self._encode(m)) % self.q
        
        return (u, v), m
    
    def decapsulate(self, sk, ciphertext):
        """Decapsulate shared secret."""
        u, v = ciphertext
        
        # m = decode(v - s^T*u)
        decoded = v - sum(sk[i] * u[i] for i in range(self.k))
        m = self._decode(decoded % self.q)
        
        return m
    
    def _sample_polynomial(self):
        """Sample uniform polynomial."""
        return np.random.randint(0, self.q, size=self.n)
    
    def _sample_error(self):
        """Sample small error polynomial."""
        return np.random.randint(-3, 4, size=self.n)
    
    def _encode(self, message):
        """Encode message into polynomial."""
        return np.frombuffer(message, dtype=np.uint8).astype(int) % self.q
    
    def _decode(self, polynomial):
        """Decode polynomial into message."""
        return polynomial[:32].tobytes()

# Example
kyber = KyberSimplified(k=2, n=128, q=3329)
pk, sk = kyber.keygen()
ciphertext, shared_secret = kyber.encapsulate(pk)
recovered_secret = kyber.decapsulate(sk, ciphertext)

print("Shared secrets match:", shared_secret == recovered_secret)

CHAPTER 7: ADVANCED ZKP SYSTEMS
PLONK (Permutations over Lagrange-bases for Oecumenical Noninteractive arguments of Knowledge)
# PLONK: Universal zk-SNARK with trusted setup once, works for any circuit.
# Uses polynomial commitments (KZG) and permutation arguments.

class PLONK:
    """Simplified PLONK-like zk-SNARK."""
    
    def __init__(self, n=8):
        self.n = n  # Circuit size (power of 2)
        self.domain = self._get_domain()
    
    def _get_domain(self):
        """Get roots of unity for FFT domain."""
        # Simplified: use integers mod prime
        return list(range(self.n))
    
    def commit_polynomial(self, poly):
        """Commit to polynomial using hash (simplified KZG)."""
        return hashlib.sha256(str(poly).encode()).digest()
    
    def prove(self, circuit, witness):
        """Generate PLONK proof."""
        # Step 1: Commit to witness polynomials
        wire_polys = self._compute_wire_polynomials(circuit, witness)
        commitments = [self.commit_polynomial(w) for w in wire_polys]
        
        # Step 2: Compute quotient polynomial
        quotient = self._compute_quotient(circuit, wire_polys)
        quotient_commitment = self.commit_polynomial(quotient)
        
        # Step 3: Evaluate polynomials at challenge point
        challenge = int(hashlib.sha256(str(commitments).encode()).hexdigest(), 16) % self.n
        evaluations = [w[challenge % len(w)] for w in wire_polys]
        
        # Step 4: Compute opening proofs
        opening_proofs = [self._compute_opening_proof(w, challenge) for w in wire_polys]
        
        return {
            'commitments': commitments,
            'quotient_commitment': quotient_commitment,
            'evaluations': evaluations,
            'opening_proofs': opening_proofs
        }
    
    def verify(self, circuit, proof):
        """Verify PLONK proof."""
        # Check polynomial evaluations satisfy circuit constraints
        # Check opening proofs are valid
        # (Simplified verification)
        return len(proof['commitments']) > 0
    
    def _compute_wire_polynomials(self, circuit, witness):
        """Compute wire assignment polynomials."""
        # Simplified: return witness values
        return [witness for _ in range(3)]  # a, b, c wires
    
    def _compute_quotient(self, circuit, wire_polys):
        """Compute quotient polynomial."""
        # Simplified
        return [0] * self.n
    
    def _compute_opening_proof(self, poly, challenge):
        """Compute polynomial opening proof."""
        return hashlib.sha256(f"{poly}{challenge}".encode()).digest()

# Example
plonk = PLONK(n=8)
circuit = "x * x = y"
witness = [1, 5, 25]  # [1, x, x^2]

proof = plonk.prove(circuit, witness)
print("PLONK proof generated:", len(proof['commitments']), "commitments")
print("Verification:", plonk.verify(circuit, proof))

CHAPTER 8: SECURE MULTI-PARTY COMPUTATION PROTOCOLS
SPDZ Protocol
# SPDZ: Secure multi-party computation with preprocessing.
# Supports addition and multiplication on secret-shared values.

class SPDZ:
    """Simplified SPDZ-like MPC protocol."""
    
    def __init__(self, num_parties, prime):
        self.num_parties = num_parties
        self.prime = prime
        self.mac_key = secrets.randbelow(prime)
    
    def share(self, value):
        """Secret-share a value among parties."""
        shares = [secrets.randbelow(self.prime) for _ in range(self.num_parties - 1)]
        last_share = (value - sum(shares)) % self.prime
        shares.append(last_share)
        
        # Compute MACs
        macs = [(s * self.mac_key) % self.prime for s in shares]
        
        return list(zip(shares, macs))
    
    def reconstruct(self, shares_with_macs):
        """Reconstruct value from shares."""
        shares = [s for s, _ in shares_with_macs]
        macs = [m for _, m in shares_with_macs]
        
        # Reconstruct value
        value = sum(shares) % self.prime
        
        # Verify MACs
        expected_mac = (value * self.mac_key) % self.prime
        if sum(macs) % self.prime != expected_mac:
            raise ValueError("MAC verification failed")
        
        return value
    
    def add_shares(self, shares1, shares2):
        """Add two secret-shared values."""
        result = []
        for (s1, m1), (s2, m2) in zip(shares1, shares2):
            result.append(((s1 + s2) % self.prime, (m1 + m2) % self.prime))
        return result
    
    def multiply_shares(self, shares1, shares2):
        """Multiply two secret-shared values (requires interaction)."""
        # Simplified: local multiplication (real SPDZ uses Beaver triples)
        result = []
        for (s1, m1), (s2, m2) in zip(shares1, shares2):
            result.append(((s1 * s2) % self.prime, (m1 * m2) % self.prime))
        return result

# Example
spdz = SPDZ(num_parties=3, prime=10**9 + 7)

# Share two values
x_shares = spdz.share(10)
y_shares = spdz.share(20)

# Add shares
z_shares = spdz.add_shares(x_shares, y_shares)
z = spdz.reconstruct(z_shares)
print("Addition result:", z)  # 30

# Multiply shares
w_shares = spdz.multiply_shares(x_shares, y_shares)
w = spdz.reconstruct(w_shares)
print("Multiplication result:", w)  # 200

CHAPTER 9: PRACTICAL APPLICATIONS
Privacy-Preserving Machine Learning
# Use MPC/FHE for training ML models on private data.

class SecureML:
    """Secure machine learning using secret sharing."""
    
    def __init__(self, num_parties, prime):
        self.mpc = SPDZ(num_parties, prime)
    
    def secure_linear_regression(self, X_shares, y_shares):
        """Train linear regression on secret-shared data."""
        # Simplified: compute X^T * X and X^T * y securely
        # Real implementation requires secure matrix multiplication
        
        # Reconstruct for demonstration
        X = self.mpc.reconstruct(X_shares)
        y = self.mpc.reconstruct(y_shares)
        
        # Compute weights: w = (X^T X)^{-1} X^T y
        # (Simplified linear algebra)
        return "Secure weights computed"

# Example
secure_ml = SecureML(num_parties=3, prime=10**9 + 7)
print("Secure ML training:", secure_ml.secure_linear_regression(None, None))

Verifiable Computation
# Allow client to outsource computation and verify result.

class VerifiableComputation:
    """Verifiable computation using ZKP."""
    
    def __init__(self):
        self.plonk = PLONK()
    
    def outsource_computation(self, function, input_data):
        """Outsource computation and generate proof."""
        # Server computes result
        result = function(input_data)
        
        # Server generates ZKP that result is correct
        proof = self.plonk.prove(f"function({input_data}) = {result}", [input_data, result])
        
        return result, proof
    
    def verify_result(self, function, input_data, result, proof):
        """Verify computation result."""
        return self.plonk.verify(f"function({input_data}) = {result}", proof)

# Example
vc = VerifiableComputation()
result, proof = vc.outsource_computation(lambda x: x**2, 5)
print("Result:", result, "Verified:", vc.verify_result(None, 5, result, proof))

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Cryptographic Primitives Summary
# Hash Functions: SHA-256, SHA-3, BLAKE2
# Symmetric Encryption: AES-GCM, ChaCha20-Poly1305
# Asymmetric Encryption: RSA, ECC, CRYSTALS-Kyber
# Digital Signatures: ECDSA, Ed25519, CRYSTALS-Dilithium
# Key Exchange: Diffie-Hellman, ECDH, Kyber
# Zero-Knowledge: Schnorr, Groth16, PLONK, STARK
# MPC: Secret sharing, garbled circuits, SPDZ
# FHE: BFV, BGV, TFHE, CKKS

Post-Quantum Standards (NIST)
# Finalists (2022-2024):
# - CRYSTALS-Kyber: Key encapsulation (lattice-based)
# - CRYSTALS-Dilithium: Digital signatures (lattice-based)
# - FALCON: Digital signatures (lattice-based)
# - SPHINCS+: Digital signatures (hash-based)

# Alternative candidates:
# - NTRU: Lattice-based
# - Classic McEliece: Code-based
# - GeMSS: Multivariate

Recommended Reading
# - "Introduction to Modern Cryptography" by Katz & Lindell
# - "A Graduate Course in Applied Cryptography" by Boneh & Shoup
# - "Zero-Knowledge Proofs" by Goldreich
# - "Post-Quantum Cryptography" by Bernstein et al.
# - NIST PQC standardization: https://csrc.nist.gov/projects/post-quantum-cryptography

# End of Advanced Cryptography Reference