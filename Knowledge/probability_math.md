# CHAPTER 7: PROBABILITY & STOCHASTICS


## Measure-Theoretic Probability

### Probability Spaces

**Definition:**
(Ω, F, P) where:
- Ω = sample space
- F = σ-algebra of events
- P: F → [0,1] probability measure (P(Ω) = 1, countable additivity)

**Random Variables:**
X: Ω → ℝ measurable function.
- Distribution: μ_X(A) = P(X ∈ A)
- CDF: F_X(x) = P(X ≤ x)
- PDF: f_X(x) = dF_X/dx (when exists)

**Expectation:**
E[X] = ∫_Ω X dP = ∫_ℝ x dμ_X(x)
- Linearity: E[aX + bY] = aE[X] + bE[Y]
- For independent X,Y: E[XY] = E[X]E[Y]

**Variance & Covariance:**
Var(X) = E[(X - E[X])²] = E[X²] - E[X]²
Cov(X,Y) = E[(X-E[X])(Y-E[Y])] = E[XY] - E[X]E[Y]
- Var(aX + bY) = a²Var(X) + b²Var(Y) + 2ab Cov(X,Y)
- Correlation: ρ(X,Y) = Cov(X,Y)/√(Var(X)Var(Y))

**Conditional Expectation:**
E[X|G] = Y where Y is G-measurable and ∫_A Y dP = ∫_A X dP for all A ∈ G.
- Tower property: E[E[X|G]] = E[X]
- For σ(Y): E[X|Y] = E[X|σ(Y)]

**Conditional Probability:**
P(A|B) = P(A∩B)/P(B) for P(B) > 0
- Bayes' theorem: P(A|B) = P(B|A)P(A)/P(B)
- Law of total probability: P(A) = Σ P(A|Bᵢ)P(Bᵢ)

### Convergence

**Modes of Convergence:**
1. Almost sure: Xₙ → X a.s. if P(lim Xₙ = X) = 1
2. In probability: Xₙ →P X if ∀ε>0, P(|Xₙ-X|>ε) → 0
3. In L^p: Xₙ →_{L^p} X if E[|Xₙ-X|^p] → 0
4. In distribution: Xₙ →D X if E[f(Xₙ)] → E[f(X)] for bounded continuous f

**Relationships:**
- a.s. ⇒ in probability
- L^p ⇒ in probability
- In probability ⇒ subsequence a.s.
- In probability ⇔ in distribution for constant limit

**Key Theorems:**
1. **Law of Large Numbers:**
   - Weak (WLLN): (1/n)Σ Xᵢ →P E[X] for i.i.d. with finite mean
   - Strong (SLLN): (1/n)Σ Xᵢ → E[X] a.s. for i.i.d. with finite mean

2. **Central Limit Theorem:**
   For i.i.d. Xᵢ with mean μ, variance σ²:
   (√n)(X̄ₙ - μ)/σ →D N(0,1)

3. **Glivenko-Cantelli:**
   Empirical distribution function converges uniformly to true CDF.

### Martingales

**Definition:**
Sequence (Mₙ) adapted to filtration (Fₙ) with:
1. E[|Mₙ|] < ∞
2. E[M_{n+1}|Fₙ] = Mₙ (martingale)
   Or E[M_{n+1}|Fₙ] ≥ Mₙ (submartingale)
   Or E[M_{n+1}|Fₙ] ≤ Mₙ (supermartingale)

**Examples:**
- Random walk with zero-mean steps
- Gambler's fortune in fair game
- Doob martingale: Mₙ = E[X|Fₙ]
- Exponential martingale: exp(θSₙ - nψ(θ))

**Stopping Times:**
τ: Ω → ℕ ∪ {∞} with {τ ≤ n} ∈ Fₙ for all n.

**Optional Stopping Theorem:**
For bounded stopping time τ: E[M_τ] = E[M₀]
(Under appropriate conditions)

**Martingale Convergence Theorems:**
- L^1-bounded martingale converges a.s.
- L^p-bounded martingale (p>1) converges a.s. and in L^p
- Uniformly integrable martingale converges a.s. and in L^1

**Doob's Inequalities:**
- Maximal: P(sup_{k≤n} |Mₖ| ≥ λ) ≤ E[|Mₙ|]/λ
- L^p: E[(sup_{k≤n} |Mₖ|)^p] ≤ (p/(p-1))^p E[|Mₙ|^p]

### Markov Processes

**Markov Property:**
P(X_{n+1} ∈ A | Fₙ) = P(X_{n+1} ∈ A | Xₙ)
Future depends only on present, not past.

**Transition Kernel:**
P(x, A) = P(X_{n+1} ∈ A | Xₙ = x)

**Chapman-Kolmogorov:**
P^{n+m}(x, A) = ∫ Pⁿ(y, A) P^m(x, dy)

**Stationary Distribution:**
π satisfies π(A) = ∫ P(x, A) π(dx)

**Ergodicity:**
- Irreducible: can reach any state from any state
- Aperiodic: gcd of return times is 1
- Positive recurrent: expected return time finite
- **Ergodic Theorem:** For ergodic chain, time averages = space averages

**Convergence to Stationarity:**
For irreducible, aperiodic, positive recurrent chain:
P(Xₙ = y | X₀ = x) → π(y) as n → ∞

**Rate of Convergence:**
- Mixing time: time to get within ε of stationary
- Spectral gap: 1 - λ₂ where λ₂ is second eigenvalue
- Conductance, Cheeger inequality

### Brownian Motion

**Definition:**
(W_t)_{t≥0} stochastic process with:
1. W₀ = 0
2. Independent increments
3. W_t - W_s ~ N(0, t-s) for t > s
4. Continuous paths

**Properties:**
- Self-similar: (c^{-1/2}W_{ct}) has same distribution
- Martingale: E[W_t|F_s] = W_s for t > s
- Quadratic variation: [W]_t = t
- Nowhere differentiable (a.s.)
- Law of iterated logarithm: limsup_{t→0} W_t/√(2t log log(1/t)) = 1

**Itô Calculus:**
For f(W_t,t):
df = ∂f/∂t dt + ∂f/∂x dW_t + ½ ∂²f/∂x² dt
(Itô's lemma: extra term from quadratic variation)

**Stochastic Differential Equations:**
dX_t = μ(X_t,t)dt + σ(X_t,t)dW_t
- Existence and uniqueness under Lipschitz conditions
- Examples: geometric Brownian motion, Ornstein-Uhlenbeck

**Feynman-Kac Formula:**
Solution of PDE can be represented as expectation of functional of diffusion.

### Large Deviations

**Cramér's Theorem:**
For i.i.d. Xᵢ with MGF M(θ) = E[e^{θX}]:
P(Sₙ/n ≥ a) ≈ exp(-nI(a))
where I(a) = sup_θ (θa - log M(θ)) is rate function.

**Gärtner-Ellis Theorem:**
For dependent sequences with:
Λ(θ) = lim (1/n) log E[e^{θSₙ}]
Rate function: I(x) = sup_θ (θx - Λ(θ))

**Sanov's Theorem:**
Large deviations for empirical measures.

**Applications:**
- Statistical mechanics
- Queueing theory
- Hypothesis testing (Chernoff bound)
- Random graph theory

### Gaussian Processes

**Definition:**
Process where all finite-dimensional distributions are Gaussian.
- Determined by mean function μ(t) and covariance kernel K(s,t)

**Examples:**
- Brownian motion: K(s,t) = min(s,t)
- Brownian bridge: K(s,t) = min(s,t) - st
- Ornstein-Uhlenbeck: K(s,t) = exp(-|s-t|)
- Squared exponential (RBF): K(s,t) = exp(-(s-t)²/(2ℓ²))

**Karhunen-Loève Expansion:**
X_t = Σ_{k=1}^∞ Zₖ √λₖ eₖ(t)
where (λₖ, eₖ) are eigenpairs of covariance operator.

**Gaussian Free Field:**
Generalization of Brownian motion to higher dimensions.
- Logarithmic covariance: K(x,y) ~ log|x-y|
- Conformally invariant
- Related to SLE, Liouville quantum gravity


## Information Theory

### Entropy

**Shannon Entropy:**
For discrete random variable X with pmf p:
H(X) = -Σ p(x) log p(x)
- Units: bits (log₂), nats (logₑ)
- H(X) ≥ 0, H(X) ≤ log|X|

**Joint & Conditional Entropy:**
H(X,Y) = -Σ p(x,y) log p(x,y)
H(X|Y) = H(X,Y) - H(Y) = E_Y[H(X|Y=y)]

**Mutual Information:**
I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)
= H(X) + H(Y) - H(X,Y)
- I(X;Y) ≥ 0, I(X;Y) = 0 iff X,Y independent
- I(X;Y) = I(Y;X)

**Kullback-Leibler Divergence:**
D(P||Q) = Σ p(x) log(p(x)/q(x))
- D(P||Q) ≥ 0 (Gibbs' inequality), = 0 iff P = Q
- Not symmetric, not metric
- I(X;Y) = D(P_{X,Y} || P_X ⊗ P_Y)

**Differential Entropy:**
For continuous X with pdf f:
h(X) = -∫ f(x) log f(x) dx
- Can be negative
- Gaussian maximizes entropy for given variance

### Data Compression

**Source Coding Theorem:**
For i.i.d. source with entropy H:
- Can compress to H + ε bits/symbol
- Cannot compress below H bits/symbol

**Huffman Coding:**
Optimal prefix code for given distribution.
- Expected length ≤ H(X) + 1

**Arithmetic Coding:**
Maps sequence to interval in [0,1].
- Approaches entropy for long sequences

**Lempel-Ziv:**
Universal compression (no knowledge of distribution).
- LZ77, LZ78, LZW variants
- Optimal for ergodic sources

### Channel Coding

**Channel Capacity:**
C = max_{P_X} I(X;Y)

**Shannon's Channel Coding Theorem:**
For rate R < C: ∃ codes with arbitrarily small error probability
For rate R > C: error probability bounded away from 0

**Examples:**
- Binary symmetric channel: C = 1 - H(p)
- AWGN channel: C = ½ log(1 + SNR)
- Band-limited AWGN: C = W log(1 + P/(N₀W))

**Error Exponent:**
For R < C, optimal error probability decays as exp(-nE(R)).

### Algorithmic Information Theory

**Kolmogorov Complexity:**
K(x) = length of shortest program that outputs x on universal Turing machine.
- Incomputable (halting problem)
- K(x|y) = conditional complexity
- K(x,y) ≤ K(x) + K(y|x) + O(1)

**Algorithmic Randomness:**
Sequence is random if K(x₁...xₙ) ≈ n for all n.
- Martin-Löf randomness
- Equivalent to passing all computable statistical tests

**Minimum Description Length (MDL):**
Model selection principle: choose model minimizing
L(model) + L(data|model)


## Random Matrix Theory

### Classical Ensembles

**Gaussian Ensembles:**
1. **GOE (Orthogonal):** Real symmetric matrices, P(H) ∝ exp(-tr(H²)/2)
2. **GUE (Unitary):** Hermitian matrices, P(H) ∝ exp(-tr(H²)/2)
3. **GSE (Symplectic):** Quaternion self-dual matrices

**Joint Eigenvalue Distribution:**
For GUE: P(λ₁,...,λₙ) ∝ ∏_{i<j} |λᵢ - λⱼ|² exp(-Σ λᵢ²)

**Wigner's Semicircle Law:**
For GOE/GUE/GSE, empirical spectral distribution converges to:
ρ(x) = (1/2π)√(4 - x²) for |x| ≤ 2

**Level Spacing Distribution:**
- GOE: p(s) ~ (πs/2)exp(-πs²/4) (Wigner surmise)
- GUE: p(s) ~ (32s²/π²)exp(-4s²/π)
- Poisson: p(s) = exp(-s) (integrable systems)

### Universality

**Wigner Matrices:**
Symmetric/Hermitian matrices with i.i.d. entries (up to symmetry).
- Semicircle law holds under mild conditions (Lindeberg)
- Local statistics converge to GOE/GUE

**Sample Covariance Matrices:**
XX^T/n where X is n×p matrix with i.i.d. entries.
- Marchenko-Pastur law for spectral distribution

**Universality Classes:**
- Bulk universality: local statistics in interior of spectrum
- Edge universality: local statistics at spectral edge (Tracy-Widom)

### Applications

**Quantum Chaos:**
- Berry-Tabor conjecture: integrable systems have Poisson statistics
- Bohigas-Giannoni-Schmit conjecture: chaotic systems have random matrix statistics

**Number Theory:**
- Riemann zeta zeros: GUE statistics (Montgomery-Odlyzko)
- Connections to L-functions

**Statistical Learning:**
- Spiked covariance model
- Phase transitions in PCA
- High-dimensional statistics

**Wireless Communications:**
- MIMO channel capacity
- Eigenvalue distributions


---
