# CHAPTER 19: ERGODIC THEORY & DYNAMICAL SYSTEMS (ADVANCED)


## Ergodic Theory

### Measure-Preserving Systems

**Definition:**
(X, B, μ, T) where T: X → X preserves μ: μ(T⁻¹A) = μ(A).

**Ergodicity:**
T is ergodic if invariant sets have measure 0 or 1.
- Equivalently: ∫ f∘T dμ = ∫ f dμ ⇒ f = constant a.e.
- Mixing: stronger than ergodicity
- Weak mixing, strong mixing, Bernoulli

**Birkhoff Ergodic Theorem:**
For f ∈ L¹ and ergodic T:
(1/n) Σ_{k=0}^{n-1} f(T^k x) → ∫ f dμ  a.e.

**Kingman's Subadditive Ergodic Theorem:**
For subadditive sequence f_n:
f_n(x) ≤ f_k(x) + f_{n-k}(T^k x)
⇒ (1/n)f_n(x) → inf (1/n)∫ f_n dμ  a.e.

**Poincaré Recurrence:**
For measurable A with μ(A) > 0:
Almost every x ∈ A returns to A infinitely often.

**Kac's Lemma:**
Expected return time to A = 1/μ(A).

### Entropy

**Kolmogorov-Sinai Entropy:**
h_μ(T) = sup_P h_μ(T,P) where
h_μ(T,P) = lim_{n→∞} (1/n) H(∨_{k=0}^{n-1} T^{-k}P)
- Measures complexity/information production
- Isomorphism invariant
- Bernoulli shifts: h = Σ -pᵢ log pᵢ

**Topological Entropy:**
h_{top}(T) = sup_P lim_{n→∞} (1/n) log N(∨_{k=0}^{n-1} T^{-k}P)
- h_μ ≤ h_{top} for all invariant μ
- Variational principle: h_{top} = sup_μ h_μ

**Lyapunov Exponents:**
For differentiable map T:
λ(x,v) = lim_{n→∞} (1/n) log ||DT^n(x)v||
- Oseledets theorem: existence for a.e. x
- Pesin theory: non-uniform hyperbolicity
- Ruelle inequality: h_μ ≤ Σ λ⁺ᵢ
- Pesin formula: equality for SRB measures

### Symbolic Dynamics

**Shift Spaces:**
Σ_A = {x ∈ A^ℤ : M_{xᵢ,x_{i+1}} = 1}
- Subshift of finite type (SFT)
- Sofic shift
- Coded shift

**Topological Properties:**
- Transitivity: dense orbit
- Mixing: product system transitive
- Specification: shadowing property
- Entropy: log of spectral radius

**Zeta Function:**
ζ(z) = exp(Σ_{n=1}^∞ (N_n/n)zⁿ)
where N_n = number of periodic points of period n.
- For SFT: rational function
- Ruelle zeta function

**Thermodynamic Formalism:**
For potential φ:
P(φ) = sup_μ [h_μ(T) + ∫φ dμ]
- Pressure = topological entropy for φ = 0
- Equilibrium state: measure achieving supremum
- Gibbs measure

### Smooth Ergodic Theory

**Anosov Diffeomorphisms:**
Uniform hyperbolicity: TM = E^s ⊕ E^u
- Stable/unstable manifolds
- Markov partitions
- SRB measures
- Structural stability

**Axiom A Systems:**
- Non-wandering set hyperbolic
- Periodic points dense
- Spectral decomposition
- Smale's horseshoe

**Hénon Map:**
(x,y) ↦ (1 - ax² + y, bx)
- Strange attractor for a = 1.4, b = 0.3
- Benedicks-Carleson: positive measure of parameters with strange attractor
- SRB measures

**Lorenz Attractor:**
ẋ = σ(y-x), ẏ = x(ρ-z)-y, ż = xy-βz
- Geometric Lorenz attractor
- Expanding Lorenz map
- Statistical properties

### Infinite Ergodic Theory

**Conservative Systems:**
μ(X) = ∞ but no wandering sets of positive measure.
- Hopf's ratio ergodic theorem
- Darling-Kac theorem
- Aaronson's distributional limits

**Intermittent Maps:**
T(x) = x + x^{1+α} (mod 1)
- Polynomial decay of correlations
- Darling-Kac law
- Stable laws for Birkhoff sums

**Infinite Measure-Preserving Transformations:**
- Renewal theory approach
- Mittag-Leffler distributions
- Arcsine laws

### Homogeneous Dynamics

**Unipotent Flows:**
- Ratner's theorems: orbit closures, invariant measures, equidistribution
- Oppenheim conjecture (Margulis)
- Littlewood conjecture (partial results)

**Diagonal Flows:**
- Geodesic flow on moduli space
- Teichmüller dynamics
- Eskin-Mirzakhani-Mohammadi: orbit closures are affine invariant submanifolds

**Arithmetic Applications:**
- Duke's theorem: equidistribution of Heegner points
- Linnik problems
- Quantum unique ergodicity (QUE)

## Complex Dynamics

### Iteration of Rational Maps

**Julia Set:**
J(f) = boundary of Fatou set = closure of repelling periodic points.
- Connected or totally disconnected (Cantor set)
- Self-similar, fractal structure
- Hausdorff dimension: 2 for generic f

**Fatou Set:**
F(f) = set of normality = basin of attraction.
- Components: attracting, parabolic, Siegel disk, Herman ring
- Sullivan's no wandering domains theorem

**Mandelbrot Set:**
M = {c ∈ ℂ : J(z² + c) is connected}
- Connected (Douady-Hubbard)
- Local connectivity: open (MLC conjecture)
- Hyperbolic components: interior
- Main cardioid, bulbs

**Bifurcation Theory:**
- Period doubling cascade
- Feigenbaum universality
- Mandelbrot set as bifurcation locus
- Lavaurs theorem

### Higher-Dimensional Complex Dynamics

**Hénon Maps (Complex):**
(z,w) ↦ (z² + c + aw, z)
- Newhouse phenomena
- Benedicks-Carleson parameters
- Currents and pluripotential theory

**Holomorphic Endomorphisms of ℙⁿ:**
- Green current
- Equilibrium measure
- Lyapunov exponents
- Large deviations

### Transcendental Dynamics

**Exponential Family:**
f_λ(z) = λe^z
- Escaping set
- Julia set = ℂ for many parameters
- Cantor bouquets
- Devaney hairs

**Trigonometric Functions:**
- Sine family: λ sin(z)
- Cosine family
- Escaping points and dimension

## Arithmetic Dynamics

### Dynamical Systems on Algebraic Varieties

**Canonical Height:**
For morphism f: ℙⁿ → ℙⁿ of degree d ≥ 2:
ĥ_f(P) = lim_{n→∞} d^{-n} h(fⁿ(P))
- ĥ_f(P) = 0 iff P is preperiodic
- Northcott property

**Equidistribution:**
- Yuan, Thuillier, Chambert-Loir: equidistribution of small points
- Arakelov-Zhang intersection
- Adelic dynamics

**Dynamical Mordell-Lang Conjecture:**
For f: X → X and subvariety V:
{n : fⁿ(P) ∈ V} is finite union of arithmetic progressions.
- Proved for étale maps (Bell-Ghioca-Tucker)
- Open in general

### p-adic Dynamics

**Dynamics on ℙ¹(ℂ_p):**
- Berkovich projective line
- Julia set in Berkovich space
- Rivera-Letelier theory
- Equidistribution of preperiodic points

**Polynomial Dynamics over ℚ_p:**
- Reduction dynamics
- Good/bad reduction
- filled Julia set
- Local canonical height

---
