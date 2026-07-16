Cryptography Engineering & Hardware Security Complete Reference
CHAPTER 1: GETTING STARTED WITH CRYPTOGRAPHY ENGINEERING
Remarks
Cryptography engineering focuses on the practical implementation of cryptographic algorithms, ensuring they are secure against real-world attacks (side-channels, fault injection, timing attacks) rather than just theoretical breaks. It bridges the gap between mathematical theory and hardware/software reality. Key areas: Side-Channel Analysis (SCA), Fault Injection, Secure Enclaves (TPM, HSM, SGX), Constant-Time Programming, and Hardware Trojans.
Tools: Python (for analysis), C/C++ (implementation), ChipWhisperer (SCA hardware), OpenOCD/JTAG (debugging), QEMU (emulation), Verilator (hardware simulation).
Hello Crypto Engineering
# hello_crypto_eng.py
"""
First crypto engineering program: Demonstrate timing attack vulnerability.
"""
import time
import secrets
import string

def insecure_compare(secret: str, guess: str) -> bool:
    """VULNERABLE: String comparison that leaks timing information."""
    if len(secret) != len(guess):
        return False
    for i in range(len(secret)):
        if secret[i] != guess[i]:
            return False  # Returns early! Attacker measures time to find correct char.
    return True

def secure_compare(secret: str, guess: str) -> bool:
    """SECURE: Constant-time comparison."""
    if len(secret) != len(guess):
        return False
    result = 0
    for s, g in zip(secret, guess):
        result |= ord(s) ^ ord(g)  # XOR all bytes, accumulate differences
    return result == 0

def simulate_timing_attack(secret: str, charset: str = string.ascii_lowercase + string.digits):
    """Simulate a simple timing attack to recover the secret."""
    recovered = ""
    for i in range(len(secret)):
        best_char = None
        max_time = 0
        
        for c in charset:
            guess = recovered + c + "x" * (len(secret) - len(recovered) - 1)
            
            # Measure average time over many runs to reduce noise
            times = []
            for _ in range(100):
                start = time.perf_counter_ns()
                insecure_compare(secret, guess)
                end = time.perf_counter_ns()
                times.append(end - start)
            
            avg_time = sum(times) / len(times)
            
            if avg_time > max_time:
                max_time = avg_time
                best_char = c
        
        recovered += best_char
        print(f"Step {i+1}: Recovered '{recovered}' (time diff: {max_time:.0f}ns)")
        
    return recovered

# Demo
TARGET_SECRET = "a3f9b2"
print(f"Target Secret: {TARGET_SECRET}")
print("\n--- Insecure Comparison Timing Attack ---")
recovered = simulate_timing_attack(TARGET_SECRET)
print(f"Recovered:     {recovered}")
print(f"Match:         {recovered == TARGET_SECRET}")

print("\n--- Secure Comparison Test ---")
# Secure compare should take same time regardless of correctness
t1 = time.perf_counter_ns()
secure_compare(TARGET_SECRET, "wrong!")
t2 = time.perf_counter_ns()
t3 = time.perf_counter_ns()
secure_compare(TARGET_SECRET, TARGET_SECRET)
t4 = time.perf_counter_ns()
print(f"Time for wrong guess: {t2-t1} ns")
print(f"Time for right guess: {t4-t3} ns")
print("(Times should be nearly identical)")

CHAPTER 2: SIDE-CHANNEL ANALYSIS (SCA)
Power Analysis Attacks
# Simple Power Analysis (SPA): Visual inspection of power traces.
# Differential Power Analysis (DPA): Statistical analysis of many traces.
# Correlation Power Analysis (CPA): Correlate hypothetical power model with actual traces.

import numpy as np
import matplotlib.pyplot as plt

def generate_mock_power_trace(data_byte: int, num_samples=1000, noise_level=0.1):
    """Generate a mock power trace for a single AES S-Box operation."""
    # Hamming Weight model: Power consumption proportional to number of 1s in data
    hamming_weight = bin(data_byte).count('1')
    
    # Base signal: A spike corresponding to the operation
    signal = np.zeros(num_samples)
    center = num_samples // 2
    width = 50
    x = np.arange(num_samples)
    signal += hamming_weight * np.exp(-((x - center)**2) / (2 * width**2))
    
    # Add noise
    noise = np.random.normal(0, noise_level, num_samples)
    return signal + noise

def perform_cpa(traces: np.ndarray, plaintexts: np.ndarray, key_guess_range: range):
    """Simplified Correlation Power Analysis."""
    num_traces, num_samples = traces.shape
    max_corr = np.zeros(256)
    
    # S-Box lookup (AES)
    sbox = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ]
    
    # For each key guess
    for k_guess in key_guess_range:
        # Hypothetical power consumption (Hamming Weight of S-Box output)
        hyp_power = np.array([bin(sbox[p ^ k_guess]).count('1') for p in plaintexts])
        
        # Correlate with each sample point in traces
        # Simplified: Just check the peak correlation for demo
        corr_matrix = np.corrcoef(hyp_power, traces.T) 
        # Take max absolute correlation across all time samples for this key guess
        max_corr[k_guess] = np.max(np.abs(corr_matrix[0, 1:]))
        
    return max_corr

# Demo CPA
NUM_TRACES = 1000
TRACE_LEN = 1000
TRUE_KEY = 0xAB

plaintexts = np.random.randint(0, 256, NUM_TRACES)
traces = np.array([generate_mock_power_trace(sbox[p ^ TRUE_KEY], TRACE_LEN) for p in plaintexts])

print("\n--- Correlation Power Analysis (CPA) Demo ---")
correlations = perform_cpa(traces, plaintexts, range(256))

best_key_guess = np.argmax(correlations)
print(f"True Key:      0x{TRUE_KEY:02X}")
print(f"Guessed Key:   0x{best_key_guess:02X}")
print(f"Correlation:   {correlations[best_key_guess]:.4f}")

# Plot top 10 correlations
top_keys = np.argsort(correlations)[-10:]
plt.figure(figsize=(10, 5))
plt.bar(range(10), correlations[top_keys])
plt.xticks(range(10), [f"0x{k:02X}" for k in top_keys])
plt.title("Top 10 Key Guesses by Correlation")
plt.xlabel("Key Guess")
plt.ylabel("Max Correlation Coefficient")
plt.tight_layout()
plt.show()

Electromagnetic (EM) Analysis
# Similar to power analysis but uses EM probes.
# Higher spatial resolution: can target specific parts of the chip.
# Non-invasive: No need to modify the device or measure power lines.

# Fault Injection
# Glitching: Voltage glitch, clock glitch, laser fault injection.
# Goal: Skip instructions, corrupt memory, bypass security checks.

class FaultInjector:
    """Simulator for instruction skip faults."""
    
    def __init__(self, code: list):
        self.original_code = code[:]
        self.code = code[:]
        self.fault_injected = False
        
    def inject_skip_fault(self, line_index: int):
        """Replace an instruction with NOP (No Operation)."""
        if 0 <= line_index < len(self.code):
            self.code[line_index] = "NOP"
            self.fault_injected = True
            print(f"Fault injected at line {line_index}: '{self.original_code[line_index]}' -> 'NOP'")
    
    def run(self):
        """Execute the (possibly faulty) code."""
        pc = 0
        registers = {'R0': 0, 'R1': 0, 'RESULT': 0}
        
        while pc < len(self.code):
            instr = self.code[pc]
            
            if instr == "NOP":
                pass
            elif instr.startswith("MOV"):
                _, reg, val = instr.split()
                registers[reg] = int(val)
            elif instr.startswith("ADD"):
                _, dest, src1, src2 = instr.split()
                registers[dest] = registers[src1] + registers[src2]
            elif instr.startswith("CHECK_SECURITY"):
                # Simulated security check
                if registers['R0'] != 1234:
                    return "ACCESS DENIED"
            elif instr.startswith("GRANT_ACCESS"):
                return "ACCESS GRANTED"
            
            pc += 1
            
        return "EXECUTION FINISHED"

# Demo Fault Injection
code = [
    "MOV R0 1234",       # Load secret key
    "CHECK_SECURITY",    # Check if R0 is correct
    "GRANT_ACCESS",      # If yes, grant access
    "MOV R1 0",          # Cleanup
]

injector = FaultInjector(code)
print("\n--- Fault Injection Demo ---")
print("Normal Execution:")
result = injector.run()
print(f"Result: {result}")

# Reset and inject fault
injector.code = injector.original_code[:]
injector.inject_skip_fault(1)  # Skip the security check!
print("\nFaulty Execution:")
result = injector.run()
print(f"Result: {result}")  # Should be ACCESS GRANTED despite wrong/no key setup if check skipped

CHAPTER 3: CONSTANT-TIME PROGRAMMING
Timing Attack Mitigation
# Rule 1: No data-dependent branches.
# Rule 2: No data-dependent memory accesses (cache timing).
# Rule 3: Use constant-time libraries for crypto ops.

def constant_time_select(condition: int, a: int, b: int) -> int:
    """Select a if condition is 0, else b. Constant time."""
    # condition must be 0 or 1
    mask = -condition  # If cond=1, mask=-1 (all 1s). If cond=0, mask=0.
    return (a & ~mask) | (b & mask)

def constant_time_lookup(table: list, index: int) -> int:
    """Lookup in table without cache timing leaks (simplified)."""
    # In real hardware, this is hard. Often use bit-slicing or masked loads.
    # This is a software approximation: read ALL elements, select one.
    result = 0
    for i, val in enumerate(table):
        # If i == index, select val, else select 0 (or keep result)
        # This is still vulnerable to cache effects in complex CPUs, 
        # but better than direct indexing for simple cases.
        mask = -(i == index)
        result = (result & ~mask) | (val & mask)
    return result

# Example: AES S-Box constant-time lookup (conceptual)
AES_SBOX = [0x63, 0x7c, 0x77, ...] # Full 256 entries

def aes_sub_bytes_constant_time(state: list) -> list:
    new_state = []
    for byte in state:
        # Instead of new_state.append(AES_SBOX[byte]), use constant-time lookup
        new_state.append(constant_time_lookup(AES_SBOX, byte))
    return new_state

Cache Timing Attacks
# Prime+Probe: Attacker fills cache, victim runs, attacker checks which lines were evicted.
# Flush+Reload: Attacker flushes cache line, victim runs, attacker reloads and measures time.
# Mitigation: Cache partitioning, randomization, constant-time code.

CHAPTER 4: SECURE ENCLAVES & HARDWARE SECURITY MODULES
Trusted Platform Module (TPM)
# Dedicated microcontroller for secure crypto operations.
# Stores keys, performs RSA/ECC, measures boot process (PCRs).
# Commands via TSS (TCG Software Stack).

# Example: Using tpm2-tools (command line)
"""
# Create a primary key
tpm2_createprimary -C e -c primary.ctx

# Create a signing key under the primary
tpm2_create -C primary.ctx -u pub.key -r priv.key

# Sign data
echo "Hello TPM" > data.txt
tpm2_sign -c primary.ctx -g sha256 -o sig.bin data.txt

# Verify signature
tpm2_verify -c primary.ctx -g sha256 -s sig.bin data.txt
"""

Hardware Security Module (HSM)
# Physical device for managing digital keys and performing crypto.
# FIPS 140-2/3 certified.
# Used in banking, CA root keys, cloud KMS.
# Interfaces: PKCS#11, JCE, CAPI.

Intel SGX / AMD SEV
# Trusted Execution Environment (TEE).
# Creates encrypted enclaves in memory.
# Code and data protected from OS/Hypervisor.
# Remote attestation proves code integrity.

# SGX Development Model:
# 1. Define enclave.edl (interface)
# 2. Write enclave code (C/C++)
# 3. Sign enclave with private key
# 4. Application loads enclave via SDK

# Example SGX Enclave Interface (enclave.edl)
"""
enclave {
    trusted {
        public void ecall_add(int a, int b, [out, size=4] int* result);
        public void ecall_seal_data([in, size=data_size] const uint8_t* data, size_t data_size,
                                    [out, size=*sealed_size] uint8_t* sealed_blob, size_t* sealed_size);
    };
    untrusted {
        void ocall_print_string([in, string] const char* str);
    };
};
"""

CHAPTER 5: SECURE BOOT & ROOT OF TRUST
Secure Boot Chain
# 1. ROM Code (Immutable): Verifies Bootloader signature.
# 2. Bootloader (U-Boot, GRUB): Verifies Kernel signature.
# 3. Kernel: Verifies Initramfs/Modules.
# 4. User Space: Verifies Applications (optional).

# Each step measures the next component into TPM PCRs.
# If any signature fails, boot halts.

# UEFI Secure Boot:
# Uses Platform Key (PK), Key Exchange Key (KEK), Signature Database (db).
# Only signed EFI binaries allowed.

Root of Trust for Measurement (RTM)
# Core Root of Trust for Measurement (CRTM): Static (SRTM) or Dynamic (DRTM).
# SRTM: BIOS/UEFI measures everything.
# DRTM: Late launch (e.g., Intel TXT) creates isolated environment after boot.

CHAPTER 6: PHYSICAL UNCLONABLE FUNCTIONS (PUFs)
PUF Basics
# Hardware fingerprint based on manufacturing variations.
# Challenge-Response Pair (CRP).
# Types: Arbiter PUF, Ring Oscillator PUF, SRAM PUF.

class SRAM_PUF:
    """Simulated SRAM PUF based on startup values."""
    
    def __init__(self, size=128):
        # In real hardware, this is fixed by physics. Here, we fix it randomly once.
        self.fingerprint = [secrets.randbits(1) for _ in range(size)]
        
    def get_response(self, challenge: int) -> list:
        """Simple PUF: Return fingerprint bits indexed by challenge."""
        # Real PUFs are more complex
        response = []
        for i in range(8): # 8-bit response
            idx = (challenge + i) % len(self.fingerprint)
            response.append(self.fingerprint[idx])
        return response

puf = SRAM_PUF()
challenge = 42
response = puf.get_response(challenge)
print(f"\n--- PUF Demo ---")
print(f"Challenge: {challenge}")
print(f"Response:  {response}")
print(f"(This response is unique to this 'chip' and cannot be cloned)")

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Glitching Tools
# ChipWhisperer: Open-source SCA/Fault injection platform.
# JTAGulator: Automated fault injection via JTAG.
# VoltJockey: Voltage glitching.

Side-Channel Resistant Algorithms
# Masking: Split sensitive data into random shares.
# Hiding: Add noise, balance power consumption.
# Shuffling: Randomize operation order.

Recommended Reading
# - "Hardware Security: Design, Threats, and Safeguards" by Dutta et al.
# - "The Art of Hardware Architecture" by Mohit Kumar
# - "Chipwhisperer Wiki": https://wiki.newae.com/
# - "NIST SP 800-193": Platform Firmware Resiliency Guidelines

# End of Cryptography Engineering Reference