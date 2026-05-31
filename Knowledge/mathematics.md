# Mathematics Complete Reference


---

# CHAPTER 1: ALGEBRA AND ARITHMETIC


## Fundamental Algebra

```
=== NUMBER SYSTEMS ===
ℕ Natural numbers:   0, 1, 2, 3, ...
ℤ Integers:          ..., -2, -1, 0, 1, 2, ...
ℚ Rationals:         p/q where p,q ∈ ℤ, q ≠ 0
ℝ Reals:             includes irrationals (√2, π, e)
ℂ Complex:           a + bi where i² = -1

Order: ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ ⊂ ℂ

=== EXPONENTS AND LOGARITHMS ===
aⁿ · aᵐ = aⁿ⁺ᵐ            (product rule)
aⁿ / aᵐ = aⁿ⁻ᵐ            (quotient rule)
(aⁿ)ᵐ = aⁿᵐ               (power rule)
(ab)ⁿ = aⁿbⁿ              (distribute)
a⁰ = 1   (a ≠ 0)
a⁻ⁿ = 1/aⁿ
aˣ = e^(x ln a)

log_b(xy)   = log_b(x) + log_b(y)
log_b(x/y)  = log_b(x) - log_b(y)
log_b(xⁿ)  = n · log_b(x)
log_b(x)    = log(x)/log(b)          (change of base)
log_b(bˣ)   = x
b^(log_b x) = x
ln(e)       = 1,  ln(1) = 0,  e ≈ 2.71828

=== FACTORING ===
a² - b²       = (a+b)(a-b)           (difference of squares)
a² + 2ab + b² = (a+b)²               (perfect square)
a³ - b³       = (a-b)(a²+ab+b²)      (difference of cubes)
a³ + b³       = (a+b)(a²-ab+b²)      (sum of cubes)

=== QUADRATIC FORMULA ===
ax² + bx + c = 0
x = (-b ± √(b²-4ac)) / (2a)

Discriminant Δ = b²-4ac:
  Δ > 0: two distinct real roots
  Δ = 0: one repeated real root
  Δ < 0: two complex conjugate roots

Vieta's formulas (for ax²+bx+c=0, roots x₁, x₂):
  x₁ + x₂ = -b/a
  x₁ · x₂ = c/a

=== SEQUENCES AND SERIES ===
Arithmetic:   a, a+d, a+2d, ...    Sₙ = n(2a+(n-1)d)/2
Geometric:    a, ar, ar², ...      Sₙ = a(1-rⁿ)/(1-r), |r|<1: S∞=a/(1-r)
Harmonic:     1, 1/2, 1/3, ...     Hₙ = Σ 1/k ≈ ln(n) + γ

Sum formulas:
  Σₖ₌₁ⁿ k     = n(n+1)/2
  Σₖ₌₁ⁿ k²    = n(n+1)(2n+1)/6
  Σₖ₌₁ⁿ k³    = [n(n+1)/2]²
  Σₖ₌₀ⁿ rᵏ   = (1-rⁿ⁺¹)/(1-r)  for r ≠ 1
```


---

# CHAPTER 2: CALCULUS


## Differential and Integral Calculus

```
=== DERIVATIVES ===
Notation: f'(x), dy/dx, d/dx[f(x)], Df

Basic rules:
  d/dx[c]       = 0           (constant)
  d/dx[xⁿ]     = nxⁿ⁻¹       (power rule)
  d/dx[eˣ]     = eˣ
  d/dx[aˣ]     = aˣ ln(a)
  d/dx[ln x]   = 1/x
  d/dx[sin x]  = cos x
  d/dx[cos x]  = -sin x
  d/dx[tan x]  = sec² x
  d/dx[arcsin x] = 1/√(1-x²)
  d/dx[arctan x] = 1/(1+x²)

Combination rules:
  (f±g)' = f' ± g'            (linearity)
  (cf)'  = cf'                (constant multiple)
  (fg)'  = f'g + fg'          (product rule)
  (f/g)' = (f'g - fg')/g²    (quotient rule)
  (f∘g)' = f'(g(x))·g'(x)   (chain rule)

=== INTEGRALS ===
∫xⁿ dx       = xⁿ⁺¹/(n+1) + C    (n ≠ -1)
∫1/x dx      = ln|x| + C
∫eˣ dx       = eˣ + C
∫aˣ dx       = aˣ/ln(a) + C
∫sin x dx    = -cos x + C
∫cos x dx    = sin x + C
∫tan x dx    = -ln|cos x| + C
∫sec² x dx   = tan x + C
∫1/√(1-x²) dx = arcsin x + C
∫1/(1+x²) dx  = arctan x + C

Integration by parts: ∫u dv = uv - ∫v du
                      choose u = LIATE (Log, Inverse trig, Algebraic, Trig, Exponential)

Substitution: if integral has f(g(x))g'(x), let u = g(x)

=== FUNDAMENTAL THEOREM OF CALCULUS ===
Part 1: d/dx[∫ₐˣ f(t)dt] = f(x)
Part 2: ∫ₐᵇ f(x)dx = F(b) - F(a)  where F' = f

=== LIMITS ===
L'Hôpital's rule: if lim f(x)/g(x) = 0/0 or ∞/∞, then = lim f'(x)/g'(x)

Important limits:
  lim(x→0) sin(x)/x = 1
  lim(x→0) (1-cos x)/x² = 1/2
  lim(x→∞) (1 + 1/x)ˣ = e
  lim(x→0) (1+x)^(1/x) = e
  lim(x→∞) xⁿ/eˣ = 0    (exponential beats polynomial)

=== TAYLOR/MACLAURIN SERIES ===
eˣ  = Σ xⁿ/n! = 1 + x + x²/2! + x³/3! + ...
sin x = Σ (-1)ⁿx^(2n+1)/(2n+1)! = x - x³/6 + x⁵/120 - ...
cos x = Σ (-1)ⁿx^(2n)/(2n)! = 1 - x²/2 + x⁴/24 - ...
ln(1+x) = Σ (-1)ⁿ⁺¹xⁿ/n = x - x²/2 + x³/3 - ...   |x| < 1
1/(1-x) = Σ xⁿ = 1 + x + x² + ...   |x| < 1
(1+x)ⁿ = Σ C(n,k)xᵏ   (Binomial theorem)
```


---

# CHAPTER 3: LINEAR ALGEBRA


## Vectors, Matrices, and Systems

```
=== VECTORS ===
Vector v = (v₁, v₂, ..., vₙ)
‖v‖ = √(v₁² + v₂² + ... + vₙ²)  (Euclidean norm)
Unit vector: v̂ = v/‖v‖

Dot product: u·v = Σ uᵢvᵢ = ‖u‖‖v‖cos θ
Cross product (3D): u×v = (u₂v₃-u₃v₂, u₃v₁-u₁v₃, u₁v₂-u₂v₁)
  ‖u×v‖ = ‖u‖‖v‖sin θ, perpendicular to both

Projection of u onto v: proj_v(u) = (u·v/v·v)v

=== MATRICES ===
A is m×n: m rows, n columns
(AB)ᵢⱼ = Σₖ AᵢₖBₖⱼ  (matrix multiplication, requires A: m×n, B: n×p → C: m×p)

Properties:
  (AB)ᵀ = BᵀAᵀ
  (AB)⁻¹ = B⁻¹A⁻¹
  (Aᵀ)⁻¹ = (A⁻¹)ᵀ

Determinant (2×2): det[[a,b],[c,d]] = ad - bc
Determinant (3×3): cofactor expansion

Inverse: A⁻¹ exists iff det(A) ≠ 0
  A⁻¹ = adj(A)/det(A)
  For 2×2: [[a,b],[c,d]]⁻¹ = (1/(ad-bc))[[d,-b],[-c,a]]

=== EIGENVALUES/EIGENVECTORS ===
Av = λv  (v ≠ 0)
Find eigenvalues: det(A - λI) = 0  (characteristic polynomial)
Then find eigenvectors for each λ

Diagonalization: A = PDP⁻¹
  D = diagonal matrix of eigenvalues
  P = matrix of eigenvectors as columns

=== SYSTEMS OF LINEAR EQUATIONS ===
Ax = b
Solutions: none (inconsistent), one (unique), infinitely many (dependent)

Gaussian elimination: row reduce augmented matrix [A|b]
  Row operations: swap rows, scale row, add multiple of one row to another

Solution methods:
  Gaussian elimination: O(n³)
  Cramer's rule: det-based, O(n! or n³ for det), impractical for large n
  LU decomposition: A = LU, solve Ly=b then Ux=y
  Iterative: Jacobi, Gauss-Seidel (for large sparse systems)

=== VECTOR SPACES ===
Span: all linear combinations of a set of vectors
Linear independence: no vector is a combo of others
Basis: linearly independent spanning set
Dimension: number of vectors in any basis
Rank(A): dimension of column space = dimension of row space
Null space: {x : Ax = 0}; Rank + Nullity = n (columns)

Gram-Schmidt: orthogonalize a set of vectors
QR decomposition: A = QR (Q orthogonal, R upper triangular)
SVD: A = UΣVᵀ (singular value decomposition, general)
```


---

# CHAPTER 4: PROBABILITY AND STATISTICS


## Probability Theory

```
=== PROBABILITY BASICS ===
Sample space Ω, events A, B ⊆ Ω
P(Ω) = 1,  P(∅) = 0,  0 ≤ P(A) ≤ 1
P(A∪B) = P(A) + P(B) - P(A∩B)         (addition rule)
P(Aᶜ) = 1 - P(A)                      (complement)
P(A|B) = P(A∩B)/P(B)   (B≠0)          (conditional)
P(A∩B) = P(A|B)P(B)                    (multiplication)
Independent: P(A∩B) = P(A)P(B)

Bayes' theorem:
P(A|B) = P(B|A)P(A) / P(B)
       = P(B|A)P(A) / [P(B|A)P(A) + P(B|Aᶜ)P(Aᶜ)]

=== RANDOM VARIABLES ===
Discrete: P(X=k), PMF, sum to 1
Continuous: f(x) density, ∫f(x)dx = 1, P(a≤X≤b) = ∫ₐᵇf(x)dx

E[X] = Σk·P(X=k)  or  ∫x·f(x)dx     (expected value)
Var(X) = E[X²] - (E[X])²              (variance)
SD(X) = √Var(X)                        (standard deviation)

E[aX+b] = aE[X]+b
Var(aX+b) = a²Var(X)
E[X+Y] = E[X]+E[Y]                    (always)
Var(X+Y) = Var(X)+Var(Y)              (if independent)

Covariance: Cov(X,Y) = E[(X-μₓ)(Y-μᵧ)] = E[XY]-E[X]E[Y]
Correlation: ρ = Cov(X,Y)/(σₓσᵧ)     (-1 ≤ ρ ≤ 1)

=== DISTRIBUTIONS ===
Bernoulli(p): P(X=1)=p, E[X]=p, Var(X)=p(1-p)
Binomial(n,p): P(X=k)=C(n,k)pᵏ(1-p)ⁿ⁻ᵏ, E[X]=np, Var=np(1-p)
Poisson(λ): P(X=k)=e⁻ᵏλᵏ/k!, E[X]=Var(X)=λ
Geometric(p): P(X=k)=(1-p)ᵏ⁻¹p, E[X]=1/p

Normal N(μ,σ²): f(x)=(1/σ√2π)exp(-(x-μ)²/2σ²)
  Standardize: Z=(X-μ)/σ ~ N(0,1)
  68-95-99.7 rule: 68% within 1σ, 95% within 2σ, 99.7% within 3σ

Uniform U(a,b): f(x)=1/(b-a), E[X]=(a+b)/2, Var=(b-a)²/12
Exponential(λ): f(x)=λe⁻ᵏˣ, E[X]=1/λ, Var=1/λ², memoryless
Chi-squared(k): sum of k squared standard normals
t-distribution(k): for small samples (Student's t)
F-distribution: ratio of chi-squared (ANOVA, regression)

=== STATISTICAL INFERENCE ===
Point estimate: single value estimate of parameter
Confidence interval: (estimate ± margin) with probability 1-α
Hypothesis test: H₀ (null) vs H₁ (alternative)
  p-value: probability of data given H₀ is true
  Reject H₀ if p < α (significance level, typically 0.05)
Type I error (α): reject true H₀ (false positive)
Type II error (β): fail to reject false H₀ (false negative)
Power = 1 - β

Central Limit Theorem: Xbar ~ N(μ, σ²/n) for large n
Law of Large Numbers: Xbar → μ as n → ∞
```


---

# CHAPTER 5: DISCRETE MATHEMATICS


## Logic, Sets, and Combinatorics

```
=== PROPOSITIONAL LOGIC ===
Connectives: ¬p (not), p∧q (and), p∨q (or), p→q (implies), p↔q (iff)
Truth values: T (true), F (false)

Logical laws:
  Double negation: ¬¬p ≡ p
  De Morgan: ¬(p∧q) ≡ ¬p∨¬q,  ¬(p∨q) ≡ ¬p∧¬q
  Contrapositive: (p→q) ≡ (¬q→¬p)
  Implication: (p→q) ≡ (¬p∨q)
  Biconditional: (p↔q) ≡ (p→q)∧(q→p)

Tautologies: p∨¬p, p→p
Contradictions: p∧¬p

=== SET THEORY ===
A∪B: union (elements in A or B)
A∩B: intersection (elements in both)
A\B: difference (in A but not B)
Aᶜ: complement (not in A)
A×B: Cartesian product {(a,b): a∈A, b∈B}
P(A): power set (all subsets)  |P(A)| = 2^|A|

Laws:
  Commutative: A∪B = B∪A
  Associative: A∪(B∪C) = (A∪B)∪C
  Distributive: A∩(B∪C) = (A∩B)∪(A∩C)
  De Morgan: (A∪B)ᶜ = Aᶜ∩Bᶜ

=== COMBINATORICS ===
Permutations: ordered arrangements
  P(n,r) = n!/(n-r)!   (r items from n)
  n! = n permutations of n items

Combinations: unordered selections
  C(n,r) = n!/(r!(n-r)!) = "n choose r"

Binomial theorem: (a+b)ⁿ = Σ C(n,k) aᵏbⁿ⁻ᵏ

Stars and bars: distribute n identical items into k bins = C(n+k-1, k-1)

Principle of inclusion-exclusion:
|A∪B| = |A|+|B|-|A∩B|
|A∪B∪C| = |A|+|B|+|C| - |A∩B| - |A∩C| - |B∩C| + |A∩B∩C|

Pigeonhole: if n+1 items in n bins, some bin has ≥2 items

=== GRAPH THEORY ===
Graph G = (V, E): vertices + edges
Degree: number of edges incident to vertex
Handshaking lemma: Σdeg(v) = 2|E|

Path: sequence of distinct vertices
Cycle: path that returns to start
Connected: path between any two vertices
Tree: connected, acyclic graph; |E| = |V|-1
  Spanning tree: tree using all vertices

Planar graph: can be drawn without edge crossings
Euler's formula: V - E + F = 2 (for connected planar graphs)
  F = faces (including outer face)
  Corollary: E ≤ 3V - 6 for planar graphs

Eulerian path: visits every edge once (all vertices even degree, or exactly 2 odd)
Hamiltonian path: visits every vertex once (NP-complete to decide)

Coloring: assign colors to vertices, no adjacent same color
Chromatic number χ(G): minimum colors needed
4-color theorem: planar graphs need at most 4 colors
```


---

# CHAPTER 6: NUMBER THEORY


## Integers and Modular Arithmetic

```
=== DIVISIBILITY ===
a | b: a divides b (b = ka for some integer k)
gcd(a,b): greatest common divisor
lcm(a,b) = ab/gcd(a,b)

Euclidean algorithm: gcd(a,b) = gcd(b, a mod b), gcd(a,0)=a
  gcd(48, 18) = gcd(18, 12) = gcd(12, 6) = gcd(6, 0) = 6

Extended Euclidean: find x,y such that ax + by = gcd(a,b)

Fundamental theorem of arithmetic: 
  Every integer > 1 is a unique product of primes

=== PRIME NUMBERS ===
Prime: only divisors are 1 and itself
Sieve of Eratosthenes: find all primes up to n in O(n log log n)
There are infinitely many primes (Euclid's proof)
Prime counting function π(n) ≈ n/ln(n) (Prime Number Theorem)
Goldbach's conjecture: every even n > 2 is sum of two primes (unproven)
Twin prime conjecture: infinitely many (p, p+2) primes (unproven)

Primality testing:
  Trial division: O(√n) 
  Fermat test: aⁿ⁻¹ ≡ 1 (mod n) for prime n (not sufficient)
  Miller-Rabin: probabilistic, efficient
  AKS: deterministic polynomial time

=== MODULAR ARITHMETIC ===
a ≡ b (mod m): m | (a-b)
(a+b) mod m = ((a mod m)+(b mod m)) mod m
(a·b) mod m = ((a mod m)·(b mod m)) mod m

Modular inverse: a⁻¹ ≡ x (mod m) such that ax ≡ 1 (mod m)
  Exists iff gcd(a,m) = 1
  Find via extended Euclidean or Fermat's little theorem

Fermat's little theorem: aᵖ⁻¹ ≡ 1 (mod p) for prime p, gcd(a,p)=1
Euler's theorem: aᵠ⁽ᵐ⁾ ≡ 1 (mod m) for gcd(a,m)=1
  φ(m) = Euler's totient = count of k ≤ m with gcd(k,m)=1

Chinese Remainder Theorem:
  System x ≡ aᵢ (mod mᵢ) with coprime mᵢ has unique solution mod Πmᵢ

=== RSA ALGORITHM ===
1. Choose large primes p, q; n = pq
2. φ(n) = (p-1)(q-1)
3. Choose e coprime to φ(n); d = e⁻¹ mod φ(n)
4. Public key: (n, e); Private key: (n, d)
5. Encrypt: c = mᵉ mod n; Decrypt: m = cᵈ mod n
```


---

# CHAPTER 7: COMPLEX NUMBERS AND TRANSFORMS


## Complex Analysis and Signal Processing

```
=== COMPLEX NUMBERS ===
z = a + bi  where i² = -1
a = Re(z) (real part), b = Im(z) (imaginary part)
z̄ = a - bi (complex conjugate)
|z| = √(a²+b²) (modulus/magnitude)
arg(z) = arctan(b/a) (argument/phase)

Polar form: z = r·e^(iθ) = r(cos θ + i sin θ)
  r = |z|, θ = arg(z)

Euler's formula: e^(iθ) = cos θ + i sin θ
Euler's identity: e^(iπ) + 1 = 0

Operations:
  (a+bi)+(c+di) = (a+c)+(b+d)i
  (a+bi)(c+di) = (ac-bd)+(ad+bc)i
  (a+bi)/(c+di) = (a+bi)(c-di)/|c+di|²

De Moivre's theorem: (cos θ + i sin θ)ⁿ = cos(nθ) + i sin(nθ)
nth roots of unity: e^(2πik/n) for k=0,1,...,n-1

=== FOURIER TRANSFORM ===
Continuous FT: F(ω) = ∫ f(t)e^(-iωt)dt
Inverse FT:    f(t) = (1/2π) ∫ F(ω)e^(iωt)dω

Properties:
  Linearity: F(af+bg) = aF(f) + bF(g)
  Time shift: F(f(t-t₀)) = e^(-iωt₀)F(ω)
  Frequency shift: F(e^(iω₀t)f(t)) = F(ω-ω₀)
  Convolution: F(f*g) = F(f)·F(g)
  Parseval's theorem: ∫|f(t)|²dt = (1/2π)∫|F(ω)|²dω

DFT (Discrete Fourier Transform):
  Xₖ = Σₙ₌₀ᴺ⁻¹ xₙ e^(-2πikn/N)
  FFT: O(N log N) algorithm for DFT

=== LAPLACE TRANSFORM ===
L{f(t)} = F(s) = ∫₀^∞ f(t)e^(-st)dt

Common transforms:
  L{1} = 1/s
  L{t} = 1/s²
  L{eᵃᵗ} = 1/(s-a)
  L{sin(ωt)} = ω/(s²+ω²)
  L{cos(ωt)} = s/(s²+ω²)
  L{f'(t)} = sF(s) - f(0)

Used for: solving ODEs, control systems, signal processing

=== Z-TRANSFORM ===
X(z) = Σₙ₌₋∞^∞ x[n]z⁻ⁿ
Discrete-time analog of Laplace transform
Used for: digital filters, DSP
```


---

# CHAPTER 8: DIFFERENTIAL EQUATIONS AND OPTIMIZATION


## Applied Mathematics

```
=== ORDINARY DIFFERENTIAL EQUATIONS ===
ODE: equation involving y(x) and its derivatives
Order: highest derivative; Linear if no y², y·y', etc.

First-order linear: y' + P(x)y = Q(x)
  Integrating factor: μ = e^∫P(x)dx
  Solution: y = (1/μ)∫μQ(x)dx

Separable: y' = f(x)g(y)
  Separate: dy/g(y) = f(x)dx, integrate both sides

Second-order linear with constant coefficients: ay'' + by' + cy = 0
  Characteristic equation: ar² + br + c = 0
  Case 1: r₁≠r₂ real → y = C₁e^(r₁x) + C₂e^(r₂x)
  Case 2: r = α±βi → y = e^(αx)(C₁cos βx + C₂sin βx)
  Case 3: r₁=r₂=r → y = (C₁+C₂x)e^(rx)

Euler's method (numerical): yₙ₊₁ = yₙ + hf(xₙ, yₙ)
Runge-Kutta 4th order: more accurate numerical method

=== PARTIAL DIFFERENTIAL EQUATIONS ===
Common PDEs in science:
  Heat equation: ∂u/∂t = α∇²u   (diffusion)
  Wave equation: ∂²u/∂t² = c²∇²u  (waves)
  Laplace: ∇²u = 0               (steady-state)
  Poisson: ∇²u = f               (with source)
  Schrödinger: iℏ∂ψ/∂t = Ĥψ     (quantum)

=== OPTIMIZATION ===
Unconstrained:
  Necessary condition: ∇f = 0 (stationary point)
  Second-order: Hessian H positive definite → local min
  
Gradient descent: xₙ₊₁ = xₙ - α∇f(xₙ)
Newton's method: xₙ₊₁ = xₙ - H⁻¹∇f(xₙ)
  Faster convergence but requires Hessian

Constrained (Lagrange multipliers):
  Minimize f(x) subject to g(x) = 0
  Solution: ∇f = λ∇g (at optimum)
  Form Lagrangian: L(x,λ) = f(x) - λg(x)

Linear programming (LP):
  Minimize cᵀx subject to Ax ≤ b, x ≥ 0
  Simplex method: O(exponential worst, polynomial avg)
  Interior point: O(n³) guaranteed

Convex optimization:
  Convex function: f(λx+(1-λ)y) ≤ λf(x)+(1-λ)f(y)
  Any local minimum is global minimum
  KKT conditions: necessary and sufficient for convex problems

=== INFORMATION THEORY ===
Entropy: H(X) = -Σ p(x) log₂ p(x)   (bits of information)
  H(X) = 0 for deterministic, H(X) = log₂n for uniform over n
Cross-entropy: H(p,q) = -Σ p(x) log₂ q(x)
KL divergence: DKL(p||q) = Σ p(x) log(p(x)/q(x)) ≥ 0
Mutual information: I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)

Shannon's channel capacity: C = B log₂(1 + S/N)
  B = bandwidth, S/N = signal-to-noise ratio
```
