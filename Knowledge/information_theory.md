Information Theory & Coding Complete Reference
CHAPTER 1: GETTING STARTED WITH INFORMATION THEORY
Remarks
Information theory, founded by Claude Shannon (1948), quantifies information, compression limits, and reliable communication over noisy channels. Key concepts: entropy (uncertainty), mutual information (shared information), channel capacity (maximum reliable rate), source coding (compression), channel coding (error correction). Applications: data compression (ZIP, JPEG, MP3), error correction (CDs, QR codes, 5G), cryptography, machine learning, neuroscience.
Tools: Python (NumPy, SciPy), MATLAB (Communications Toolbox), GNU Radio (SDR), eccodes (meteorology).
Hello Information Theory
# hello_info_theory.py
"""
First program: compute entropy of a message and compare to theoretical limit.
"""
import numpy as np
from collections import Counter
import math

def entropy(probabilities):
    """Shannon entropy: H(X) = -Σ p(x) log2 p(x) bits."""
    H = 0.0
    for p in probabilities:
        if p > 0:
            H -= p * math.log2(p)
    return H

def empirical_entropy(message):
    """Compute entropy from observed symbol frequencies."""
    counts = Counter(message)
    total = len(message)
    probs = [count / total for count in counts.values()]
    return entropy(probs)

# Example: English text statistics
english = "the quick brown fox jumps over the lazy dog " * 100
random_text = "".join(np.random.choice(list("abcdefghijklmnopqrstuvwxyz "), len(english)))

H_english = empirical_entropy(english)
H_random = empirical_entropy(random_text)

print(f"English text entropy: {H_english:.3f} bits/char")
print(f"Random text entropy:  {H_random:.3f} bits/char")
print(f"Max possible (27 symbols): {math.log2(27):.3f} bits/char")
print(f"\nEnglish is {H_english/math.log2(27)*100:.1f}% of maximum entropy")
print(f"Compression potential: {(1 - H_english/math.log2(27))*100:.1f}%")

# Shannon's source coding theorem:
# Optimal compression rate → entropy H(X)
# Cannot compress below H(X) bits/symbol on average

CHAPTER 2: SHANNON ENTROPY AND INFORMATION MEASURES
Entropy Properties
# Entropy H(X): average uncertainty of random variable X
# Properties:
# 1. H(X) ≥ 0 (non-negative)
# 2. H(X) = 0 iff X is deterministic
# 3. H(X) ≤ log2(|X|) (max for uniform distribution)
# 4. H(X,Y) ≤ H(X) + H(Y) (subadditivity)

import numpy as np
import math

def entropy_bits(probabilities):
    """Entropy in bits (base 2)."""
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def entropy_nats(probabilities):
    """Entropy in nats (base e)."""
    return -sum(p * math.log(p) for p in probabilities if p > 0)

def entropy_hartleys(probabilities):
    """Entropy in hartleys (base 10)."""
    return -sum(p * math.log10(p) for p in probabilities if p > 0)

# Binary entropy function
def binary_entropy(p):
    """Entropy of Bernoulli(p): H = -p log p - (1-p) log (1-p)."""
    if p == 0 or p == 1:
        return 0.0
    return -p * math.log2(p) - (1-p) * math.log2(1-p)

# Plot binary entropy
import matplotlib.pyplot as plt
p_values = np.linspace(0.001, 0.999, 100)
H_values = [binary_entropy(p) for p in p_values]

plt.figure(figsize=(10, 5))
plt.plot(p_values, H_values, 'b-', linewidth=2)
plt.xlabel('Probability p')
plt.ylabel('Entropy H(p) (bits)')
plt.title('Binary Entropy Function')
plt.grid(alpha=0.3)
plt.axhline(1, color='r', linestyle='--', label='Max = 1 bit')
plt.axvline(0.5, color='g', linestyle='--', label='p = 0.5 (max entropy)')
plt.legend()
plt.tight_layout()
plt.show()

Joint and Conditional Entropy
# Joint entropy: H(X,Y) = -Σ p(x,y) log p(x,y)
# Conditional entropy: H(Y|X) = H(X,Y) - H(X)
# Chain rule: H(X,Y) = H(X) + H(Y|X)

def joint_entropy(joint_probs):
    """Joint entropy of two variables."""
    H = 0.0
    for row in joint_probs:
        for p in row:
            if p > 0:
                H -= p * math.log2(p)
    return H

def conditional_entropy(joint_probs):
    """H(Y|X) = H(X,Y) - H(X)."""
    # Marginal of X
    px = [sum(row) for row in joint_probs]
    H_XY = joint_entropy(joint_probs)
    H_X = entropy_bits(px)
    return H_XY - H_X

# Example: weather and activity
# Joint distribution P(Weather, Activity)
# Weather: Sunny(0), Rainy(1)
# Activity: Outdoor(0), Indoor(1)
joint = [
    [0.4, 0.1],  # Sunny: outdoor 40%, indoor 10%
    [0.1, 0.5]   # Rainy: outdoor 10%, indoor 50%
]

H_XY = joint_entropy(joint)
H_X = entropy_bits([0.5, 0.5])  # Weather is uniform
H_Y = entropy_bits([0.5, 0.6])  # Activity
H_Y_given_X = conditional_entropy(joint)

print(f"H(Weather, Activity) = {H_XY:.3f} bits")
print(f"H(Weather) = {H_X:.3f} bits")
print(f"H(Activity) = {H_Y:.3f} bits")
print(f"H(Activity | Weather) = {H_Y_given_X:.3f} bits")
print(f"Knowing weather reduces uncertainty by: {H_Y - H_Y_given_X:.3f} bits")

Mutual Information
# Mutual information I(X;Y): information shared between X and Y
# I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X) = H(X) + H(Y) - H(X,Y)
# I(X;Y) ≥ 0, equals 0 iff X and Y independent

def mutual_information(joint_probs):
    """Compute I(X;Y) from joint distribution."""
    px = [sum(row) for row in joint_probs]
    py = [sum(joint_probs[i][j] for i in range(len(joint_probs))) 
          for j in range(len(joint_probs[0]))]
    
    H_X = entropy_bits(px)
    H_Y = entropy_bits(py)
    H_XY = joint_entropy(joint_probs)
    
    return H_X + H_Y - H_XY

def kl_divergence(p, q):
    """Kullback-Leibler divergence: D_KL(P || Q)."""
    return sum(pi * math.log2(pi / qi) for pi, qi in zip(p, q) if pi > 0 and qi > 0)

# Example
I_XY = mutual_information(joint)
print(f"\nMutual information I(Weather; Activity) = {I_XY:.3f} bits")
print(f"Activity is {I_XY/H_Y*100:.1f}% predictable from weather")

# KL divergence: how different are two distributions?
P = [0.5, 0.3, 0.2]
Q = [0.4, 0.4, 0.2]
D_KL = kl_divergence(P, Q)
print(f"\nD_KL(P || Q) = {D_KL:.3f} bits")
print(f"Q is a poor model of P (loses {D_KL:.3f} bits per symbol)")

CHAPTER 3: SOURCE CODING (LOSSLESS COMPRESSION)
Huffman Coding
# Huffman coding: optimal prefix-free code for known symbol probabilities.
# Average code length → entropy H(X) (within 1 bit).
# Algorithm: repeatedly merge two least probable symbols.

import heapq
from collections import Counter

class HuffmanNode:
    def __init__(self, symbol=None, freq=0, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    """Build Huffman tree from symbol frequencies."""
    heap = [HuffmanNode(sym, freq) for sym, freq in frequencies.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    
    return heap[0]

def generate_codes(node, prefix="", codes=None):
    """Generate binary codes from Huffman tree."""
    if codes is None:
        codes = {}
    
    if node.symbol is not None:
        codes[node.symbol] = prefix if prefix else "0"
    else:
        generate_codes(node.left, prefix + "0", codes)
        generate_codes(node.right, prefix + "1", codes)
    
    return codes

def huffman_encode(message, codes):
    """Encode message using Huffman codes."""
    return "".join(codes[c] for c in message)

def huffman_decode(encoded, tree):
    """Decode Huffman-encoded string."""
    result = []
    node = tree
    for bit in encoded:
        node = node.left if bit == '0' else node.right
        if node.symbol is not None:
            result.append(node.symbol)
            node = tree
    return "".join(result)

# Example
message = "abracadabra"
freq = dict(Counter(message))
print(f"Symbol frequencies: {freq}")

tree = build_huffman_tree(freq)
codes = generate_codes(tree)
print(f"Huffman codes: {codes}")

encoded = huffman_encode(message, codes)
print(f"Encoded: {encoded} ({len(encoded)} bits)")
print(f"Original: {len(message) * 8} bits (ASCII)")
print(f"Compression ratio: {len(message) * 8 / len(encoded):.2f}x")

decoded = huffman_decode(encoded, tree)
print(f"Decoded: {decoded}")
print(f"Correct: {decoded == message}")

# Average code length
avg_len = sum(freq[s] * len(codes[s]) for s in freq) / len(message)
H = entropy_bits([f / len(message) for f in freq.values()])
print(f"\nAverage code length: {avg_len:.3f} bits/symbol")
print(f"Entropy: {H:.3f} bits/symbol")
print(f"Efficiency: {H / avg_len * 100:.1f}%")

Arithmetic Coding
# Arithmetic coding: represents entire message as single number in [0,1).
# Approaches entropy limit more closely than Huffman for long messages.
# Used in: JPEG, H.264, ZIP (optional).

class ArithmeticCoder:
    """Arithmetic coder for known probability model."""
    
    def __init__(self, probabilities, symbols):
        """
        probabilities: list of symbol probabilities (sum to 1)
        symbols: corresponding symbols
        """
        self.symbols = symbols
        self.cumulative = [0.0]
        for p in probabilities:
            self.cumulative.append(self.cumulative[-1] + p)
        self.sym_to_idx = {s: i for i, s in enumerate(symbols)}
    
    def encode(self, message):
        """Encode message to interval [low, high)."""
        low, high = 0.0, 1.0
        
        for symbol in message:
            idx = self.sym_to_idx[symbol]
            range_size = high - low
            high = low + range_size * self.cumulative[idx + 1]
            low = low + range_size * self.cumulative[idx]
        
        # Return midpoint of final interval
        return (low + high) / 2
    
    def decode(self, value, length):
        """Decode value back to message of given length."""
        message = []
        
        for _ in range(length):
            for i in range(len(self.symbols)):
                if self.cumulative[i] <= value < self.cumulative[i + 1]:
                    message.append(self.symbols[i])
                    range_size = self.cumulative[i + 1] - self.cumulative[i]
                    value = (value - self.cumulative[i]) / range_size
                    break
        
        return "".join(message)

# Example
probs = [0.5, 0.3, 0.2]
symbols = ['A', 'B', 'C']
coder = ArithmeticCoder(probs, symbols)

message = "ABACAB"
encoded_value = coder.encode(message)
print(f"\nArithmetic coding:")
print(f"Message: {message}")
print(f"Encoded value: {encoded_value:.10f}")

decoded = coder.decode(encoded_value, len(message))
print(f"Decoded: {decoded}")
print(f"Correct: {decoded == message}")

# Bits needed: -log2(interval_size)
# For this message, interval ≈ 0.5^4 * 0.3 * 0.2 = 0.00125
# Bits ≈ -log2(0.00125) ≈ 9.6 bits (vs 18 bits for Huffman)

LZW Compression
# LZW (Lempel-Ziv-Welch): dictionary-based compression.
# Builds dictionary of seen substrings on the fly.
# Used in: GIF, TIFF, Unix compress.

class LZWCompressor:
    """LZW compression."""
    
    def __init__(self, initial_dict=None):
        if initial_dict is None:
            # Start with all single characters
            self.initial_dict = {chr(i): i for i in range(256)}
        else:
            self.initial_dict = initial_dict
    
    def compress(self, message):
        """Compress message to list of dictionary indices."""
        dictionary = dict(self.initial_dict)
        next_code = max(dictionary.values()) + 1
        
        result = []
        current = ""
        
        for char in message:
            combined = current + char
            if combined in dictionary:
                current = combined
            else:
                result.append(dictionary[current])
                dictionary[combined] = next_code
                next_code += 1
                current = char
        
        if current:
            result.append(dictionary[current])
        
        return result, dictionary
    
    def decompress(self, codes, initial_dict=None):
        """Decompress list of codes back to message."""
        if initial_dict is None:
            dictionary = {i: chr(i) for i in range(256)}
        else:
            dictionary = {v: k for k, v in initial_dict.items()}
        
        next_code = max(dictionary.keys()) + 1
        result = []
        
        prev_code = codes[0]
        result.append(dictionary[prev_code])
        
        for code in codes[1:]:
            if code in dictionary:
                entry = dictionary[code]
            elif code == next_code:
                entry = dictionary[prev_code] + dictionary[prev_code][0]
            else:
                raise ValueError(f"Invalid code: {code}")
            
            result.append(entry)
            dictionary[next_code] = dictionary[prev_code] + entry[0]
            next_code += 1
            prev_code = code
        
        return "".join(result)

# Example
compressor = LZWCompressor()
message = "ABABABABABABABAB" * 10
codes, final_dict = compressor.compress(message)

print(f"\nLZW compression:")
print(f"Original: {len(message)} chars = {len(message) * 8} bits")
print(f"Compressed: {len(codes)} codes = {len(codes) * 12} bits (assuming 12-bit codes)")
print(f"Compression ratio: {len(message) * 8 / (len(codes) * 12):.2f}x")

decompressed = compressor.decompress(codes)
print(f"Decompressed correctly: {decompressed == message}")
print(f"Final dictionary size: {len(final_dict)} entries")

CHAPTER 4: LOSSY COMPRESSION
Quantization Theory
# Lossy compression: trade quality for size.
# Quantization: map continuous values to discrete levels.
# Rate-distortion theory: minimum bits for given distortion.

import numpy as np

def uniform_quantize(signal, levels):
    """Uniform scalar quantization."""
    min_val, max_val = signal.min(), signal.max()
    step = (max_val - min_val) / levels
    quantized = np.round((signal - min_val) / step) * step + min_val
    return quantized, step

def compute_snr(original, quantized):
    """Signal-to-Noise Ratio in dB."""
    signal_power = np.mean(original ** 2)
    noise_power = np.mean((original - quantized) ** 2)
    if noise_power == 0:
        return float('inf')
    return 10 * np.log10(signal_power / noise_power)

# Example: quantize audio signal
np.random.seed(42)
t = np.linspace(0, 1, 1000)
signal = np.sin(2 * np.pi * 5 * t) + 0.1 * np.random.randn(len(t))

for bits in [2, 4, 8, 16]:
    levels = 2 ** bits
    quantized, step = uniform_quantize(signal, levels)
    snr = compute_snr(signal, quantized)
    print(f"{bits:2d} bits ({levels:4d} levels): SNR = {snr:.1f} dB, step = {step:.4f}")

# Theoretical: SNR ≈ 6.02 * bits + 1.76 dB (uniform quantization)

DCT and JPEG-like Compression
# DCT (Discrete Cosine Transform): concentrates energy in few coefficients.
# Used in JPEG, MP3, MPEG video.

from scipy.fft import dct, idct

def compress_block_dct(block, quality=50):
    """JPEG-like compression using DCT + quantization."""
    # 2D DCT
    dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
    
    # JPEG quantization matrix (luminance)
    quant_matrix = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ])
    
    # Scale by quality (1-100)
    scale = max(1, (100 - quality) / 5)
    qm = quant_matrix * scale
    
    # Quantize
    quantized = np.round(dct_block / qm)
    
    # Count non-zero (compression measure)
    nonzero = np.count_nonzero(quantized)
    compression_ratio = 64 / nonzero if nonzero > 0 else float('inf')
    
    return quantized, qm, compression_ratio

def decompress_block_dct(quantized, qm):
    """Decompress DCT block."""
    dct_block = quantized * qm
    block = idct(idct(dct_block.T, norm='ortho').T, norm='ortho')
    return block

# Example: compress 8x8 image block
np.random.seed(42)
block = np.random.rand(8, 8) * 255

for quality in [10, 50, 90]:
    q, qm, ratio = compress_block_dct(block, quality)
    reconstructed = decompress_block_dct(q, qm)
    mse = np.mean((block - reconstructed) ** 2)
    psnr = 10 * np.log10(255**2 / mse) if mse > 0 else float('inf')
    print(f"Quality {quality:2d}: ratio = {ratio:.2f}x, PSNR = {psnr:.1f} dB")

CHAPTER 5: CHANNEL CAPACITY AND NOISE
Shannon's Channel Capacity Theorem
# Channel capacity C: maximum reliable communication rate.
# For AWGN channel: C = B * log2(1 + SNR) bits/sec
# where B = bandwidth (Hz), SNR = signal-to-noise ratio

def channel_capacity(bandwidth_hz, snr_db):
    """Shannon capacity for AWGN channel."""
    snr_linear = 10 ** (snr_db / 10)
    return bandwidth_hz * math.log2(1 + snr_linear)

# Example: WiFi channel
B = 20e6  # 20 MHz bandwidth
for snr in [0, 10, 20, 30, 40]:
    C = channel_capacity(B, snr)
    print(f"SNR = {snr:2d} dB: C = {C/1e6:.1f} Mbps")

# Binary Symmetric Channel (BSC)
# Capacity: C = 1 - H(p) where p = crossover probability
def bsc_capacity(crossover_prob):
    """Capacity of binary symmetric channel."""
    return 1 - binary_entropy(crossover_prob)

print("\nBinary Symmetric Channel capacity:")
for p in [0.0, 0.01, 0.1, 0.2, 0.5]:
    C = bsc_capacity(p)
    print(f"  p = {p:.2f}: C = {C:.3f} bits/use")

# Erasure channel
# Capacity: C = 1 - p where p = erasure probability
def erasure_capacity(erasure_prob):
    return 1 - erasure_prob

print("\nBinary Erasure Channel capacity:")
for p in [0.0, 0.1, 0.5, 0.9, 1.0]:
    C = erasure_capacity(p)
    print(f"  p = {p:.2f}: C = {C:.3f} bits/use")

Simulating Noisy Channels
import numpy as np

class BinarySymmetricChannel:
    """Binary symmetric channel with crossover probability p."""
    
    def __init__(self, crossover_prob):
        self.p = crossover_prob
    
    def transmit(self, bits):
        """Transmit bits through noisy channel."""
        bits = np.array(bits, dtype=int)
        errors = np.random.random(len(bits)) < self.p
        received = bits.copy()
        received[errors] = 1 - received[errors]
        return received, errors

class BinaryErasureChannel:
    """Binary erasure channel with erasure probability p."""
    
    def __init__(self, erasure_prob):
        self.p = erasure_prob
    
    def transmit(self, bits):
        """Transmit bits, some are erased (marked as -1)."""
        bits = np.array(bits, dtype=int)
        erasures = np.random.random(len(bits)) < self.p
        received = bits.copy()
        received[erasures] = -1  # Erased
        return received, erasures

class AWGNChannel:
    """Additive White Gaussian Noise channel."""
    
    def __init__(self, snr_db):
        self.snr_linear = 10 ** (snr_db / 10)
    
    def transmit_bpsk(self, bits):
        """Transmit BPSK-modulated bits through AWGN."""
        # BPSK: 0 → -1, 1 → +1
        symbols = 2 * np.array(bits, dtype=float) - 1
        
        # Noise power = signal_power / SNR
        noise_power = 1.0 / self.snr_linear
        noise = np.sqrt(noise_power) * np.random.randn(len(bits))
        
        received = symbols + noise
        return received

# Example: simulate BSC
channel = BinarySymmetricChannel(crossover_prob=0.1)
original = np.random.randint(0, 2, 1000)
received, errors = channel.transmit(original)
ber = np.mean(errors)
print(f"\nBSC (p=0.1): Bit Error Rate = {ber:.3f} (expected ≈ 0.1)")

# Example: simulate AWGN with BPSK
channel = AWGNChannel(snr_db=10)
received = channel.transmit_bpsk(original)
detected = (received > 0).astype(int)
ber = np.mean(detected != original)
print(f"AWGN (SNR=10dB, BPSK): BER = {ber:.5f}")

CHAPTER 6: LINEAR BLOCK CODES
Hamming Codes
# Hamming codes: single-error-correcting codes.
# Hamming(7,4): 4 data bits → 7 bit codeword (3 parity bits).
# Can correct 1 error, detect 2 errors.

import numpy as np

class HammingCode:
    """Hamming(7,4) code implementation."""
    
    def __init__(self):
        # Generator matrix G (4x7)
        self.G = np.array([
            [1, 0, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1]
        ], dtype=int)
        
        # Parity check matrix H (3x7)
        self.H = np.array([
            [1, 1, 0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 0, 0, 1]
        ], dtype=int)
        
        # Syndrome to error position mapping
        self.syndrome_map = {
            (0, 0, 0): -1,  # No error
            (1, 1, 0): 0, (1, 0, 1): 1, (0, 1, 1): 2,
            (1, 1, 1): 3, (1, 0, 0): 4, (0, 1, 0): 5, (0, 0, 1): 6
        }
    
    def encode(self, data_bits):
        """Encode 4 data bits to 7-bit codeword."""
        data = np.array(data_bits, dtype=int)
        codeword = (data @ self.G) % 2
        return codeword
    
    def syndrome(self, received):
        """Compute syndrome (error indicator)."""
        r = np.array(received, dtype=int)
        s = (self.H @ r) % 2
        return tuple(s)
    
    def decode(self, received):
        """Decode 7-bit received word, correcting 1 error."""
        r = np.array(received, dtype=int)
        s = self.syndrome(r)
        
        error_pos = self.syndrome_map.get(s, -1)
        
        if error_pos >= 0:
            r[error_pos] ^= 1  # Flip error bit
            corrected = True
        else:
            corrected = False
        
        # Extract data bits (first 4)
        data = r[:4]
        return data, corrected, error_pos

# Example
hamming = HammingCode()
data = [1, 0, 1, 1]
codeword = hamming.encode(data)
print(f"\nHamming(7,4) encoding:")
print(f"Data:     {data}")
print(f"Codeword: {codeword}")

# Simulate single error
received = codeword.copy()
received[3] ^= 1  # Flip bit 3
print(f"Received (error at pos 3): {received}")

decoded, corrected, error_pos = hamming.decode(received)
print(f"Decoded: {decoded}, Corrected: {corrected}, Error at: {error_pos}")

# Test all single errors
print("\nTesting all single-error patterns:")
for pos in range(7):
    received = codeword.copy()
    received[pos] ^= 1
    decoded, corrected, err = hamming.decode(received)
    status = "✓" if np.array_equal(decoded, data) else "✗"
    print(f"  Error at {pos}: {status} (decoded={decoded}, err_pos={err})")

# Code rate and efficiency
rate = 4 / 7
print(f"\nCode rate: {rate:.3f} (4 data bits / 7 total bits)")
print(f"Redundancy: {(1-rate)*100:.1f}%")

Extended Hamming Code (SECDED)
# SECDED: Single Error Correction, Double Error Detection.
# Adds one overall parity bit to Hamming code.
# Hamming(8,4): 4 data + 3 parity + 1 overall parity

class ExtendedHammingCode:
    """Hamming(8,4) SECDED code."""
    
    def __init__(self):
        self.hamming = HammingCode()
    
    def encode(self, data_bits):
        """Encode to 8-bit codeword."""
        codeword = self.hamming.encode(data_bits)
        # Add overall parity bit
        parity = np.sum(codeword) % 2
        return np.append(codeword, parity)
    
    def decode(self, received):
        """Decode 8-bit received word."""
        r = np.array(received, dtype=int)
        overall_parity = np.sum(r) % 2
        syndrome = self.hamming.syndrome(r[:7])
        
        if overall_parity == 0 and syndrome == (0, 0, 0):
            # No error
            return r[:4], "no_error", -1
        elif overall_parity == 1 and syndrome != (0, 0, 0):
            # Single error (correctable)
            error_pos = self.hamming.syndrome_map.get(syndrome, -1)
            if error_pos >= 0:
                r[error_pos] ^= 1
                return r[:4], "corrected", error_pos
        elif overall_parity == 0 and syndrome != (0, 0, 0):
            # Double error (detectable, not correctable)
            return r[:4], "double_error", -1
        else:
            # Overall parity error only (error in parity bit)
            return r[:4], "parity_error", 7

# Example
ext_hamming = ExtendedHammingCode()
data = [1, 0, 1, 1]
codeword = ext_hamming.encode(data)
print(f"\nExtended Hamming(8,4):")
print(f"Data:     {data}")
print(f"Codeword: {codeword}")

# Test single error
received = codeword.copy()
received[2] ^= 1
decoded, status, pos = ext_hamming.decode(received)
print(f"Single error at 2: {status}, decoded={decoded}")

# Test double error
received = codeword.copy()
received[1] ^= 1
received[4] ^= 1
decoded, status, pos = ext_hamming.decode(received)
print(f"Double error: {status}, decoded={decoded}")

CHAPTER 7: CYCLIC AND BCH CODES
Cyclic Redundancy Check (CRC)
# CRC: polynomial-based error detection code.
# Widely used in networks, storage (Ethernet, ZIP, PNG).
# Generator polynomial determines error detection capability.

class CRC:
    """CRC implementation using polynomial division."""
    
    def __init__(self, generator_poly):
        """
        generator_poly: list of coefficients, e.g., [1,0,1,1] for x³+x+1
        """
        self.generator = generator_poly
        self.degree = len(generator_poly) - 1
    
    def _poly_div(self, dividend, divisor):
        """Polynomial division over GF(2)."""
        dividend = dividend.copy()
        divisor_degree = len(divisor) - 1
        
        for i in range(len(dividend) - divisor_degree):
            if dividend[i] == 1:
                for j in range(len(divisor)):
                    dividend[i + j] ^= divisor[j]
        
        return dividend[-divisor_degree:]
    
    def compute_crc(self, data_bits):
        """Compute CRC for data bits."""
        # Append zeros equal to degree
        padded = np.array(data_bits + [0] * self.degree, dtype=int)
        remainder = self._poly_div(padded, self.generator)
        return remainder
    
    def encode(self, data_bits):
        """Encode data with CRC appended."""
        crc = self.compute_crc(data_bits)
        return np.concatenate([data_bits, crc])
    
    def check(self, received):
        """Check if received codeword is valid."""
        remainder = self._poly_div(np.array(received, dtype=int), self.generator)
        return np.all(remainder == 0)

# Common CRC polynomials
CRC4_ITU = [1, 0, 0, 1, 1]           # x⁴+x+1
CRC8_CCITT = [1, 0, 0, 0, 0, 0, 1, 1, 1]  # x⁸+x²+x+1 (simplified)
CRC16_CCITT = [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]  # x¹⁶+x¹²+x⁵+1

# Example with CRC-4
crc = CRC(CRC4_ITU)
data = [1, 1, 0, 1, 0, 1, 1, 0]
encoded = crc.encode(data)
print(f"\nCRC-4 encoding:")
print(f"Data:    {data}")
print(f"Encoded: {encoded}")
print(f"Valid: {crc.check(encoded)}")

# Simulate error
received = encoded.copy()
received[3] ^= 1
print(f"With error: {received}")
print(f"Detected: {not crc.check(received)}")

# Test error detection capability
print("\nTesting CRC-4 error detection:")
errors_detected = 0
total_errors = 0
for _ in range(1000):
    # Random error pattern
    error = np.random.randint(0, 2, len(encoded))
    if np.any(error):
        total_errors += 1
        corrupted = (encoded + error) % 2
        if not crc.check(corrupted):
            errors_detected += 1

print(f"Errors detected: {errors_detected}/{total_errors} ({errors_detected/total_errors*100:.1f}%)")

Reed-Solomon Codes
# Reed-Solomon: powerful block code over GF(q).
# Used in: CDs, DVDs, QR codes, deep space communication.
# Can correct up to t = (n-k)/2 symbol errors.

class ReedSolomon:
    """Simplified Reed-Solomon over GF(2^m)."""
    
    def __init__(self, m, t):
        """
        m: bits per symbol (field GF(2^m))
        t: error correction capability
        n = 2^m - 1 (codeword length)
        k = n - 2t (data length)
        """
        self.m = m
        self.t = t
        self.n = 2**m - 1
        self.k = self.n - 2*t
        
        # Build GF(2^m) using primitive polynomial
        self.gf_size = 2**m
        self.gf_exp = [0] * (2 * self.gf_size)
        self.gf_log = [0] * self.gf_size
        self._build_gf()
        
        # Generator polynomial
        self.gen_poly = self._build_generator()
    
    def _build_gf(self):
        """Build GF(2^m) lookup tables."""
        # Primitive polynomial for GF(2^8): x^8 + x^4 + x^3 + x^2 + 1
        prim_poly = 0x11D  # for m=8
        
        x = 1
        for i in range(self.gf_size - 1):
            self.gf_exp[i] = x
            self.gf_log[x] = i
            x <<= 1
            if x >= self.gf_size:
                x ^= prim_poly
                x &= self.gf_size - 1
        
        for i in range(self.gf_size - 1, 2 * self.gf_size):
            self.gf_exp[i] = self.gf_exp[i - (self.gf_size - 1)]
    
    def gf_mul(self, a, b):
        """Multiply in GF(2^m)."""
        if a == 0 or b == 0:
            return 0
        return self.gf_exp[self.gf_log[a] + self.gf_log[b]]
    
    def _build_generator(self):
        """Build generator polynomial g(x) = Π(x - α^i) for i=0..2t-1."""
        g = [1]
        for i in range(2 * self.t):
            # Multiply g(x) by (x - α^i)
            new_g = [0] * (len(g) + 1)
            alpha_i = self.gf_exp[i]
            for j in range(len(g)):
                new_g[j] ^= g[j]  # x * g[j]
                new_g[j + 1] ^= self.gf_mul(g[j], alpha_i)  # -α^i * g[j]
            g = new_g
        return g
    
    def encode(self, data):
        """Encode data symbols (simplified - systematic form)."""
        # Pad data to length k
        if len(data) < self.k:
            data = [0] * (self.k - len(data)) + list(data)
        
        # Compute parity using polynomial division
        # (simplified - real implementation uses shift register)
        parity = [0] * (2 * self.t)
        return data + parity  # Systematic form

# Example
rs = ReedSolomon(m=8, t=4)
print(f"\nReed-Solomon(255, 247):")
print(f"Symbols per codeword: {rs.n}")
print(f"Data symbols: {rs.k}")
print(f"Can correct up to {rs.t} symbol errors")
print(f"Code rate: {rs.k/rs.n:.3f}")

CHAPTER 8: CONVOLUTIONAL CODES AND VITERBI
Convolutional Codes
# Convolutional codes: encode data using sliding window.
# Characterized by (n, k, K): n output bits, k input bits, K constraint length.
# Used in: GSM, satellite, WiFi (with Viterbi decoding).

class ConvolutionalEncoder:
    """Rate 1/2, K=3 convolutional encoder."""
    
    def __init__(self):
        # Generator polynomials (octal): g1=7 (111), g2=5 (101)
        self.g1 = [1, 1, 1]
        self.g2 = [1, 0, 1]
        self.state = [0, 0]  # 2 memory elements
    
    def reset(self):
        self.state = [0, 0]
    
    def encode_bit(self, bit):
        """Encode single bit, return 2 output bits."""
        # Shift register: [bit, state[0], state[1]]
        shift_reg = [bit] + self.state
        
        # Compute outputs via XOR
        out1 = sum(a & b for a, b in zip(shift_reg, self.g1)) % 2
        out2 = sum(a & b for a, b in zip(shift_reg, self.g2)) % 2
        
        # Update state
        self.state = [bit, self.state[0]]
        
        return out1, out2
    
    def encode(self, data_bits):
        """Encode sequence of bits."""
        self.reset()
        encoded = []
        for bit in data_bits:
            out1, out2 = self.encode_bit(bit)
            encoded.extend([out1, out2])
        
        # Tail bits (flush encoder to zero state)
        for _ in range(2):
            out1, out2 = self.encode_bit(0)
            encoded.extend([out1, out2])
        
        return encoded

# Example
encoder = ConvolutionalEncoder()
data = [1, 0, 1, 1, 0]
encoded = encoder.encode(data)
print(f"\nConvolutional encoding (rate 1/2, K=3):")
print(f"Data:    {data}")
print(f"Encoded: {encoded}")
print(f"Rate: {len(data)}/{len(encoded)} = {len(data)/len(encoded):.2f}")

Viterbi Decoder
# Viterbi algorithm: maximum likelihood sequence estimation.
# Finds most likely input sequence given received (noisy) sequence.
# Uses trellis diagram and dynamic programming.

class ViterbiDecoder:
    """Viterbi decoder for rate 1/2, K=3 convolutional code."""
    
    def __init__(self):
        self.g1 = [1, 1, 1]
        self.g2 = [1, 0, 1]
        self.num_states = 4  # 2^(K-1) = 2^2
    
    def _branch_output(self, state, input_bit):
        """Compute expected output for given state and input."""
        shift_reg = [input_bit, (state >> 1) & 1, state & 1]
        out1 = sum(a & b for a, b in zip(shift_reg, self.g1)) % 2
        out2 = sum(a & b for a, b in zip(shift_reg, self.g2)) % 2
        next_state = ((input_bit << 1) | ((state >> 1) & 1)) & 0x3
        return next_state, (out1, out2)
    
    def _hamming_distance(self, a, b):
        """Hamming distance between two 2-bit sequences."""
        return (a[0] != b[0]) + (a[1] != b[1])
    
    def decode(self, received):
        """Viterbi decoding of received sequence."""
        n_symbols = len(received) // 2
        
        # Initialize path metrics
        path_metric = [float('inf')] * self.num_states
        path_metric[0] = 0  # Start at state 0
        
        # Survivor paths
        survivors = [[] for _ in range(self.num_states)]
        
        for t in range(n_symbols):
            received_pair = (received[2*t], received[2*t+1])
            
            new_metric = [float('inf')] * self.num_states
            new_survivors = [[] for _ in range(self.num_states)]
            
            for state in range(self.num_states):
                if path_metric[state] == float('inf'):
                    continue
                
                for input_bit in [0, 1]:
                    next_state, expected = self._branch_output(state, input_bit)
                    distance = self._hamming_distance(received_pair, expected)
                    metric = path_metric[state] + distance
                    
                    if metric < new_metric[next_state]:
                        new_metric[next_state] = metric
                        new_survivors[next_state] = survivors[state] + [input_bit]
            
            path_metric = new_metric
            survivors = new_survivors
        
        # Find best final state (state 0 for terminated trellis)
        best_state = 0
        best_path = survivors[best_state]
        
        # Remove tail bits
        return best_path[:-2]

# Example: encode, add errors, decode
encoder = ConvolutionalEncoder()
data = [1, 0, 1, 1, 0]
encoded = encoder.encode(data)

# Simulate channel errors
import numpy as np
noisy = encoded.copy()
error_positions = [2, 7]  # Flip bits at positions 2 and 7
for pos in error_positions:
    noisy[pos] ^= 1

print(f"\nViterbi decoding:")
print(f"Original data: {data}")
print(f"Encoded:       {encoded}")
print(f"Noisy:         {noisy}")
print(f"Errors at:     {error_positions}")

decoder = ViterbiDecoder()
decoded = decoder.decode(noisy)
print(f"Decoded:       {decoded}")
print(f"Correct:       {decoded == data}")

CHAPTER 9: MODERN CODES (TURBO, LDPC, POLAR)
Turbo Codes
# Turbo codes: parallel concatenation of two convolutional codes.
# Near-Shannon-limit performance with iterative decoding.
# Used in: 3G, 4G LTE, satellite.

class TurboEncoder:
    """Simplified turbo encoder (rate 1/3)."""
    
    def __init__(self):
        self.enc1 = ConvolutionalEncoder()
        self.enc2 = ConvolutionalEncoder()
    
    def _interleave(self, data):
        """Block interleaver (reorders bits)."""
        n = len(data)
        # Simple row-column interleaver
        rows = int(np.sqrt(n))
        cols = (n + rows - 1) // rows
        interleaved = []
        for c in range(cols):
            for r in range(rows):
                idx = r * cols + c
                if idx < n:
                    interleaved.append(data[idx])
        return interleaved
    
    def encode(self, data):
        """Encode data with turbo code."""
        # Systematic bits
        systematic = data
        
        # Parity 1: from encoder 1
        parity1 = self.enc1.encode(data)[::2]  # Take every other bit
        
        # Interleave data
        interleaved = self._interleave(data)
        
        # Parity 2: from encoder 2 on interleaved data
        parity2 = self.enc2.encode(interleaved)[::2]
        
        # Multiplex: systematic, parity1, parity2
        codeword = []
        for i in range(len(systematic)):
            codeword.extend([systematic[i], parity1[i], parity2[i]])
        
        return codeword

# Example
turbo = TurboEncoder()
data = [1, 0, 1, 1, 0, 1, 0, 0]
encoded = turbo.encode(data)
print(f"\nTurbo encoding (rate 1/3):")
print(f"Data:    {data} ({len(data)} bits)")
print(f"Encoded: {len(encoded)} bits")
print(f"Rate: {len(data)/len(encoded):.3f}")

LDPC Codes
# LDPC (Low-Density Parity-Check): sparse parity-check matrix.
# Near-Shannon-limit, used in: WiFi (802.11n/ac), DVB-S2, 5G, SSDs.
# Decoded with belief propagation (message passing).

class LDPCCode:
    """Simple LDPC code with regular structure."""
    
    def __init__(self, n, k, dv, dc):
        """
        n: codeword length
        k: data length
        dv: column weight (variable node degree)
        dc: row weight (check node degree)
        """
        self.n = n
        self.k = k
        self.dv = dv
        self.dc = dc
        self.m = n - k  # Number of parity checks
        
        # Build sparse parity-check matrix H
        self.H = self._build_parity_matrix()
    
    def _build_parity_matrix(self):
        """Build regular LDPC parity-check matrix."""
        H = np.zeros((self.m, self.n), dtype=int)
        
        # Simple construction: each column has dv ones
        for j in range(self.n):
            positions = np.random.choice(self.m, self.dv, replace=False)
            H[positions, j] = 1
        
        # Ensure each row has dc ones (approximately)
        return H
    
    def encode(self, data):
        """Encode data (simplified - systematic form)."""
        data = np.array(data, dtype=int)
        # Compute parity bits: H * codeword = 0 (mod 2)
        # Systematic: codeword = [data, parity]
        # Simplified: just append random parity (real implementation uses Gaussian elimination)
        parity = np.random.randint(0, 2, self.m)
        return np.concatenate([data, parity])
    
    def decode_bp(self, received, max_iter=10):
        """Belief propagation decoding (simplified)."""
        n = len(received)
        received = np.array(received, dtype=float)
        
        # Initialize log-likelihood ratios (LLRs)
        llr = np.zeros(n)
        for i in range(n):
            if received[i] > 0.5:
                llr[i] = 1.0
            else:
                llr[i] = -1.0
        
        # Message passing iterations
        for iteration in range(max_iter):
            # Check-to-variable messages
            # Variable-to-check messages
            # (simplified - real implementation tracks all messages)
            
            # Hard decision
            decoded = (llr > 0).astype(int)
            
            # Check if valid codeword
            syndrome = (self.H @ decoded) % 2
            if np.all(syndrome == 0):
                return decoded[:self.k], True, iteration + 1
        
        return decoded[:self.k], False, max_iter

# Example
ldpc = LDPCCode(n=20, k=10, dv=3, dc=6)
data = np.random.randint(0, 2, 10)
encoded = ldpc.encode(data)
print(f"\nLDPC encoding:")
print(f"Data:    {data}")
print(f"Encoded: {encoded}")
print(f"Rate: {ldpc.k}/{ldpc.n} = {ldpc.k/ldpc.n:.3f}")

Polar Codes
# Polar codes: first provably capacity-achieving codes.
# Invented by Erdal Arıkan (2009).
# Used in: 5G control channels.

class PolarCode:
    """Simplified polar code encoder."""
    
    def __init__(self, N, K):
        """
        N: codeword length (must be power of 2)
        K: number of information bits
        """
        self.N = N
        self.K = K
        self.n = int(np.log2(N))
        
        # Determine frozen and information bit positions
        # (simplified - real implementation uses channel polarization analysis)
        self.frozen_positions = self._select_frozen_bits()
    
    def _select_frozen_bits(self):
        """Select N-K least reliable bit positions as frozen."""
        # Simplified: choose first N-K positions
        return list(range(self.N - self.K))
    
    def _polar_transform(self, u):
        """Apply polar transform: x = u * F^{⊗n}."""
        x = u.copy()
        for i in range(self.n):
            half = 2 ** i
            for j in range(0, self.N, 2 * half):
                for k in range(half):
                    x[j + k] ^= x[j + k + half]
        return x
    
    def encode(self, data):
        """Encode K information bits to N-bit codeword."""
        u = np.zeros(self.N, dtype=int)
        
        # Place information bits in reliable positions
        info_positions = [i for i in range(self.N) if i not in self.frozen_positions]
        for i, pos in enumerate(info_positions[:self.K]):
            u[pos] = data[i]
        
        # Frozen bits set to 0 (already done)
        
        # Apply polar transform
        return self._polar_transform(u)

# Example
polar = PolarCode(N=8, K=4)
data = [1, 0, 1, 1]
encoded = polar.encode(data)
print(f"\nPolar encoding (N=8, K=4):")
print(f"Data:    {data}")
print(f"Encoded: {encoded}")
print(f"Rate: {polar.K}/{polar.N} = {polar.K/polar.N:.3f}")

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Information Theory in Machine Learning
# Cross-entropy loss: L = -Σ y_true * log(y_pred)
# KL divergence: measure difference between distributions
# Mutual information: feature selection, representation learning

import numpy as np

def cross_entropy(y_true, y_pred):
    """Cross-entropy loss for classification."""
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.sum(y_true * np.log(y_pred)) / len(y_true)

# Example
y_true = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
y_pred = np.array([[0.9, 0.05, 0.05], [0.1, 0.8, 0.1], [0.2, 0.3, 0.5]])
loss = cross_entropy(y_true, y_pred)
print(f"Cross-entropy loss: {loss:.4f}")

# Mutual information for feature selection
def mutual_information_features(X, y):
    """Estimate MI between each feature and target."""
    n_features = X.shape[1]
    mi_scores = np.zeros(n_features)
    
    for i in range(n_features):
        # Discretize feature
        x_disc = np.digitize(X[:, i], bins=np.linspace(X[:, i].min(), X[:, i].max(), 10))
        
        # Compute joint and marginal distributions
        joint = np.zeros((10, len(np.unique(y))))
        for xi, yi in zip(x_disc, y):
            joint[xi, yi] += 1
        joint /= joint.sum()
        
        px = joint.sum(axis=1)
        py = joint.sum(axis=0)
        
        # MI = Σ p(x,y) log(p(x,y) / (p(x)*p(y)))
        mi = 0
        for xi in range(10):
            for yi in range(len(np.unique(y))):
                if joint[xi, yi] > 0 and px[xi] > 0 and py[yi] > 0:
                    mi += joint[xi, yi] * np.log2(joint[xi, yi] / (px[xi] * py[yi]))
        
        mi_scores[i] = mi
    
    return mi_scores

# Example
np.random.seed(42)
X = np.random.randn(100, 3)
y = (X[:, 0] > 0).astype(int)  # Only feature 0 is informative

mi_scores = mutual_information_features(X, y)
print(f"\nMutual information scores:")
for i, mi in enumerate(mi_scores):
    print(f"  Feature {i}: {mi:.3f} bits")

Channel Coding in Modern Systems
# 5G NR: LDPC for data, Polar for control
# WiFi 6/7: LDPC (optional), BCC (backward compatible)
# DVB-S2: LDPC + BCH
# Deep space: Turbo, LDPC
# Storage (SSD, HDD): LDPC

# Performance comparison (approximate SNR for BER=10^-5):
# Uncoded BPSK: 9.6 dB
# Hamming(7,4): 5.5 dB (coding gain ~4 dB)
# Convolutional K=7: 4.5 dB (coding gain ~5 dB)
# Turbo code: 0.7 dB (near Shannon limit!)
# LDPC: 0.5 dB (near Shannon limit)
# Polar: 0.6 dB (near Shannon limit)

Recommended Reading
# - "Elements of Information Theory" by Cover & Thomas
# - "Information Theory, Inference, and Learning Algorithms" by David MacKay (free online)
# - "Error Control Coding" by Lin & Costello
# - "Modern Coding Theory" by Richardson & Urbanke
# - "Channel Codes: Classical and Modern" by Ryan

# Online Resources
# - Pyitpp: https://github.com/veeresht/CommPy
# - SciPy communications: https://docs.scipy.org/
# - GNU Radio: https://www.gnuradio.org/
# - 3GPP standards: https://www.3gpp.org/

# End of Information Theory & Coding Reference