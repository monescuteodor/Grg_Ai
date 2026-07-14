# CHAPTER 4: GEOMETRY


## Euclidean Geometry

### Axiomatic Foundations

**Euclid's Postulates:**
1. Two points determine a unique line
2. Line segments can be extended indefinitely
3. Circle can be drawn with any center and radius
4. All right angles are equal
5. **Parallel Postulate:** If a line intersects two lines making interior angles on same side less than two right angles, the two lines meet on that side.

**Hilbert's Axioms (Modern Formulation):**
Seven groups: Incidence, Order, Congruence, Parallels, Continuity, Archimedean, Completeness.

**Playfair's Axiom (Equivalent to Parallel Postulate):**
Through a point not on a line, exactly one parallel line exists.

### Classical Theorems

**Triangle Theorems:**
- Sum of angles = 180°
- Pythagorean: a² + b² = c²
- Law of Sines: a/sin(A) = b/sin(B) = c/sin(C) = 2R
- Law of Cosines: c² = a² + b² - 2ab cos(C)
- Heron's Formula: Area = √[s(s-a)(s-b)(s-c)] where s = (a+b+c)/2

**Circle Theorems:**
- Inscribed angle = ½ central angle subtending same arc
- Power of a point: PA·PB = PC·PD for chords through P
- Tangent-secant: PT² = PA·PB
- Cyclic quadrilateral: opposite angles sum to 180°

**Conic Sections:**
Intersection of plane with double cone:
- Ellipse: sum of distances to foci = constant, e < 1
- Parabola: distance to focus = distance to directrix, e = 1
- Hyperbola: difference of distances to foci = constant, e > 1

Standard forms:
- Ellipse: x²/a² + y²/b² = 1
- Parabola: y² = 4ax or x² = 4ay
- Hyperbola: x²/a² - y²/b² = 1

**Focus-Directrix Property:**
For any conic: distance to focus / distance to directrix = eccentricity e

### Transformations

**Isometries (Distance-Preserving):**
- Translation: T_v(x) = x + v
- Rotation: R_θ(x,y) = (x cos θ - y sin θ, x sin θ + y cos θ)
- Reflection: across line or point
- Glide reflection: reflection + translation

**Classification:**
Every isometry of plane is one of: translation, rotation, reflection, glide reflection.

**Similarities:**
- Uniform scaling: S_k(x) = kx
- Composition of isometry and scaling
- Preserve angles, ratios of lengths

**Affine Transformations:**
x ↦ Ax + b where A is invertible matrix
- Preserve: collinearity, ratios of lengths on lines, parallelism
- Do NOT preserve: angles, distances, circles

**Projective Transformations:**
- Extend affine plane with line at infinity
- Preserve: collinearity, cross-ratio
- Map conics to conics
- Fundamental theorem: determined by images of 4 points (no 3 collinear)

**Cross-Ratio:**
For collinear points A,B,C,D:
(A,B;C,D) = (AC/CB)/(AD/DB) = (AC·BD)/(CB·DA)
- Invariant under projective transformations
- Harmonic division: (A,B;C,D) = -1

### Analytic Geometry

**Coordinate Systems:**
- Cartesian: (x,y,z)
- Polar: (r,θ), x = r cos θ, y = r sin θ
- Cylindrical: (r,θ,z)
- Spherical: (ρ,θ,φ), x = ρ sin φ cos θ, y = ρ sin φ sin θ, z = ρ cos φ

**Vectors:**
- Dot product: u·v = |u||v|cos θ = u₁v₁ + u₂v₂ + u₃v₃
- Cross product: |u×v| = |u||v|sin θ, direction by right-hand rule
- Triple product: u·(v×w) = determinant [u v w]
- Volume of parallelepiped = |u·(v×w)|

**Lines & Planes:**
- Line: r = a + tv or (x-x₀)/a = (y-y₀)/b = (z-z₀)/c
- Plane: n·(r - r₀) = 0 or ax + by + cz = d
- Distance from point to plane: |ax₀ + by₀ + cz₀ - d|/√(a²+b²+c²)
- Angle between planes: angle between normals

**Quadric Surfaces:**
General second-degree equation in 3D:
Ax² + By² + Cz² + Dxy + Exz + Fyz + Gx + Hy + Iz + J = 0

Standard forms:
- Ellipsoid: x²/a² + y²/b² + z²/c² = 1
- Hyperboloid of one sheet: x²/a² + y²/b² - z²/c² = 1
- Hyperboloid of two sheets: x²/a² - y²/b² - z²/c² = 1
- Elliptic paraboloid: z = x²/a² + y²/b²
- Hyperbolic paraboloid: z = x²/a² - y²/b²
- Elliptic cone: x²/a² + y²/b² = z²/c²


## Non-Euclidean Geometry

### Hyperbolic Geometry

**Models:**
1. **Poincaré Disk:** Points inside unit disk, lines = arcs orthogonal to boundary or diameters
2. **Poincaré Half-Plane:** H = {z ∈ ℂ : Im(z) > 0}, lines = semicircles orthogonal to real axis or vertical rays
3. **Klein Model:** Points inside disk, lines = chords
4. **Hyperboloid Model:** Sheet of hyperboloid in Minkowski space

**Metric (Poincaré Half-Plane):**
ds² = (dx² + dy²)/y²
Distance: d(z₁,z₂) = arccosh(1 + |z₁-z₂|²/(2 Im(z₁)Im(z₂)))

**Key Properties:**
- Sum of angles in triangle < 180°
- Area of triangle = π - (α+β+γ) (Gauss-Bonnet)
- No similar triangles (except congruent)
- Infinitely many parallel lines through a point
- Circumference of circle = 2π sinh(r)
- Area of disk = 2π(cosh(r) - 1)

**Isometries:**
- Poincaré disk/half-plane: Möbius transformations preserving model
- SL(2,ℝ) acts by fractional linear transformations

**Trigonometry:**
- sinh(c)/sin(γ) = sinh(a)/sin(α) (law of sines)
- cosh(c) = cosh(a)cosh(b) - sinh(a)sinh(b)cos(γ) (law of cosines)

### Elliptic Geometry

**Model:** Sphere S² with antipodal points identified (real projective plane)
Or: Sphere with great circles as "lines"

**Properties:**
- Sum of angles in triangle > 180°
- Area = α + β + γ - π
- No parallel lines (any two lines intersect)
- All lines have finite length (great circles)
- Triangle inequality can fail for antipodal points

**Spherical Trigonometry:**
- sin(a)/sin(α) = sin(b)/sin(β) = sin(c)/sin(γ)
- cos(c) = cos(a)cos(b) + sin(a)sin(b)cos(γ)
- For unit sphere: sides are angles subtended at center

### Comparison of Geometries

| Property          | Euclidean | Hyperbolic | Elliptic   |
|-------------------|-----------|------------|------------|
| Curvature K       | 0         | -1         | +1         |
| Triangle sum      | = π       | < π        | > π        |
| Parallels         | 1         | ∞          | 0          |
| Circle circumference| 2πr      | 2π sinh(r) | 2π sin(r)  |
| Area of triangle   | base·height/2 | π - sum angles | sum angles - π |
| Similar triangles  | many      | none       | none       |


## Differential Geometry

### Curves

**Parametrized Curves:**
γ: I → ℝⁿ, γ(t) = (x₁(t), ..., xₙ(t))

**Arc Length:**
s(t) = ∫_{t₀}^t |γ'(u)| du

**Curvature (Plane Curves):**
κ = |γ' × γ''| / |γ'|³ = |dT/ds|
where T = γ'/|γ'| is unit tangent

**Frenet-Serret Formulas (Space Curves):**
For unit-speed curve:
- T = γ' (tangent)
- N = T'/|T'| (normal)
- B = T × N (binormal)

dT/ds = κN
dN/ds = -κT + τB
dB/ds = -τN

where κ = curvature, τ = torsion

**Fundamental Theorem:**
Curvature and torsion determine curve up to rigid motion.

### Surfaces

**Parametrized Surfaces:**
X: U ⊆ ℝ² → ℝ³, X(u,v) = (x(u,v), y(u,v), z(u,v))

**First Fundamental Form:**
I = E du² + 2F dudv + G dv²
where E = X_u·X_u, F = X_u·X_v, G = X_v·X_v
- Measures intrinsic geometry (lengths, angles, areas)

**Second Fundamental Form:**
II = L du² + 2M dudv + N dv²
where L = X_{uu}·n, M = X_{uv}·n, N = X_{vv}·n, n = unit normal
- Measures extrinsic geometry (how surface bends in space)

**Gaussian Curvature:**
K = (LN - M²)/(EG - F²) = κ₁·κ₂
where κ₁, κ₂ are principal curvatures

**Mean Curvature:**
H = (EN + GL - 2FM)/(2(EG - F²)) = (κ₁ + κ₂)/2

**Theorema Egregium (Gauss):**
Gaussian curvature is intrinsic (depends only on first fundamental form).
- Surprising: K can be computed from measurements on surface alone
- Implies: isometric surfaces have same K

**Geodesics:**
Curves of shortest length between points (locally).
- Satisfy geodesic equation: d²uᵏ/ds² + Γᵏ_{ij}(duⁱ/ds)(duʲ/ds) = 0
- Christoffel symbols: Γᵏ_{ij} = ½g^{kl}(∂ᵢg_{jl} + ∂ⱼg_{il} - ∂ₗg_{ij})

**Gauss-Bonnet Theorem:**
For compact surface M without boundary:
∫_M K dA = 2π χ(M) = 2π(2 - 2g)
where χ = Euler characteristic, g = genus

**Classification of Surfaces:**
Closed orientable surfaces: sphere (g=0), torus (g=1), double torus (g=2), ...
χ = 2 - 2g

### Riemannian Geometry

**Riemannian Metric:**
On manifold M, g is a smooth inner product on each tangent space.
In coordinates: ds² = g_{ij} dxⁱ dxʲ

**Levi-Civita Connection:**
Unique torsion-free connection compatible with metric.
∇ₓY - ∇ᵧX = [X,Y] (torsion-free)
X(g(Y,Z)) = g(∇ₓY, Z) + g(Y, ∇ₓZ) (metric compatible)

**Curvature Tensor:**
R(X,Y)Z = ∇ₓ∇ᵧZ - ∇ᵧ∇ₓZ - ∇_{[X,Y]}Z
In coordinates: R^l_{ijk} = ∂ᵢΓ^l_{jk} - ∂ⱼΓ^l_{ik} + Γ^l_{im}Γ^m_{jk} - Γ^l_{jm}Γ^m_{ik}

**Symmetries of Riemann Tensor:**
1. R_{ijkl} = -R_{jikl} (skew in first two)
2. R_{ijkl} = -R_{ijlk} (skew in last two)
3. R_{ijkl} = R_{klij} (pair symmetry)
4. R_{ijkl} + R_{iklj} + R_{iljk} = 0 (Bianchi identity)

**Ricci Tensor & Scalar Curvature:**
Ric_{ij} = R^k_{ikj} (contraction)
R = g^{ij}Ric_{ij} (full contraction)

**Sectional Curvature:**
For 2-plane spanned by X,Y:
K(X,Y) = ⟨R(X,Y)Y, X⟩ / (|X|²|Y|² - ⟨X,Y⟩²)
- Determines full curvature tensor
- Constant sectional curvature: K = constant
  - K > 0: sphere
  - K = 0: Euclidean space
  - K < 0: hyperbolic space

**Geodesic Completeness:**
(Hopf-Rinow) For connected Riemannian manifold, following are equivalent:
1. Complete as metric space
2. Geodesically complete (all geodesics extend indefinitely)
3. Closed bounded sets are compact

**Jacobi Fields:**
Vector fields along geodesics describing variation through geodesics.
- Jacobi equation: J'' + R(J,γ')γ' = 0
- Conjugate points: where non-trivial Jacobi field vanishes

**Comparison Theorems:**
- Rauch: curvature bounds imply comparison of Jacobi fields
- Toponogov: curvature bounds imply triangle comparison
- Bishop-Gromov: volume comparison

### Symplectic Geometry

**Symplectic Form:**
ω is a closed (dω = 0), non-degenerate 2-form on manifold M.
- Non-degenerate: ω(X,·) = 0 ⇒ X = 0
- dim(M) = 2n

**Darboux's Theorem:**
Every symplectic manifold is locally like (ℝ²ⁿ, ω₀) where
ω₀ = Σᵢ dxⁱ ∧ dyⁱ

**Hamiltonian Vector Fields:**
For H: M → ℝ, X_H defined by: ι_{X_H}ω = dH
- Flow preserves ω (symplectomorphism)
- Hamilton's equations: ẋ = ∂H/∂y, ẏ = -∂H/∂x

**Liouville's Theorem:**
Hamiltonian flow preserves volume (Liouville measure).

**Moment Map:**
For Hamiltonian G-action on M:
μ: M → g* satisfying d⟨μ,ξ⟩ = ι_{X_ξ}ω
- μ⁻¹(0)/G is symplectic reduction (Marsden-Weinstein)


## Algebraic Geometry

### Affine Varieties

**Algebraic Set:**
V(S) = {x ∈ 𝔸ⁿ : f(x) = 0 for all f ∈ S} where S ⊆ k[x₁,...,xₙ]

**Zariski Topology:**
Closed sets = algebraic sets.
- Much coarser than Euclidean topology
- Every two non-empty open sets intersect
- Compact (in the sense that every open cover has finite subcover)

**Hilbert's Nullstellensatz:**
For algebraically closed k:
I(V(J)) = √J (radical of J)
Bijection: {radical ideals} ↔ {algebraic sets}
{prime ideals} ↔ {irreducible varieties}
{maximal ideals} ↔ {points}

**Coordinate Ring:**
k[V] = k[x₁,...,xₙ]/I(V)
- Regular functions on V
- V is affine variety iff k[V] is finitely generated reduced k-algebra

### Projective Varieties

**Projective Space:**
ℙⁿ = (𝔸ⁿ⁺¹ \ {0})/~ where x ~ λx for λ ∈ k*
Points = lines through origin in 𝔸ⁿ⁺¹

**Homogeneous Coordinates:**
[x₀:x₁:...:xₙ] (defined up to scaling)

**Projective Variety:**
Zero locus of homogeneous polynomials.
- Affine chart: Uᵢ = {xᵢ ≠ 0} ≅ 𝔸ⁿ
- Projective closure of affine variety

**Projective Nullstellensatz:**
Bijection between homogeneous radical ideals (not containing irrelevant ideal) and projective varieties.

### Sheaves & Schemes

**Sheaf:**
Assignment of rings/groups to open sets with restriction maps.
- Local data that glues consistently

**Structure Sheaf:**
O_X(U) = regular functions on U
- For affine variety X: O_X = k[X] localized at points

**Scheme:**
Locally ringed space (X, O_X) locally isomorphic to affine schemes Spec(A).
- Generalizes varieties by allowing nilpotents and non-algebraically closed fields
- Spec(ℤ) is a scheme, not a variety

**Properties:**
- Noetherian: ascending chain condition on open sets
- Reduced: no nilpotents in structure sheaf
- Integral: reduced and irreducible
- Regular: local rings are regular local rings

### Cohomology in Algebraic Geometry

**Sheaf Cohomology:**
H^i(X, F) for sheaf F on X.
- H⁰(X, F) = global sections Γ(X, F)
- H^i measures obstructions to global sections

**Key Results:**
- Serre Duality: H^i(X, F) ≅ H^{n-i}(X, ω_X ⊗ F*)* for smooth projective X
- Riemann-Roch: For curve C of genus g:
  dim H⁰(C, L) - dim H¹(C, L) = deg(L) + 1 - g
- Kodaira Vanishing: H^i(X, K_X ⊗ L) = 0 for i > 0, L ample

**Étale Cohomology:**
For schemes over fields of characteristic p.
- H^i_{ét}(X, ℚ_ℓ) for ℓ ≠ p
- Weil Conjectures (proved by Deligne)

### Curves & Surfaces

**Algebraic Curves:**
Smooth projective curve C of genus g.
- g = 0: ℙ¹ (rational)
- g = 1: elliptic curves
- g ≥ 2: hyperelliptic and general curves

**Elliptic Curves:**
Smooth cubic curve in ℙ².
Weierstrass form: y² = x³ + ax + b
- Group structure: chord-tangent method
- j-invariant classifies over algebraically closed fields
- Complex: torus ℂ/Λ (uniformization)

**Riemann Surfaces:**
One-dimensional complex manifolds.
- Genus g = number of "holes"
- Riemann-Roch theorem
- Moduli space M_g of curves of genus g (dimension 3g-3 for g ≥ 2)

**Algebraic Surfaces:**
Kodaira classification by Kodaira dimension κ:
- κ = -∞: rational, ruled
- κ = 0: K3, Enriques, abelian, hyperelliptic
- κ = 1: elliptic surfaces
- κ = 2: surfaces of general type

**Birational Geometry:**
Two varieties are birational if they have isomorphic open subsets.
- Minimal model program
- Flips, flops, divisorial contractions
- Cone theorem, basepoint-free theorem


## Topology & Geometry

### Algebraic Topology

**Homotopy:**
Maps f,g: X → Y are homotopic (f ≃ g) if ∃ H: X×[0,1] → Y with H(·,0) = f, H(·,1) = g.

**Fundamental Group:**
π₁(X,x₀) = homotopy classes of loops based at x₀
- Simply connected: π₁ = 0
- π₁(S¹) = ℤ
- π₁(Sⁿ) = 0 for n ≥ 2
- π₁(Tⁿ) = ℤⁿ
- Van Kampen theorem: compute π₁ of unions

**Higher Homotopy Groups:**
πₙ(X,x₀) = homotopy classes of maps (Sⁿ, *) → (X, x₀)
- Abelian for n ≥ 2
- πₙ(Sⁿ) = ℤ
- π₃(S²) = ℤ (Hopf fibration)
- π₄(S³) = ℤ/2ℤ
- π_{n+1}(Sⁿ) = ℤ/2ℤ for n ≥ 3

**Homology:**
Hₙ(X) = n-th homology group
- H₀(X) = free abelian on path components
- H₁(X) = abelianization of π₁(X)
- Hₙ(Sⁿ) = ℤ, Hₖ(Sⁿ) = 0 for k ≠ 0,n
- Hₖ(Tⁿ) = ℤ^{C(n,k)}

**Cellular Homology:**
For CW complex:
Hₙ^{CW}(X) = ker(∂ₙ)/im(∂_{n+1})
where ∂ₙ: Cₙ → C_{n-1} is cellular boundary map.

**Cohomology:**
Hⁿ(X; G) = Hom(Hₙ(X), G) (universal coefficient theorem)
- Cup product: Hⁱ × Hʲ → Hⁱ⁺ʲ makes H*(X) a ring
- Poincaré duality: Hⁱ(M) ≅ H_{n-i}(M) for closed oriented n-manifold

**Euler Characteristic:**
χ(X) = Σ (-1)ⁿ rank(Hₙ(X))
- For finite CW complex: χ = Σ (-1)ⁿ (number of n-cells)
- χ(M ⊔ N) = χ(M) + χ(N)
- χ(M × N) = χ(M)·χ(N)

### Differential Topology

**Smooth Manifolds:**
Hausdorff, second countable, locally Euclidean with smooth transition maps.

**Tangent Bundle:**
TM = ⊔_{p∈M} T_pM
- Vector bundle over M
- Sections = vector fields

**Differential Forms:**
Ω^k(M) = sections of Λ^k(T*M)
- Exterior derivative: d: Ω^k → Ω^{k+1}, d² = 0
- de Rham cohomology: H^k_{dR}(M) = ker(d)/im(d)

**de Rham's Theorem:**
H^k_{dR}(M) ≅ H^k(M; ℝ)

**Stokes' Theorem:**
∫_M dω = ∫_{∂M} ω
for compact oriented M with boundary.

**Degree of Map:**
For f: M → N between oriented n-manifolds:
deg(f) = Σ_{x∈f⁻¹(y)} sign(det(Df_x))
- Integer invariant
- Homotopy invariant
- deg(id) = 1, deg(constant) = 0

**Morse Theory:**
Study topology via critical points of smooth functions.
- Morse function: non-degenerate critical points
- Morse inequalities: number of critical points ≥ Betti numbers
- Handle decomposition of manifold

**Transversality:**
Submanifolds intersect transversally if T_pX + T_pY = T_pM at intersection points.
- Transverse intersections are manifolds
- Thom's transversality theorem: generic maps are transverse

**Fibre Bundles:**
π: E → B with fibre F, locally trivial.
- Vector bundles: fibre is vector space
- Principal bundles: fibre is Lie group
- Associated bundles

**Characteristic Classes:**
Invariants of vector bundles:
- Stiefel-Whitney: wᵢ ∈ Hⁱ(B; ℤ/2)
- Chern: cᵢ ∈ H²ⁱ(B; ℤ) for complex bundles
- Pontryagin: pᵢ ∈ H⁴ⁱ(B; ℤ) for real bundles
- Euler: e ∈ Hⁿ(B; ℤ) for oriented rank n bundles

**Thom Isomorphism:**
For oriented rank n vector bundle E → B:
Hⁱ(B) ≅ Hⁱ⁺ⁿ(E, E\0)

**Index Theorems:**
- Atiyah-Singer: analytical index = topological index for elliptic operators
- Chern-Gauss-Bonnet: ∫e(TM) = χ(M)
- Hirzebruch signature theorem
- Riemann-Roch for complex manifolds

### Geometric Topology

**Knot Theory:**
Embedding of S¹ in S³ (or ℝ³).
- Knot invariant: quantity unchanged by ambient isotopy
- Alexander polynomial, Jones polynomial, HOMFLY polynomial
- Knot group: π₁(S³ \ K)
- Seifert surfaces, genus of knot

**3-Manifolds:**
- Prime decomposition: every 3-manifold is connected sum of primes
- Geometrization Conjecture (Perelman, proved): every prime 3-manifold has geometric structure
- Eight Thurston geometries: S³, ℝ³, H³, S²×ℝ, H²×ℝ, SL(2,ℝ), Nil, Sol

**4-Manifolds:**
- Simply connected: classified by intersection form and Kirby-Siebenmann invariant
- Donaldson invariants (using instantons)
- Seiberg-Witten invariants
- Exotic ℝ⁴: smooth structures on ℝ⁴ not diffeomorphic to standard

**Higher Dimensions:**
- h-cobordism theorem (Smale): simply connected h-cobordism of dim ≥ 5 is trivial
- Poincaré conjecture: proved in all dimensions (Perelman for n=3)
- Smooth Poincaré conjecture: open in dimension 4


---
