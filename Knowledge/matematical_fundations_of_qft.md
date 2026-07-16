# CHAPTER 24: MATHEMATICAL FOUNDATIONS OF QUANTUM FIELD THEORY


## Axiomatic QFT

### Wightman Axioms

**Assumptions:**
1. **Relativistic invariance:** Unitary representation U(a,Λ) of Poincaré group on Hilbert space H.
2. **Spectral condition:** Spectrum of energy-momentum in forward light cone.
3. **Locality:** Fields commute/anticommute at spacelike separations.
4. **Completeness:** Vacuum cyclic for polynomial algebra of fields.

**Wightman Functions:**
W_n(x₁,...,xₙ) = ⟨Ω, φ(x₁)...φ(xₙ)Ω⟩
- Analytic continuation to complex domain
- Reconstruction theorem: Wightman functions determine theory

**Spin-Statistics Theorem:**
Integer spin → bosons (commutation)
Half-integer spin → fermions (anticommutation)
- Consequence of PCT theorem

**PCT Theorem:**
Combined operation of parity, charge conjugation, time reversal is symmetry.
- PCT = antiunitary operator Θ
- Θφ(x)Θ⁻¹ = η φ(-x)*

### Haag-Kastler Axioms

**Local Nets:**
Assignment O ↦ A(O) of C*-algebras to open regions in Minkowski space.
- Isotony: O₁ ⊆ O₂ ⇒ A(O₁) ⊆ A(O₂)
- Locality: [A(O₁), A(O₂)] = 0 for spacelike separated O₁, O₂
- Poincaré covariance
- Spectrum condition
- Vacuum: cyclic and separating for wedge algebras

**Type III Factors:**
Local algebras in QFT are type III₁ factors.
- Connes' classification
- Modular theory
- Bisognano-Wichmann theorem: modular group = Lorentz boosts

**DHR Theory (Doplicher-Haag-Roberts):**
Superselection sectors in terms of localized endomorphisms.
- Charge quantum numbers
- Braiding and statistics
- Doplicher-Roberts reconstruction: gauge group from sectors

### Constructive QFT

**Models in 2D:**
- P(φ)₂: polynomial interaction
- Yukawa₂
- Sine-Gordon
- Thirring model

**Methods:**
- Euclidean path integral
- Lattice approximation
- Nelson-Symanzik positivity
- Osterwalder-Schrader reconstruction

**Phase Transitions:**
- λφ⁴ in 2D and 3D
- Symmetry breaking
- Critical behavior

## Perturbative QFT

### Feynman Diagrams

**S-Matrix Expansion:**
S = T exp(-i ∫ H_I(t) dt)
- Dyson series
- Time-ordered products
- Wick's theorem

**Feynman Rules:**
- Propagators: lines
- Vertices: interactions
- Loops: momentum integrals
- Symmetry factors

**Renormalization:**
- UV divergences
- Regularization: cutoff, dimensional, Pauli-Villars
- Counterterms
- BPHZ (Bogoliubov-Parasiuk-Hepp-Zimmermann) renormalization

**Renormalization Group:**
- Callan-Symanzik equation
- β-functions
- Fixed points
- Asymptotic freedom (Gross-Wilczek-Politzer)
- Asymptotic safety

### Gauge Theory

**Classical Gauge Theory:**
- Principal G-bundle P → M
- Connection A ∈ Ω¹(P, g)
- Curvature F = dA + ½[A,A]
- Yang-Mills action: S = ∫ tr(F∧*F)

**Quantization:**
- Faddeev-Popov method
- Ghost fields
- BRST symmetry
- Slavnov-Taylor identities

**Anomalies:**
- Classical symmetry broken at quantum level
- Adler-Bell-Jackiw (ABJ) anomaly
- Fujikawa method
- Consistency conditions (Wess-Zumino)

**Instantons:**
- Self-dual connections: F = ±*F
- Topological charge: Q = (1/8π²) ∫ tr(F∧F)
- Tunneling between vacua
- θ-vacuum
- U(1) problem

### Algebraic QFT

**Conformal Nets:**
Local nets on circle (1D) or higher.
- Diffeomorphism covariance
- Virasoro algebra
- Representation theory
- μ-index (Kawahigashi-Longo)

**Modular Tensor Categories:**
- Objects = superselection sectors
- Braiding
- Fusion rules
- Modular S, T matrices
- Verlinde formula

**Boundary Conformal Field Theory:**
- Boundary states
- Cardy's condition
- Ishibashi states
- Entanglement entropy

## Topological QFT

### Atiyah-Segal Axioms

**Definition:**
Functor Z: Bord_n → Vect from bordism category to vector spaces.
- Z(∅) = ℂ
- Z(M₁ ⊔ M₂) = Z(M₁) ⊗ Z(M₂)
- Z(∂M) = Z(M) for closed M

**Examples in 2D:**
- Semisimple Frobenius algebras
- Finite group gauge theory
- Chern-Simons with finite gauge group

**Extended TQFT:**
- Bordism n-category
- Values on manifolds of all dimensions
- Fully dualizable objects

### Chern-Simons Theory

**Action:**
S_CS = (k/4π) ∫_M tr(A∧dA + ⅔A∧A∧A)
- Level k ∈ ℤ
- Gauge group G compact
- 3D manifold M

**Quantization:**
- Conformal blocks on boundary
- Reshetikhin-Turaev invariants
- Jones polynomial for knots
- Witten's path integral interpretation

**Modular Functor:**
- Assigns vector space to surface
- Mapping class group action
- Verlinde formula for dimension

**Applications:**
- Knot invariants
- 3-manifold invariants
- Topological quantum computing
- Fractional quantum Hall effect

### 4D TQFT

**Donaldson-Witten Theory:**
- Twist of N=2 supersymmetric Yang-Mills
- Donaldson invariants from correlation functions
- Seiberg-Witten simplification

**Seiberg-Witten TQFT:**
- Abelian gauge theory with monopole
- SW invariants
- Simple type conjecture
- Relation to Gromov-Witten theory

**Crane-Yetter-Broda:**
- State-sum models
- Categorical construction
- Turaev-Viro (3D) and Crane-Yetter (4D)

## String Theory Mathematics

### Worldsheet Theory

**Polyakov Action:**
S = -(T/2) ∫ d²σ √g g^{ab} ∂_a X^μ ∂_b X_μ
- Conformal invariance
- Critical dimension: D = 26 (bosonic), D = 10 (super)

**Conformal Field Theory on Worldsheet:**
- Virasoro algebra
- Primary fields
- OPE (operator product expansion)
- Conformal blocks

**String Perturbation Theory:**
- Genus expansion
- Moduli space of Riemann surfaces M_g
- Measure: Belavin-Knizhnik
- Divergences

### Calabi-Yau Manifolds

**Definition:**
Kähler manifold with c₁ = 0 and holonomy ⊆ SU(n).
- Ricci-flat Kähler metric (Yau's theorem)
- H^{p,0} = 0 for 0 < p < n (except H^{n,0} = ℂ)
- Canonical bundle trivial

**Hodge Numbers:**
- h^{1,1}: Kähler moduli
- h^{2,1}: complex structure moduli
- Euler characteristic: χ = 2(h^{1,1} - h^{2,1})

**Mirror Symmetry:**
X and X* are mirror if h^{p,q}(X) = h^{n-p,q}(X*).
- Hodge number exchange
- Yukawa couplings
- Gromov-Witten invariants ↔ periods
- B-model (complex structure) ↔ A-model (Kähler)

**Gromov-Witten Theory:**
- Counting holomorphic curves
- Gromov-Witten invariants
- Quantum cohomology
- Mirror theorem (Givental, Lian-Liu-Yau)

### D-Branes

**Definition:**
Submanifolds where open strings end.
- Dirichlet boundary conditions
- Chan-Paton factors
- Gauge fields on brane worldvolume

**Derived Category Description:**
- D-branes = objects in derived category of coherent sheaves
- Tachyon condensation = cone construction
- Stability conditions (Bridgeland)
- Pi-stability

**Homological Mirror Symmetry (Kontsevich):**
Fuk(X) ≅ D^b(Coh(X*))
- Fukaya category on A-side
- Derived category on B-side
- Open string states = morphisms

### M-Theory & F-Theory

**M-Theory:**
11-dimensional theory.
- Membranes and fivebranes
- Compactification on circle → IIA string theory
- Compactification on torus → type IIB (T-duality)

**F-Theory:**
Elliptically fibered Calabi-Yau fourfolds.
- Singular fibers encode gauge groups
- GUT model building
- Yukawa couplings from singularities

**AdS/CFT Correspondence:**
Type IIB on AdS₅ × S⁵ ↔ N=4 SYM on boundary.
- GKP-Witten relation
- Holographic renormalization
- Wilson loops
- Entanglement entropy (Ryu-Takayanagi)

## Algebraic QFT & Vertex Algebras

### Vertex Algebras

**Definition:**
Vector space V with vacuum |0⟩, translation operator T, and vertex operators:
Y(a,z) = Σ_{n∈ℤ} a_{(n)} z^{-n-1}
- Locality: (z-w)^N [Y(a,z), Y(b,w)] = 0 for N >> 0
- Translation: [T, Y(a,z)] = ∂_z Y(a,z)
- Vacuum: Y(|0⟩,z) = id, Y(a,z)|0⟩ = a + O(z)

**Examples:**
- Heisenberg vertex algebra
- Lattice vertex algebras
- Affine Kac-Moody vertex algebras
- Virasoro vertex algebra
- W-algebras

**Modules:**
- Admissible modules
- Zhu's algebra
- Rational vertex algebras
- Modular tensor category of modules

### Conformal Blocks

**Definition:**
Space of coinvariants of tensor product of modules.
- Flat connection (Knizhnik-Zamolodchikov)
- Monodromy = braid group representation
- Fusion rules

**Verlinde Formula:**
dim V(Σ, g, k) = |T_k|^{-g} Σ_{μ∈T_k} S_{0μ}^{2-2g}
where T_k = level k weights, S = modular matrix.

**Applications:**
- WZW models
- Chern-Simons theory
- Topological quantum computing

### Chiral Algebras

**Beilinson-Drinfeld:**
- Factorization algebras
- Chiral homology
- Hecke eigensheaves
- Geometric Langlands

**4D N=2 Theories:**
- Seiberg-Witten curves
- BPS states
- Wall-crossing
- Spectral networks

---
