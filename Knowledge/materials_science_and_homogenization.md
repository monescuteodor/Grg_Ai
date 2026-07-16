# CHAPTER 20: MATHEMATICAL MATERIALS SCIENCE & HOMOGENIZATION


## Continuum Mechanics

### Kinematics & Balance Laws

**Deformation Gradient:**
F = ∂x/∂X = I + ∇u
- Polar decomposition: F = RU = VR
- Right Cauchy-Green: C = F^T F
- Left Cauchy-Green: B = FF^T
- Green-Lagrange strain: E = ½(C - I)

**Balance Laws:**
- Mass: ρ₀ = ρJ (J = det F)
- Momentum: ρü = div σ + f
- Angular momentum: σ = σ^T
- Energy: ρė = σ:D - div q + r

**Constitutive Relations:**
- Elastic: σ = ∂W/∂F
- Hyperelastic: W = W(F)
- Frame indifference: W(F) = W(QF) for all Q ∈ SO(3)
- Isotropic: W(F) = W(λ₁,λ₂,λ₃) where λᵢ are principal stretches

### Elasticity Theory

**Linear Elasticity:**
σ = ℂ:ε where ℂ is elasticity tensor.
- Symmetries: major and minor
- Isotropic: σ = λ(tr ε)I + 2με
- Lamé parameters: λ, μ
- Young's modulus E, Poisson's ratio ν

**Variational Principles:**
- Minimum potential energy
- Hellinger-Reissner
- Hu-Washizu

**Existence Theory:**
- Korn's inequality
- Lax-Milgram
- Existence for linear elasticity
- Nonlinear elasticity: polyconvexity, quasiconvexity, rank-one convexity

**Saint-Venant's Principle:**
Statically equivalent loads produce same stresses far from boundary.

### Plasticity

**Yield Criteria:**
- von Mises: J₂ = k² where J₂ = ½s:s (s = deviatoric stress)
- Tresca: max shear stress = k
- Mohr-Coulomb
- Drucker-Prager

**Flow Rules:**
- Associative: ε̇^p = λ ∂f/∂σ (normality)
- Non-associative
- Kuhn-Tucker conditions

**Hardening:**
- Isotropic: yield surface expands
- Kinematic: yield surface translates (Bauschinger effect)
- Combined

**Variational Inequalities:**
- Prandtl-Reuss equations
- Hencky vs incremental plasticity
- Perfect plasticity limit

### Fracture Mechanics

**Griffith's Criterion:**
Crack propagates when energy release rate G ≥ G_c.

**Stress Intensity Factors:**
- K_I (opening), K_II (sliding), K_III (tearing)
- K_{Ic}: critical value (fracture toughness)

**Phase Field Models:**
- Ambrosio-Tortorelli approximation
- AT-1, AT-2 functionals
- Crack path prediction

**Variational Approach to Fracture (Francfort-Marigo):**
Minimize total energy: elastic energy + surface energy.
- Quasi-static evolution
- Crack initiation
- Griffith vs Barenblatt

## Homogenization

### Periodic Homogenization

**Two-Scale Convergence:**
u_ε(x) → u₀(x,y) where y = x/ε.
- Test functions: φ(x, x/ε)
- Limit equation contains corrector

**Homogenized Coefficients:**
For -div(A(x/ε)∇u_ε) = f:
-div(A*∇u₀) = f
where A*_{ij} = ∫_Y A_{ik}(∂χ^j/∂y_k + δ_{jk}) dy
and χ^j solves cell problem.

**Correctors:**
u_ε(x) = u₀(x) + εu₁(x, x/ε) + O(ε²)
- First-order corrector: u₁(x,y) = -χ^j(y) ∂u₀/∂x_j

**Rate of Convergence:**
||u_ε - u₀||_{L²} ≤ Cε
||u_ε - u₀ - εu₁||_{H¹} ≤ Cε

### Stochastic Homogenization

**Random Media:**
A(ω, x) stationary and ergodic.
- Subadditive ergodic theorem
- Homogenized coefficients: A* = E[A(I + ∇χ)]

**Quantitative Estimates:**
- Gloria-Otto: optimal variance decay
- Armstrong-Souganidis: quantitative homogenization
- Regularity theory in random media

**Percolation Homogenization:**
- Conductivity of percolation clusters
- Critical exponents
- Alexander-Orbach conjecture

### Γ-Convergence

**Definition:**
F_ε Γ-converges to F if:
1. Liminf inequality: F(u) ≤ liminf F_ε(u_ε) for u_ε → u
2. Recovery sequence: ∃ u_ε → u with F(u) ≥ limsup F_ε(u_ε)

**Properties:**
- Stability under continuous perturbations
- Convergence of minimizers
- Compactness of minimizing sequences

**Applications:**
- Phase transitions (Modica-Mortola)
- Thin structures
- Perforated domains
- Dimension reduction

### H-Convergence

**Definition:**
A_ε H-converges to A* if for all f:
u_ε → u₀ weakly in H¹
A_ε∇u_ε → A*∇u₀ weakly in L²
where -div(A_ε∇u_ε) = -div(A*∇u₀) = f.

**Properties:**
- Compactness: bounded sequences have H-convergent subsequences
- Local character
- G-closure problems

**Bounds:**
- Hashin-Shtrikman bounds
- Wiener bounds
- Milton's translation method
- Optimal microstructures

## Microstructure

### Calculus of Variations in Materials

**Quasiconvexity:**
W is quasiconvex if:
∫_Ω W(F + ∇φ) dx ≥ |Ω|W(F) for all φ with φ|_{∂Ω} = 0.
- Necessary and sufficient for weak lower semicontinuity
- Difficult to verify

**Rank-One Convexity:**
W(F + t a⊗b) is convex in t.
- Necessary for quasiconvexity
- Not sufficient (Šverák's counterexample)

**Polyconvexity:**
W(F) = g(F, cof F, det F) with g convex.
- Sufficient for quasiconvexity
- Used in existence theory for nonlinear elasticity

**Microstructure Formation:**
- Non-attainment of infimum
- Oscillations and concentrations
- Young measures
- Lamination, branching

### Young Measures

**Definition:**
For sequence u_ε with |u_ε|^p uniformly integrable:
∃ subsequence and probability measures ν_x such that:
f(u_ε) → ∫ f(λ) dν_x(λ) weakly for continuous f.

**Properties:**
- ν_x captures oscillation
- Barycenter: ū(x) = ∫ λ dν_x(λ)
- Jensen's inequality for quasiconvex functions

**Gradient Young Measures:**
- Characterization (Kinderlehrer-Pedregal)
- Lamination convex hull
- Quasiconvex hull

### Shape Memory Alloys

**Modeling:**
- Multiple energy wells
- Austenite and martensite phases
- Hysteresis
- Pseudoelasticity

**Mathematical Models:**
- Landau theory
- Ginzburg-Landau type
- Phase field models
- Rate-independent systems

### Liquid Crystals

**Order Parameter:**
Q = S(n⊗n - ⅓I) where n is director.

**Free Energy:**
- Oseen-Frank: ∫ W(∇n, n) dx
- Landau-de Gennes: ∫ f(Q, ∇Q) dx
- Ericksen-Leslie equations

**Defects:**
- Point defects (hedgehogs)
- Line defects (disclinations)
- Surface defects

## Active Matter

### Collective Motion

**Vicsek Model:**
θᵢ(t+1) = atan2(Σ sin θⱼ, Σ cos θⱼ) + noise
- Phase transition to ordered motion
- Long-range order in 2D (violation of Mermin-Wagner due to non-equilibrium)

**Continuum Models:**
- Toner-Tu equations
- Broken Galilean invariance
- Giant number fluctuations

**Hydrodynamic Theories:**
- Active nematics
- Active polar fluids
- Defect dynamics

### Cell Mechanics

**Cytoskeleton Models:**
- Active gel theory
- Motor-filament interactions
- Contractility
- Pattern formation

**Cell Migration:**
- Keratocyte model
- Free boundary problems
- Actin polymerization
- Adhesion dynamics

---
