# CHAPTER 8: MATHEMATICAL PHYSICS


## Classical Mechanics

### Lagrangian Mechanics

**Principle of Least Action:**
δS = 0 where S = ∫_{t₁}^{t₂} L(q, q̇, t) dt

**Euler-Lagrange Equations:**
d/dt(∂L/∂q̇ᵢ) - ∂L/∂qᵢ = 0

**Examples:**
- Free particle: L = ½mv²
- Harmonic oscillator: L = ½mq̇² - ½kq²
- Central force: L = ½m(ṙ² + r²θ̇²) - V(r)

**Noether's Theorem:**
Every continuous symmetry of L gives conserved quantity:
- Time translation → Energy
- Space translation → Momentum
- Rotation → Angular momentum

**Legendre Transform:**
H(q,p) = p·q̇ - L(q,q̇) where p = ∂L/∂q̇

### Hamiltonian Mechanics

**Hamilton's Equations:**
q̇ᵢ = ∂H/∂pᵢ
ṗᵢ = -∂H/∂qᵢ

**Poisson Brackets:**
{f,g} = Σᵢ (∂f/∂qᵢ ∂g/∂pᵢ - ∂f/∂pᵢ ∂g/∂qᵢ)
- {qᵢ, pⱼ} = δᵢⱼ
- Time evolution: df/dt = {f,H} + ∂f/∂t
- Jacobi identity: {f,{g,h}} + {g,{h,f}} + {h,{f,g}} = 0

**Canonical Transformations:**
Preserve Poisson brackets / symplectic form.
- Generating functions F₁(q,Q), F₂(q,P), etc.
- Hamilton-Jacobi equation: H(q, ∂S/∂q) + ∂S/∂t = 0

**Liouville's Theorem:**
Hamiltonian flow preserves phase space volume.

**Integrable Systems:**
System with n degrees of freedom and n independent conserved quantities in involution.
- Action-angle variables
- Arnold-Liouville theorem: tori in phase space
- KAM theorem: persistence of invariant tori under perturbation

### Symplectic Geometry in Mechanics

**Symplectic Manifold:**
(M, ω) with closed non-degenerate 2-form.
- Phase space of Hamiltonian system
- Darboux coordinates: ω = Σ dpᵢ ∧ dqᵢ

**Hamiltonian Vector Field:**
X_H defined by ι_{X_H}ω = dH
- Flow preserves ω
- Integral curves = solutions of Hamilton's equations

**Moment Map:**
For Hamiltonian G-action: μ: M → g*
- Noether's theorem: μ is conserved
- Symplectic reduction: M//G = μ⁻¹(0)/G


## Quantum Mechanics

### Mathematical Foundations

**Hilbert Space:**
H = complex Hilbert space (complete inner product space)
- States: unit vectors ψ ∈ H (up to phase)
- Observables: self-adjoint operators A = A*

**Postulates:**
1. State: |ψ⟩ ∈ H, ||ψ|| = 1
2. Observable: Hermitian operator A
3. Measurement: eigenvalue a with probability |⟨a|ψ⟩|²
4. After measurement: state collapses to |a⟩
5. Evolution: |ψ(t)⟩ = U(t)|ψ(0)⟩ where U = e^{-iHt/ℏ}

**Schrödinger Equation:**
iℏ ∂ψ/∂t = Hψ
where H = -ℏ²/2m ∇² + V (Hamiltonian operator)

**Stationary States:**
ψ(x,t) = φ(x)e^{-iEt/ℏ} where Hφ = Eφ (time-independent Schrödinger equation)

### Operator Theory in QM

**Spectral Theorem:**
For self-adjoint A:
A = ∫ λ dE(λ)
where E is projection-valued measure.

**Commutation Relations:**
[q, p] = iℏ
- Heisenberg uncertainty: Δq Δp ≥ ℏ/2
- [Lᵢ, Lⱼ] = iℏ εᵢⱼₖ Lₖ (angular momentum)

**Harmonic Oscillator:**
H = ℏω(a*a + ½)
where a = √(mω/2ℏ)(q + ip/mω), a* = √(mω/2ℏ)(q - ip/mω)
- [a, a*] = 1
- Eigenvalues: Eₙ = ℏω(n + ½)
- Eigenstates: |n⟩ = (a*)ⁿ/√(n!) |0⟩

### Advanced Topics

**Path Integrals (Feynman):**
⟨x_f, t_f | x_i, t_i⟩ = ∫_{x(t_i)=x_i}^{x(t_f)=x_f} e^{iS[x]/ℏ} Dx
- Sum over all paths
- Connection to classical mechanics (ℏ → 0: stationary phase)

**Density Matrix:**
ρ = Σᵢ pᵢ |ψᵢ⟩⟨ψᵢ|
- Pure state: ρ = |ψ⟩⟨ψ|, ρ² = ρ
- Mixed state: ρ² ≠ ρ
- Evolution: iℏ ∂ρ/∂t = [H, ρ]
- Entropy: S = -tr(ρ log ρ)

**Entanglement:**
|ψ⟩ cannot be written as |ψ₁⟩ ⊗ |ψ₂⟩.
- Bell states: maximally entangled
- EPR paradox, Bell inequalities
- Quantum teleportation, superdense coding

**Quantum Field Theory (Mathematical Aspects):**
- Wightman axioms
- Haag-Kastler axioms (algebraic QFT)
- Constructive QFT in 2D and 3D
- Renormalization group


## General Relativity

### Differential Geometry of Spacetime

**Manifold:**
4-dimensional smooth manifold M.

**Metric:**
Lorentzian metric g with signature (-,+,+,+) or (+,-,-,-).
- Spacetime interval: ds² = g_{μν} dx^μ dx^ν

**Levi-Civita Connection:**
Christoffel symbols: Γ^λ_{μν} = ½g^{λσ}(∂_μ g_{νσ} + ∂_ν g_{μσ} - ∂_σ g_{μν})

**Curvature:**
- Riemann tensor: R^ρ_{σμν} = ∂_μΓ^ρ_{νσ} - ∂_νΓ^ρ_{μσ} + Γ^ρ_{μλ}Γ^λ_{νσ} - Γ^ρ_{νλ}Γ^λ_{μσ}
- Ricci tensor: R_{μν} = R^λ_{μλν}
- Scalar curvature: R = g^{μν}R_{μν}
- Einstein tensor: G_{μν} = R_{μν} - ½g_{μν}R

### Einstein's Equations

**Field Equations:**
G_{μν} + Λg_{μν} = (8πG/c⁴)T_{μν}

**In vacuum (T = 0, Λ = 0):**
R_{μν} = 0

**Schwarzschild Solution:**
Spherically symmetric, static vacuum solution:
ds² = -(1-2GM/rc²)c²dt² + (1-2GM/rc²)⁻¹dr² + r²dΩ²
- Event horizon at r = 2GM/c² (Schwarzschild radius)
- Singularity at r = 0

**Kerr Solution:**
Rotating black hole:
- Inner and outer event horizons
- Ergosphere
- Penrose process

**Friedmann-Lemaître-Robertson-Walker (FLRW):**
Homogeneous, isotropic universe:
ds² = -c²dt² + a(t)²[dr²/(1-kr²) + r²dΩ²]
- Scale factor a(t)
- Curvature k = -1, 0, +1

**Friedmann Equations:**
(ȧ/a)² = (8πG/3)ρ - k/a² + Λ/3
ä/a = -(4πG/3)(ρ + 3p) + Λ/3

### Black Hole Thermodynamics

**Laws:**
0. Surface gravity κ is constant on horizon (stationary BH)
1. δM = (κ/8πG)δA + ΩδJ + ΦδQ (analogous to dE = TdS)
2. δA ≥ 0 (second law)
3. Cannot reach κ = 0 in finite steps (third law)

**Bekenstein-Hawking Entropy:**
S_{BH} = k_B A/(4ℓ_P²) = k_B c³A/(4Gℏ)
where A = horizon area, ℓ_P = √(Gℏ/c³) = Planck length.

**Hawking Temperature:**
T_H = ℏκ/(2πk_B c) = ℏc³/(8πGMk_B)
- Black holes emit thermal radiation
- Connection to quantum field theory in curved spacetime

### Cosmology

**Standard Model (ΛCDM):**
- Dark energy (Λ): ~68% of energy density
- Dark matter: ~27%
- Baryonic matter: ~5%

**Inflation:**
Exponential expansion in early universe.
- Solves flatness, horizon, monopole problems
- Predicts nearly scale-invariant perturbations

**Cosmic Microwave Background:**
- Blackbody spectrum at T ≈ 2.725 K
- Anisotropies: δT/T ~ 10⁻⁵
- Power spectrum: C_ℓ as function of multipole ℓ


## Statistical Mechanics

### Ensembles

**Microcanonical Ensemble:**
Isolated system with fixed E, V, N.
- Entropy: S = k_B log Ω(E)
- Temperature: 1/T = ∂S/∂E

**Canonical Ensemble:**
System in contact with heat bath at temperature T.
- Partition function: Z = Σᵢ e^{-Eᵢ/k_BT}
- Probability: Pᵢ = e^{-Eᵢ/k_BT}/Z
- Free energy: F = -k_BT log Z

**Grand Canonical Ensemble:**
System with fixed T, V, μ.
- Grand partition function: Ξ = Σ_N e^{μN/k_BT} Z_N

### Phase Transitions

**Types:**
- First order: discontinuity in first derivative of free energy
- Second order: discontinuity in second derivative
- Critical point: where phase boundary ends

**Critical Exponents:**
Near critical temperature T_c:
- Specific heat: C ~ |T-T_c|^{-α}
- Magnetization: M ~ (T_c - T)^β
- Susceptibility: χ ~ |T-T_c|^{-γ}
- Correlation length: ξ ~ |T-T_c|^{-ν}

**Universality:**
Systems in same universality class have same critical exponents.
- Determined by dimension and symmetry
- Ising model (d=2): α=0, β=1/8, γ=7/4, ν=1
- Mean field (d≥4): α=0, β=1/2, γ=1, ν=1/2

**Ising Model:**
H = -J Σ_{⟨i,j⟩} σᵢσⱼ - h Σᵢ σᵢ
where σᵢ = ±1.
- d=1: no phase transition (exact solution)
- d=2: exact solution (Onsager), T_c = 2J/(k_B log(1+√2))
- d≥3: no exact solution, numerical and series methods

**Renormalization Group:**
- Coarse-graining procedure
- Fixed points = critical points
- Critical exponents from linearization at fixed point
- ε-expansion: d = 4 - ε

### Exactly Solved Models

**2D Ising Model:**
Partition function: Z = (2 sinh(2J/k_BT))^{N/2} exp(Σ γ_{2n+1})
where γₙ = arccosh(cosh(2K)cosh(2K') - sinh(2K)sinh(2K')cos(nπ/N))

**6-Vertex Model:**
Ice-type model with 6 allowed vertex configurations.
- Exact solution by Lieb
- Connection to XXZ spin chain

**8-Vertex Model:**
Generalization of 6-vertex model.
- Solved by Baxter
- Free fermion condition

**XY Model:**
H = -J Σ_{⟨i,j⟩} (Sᵢ^x Sⱼ^x + Sᵢ^y Sⱼ^y)
- Kosterlitz-Thouless transition
- Vortex-antivortex unbinding

### Integrable Systems

**Classical Integrability:**
System with n degrees of freedom and n independent conserved quantities in involution.
- Lax pair: dL/dt = [L,M]
- Spectral curve: det(L(λ) - μI) = 0

**Quantum Integrability:**
- Yang-Baxter equation: R₁₂R₁₃R₂₃ = R₂₃R₁₃R₁₂
- Transfer matrix: t(λ) = tr(T(λ))
- Commuting transfer matrices: [t(λ), t(μ)] = 0
- Bethe ansatz for eigenvalues

**Bethe Ansatz:**
Method for solving quantum integrable models.
- Coordinate Bethe ansatz
- Algebraic Bethe ansatz
- Thermodynamic Bethe ansatz


---
