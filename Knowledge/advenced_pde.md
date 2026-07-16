# CHAPTER 18: PARTIAL DIFFERENTIAL EQUATIONS (ADVANCED)


## Nonlinear PDEs & Regularity Theory

### Navier-Stokes Equations

**Incompressible Navier-Stokes:**
∂u/∂t + (u·∇)u = -∇p + νΔu + f
∇·u = 0

**Weak Solutions (Leray-Hopf):**
u ∈ L^∞(0,T; L²) ∩ L²(0,T; H¹)
- Existence in 3D (Leray, 1934)
- Uniqueness: open (Millennium Prize Problem)
- Partial regularity (Caffarelli-Kohn-Nirenberg): singular set has Hausdorff dimension ≤ 1

**Blow-up Criteria:**
- Beale-Kato-Majda: ∫₀^T ||ω(t)||_{L^∞} dt < ∞ prevents blow-up
- Prodi-Serrin: u ∈ L^q(0,T; L^p) with 2/q + 3/p ≤ 1

**Euler Equations (ν = 0):**
- Local well-posedness in H^s, s > 5/2
- Global regularity open in 3D
- Onsager conjecture: Hölder 1/3 solutions conserve energy

**Turbulence:**
- Kolmogorov's K41 theory
- Energy cascade: E(k) ~ Cε^{2/3}k^{-5/3}
- Intermittency
- Anomalous dissipation

### Regularity Theory

**De Giorgi-Nash-Moser Theory:**
For divergence-form elliptic equations:
- Harnack inequality
- Hölder continuity of solutions
- No continuity assumptions on coefficients needed

**Krylov-Safonov Theory:**
For non-divergence form equations:
- ABP estimate
- Harnack inequality
- Hölder estimates

**Calderón-Zygmund Theory:**
- Singular integrals
- L^p estimates for elliptic equations
- Commutator estimates

**Schauder Estimates:**
For Lu = f with Hölder continuous coefficients:
||u||_{C^{2,α}} ≤ C(||f||_{C^α} + ||u||_{C⁰})

**Fully Nonlinear Equations:**
F(D²u, Du, u, x) = 0
- Evans-Krylov theorem: C^{2,α} regularity for concave F
- Caffarelli's perturbation theory
- Monge-Ampère equation: det(D²u) = f

### Geometric PDEs

**Minimal Surface Equation:**
div(∇u/√(1+|∇u|²)) = 0
- Bernstein problem
- De Giorgi-Nash-Moser for minimal graphs
- Colding-Minicozzi theory

**Mean Curvature Flow:**
∂X/∂t = H·ν
- Huisken's theorem: convex → round point
- Singularity analysis
- Surgery (Huisken-Sinestrari)

**Ricci Flow PDE:**
∂g/∂t = -2Ric(g)
- Hamilton's program
- Perelman's entropy functionals
- No local collapsing
- Canonical neighborhood theorem

**Yamabe Equation:**
-Δu + (n-2)/4(n-1) R u = λu^{(n+2)/(n-2)}
- Yamabe problem solved by Aubin, Schoen, Trudinger
- Compactness of solution set

**Prescribed Curvature Problems:**
- Nirenberg problem: prescribed Gaussian curvature on S²
- Kazdan-Warner obstruction
- Chern-Yamabe flow

### Dispersive PDEs

**Nonlinear Schrödinger Equation:**
i∂u/∂t + Δu = ±|u|^{p-1}u
- Local well-posedness (Strichartz estimates)
- Global well-posedness (conservation laws)
- Blow-up vs scattering dichotomy
- Solitons and stability

**Korteweg-de Vries (KdV) Equation:**
∂u/∂t + ∂³u/∂x³ + 6u∂u/∂x = 0
- Complete integrability
- Inverse scattering transform
- Lax pair
- Infinite conservation laws

**Wave Maps:**
□u = A(u)(∂u, ∂u)
- Critical dimension: n = 2
- Global regularity for symmetric targets
- Bubbling analysis

**Einstein Vacuum Equations:**
R_{μν} = 0
- Local existence (Choquet-Bruhat)
- Global stability of Minkowski (Christodoulou-Klainerman)
- Formation of singularities (Christodoulou)
- Cosmic censorship conjectures

### Free Boundary Problems

**Stefan Problem:**
Heat equation in domain with moving boundary.
- Classical vs weak solutions
- Regularity of free boundary
- Applications: phase transitions, melting ice

**Obstacle Problem:**
min{∫ |∇u|² : u ≥ φ}
- Regularity of solution: C^{1,1}
- Regularity of free boundary
- Thin obstacle problem

**Hele-Shaw Flow:**
Darcy's law in thin gap.
- Saffman-Taylor instability
- Laplacian growth
- Integrable structure

### Stochastic PDEs

**Stochastic Heat Equation:**
∂u/∂t = Δu + ξ
where ξ = space-time white noise.
- Solution theory (Walsh, Da Prato-Zabczyk)
- Regularity: u ∈ C^{1/2-, 1/4-}

**Stochastic Navier-Stokes:**
∂u/∂t + (u·∇)u = -∇p + νΔu + σ(u)Ẇ
- Martingale solutions
- Pathwise uniqueness open in 3D
- Ergodicity

**Kardar-Parisi-Zhang (KPZ) Equation:**
∂h/∂t = ν∂²h/∂x² + λ/2 (∂h/∂x)² + ξ
- Ill-posed in classical sense
- Regularization (Hairer, 2013)
- Universality class
- Tracy-Widom fluctuations

**Parabolic Anderson Model:**
∂u/∂t = Δu + u·ξ
- Intermittency
- Lyapunov exponents
- Moment asymptotics

### Microlocal Analysis

**Pseudodifferential Operators:**
Op(a)u(x) = (2π)^{-n} ∫∫ e^{i(x-y)·ξ} a(x,ξ) u(y) dy dξ
- Symbol classes S^m_{ρ,δ}
- Composition formula
- Parametrix construction

**Wave Front Set:**
WF(u) = directions where u is not smooth.
- Propagation of singularities
- Hormander's theorem

**Fourier Integral Operators:**
Generalization of pseudodifferential operators.
- Canonical relation
- Clean intersection calculus
- Applications: hyperbolic equations, spectral theory

---
