# CHAPTER 11: DIFFERENTIAL GEOMETRY & GEOMETRIC ANALYSIS


## Riemannian Geometry (Advanced)

### Comparison Geometry

**Rauch Comparison Theorem:**
For Riemannian manifolds M, M̃ with sectional curvature K ≥ K̃:
- Jacobi fields along geodesics in M are smaller than in M̃
- Applications: volume comparison, injectivity radius estimates

**Toponogov Comparison Theorem:**
For K ≥ κ, geodesic triangles are "fatter" than in space form of curvature κ.
- Generalization of Alexandrov comparison
- Applications: structure of manifolds with K ≥ κ > 0

**Bishop-Gromov Volume Comparison:**
For Ricci curvature Ric ≥ (n-1)κg:
- Vol(B(r))/V_κ(r) is non-increasing in r
- V_κ(r) = volume of ball in space form
- Equality iff M is locally isometric to space form

**Cheeger-Gromoll Splitting Theorem:**
If complete M with Ric ≥ 0 contains a line:
M ≅ N × ℝ isometrically.

**Soul Theorem (Cheeger-Gromoll):**
For complete non-compact M with K ≥ 0:
∃ compact totally geodesic submanifold S (soul) such that M is diffeomorphic to normal bundle of S.

### Geometric Flows

**Ricci Flow:**
∂g/∂t = -2 Ric(g)
- Introduced by Hamilton (1982)
- Perelman (2002-2003): proof of Poincaré and geometrization
- Singularity analysis: neck-pinching, surgery

**Evolution Equations:**
Under Ricci flow:
- ∂R/∂t = ΔR + 2|Ric|²
- ∂|Rm|²/∂t = Δ|Rm|² - 2|∇Rm|² + quadratic terms

**Perelman's Functionals:**
- F-functional: F(g,f) = ∫ (R + |∇f|²)e^{-f} dV
- W-functional (entropy): W(g,f,τ)
- Monotonicity along Ricci flow with surgery
- No local collapsing theorem

**Mean Curvature Flow:**
∂F/∂t = H·ν
- Surfaces evolve by mean curvature
- Singularities: self-similar shrinkers
- Huisken's theorem: convex hypersurfaces shrink to round point

**Yamabe Flow:**
∂g/∂t = -(R - r̄)g
- Preserves conformal class
- Converges to constant scalar curvature metric

**Harmonic Map Heat Flow:**
∂u/∂t = τ(u)
- Eells-Sampson: converges for K_N ≤ 0
- Struwe's monotonicity formula
- Bubbling analysis

### Minimal Surfaces

**First Variation:**
Area'(0) = -∫_M H·φ dA
- Minimal surface: H = 0 (mean curvature zero)
- Critical point of area functional

**Second Variation:**
Area''(0) = ∫_M (|∇φ|² - (|A|² + Ric(ν,ν))φ²) dA
- Stability: second variation non-negative
- Index: number of negative eigenvalues of Jacobi operator

**Classical Results:**
- Bernstein problem: entire minimal graph in ℝ³ is plane (true for n ≤ 7, false for n ≥ 8)
- Douglas-Rado solution of Plateau problem
- Meeks-Yau: least area disks in 3-manifolds
- Colding-Minicozzi: structure of embedded minimal surfaces

**Geometric Measure Theory:**
- Rectifiable currents
- Federer-Fleming compactness
- Regularity theory (Allard, De Giorgi)
- Monotonicity formula

### Hodge Theory

**Hodge Star:**
*: Ω^k(M) → Ω^{n-k}(M)
- α ∧ *β = ⟨α,β⟩ dV
- ** = (-1)^{k(n-k)} on k-forms

**Laplacian:**
Δ = dδ + δd where δ = (-1)^{nk+n+1} *d*
- Harmonic forms: Δω = 0
- Hodge theorem: H^k_{dR}(M) ≅ H^k(M) ≅ {harmonic k-forms}

**Hodge Decomposition:**
Ω^k(M) = H^k ⊕ dΩ^{k-1} ⊕ δΩ^{k+1}
- Orthogonal decomposition
- Every form has unique harmonic representative

**Kähler Manifolds:**
Complex manifold with Hermitian metric g satisfying dω = 0 (ω = Kähler form).
- Hodge numbers h^{p,q}
- Hodge symmetry: h^{p,q} = h^{q,p}
- Hard Lefschetz theorem
- L² cohomology

**Hodge Conjecture:**
For projective algebraic variety X:
Every Hodge class (rational (p,p)-class) is algebraic (linear combination of classes of algebraic cycles).
- One of Clay Millennium Prize Problems
- Known for p = 1 (Lefschetz (1,1) theorem)
- Open for p ≥ 2

### Spin Geometry

**Spin Structures:**
For oriented Riemannian manifold with w₂(M) = 0:
- Double cover of SO(n) bundle: Spin(n) → SO(n)
- Spinor bundle S = P_{Spin} ×_{Spin} Δ

**Dirac Operator:**
D: Γ(S) → Γ(S)
- Locally: D = Σ eᵢ·∇_{eᵢ}
- Self-adjoint, elliptic
- Index = Â-genus (Atiyah-Singer)

**Lichnerowicz Formula:**
D² = ∇*∇ + ¼R
- If R > 0, no harmonic spinors
- Obstruction to positive scalar curvature

**Seiberg-Witten Equations:**
For 4-manifold with spin^c structure:
D_Aψ = 0
F_A^+ = q(ψ)
- Monopole equations
- Seiberg-Witten invariants
- Applications: symplectic geometry, 4-manifold classification

### Geometric Analysis

**Elliptic Regularity:**
For elliptic operator L:
- If Lu ∈ C^∞, then u ∈ C^∞
- Schauder estimates: ||u||_{C^{2,α}} ≤ C(||Lu||_{C^α} + ||u||_{C⁰})
- L^p estimates: ||u||_{W^{2,p}} ≤ C(||Lu||_{L^p} + ||u||_{L^p})

**Maximum Principles:**
- Weak: if Δu ≥ 0, u attains maximum on boundary
- Strong: if Δu ≥ 0 and u has interior maximum, u is constant
- Hopf boundary lemma

**Moser Iteration:**
Technique for obtaining L^∞ bounds from L^p bounds.
- Harnack inequality
- Applications: De Giorgi-Nash-Moser theory

**Blow-up Analysis:**
Rescaling near singularities to understand limiting behavior.
- Bubble tree
- Energy quantization
- Removable singularity theorems

**Conformal Geometry:**
- Yamabe problem: find constant scalar curvature in conformal class
- Aubin-Schoen solution
- Paneitz operator (4D)
- Q-curvature
- Conformally compact manifolds (AdS/CFT)

### Optimal Transport

**Monge Problem:**
Minimize ∫ c(x,T(x)) dμ(x) over T with T_*μ = ν.

**Kantorovich Relaxation:**
Minimize ∫ c(x,y) dπ(x,y) over couplings π ∈ Π(μ,ν).
- Linear programming problem
- Dual: maximize ∫ φ dμ + ∫ ψ dν with φ(x) + ψ(y) ≤ c(x,y)

**Optimal Maps:**
For c(x,y) = |x-y|²/2:
- Brenier's theorem: optimal map T = ∇φ for convex φ
- Monge-Ampère equation: det(D²φ) = f/g(∇φ)

**Wasserstein Distance:**
W_p(μ,ν) = (inf_{π∈Π(μ,ν)} ∫ d(x,y)^p dπ)^{1/p}
- Metric on space of probability measures
- Geodesics: displacement interpolation
- Ricci curvature lower bounds (Lott-Villani-Sturm)

**Applications:**
- Gradient flows in metric spaces
- Mean field games
- Machine learning (Wasserstein GANs)
- Economics


---
