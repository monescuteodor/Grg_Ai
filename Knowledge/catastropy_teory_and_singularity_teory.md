# CHAPTER 22: CATASTROPHE THEORY & SINGULARITY THEORY


## Catastrophe Theory

### Elementary Catastrophes

**Thom's Classification:**
For families of functions f: ℝⁿ → ℝ depending on ≤ 4 parameters:
- Stable unfoldings of singularities
- Seven elementary catastrophes

**The Seven Catastrophes:**

| Name | Codim | Normal Form | Potential |
|------|-------|-------------|-----------|
| Fold | 1 | x³ + ux | u = -3x² |
| Cusp | 2 | x⁴ + ux² + vx | u = -6x², v = 4x³ |
| Swallowtail | 3 | x⁵ + ux³ + vx² + wx | |
| Butterfly | 4 | x⁶ + tx⁴ + ux³ + vx² + wx | |
| Hyperbolic umbilic | 3 | x³ + y³ + uxy + vx + wy | |
| Elliptic umbilic | 3 | x³ - 3xy² + u(x²+y²) + vx + wy | |
| Parabolic umbilic | 4 | x²y + y⁴ + ux² + vy² + wx + ty | |

**Bifurcation Sets:**
- Catastrophe set: parameter values where topology changes
- Cusp lines
- Riemann-Hugoniot
- Applications: caustics, phase transitions, buckling

### Bifurcation Theory

**Local Bifurcations:**
- Saddle-node: ẋ = r + x²
- Transcritical: ẋ = rx - x²
- Pitchfork: ẋ = rx - x³
- Hopf: ẋ = (r + iω)z - z|z|²
- Period-doubling: logistic map

**Global Bifurcations:**
- Homoclinic bifurcation
- Heteroclinic bifurcation
- Saddle-node on invariant circle (SNIC)
- Blue sky catastrophe

**Center Manifold Reduction:**
For system ẋ = Ax + f(x,y), ẏ = By + g(x,y):
- Center manifold: y = h(x)
- Reduced dynamics on center manifold
- Normal form theory

**Normal Forms:**
- Poincaré-Dulac
- Unfoldings
- Versal deformations
- Codimension

## Singularity Theory

### Finite Determinacy

**k-Determinacy:**
f is k-determined if g with same k-jet as f is equivalent to f.
- Right equivalence: f ~ g if g = f∘φ for diffeomorphism φ
- Left-right equivalence
- Contact equivalence

**Finite Determinacy Theorem:**
f is finitely determined iff m^{k+1} ⊆ m⟨∂f/∂x₁,...,∂f/∂xₙ⟩ for some k.

**Classification:**
- A_k singularities: x^{k+1}
- D_k singularities: x²y + y^{k-1}
- E_6, E_7, E_8: exceptional
- Simple singularities correspond to ADE Dynkin diagrams

### Milnor Fibration

**Setup:**
f: ℂⁿ → ℂ holomorphic with isolated singularity at 0.

**Milnor Fibration:**
f/|f|: S_ε^{2n-1} \ f⁻¹(0) → S¹
- Fibre F = Milnor fibre
- Homotopy type: bouquet of (n-1)-spheres

**Milnor Number:**
μ = dim_ℂ ℂ{x₁,...,xₙ}/⟨∂f/∂x₁,...,∂f/∂xₙ⟩
- Number of spheres in bouquet
- Topological invariant

**Monodromy:**
h: F → F (geometric monodromy)
- Monodromy operator: h_*: H_{n-1}(F) → H_{n-1}(F)
- Characteristic polynomial = zeta function
- Picard-Lefschetz formula

**Mixed Hodge Structure:**
- On cohomology of Milnor fibre
- Steenbrink's construction
- Spectrum of singularity
- Varchenko's semicontinuity

### Stratification Theory

**Whitney Stratification:**
Decomposition of variety into smooth manifolds satisfying Whitney conditions.
- Condition (a): tangent spaces converge
- Condition (b): secants converge to tangent
- Existence (Whitney, Thom, Mather)
- Uniqueness (not canonical)

**Thom's Isotopy Lemma:**
For proper stratified submersion: local topological triviality.

**Stratified Morse Theory (Goresky-MacPherson):**
- Morse functions on stratified spaces
- Morse inequalities
- Intersection homology
- L² cohomology

### Resolution of Singularities

**Hironaka's Theorem:**
Every algebraic variety over ℂ has resolution of singularities.
- Blowing up
- Embedded resolution
- Log resolution
- Characteristic p: open (Abhyankar for surfaces, Cossart-Jannsen-Saito in general)

**Multiplier Ideals:**
J(c·|D|) for divisor D.
- Nadel vanishing
- Inversion of adjunction
- Asymptotic constructions

**Arc Spaces & Jet Schemes:**
- Arc space: X_∞ = lim X_n where X_n = n-jets
- Nash problem
- Motivic integration
- Denef-Loeser theory

### Deformation Theory

**Infinitesimal Deformations:**
For scheme X:
- First-order: Ext¹(Ω_X, O_X) = H¹(X, T_X)
- Obstructions: H²(X, T_X)
- Kodaira-Spencer map

**Formal Deformations:**
- Over Artin rings
- Schlessinger's criteria
- Pro-representable hull
- Versal deformation

**Moduli Problems:**
- Fine vs coarse moduli
- Representability
- Stacks
- Geometric invariant theory (GIT)

## Applications

### Optics & Caustics

**Wave Fronts:**
- Eikonal equation
- Lagrangian singularities
- Caustics as catastrophe sets
- Airy, Pearcey functions

**Oscillatory Integrals:**
I(λ) = ∫ e^{iλf(x)} a(x) dx
- Stationary phase
- Asymptotic expansion
- Catastrophe theory gives uniform approximations

### Phase Transitions

**Landau Theory:**
Free energy as function of order parameter.
- Symmetry breaking
- Critical exponents
- Universality
- Renormalization group

**Structural Stability:**
- Thom's philosophy: observable phenomena are structurally stable
- Catastrophes = boundaries of stability
- Applications: embryology, linguistics, economics

### Wave Propagation

**Shock Waves:**
- Burgers equation
- Riemann problem
- Lax entropy condition
- Oleinik condition

**Whitham Modulation Theory:**
- Slowly varying periodic waves
- KdV modulation
- DSW (dispersive shock waves)
- Riemann invariants

---
