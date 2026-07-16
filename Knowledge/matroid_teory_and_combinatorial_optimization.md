# CHAPTER 23: MATROID THEORY & COMBINATORIAL OPTIMIZATION


## Matroid Theory

### Fundamentals

**Definition:**
Matroid M = (E, I) where E is ground set, I ⊆ P(E) independent sets satisfying:
1. ∅ ∈ I
2. Hereditary: A ⊆ B ∈ I ⇒ A ∈ I
3. Exchange: A,B ∈ I, |A| < |B| ⇒ ∃x ∈ B\A: A∪{x} ∈ I

**Bases:**
Maximal independent sets.
- All bases have same cardinality (rank)
- Basis exchange property

**Circuits:**
Minimal dependent sets.
- Circuit elimination
- Fundamental circuit for basis

**Rank Function:**
r: P(E) → ℕ where r(A) = max{|I| : I ⊆ A, I ∈ I}
- r(A) ≤ |A|
- r(A∪B) + r(A∩B) ≤ r(A) + r(B) (submodular)

**Closure:**
cl(A) = {x ∈ E : r(A∪{x}) = r(A)}
- Closed sets = flats
- Lattice of flats

**Duality:**
M* = (E, I*) where I* = {A ⊆ E : E\A contains basis of M}
- (M*)* = M
- r*(A) = |A| - r(E) + r(E\A)

### Examples

**Graphic Matroids:**
M(G) for graph G.
- Independent = forests
- Bases = spanning trees
- Circuits = simple cycles
- Rank = n - c (components)

**Cographic Matroids:**
M*(G) = dual of graphic.
- Independent = complements of connected subgraphs
- Bases = complements of spanning trees

**Representable Matroids:**
M is representable over field F if ∃ matrix A over F with M = column matroid.
- Binary matroids: representable over 𝔽₂
- Regular matroids: representable over all fields
- Unimodular matrices

**Transversal Matroids:**
From family of sets (A₁,...,Aₙ).
- Partial transversals = independent sets
- Hall's marriage theorem

**Algebraic Matroids:**
From field extensions.
- Independent = algebraically independent sets
- Rank = transcendence degree

### Minors & Decomposition

**Minors:**
- Deletion: M\e = (E\{e}, I')
- Contraction: M/e = (M*\e)*
- Minor: sequence of deletions and contractions

**Tutte's Theorem:**
M is regular iff M has no minor isomorphic to U_{2,4}.

**Seymour's Decomposition:**
Regular matroids decompose into graphic, cographic, and R₁₀.
- Tree of matroids
- k-sums

**Excluded Minor Characterizations:**
- Binary: no U_{2,4} minor
- Regular: no U_{2,4}, F₇, F₇* minors
- Graphic: no U_{2,4}, F₇, F₇*, M*(K₅), M*(K_{3,3}) minors
- Cographic: dual of above

### Tutte Polynomial

**Definition:**
T_M(x,y) = Σ_{A⊆E} (x-1)^{r(E)-r(A)} (y-1)^{|A|-r(A)}

**Specializations:**
- T(1,1) = number of bases
- T(2,1) = number of spanning sets
- T(1,2) = number of independent sets
- T(2,0) = number of acyclic orientations
- T(0,2) = number of totally cyclic orientations
- T(2,2) = 2^{|E|}
- Chromatic polynomial: χ_G(λ) = (-1)^{r(E)} λ^{c(G)} T(1-λ, 0)
- Flow polynomial: φ_G(λ) = (-1)^{|E|-r(E)} T(0, 1-λ)

**Deletion-Contraction:**
T_M = T_{M\e} + T_{M/e} if e is neither loop nor isthmus
T_M = x·T_{M/e} if e is isthmus
T_M = y·T_{M\e} if e is loop

**Tutte-Grothendieck Invariants:**
- Any function satisfying deletion-contraction is evaluation of T_M
- Applications: reliability, percolation, knot invariants

### Oriented Matroids

**Definition:**
Matroid with additional sign structure on circuits and cocircuits.
- Chirotope: orientation function
- Signed circuits
- Face lattice

**Topological Representation:**
- Pseudosphere arrangements
- Folkman-Lawrence theorem
- Topological representation theorem

**Realizable Oriented Matroids:**
- Hyperplane arrangements
- Convex polytopes
- Gale transforms

### Greedoids

**Definition:**
Set system satisfying exchange property without hereditary.
- Accessible: ∅ ∈ F, and every feasible set has feasible predecessor
- Exchange: A,B ∈ F, |A| < |B| ⇒ ∃x ∈ B\A: A∪{x} ∈ F

**Examples:**
- Matroids
- Antimatroids (feasible = unions of paths)
- Gaussian elimination greedoids
- Undirected branching greedoids

**Optimization:**
- Greedy algorithm works for greedoids with appropriate objective
- Generalizes matroid greedy algorithm

## Combinatorial Optimization

### Linear Programming

**Standard Form:**
Minimize c^T x subject to Ax = b, x ≥ 0

**Duality:**
Primal: min c^T x s.t. Ax = b, x ≥ 0
Dual: max b^T y s.t. A^T y ≤ c

**Strong Duality:**
If primal has optimal solution, so does dual, and optima coincide.

**Simplex Method:**
- Pivot operations
- BFS = basic feasible solutions
- Dantzig's rule
- Exponential worst case (Klee-Minty)
- Polynomial average case

**Interior Point Methods:**
- Karmarkar (1984): polynomial time
- Central path
- Barrier functions
- Mehrotra predictor-corrector

**Ellipsoid Method:**
- Khachiyan (1979): polynomial time
- Separation oracle
- Theoretical importance

### Integer Programming

**Formulation:**
Minimize c^T x subject to Ax ≤ b, x ∈ ℤⁿ

**LP Relaxation:**
Drop integrality constraints.
- Integer hull
- Cutting planes
- Branch and bound

**Total Unimodularity:**
A totally unimodular ⇒ LP relaxation gives integer solutions.
- Network matrices
- Consecutive ones property
- Seymour's decomposition

**Cutting Planes:**
- Gomory cuts
- Chvátal closure
- Split cuts
- Lift-and-project

**Branch and Bound:**
- Tree search
- LP bounds
- Branching rules
- Pruning

### Network Flows (Advanced)

**Multicommodity Flow:**
Multiple flows sharing capacities.
- LP formulation
- Fractional vs integral
- Flow-cut gap

**Minimum Cost Flow:**
Minimize Σ c_e f_e subject to flow conservation and capacities.
- Network simplex
- Successive shortest path
- Capacity scaling

**Circulation Problems:**
- Feasible circulation
- Lower bounds on arcs
- Demand nodes

**Matching Theory:**
- Maximum matching in bipartite graphs (Hungarian algorithm)
- Maximum matching in general graphs (Edmonds' blossom algorithm)
- Perfect matching polytope (Edmonds)
- Matching polytope
- T-joins
- Chinese postman problem

### Polyhedral Combinatorics

**Polytope Descriptions:**
- Spanning tree polytope (Edmonds)
- Perfect matching polytope (Edmonds)
- Stable set polytope
- Traveling salesman polytope

**Total Dual Integrality (TDI):**
Ax ≤ b, A integral, b integral.
- If TDI, then integer hull = polyhedron
- Applications: matroid polytopes, network matrices

**Lifting Theorems:**
- Balas
- Sequential lifting
- Simultaneous lifting
- Superadditive lifting

### Approximation Algorithms

**Techniques:**
- Greedy algorithms
- Local search
- Linear programming relaxation
- Randomized rounding
- Primal-dual
- Metric methods

**Hardness of Approximation:**
- PCP theorem
- Gap-preserving reductions
- Unique Games Conjecture (UGC)
- Approximation resistance

**Examples:**
- Set cover: O(log n) greedy
- Vertex cover: 2-approximation
- MAX-CUT: 0.878 (Goemans-Williamson)
- Traveling salesman: 1.5 (Christofides) for metric
- k-center: 2-approximation

### Submodular Optimization

**Submodular Functions:**
f: 2^E → ℝ with f(A) + f(B) ≥ f(A∪B) + f(A∩B).
- Diminishing returns: f(A∪{e}) - f(A) ≥ f(B∪{e}) - f(B) for A ⊆ B

**Examples:**
- Coverage functions
- Rank functions of matroids
- Entropy
- Cut functions
- Influence in social networks

**Minimization:**
- Polynomial time (Grötschel-Lovász-Schrijver, Iwata-Fleischer-Fujishige)
- Ellipsoid method
- Combinatorial algorithms

**Maximization:**
- Greedy: (1-1/e)-approximation for monotone submodular under cardinality constraint
- Continuous greedy (Vondrák)
- Local search
- Hardness: (1-1/e) is optimal under UGC

**Applications:**
- Sensor placement
- Feature selection
- Document summarization
- Influence maximization
- Network monitoring

---
