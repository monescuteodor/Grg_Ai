# CHAPTER 3: ANALYSIS


## Real Analysis

### Measure Theory

**σ-Algebra:**
A collection Σ of subsets of X such that:
1. X ∈ Σ
2. A ∈ Σ ⇒ A' ∈ Σ
3. Countable unions of sets in Σ are in Σ

**Measure:**
μ: Σ → [0, ∞] satisfying:
1. μ(∅) = 0
2. Countable additivity: μ(⊔ Aₙ) = Σ μ(Aₙ) for disjoint Aₙ

**Lebesgue Measure on ℝ:**
- Outer measure: μ*(A) = inf{Σ|Iₙ| : A ⊆ ∪Iₙ, Iₙ intervals}
- Measurable: A is Lebesgue measurable iff ∀E ⊆ ℝ:
  μ*(E) = μ*(E∩A) + μ*(E\A)
- Properties: translation invariant, σ-finite, complete
- Non-measurable sets exist (require AC)

**Measurable Functions:**
f: X → ℝ is measurable if f⁻¹(U) ∈ Σ for all open U.
- Continuous functions are measurable
- Pointwise limits of measurable functions are measurable

**Integration (Lebesgue):**
For simple function s = Σ aᵢ χ_{Aᵢ}: ∫s dμ = Σ aᵢ μ(Aᵢ)
For non-negative f: ∫f dμ = sup{∫s dμ : 0 ≤ s ≤ f, s simple}
For general f: ∫f = ∫f⁺ - ∫f⁻ (if at least one finite)

**Key Theorems:**
1. **Monotone Convergence:** fₙ ↑ f ⇒ ∫fₙ → ∫f
2. **Dominated Convergence:** fₙ → f, |fₙ| ≤ g integrable ⇒ ∫fₙ → ∫f
3. **Fatou's Lemma:** ∫liminf fₙ ≤ liminf ∫fₙ
4. **Fubini's Theorem:** For f integrable on product space:
   ∫_{X×Y} f d(μ×ν) = ∫_X (∫_Y f dν) dμ = ∫_Y (∫_X f dμ) dν

**L^p Spaces:**
L^p(X, μ) = {f : ∫|f|^p dμ < ∞} / (f = g a.e.)
- ||f||_p = (∫|f|^p)^{1/p} for 1 ≤ p < ∞
- ||f||_∞ = ess sup|f|
- Hölder's inequality: ||fg||₁ ≤ ||f||_p ||g||_q for 1/p + 1/q = 1
- Minkowski's inequality: ||f+g||_p ≤ ||f||_p + ||g||_p
- L^p is Banach space; L² is Hilbert space

**Modes of Convergence:**
- Almost everywhere: fₙ(x) → f(x) for a.e. x
- In measure: μ({|fₙ - f| > ε}) → 0
- In L^p: ||fₙ - f||_p → 0
- Uniform: sup|fₙ - f| → 0

Relationships:
- Uniform ⇒ pointwise ⇒ a.e.
- L^p convergence ⇒ convergence in measure
- Convergence in measure ⇒ subsequence converges a.e.

### Functional Analysis

**Banach Spaces:**
Complete normed vector space.
Examples: C([0,1]), L^p(ℝ), ℓ^p, C_b(X)

**Hilbert Spaces:**
Complete inner product space.
Examples: L²(ℝ), ℓ², L²([0,2π])

**Key Theorems:**
1. **Hahn-Banach:** Norm-preserving extension of linear functionals
2. **Open Mapping:** Surjective bounded linear map between Banach spaces is open
3. **Closed Graph:** T: X → Y has closed graph iff T is bounded
4. **Uniform Boundedness (Banach-Steinhaus):**
   If supₙ ||Tₙx|| < ∞ for all x, then supₙ ||Tₙ|| < ∞

**Dual Spaces:**
X* = space of continuous linear functionals on X
- (L^p)* ≅ L^q for 1 ≤ p < ∞, 1/p + 1/q = 1
- (ℓ^p)* ≅ ℓ^q
- (C([0,1]))* = space of finite signed Borel measures (Riesz Representation)

**Weak & Weak* Topologies:**
- Weak topology on X: coarsest making all f ∈ X* continuous
- Weak* topology on X*: coarsest making all evaluation maps continuous
- Banach-Alaoglu: Closed unit ball in X* is weak* compact

**Spectral Theory in Banach Algebras:**
For Banach algebra A with unity:
- Spectrum: σ(x) = {λ : x - λ·1 not invertible}
- Spectral radius: r(x) = sup{|λ| : λ ∈ σ(x)} = lim ||xⁿ||^{1/n}
- Gelfand-Mazur: Complex Banach division algebra is ℂ
- Gelfand-Naimark: Commutative C*-algebra ≅ C(X) for compact X

### Complex Analysis

**Holomorphic Functions:**
f: U → ℂ (U open) is holomorphic if f'(z) exists for all z ∈ U.
Equivalently: f satisfies Cauchy-Riemann equations.

**Cauchy's Theorem:**
For f holomorphic on simply connected U and γ contractible in U:
∮_γ f(z) dz = 0

**Cauchy's Integral Formula:**
f(z) = (1/2πi) ∮_γ f(ζ)/(ζ-z) dζ
f^{(n)}(z) = (n!/2πi) ∮_γ f(ζ)/(ζ-z)^{n+1} dζ

**Consequences:**
- Holomorphic functions are infinitely differentiable
- Liouville's Theorem: Bounded entire functions are constant
- Fundamental Theorem of Algebra: Every non-constant polynomial has a root in ℂ
- Maximum Modulus Principle: |f| has no local maximum inside domain
- Identity Theorem: If f = g on set with accumulation point, f = g everywhere

**Laurent Series & Residues:**
f(z) = Σ_{n=-∞}^∞ aₙ(z-z₀)ⁿ in annulus
Res(f, z₀) = a_{-1} = (1/2πi) ∮_γ f(z) dz

**Residue Theorem:**
∮_γ f(z) dz = 2πi Σ Res(f, zₖ) for zₖ inside γ

**Applications:**
- Evaluating real integrals: ∫_{-∞}^∞, ∫_0^{2π}
- Summing series: Σ f(n) using cot(πz)
- Argument Principle: (1/2πi) ∮ f'/f = N - P (zeros minus poles)

**Conformal Mappings:**
Holomorphic bijections preserve angles.
- Riemann Mapping Theorem: Any simply connected proper subset of ℂ is conformally equivalent to unit disk
- Schwarz-Christoffel: Maps upper half-plane to polygons

**Analytic Continuation:**
Extending holomorphic function beyond original domain.
- Uniqueness: continuation is unique if it exists
- Natural boundary: some functions cannot be continued
- Riemann surfaces: multi-valued functions (e.g., √z, log z)

**Entire & Meromorphic Functions:**
- Entire: holomorphic on all of ℂ
- Meromorphic: holomorphic except for isolated poles
- Mittag-Leffler: Construct meromorphic functions with prescribed principal parts
- Weierstrass: Construct entire functions with prescribed zeros

### Harmonic Analysis

**Fourier Series:**
For f ∈ L²([0,2π]):
f(x) = Σ_{n=-∞}^∞ cₙ e^{inx}  where cₙ = (1/2π) ∫_0^{2π} f(x)e^{-inx} dx
Or: f(x) = a₀/2 + Σ(aₙ cos(nx) + bₙ sin(nx))

**Convergence:**
- L² convergence: always (Plancherel)
- Pointwise: Dirichlet conditions (piecewise smooth)
- Uniform: if f is C¹ and periodic
- Gibbs phenomenon at discontinuities

**Fourier Transform:**
For f ∈ L¹(ℝ):
̂f(ξ) = ∫_{-∞}^∞ f(x)e^{-2πixξ} dx
Inverse: f(x) = ∫_{-∞}^∞ ̂f(ξ)e^{2πixξ} dξ

**Properties:**
- Linearity, translation, modulation, scaling
- Convolution: ̂(f * g) = ̂f · ĝ
- Differentiation: ̂(f') = 2πiξ · ̂f
- Plancherel: ||f||₂ = ||̂f||₂ (extends to L²)

**Distributions (Generalized Functions):**
- Dirac delta: δ(x) = 0 for x ≠ 0, ∫δ(x)dx = 1
- ̂δ = 1, ̂1 = δ
- Tempered distributions: dual of Schwartz space

**Applications:**
- PDEs: heat equation, wave equation, Laplace equation
- Signal processing: filtering, sampling theorem
- Number theory: Poisson summation, theta functions

### Several Complex Variables

**Holomorphic Functions in ℂⁿ:**
f: U ⊆ ℂⁿ → ℂ is holomorphic if holomorphic in each variable separately.
- Hartogs' Theorem: Separate analyticity implies joint analyticity
- No analogue of Cauchy's theorem for arbitrary domains

**Domains of Holomorphy:**
Domain where there exists a function that cannot be extended.
- Characterized by pseudoconvexity
- Levi problem: solved by Oka, Bremermann, Norguet

**Sheaves & Cohomology:**
- O = sheaf of holomorphic functions
- Cousin problems: solved using sheaf cohomology
- Cartan's Theorems A and B for Stein manifolds


## Differential Equations

### Ordinary Differential Equations (ODEs)

**Existence & Uniqueness:**
For y' = f(t,y), f Lipschitz in y:
- Picard-Lindelöf: Local existence and uniqueness
- Peano: Existence without Lipschitz (not uniqueness)
- Global existence if f has linear growth

**Linear ODEs:**
y' = A(t)y + b(t)
- Homogeneous: y' = Ay has solution y = e^{At}y₀
- Variation of parameters for non-homogeneous
- Constant coefficients: solve via eigenvalues

**Stability Theory:**
For y' = f(y) with equilibrium y*:
- Lyapunov stable: nearby solutions stay nearby
- Asymptotically stable: nearby solutions converge to y*
- Linearization: stability determined by eigenvalues of Df(y*)
- Lyapunov functions for nonlinear stability

**Bifurcation Theory:**
Qualitative change in dynamics as parameter varies.
- Saddle-node: creation/annihilation of equilibria
- Hopf: creation of limit cycles
- Period doubling: route to chaos

### Partial Differential Equations (PDEs)

**Classification:**
Second-order linear PDE in two variables:
Au_{xx} + 2Bu_{xy} + Cu_{yy} + ... = 0
- Elliptic: B² - AC < 0 (e.g., Laplace: Δu = 0)
- Parabolic: B² - AC = 0 (e.g., heat: u_t = Δu)
- Hyperbolic: B² - AC > 0 (e.g., wave: u_{tt} = Δu)

**Elliptic Equations:**
**Laplace's Equation:** Δu = 0
- Harmonic functions: mean value property, maximum principle
- Dirichlet problem: u = g on boundary
- Green's functions: u(x) = ∫_∂Ω g(y) ∂G/∂n dy
- Poisson equation: Δu = f

**Parabolic Equations:**
**Heat Equation:** u_t = kΔu
- Fundamental solution: (4πkt)^{-n/2} exp(-|x|²/4kt)
- Maximum principle
- Smoothing: solutions instantly become smooth
- Backward heat equation: ill-posed

**Hyperbolic Equations:**
**Wave Equation:** u_{tt} = c²Δu
- D'Alembert solution in 1D: u(x,t) = f(x-ct) + g(x+ct)
- Huygens' principle in odd dimensions
- Finite propagation speed
- Energy conservation

**Sobolev Spaces:**
W^{k,p}(Ω) = {u : D^αu ∈ L^p for |α| ≤ k}
- H^k = W^{k,2}
- Trace theorems: boundary values
- Embedding theorems: W^{k,p} ↪ C^m under certain conditions
- Rellich-Kondrachov: compact embedding

**Weak Solutions:**
Multiply by test function, integrate by parts.
- Galerkin method for construction
- Lax-Milgram for elliptic equations
- Existence via energy methods

**Nonlinear PDEs:**
- Navier-Stokes: Millennium Prize Problem
- Reaction-diffusion: pattern formation (Turing patterns)
- KdV equation: solitons, complete integrability
- Einstein equations: general relativity

### Calculus of Variations

**Euler-Lagrange Equation:**
For functional J[y] = ∫_a^b F(x, y, y') dx:
∂F/∂y - d/dx(∂F/∂y') = 0

**Examples:**
- Shortest path: F = √(1 + y'²) ⇒ y'' = 0 (straight line)
- Brachistochrone: cycloid
- Minimal surface: mean curvature zero

**Constrained Variations:**
- Isoperimetric: ∫G dx = constant, use Lagrange multipliers
- Holonomic constraints: use generalized coordinates

**Direct Methods:**
- Tonelli's theorem: existence of minimizer
- Lower semicontinuity + coercivity + convexity

**Noether's Theorem:**
Every continuous symmetry of action corresponds to a conservation law.
- Time translation → energy conservation
- Space translation → momentum conservation
- Rotation → angular momentum conservation


## Dynamical Systems

### Discrete Dynamical Systems

**Iteration:** f: X → X, study fⁿ(x) = f∘...∘f(x)

**Fixed Points:**
x* = f(x*)
- Stable: |f'(x*)| < 1
- Unstable: |f'(x*)| > 1
- Neutral: |f'(x*)| = 1

**Periodic Points:**
fⁿ(x) = x, fᵏ(x) ≠ x for k < n

**Chaos (Devaney):**
1. Sensitive dependence on initial conditions
2. Topological transitivity
3. Dense periodic points

**Logistic Map:** x_{n+1} = rxₙ(1-xₙ)
- Period doubling cascade to chaos
- Feigenbaum constant: δ ≈ 4.669...
- Universality: same behavior in many systems

### Continuous Dynamical Systems

**Flows:** φ: ℝ × X → X satisfying φ(0,x) = x, φ(t+s,x) = φ(t, φ(s,x))

**Poincaré-Bendixson Theorem:**
In ℝ², bounded trajectories approach:
- Fixed point, or
- Periodic orbit, or
- Connection of fixed points

**Strange Attractors:**
- Lorenz attractor: x' = σ(y-x), y' = x(ρ-z)-y, z' = xy-βz
- Fractal structure, sensitive dependence
- Hausdorff dimension between 2 and 3

**Ergodic Theory:**
Study of invariant measures and long-term behavior.
- Birkhoff Ergodic Theorem: time averages = space averages
- Mixing: stronger than ergodicity
- Entropy: measure of complexity (Kolmogorov-Sinai)


---
