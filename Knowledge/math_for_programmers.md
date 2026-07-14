# Math for Programmers Complete Reference


---

# CHAPTER 1: ESSENTIAL MATH


## Remarks

You don't need a math degree to be a great programmer. But certain math concepts appear constantly: logarithms in Big O analysis, modular arithmetic in hashing, linear algebra in graphics/ML, probability in algorithms. This is the practical math every developer should know.


## Logarithms (Big O Analysis)

```
log₂(n) = "how many times can you halve n before reaching 1?"

log₂(1)     = 0      (2⁰ = 1)
log₂(2)     = 1      (2¹ = 2)
log₂(4)     = 2      (2² = 4)
log₂(8)     = 3      (2³ = 8)
log₂(16)    = 4
log₂(1024)  = 10     (2¹⁰ = 1,024)
log₂(1M)    ≈ 20     (2²⁰ = 1,048,576)
log₂(1B)    ≈ 30     (2³⁰ = 1,073,741,824)

WHY IT MATTERS FOR ALGORITHMS:
  Binary search: 1 billion items → ~30 comparisons (log₂ n)
  Balanced BST:  1 million items → ~20 lookups
  Merge sort:    n × log₂(n) → much better than n²

  n = 1,000,000:
    O(n²)      = 1,000,000,000,000  (1 trillion operations!)
    O(n log n) = 20,000,000         (20 million — 50,000x faster)
    O(n)       = 1,000,000
    O(log n)   = 20
```

```python
import math

math.log2(1024)     # 10.0
math.log10(1000)    # 3.0
math.log(math.e)    # 1.0 (natural log)

# In Big O, log base doesn't matter (constants drop):
# log₂(n) = log₁₀(n) / log₁₀(2) = log₁₀(n) × 3.32
# They differ by a constant factor → same Big O class
```


## Modular Arithmetic

```python
# Modulo (%) = remainder after division
# Used in: hashing, cryptography, circular arrays, distributed systems

7 % 3    # 1  (7 = 2×3 + 1)
10 % 5   # 0  (10 = 2×5 + 0)
-7 % 3   # 2 in Python (-1 in C/Java — language dependent!)

# PRACTICAL USES:

# 1. Hash table index
index = hash(key) % table_size

# 2. Circular array (ring buffer)
next_index = (current + 1) % buffer_size
# 0 → 1 → 2 → 3 → 0 → 1 → ...

# 3. Is even/odd
is_even = (n % 2 == 0)

# 4. Wrap around (clock, game coordinates)
hour = total_hours % 24
x_pos = x % screen_width    # Wrap around screen

# 5. Distribute work across N workers
worker_id = item_id % num_workers

# 6. Check divisibility
is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# MODULAR EXPONENTIATION (cryptography)
# Compute (base^exp) % mod efficiently
pow(base, exp, mod)    # Python built-in, uses fast algorithm
pow(7, 256, 13)        # Much faster than (7**256) % 13
```


## Bit Manipulation Math

```python
# Powers of 2
1 << 0   # 1
1 << 1   # 2
1 << 2   # 4
1 << 3   # 8
1 << 10  # 1024 (1 KB)
1 << 20  # 1048576 (1 MB)
1 << 30  # 1073741824 (1 GB)

# Check power of 2
def is_power_of_2(n):
    return n > 0 and (n & (n - 1)) == 0
# 8 = 1000, 7 = 0111 → 1000 & 0111 = 0000 ✓
# 6 = 0110, 5 = 0101 → 0110 & 0101 = 0100 ✗

# Floor division by power of 2
n >> 1   # n // 2
n >> 3   # n // 8

# Multiply by power of 2
n << 1   # n * 2
n << 3   # n * 8

# Swap without temp
a ^= b; b ^= a; a ^= b
```


---

# CHAPTER 2: LINEAR ALGEBRA BASICS


## Vectors and Matrices

```python
import numpy as np

# VECTORS: direction + magnitude
v1 = np.array([3, 4])
v2 = np.array([1, 2])

# Vector operations
v1 + v2                          # [4, 6]  (addition)
v1 * 2                           # [6, 8]  (scalar multiply)
np.linalg.norm(v1)               # 5.0     (magnitude: √(3²+4²))
v1 / np.linalg.norm(v1)          # [0.6, 0.8] (unit vector)

# Dot product: similarity measure
np.dot(v1, v2)                   # 11  (3×1 + 4×2)
# Dot product > 0: same direction
# Dot product = 0: perpendicular
# Dot product < 0: opposite direction

# COSINE SIMILARITY (used in embeddings/RAG!)
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
# Returns -1 (opposite) to 1 (identical)
# This is how ChromaDB finds similar documents!

# MATRICES: 2D array of numbers
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A @ B                            # Matrix multiplication
np.linalg.inv(A)                 # Inverse
np.linalg.det(A)                 # Determinant
A.T                              # Transpose

# WHY MATRICES MATTER:
# - Neural networks = chains of matrix multiplications
# - 3D graphics = transformation matrices (rotate, scale, translate)
# - Linear regression = solving Ax = b
# - Image processing = convolution matrices (filters)
# - Page rank = eigenvalues of link matrix
```


---

# CHAPTER 3: PROBABILITY AND STATISTICS


## Basics for Programmers

```python
# PROBABILITY
# P(event) = favorable outcomes / total outcomes
# P(heads) = 1/2 = 0.5
# P(rolling 6) = 1/6 ≈ 0.167

# EXPECTED VALUE
# E[X] = Σ (value × probability)
# Fair die: E[X] = (1+2+3+4+5+6)/6 = 3.5
# "On average, a die roll gives 3.5"

# STANDARD DEVIATION: spread around the mean
import numpy as np
data = [2, 4, 4, 4, 5, 5, 7, 9]
np.mean(data)    # 5.0
np.std(data)     # 2.0
# 68% of data within 1 std dev of mean (3.0 to 7.0)
# 95% within 2 std devs (1.0 to 9.0)

# BIRTHDAY PARADOX
# In a group of 23 people, there's a 50% chance two share a birthday!
# Why it matters: hash collisions happen sooner than you'd expect.
# With 2^32 possible hashes (~4 billion), collision expected after ~77,000 items.

# BAYES' THEOREM
# P(A|B) = P(B|A) × P(A) / P(B)
# "Probability of A given B"
#
# Example: spam filter
# P(spam | contains "free") =
#   P("free" | spam) × P(spam) / P("free")
#   = 0.8 × 0.3 / 0.35
#   = 0.686 (68.6% chance it's spam)

# RANDOMNESS IN PROGRAMMING
import random
import secrets

random.random()              # 0.0 to 1.0 (NOT cryptographically secure)
random.randint(1, 6)         # Die roll
random.choice(['a', 'b'])    # Random element
random.shuffle(deck)         # Shuffle in-place
random.sample(population, k) # k unique random elements

secrets.token_hex(32)        # Cryptographically secure random (for tokens!)
secrets.randbelow(100)       # Secure random 0-99
```


---

# CHAPTER 4: COMMON PITFALLS

```
PITFALL 1: Floating point comparison
  0.1 + 0.2 == 0.3  → False! (0.30000000000000004)
  Fix: abs(a - b) < 1e-9 or use decimal.Decimal for money.

PITFALL 2: Integer overflow
  In C/Java: INT_MAX + 1 wraps to negative!
  Python: integers have arbitrary precision (no overflow).
  Fix: use bigger types (long), or check before arithmetic.

PITFALL 3: Off-by-one errors
  for i in range(n) → 0 to n-1 (n iterations)
  for i in range(1, n) → 1 to n-1 (n-1 iterations!)
  Fix: think about boundaries carefully. Test edge cases.

PITFALL 4: Using random for security
  random.randint() is predictable (Mersenne Twister, seedable).
  Fix: secrets.token_hex() for tokens, passwords, session IDs.

PITFALL 5: Ignoring log scale
  "My algorithm handles 1000 items fine" → crashes at 1M.
  Fix: think in orders of magnitude. O(n²) at 1K = 1M ops, at 1M = 1T ops.

PITFALL 6: Division by zero
  average = total / count → crash if count is 0.
  Fix: always check: average = total / count if count else 0
```