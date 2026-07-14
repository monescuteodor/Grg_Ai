# CHAPTER 6: COMBINATORICS & DISCRETE MATHEMATICS


## Enumerative Combinatorics

### Counting Principles

**Basic Rules:**
- Sum rule: |A ∪ B| = |A| + |B| - |A ∩ B|
- Product rule: |A × B| = |A| · |B|
- Inclusion-Exclusion:
  |∪_{i=1}^n Aᵢ| = Σ|Aᵢ| - Σ|Aᵢ∩Aⱼ| + Σ|Aᵢ∩Aⱼ∩Aₖ| - ... + (-1)^{n-1}|∩Aᵢ|

**Binomial Coefficients:**
C(n,k) = n!/(k!(n-k)!)
- C(n,k) = C(n,n-k)
- Pascal's identity: C(n,k) = C(n-1,k) + C(n-1,k-1)
- Binomial theorem: (x+y)ⁿ = Σ C(n,k) x^k y^{n-k}
- Vandermonde: Σ_k C(m,k)C(n,r-k) = C(m+n,r)

**Multinomial Coefficients:**
(n; n₁,...,nₖ) = n!/(n₁!...nₖ!) for n₁+...+nₖ = n
- Counts ways to partition n objects into groups of sizes n₁,...,nₖ

**Catalan Numbers:**
Cₙ = (1/(n+1))C(2n,n) = C(2n,n) - C(2n,n+1)
- C₀=1, C₁=1, C₂=2, C₃=5, C₄=14, C₅=42, ...
- Counts: valid parentheses, binary trees, triangulations, Dyck paths, non-crossing partitions
- Recurrence: C_{n+1} = Σ_{i=0}^n Cᵢ C_{n-i}
- Generating function: C(x) = (1-√(1-4x))/(2x)

**Stirling Numbers:**
- First kind s(n,k): ways to permute n elements with k cycles
  - s(n,k) = s(n-1,k-1) + (n-1)s(n-1,k)
  - x(x-1)...(x-n+1) = Σ s(n,k) x^k
- Second kind S(n,k): ways to partition n elements into k non-empty subsets
  - S(n,k) = S(n-1,k-1) + k·S(n-1,k)
  - xⁿ = Σ S(n,k) (x)_k where (x)_k = x(x-1)...(x-k+1)

**Bell Numbers:**
B(n) = Σ_{k=0}^n S(n,k) = number of partitions of n-element set
- B(0)=1, B(1)=1, B(2)=2, B(3)=5, B(4)=15, B(5)=52
- Recurrence: B(n+1) = Σ_{k=0}^n C(n,k) B(k)
- Dobiński's formula: B(n) = (1/e) Σ_{k=0}^∞ kⁿ/k!

### Generating Functions

**Ordinary Generating Function:**
A(x) = Σ_{n=0}^∞ aₙ xⁿ

**Exponential Generating Function:**
Â(x) = Σ_{n=0}^∞ aₙ xⁿ/n!

**Operations:**
- Addition: (A+B)(x) = A(x) + B(x)
- Multiplication (convolution): (A·B)(x) = Σ_n (Σ_{k=0}^n aₖ b_{n-k}) xⁿ
- Differentiation: A'(x) = Σ_{n=0}^∞ (n+1)a_{n+1} xⁿ

**Key Generating Functions:**
- 1/(1-x) = Σ xⁿ
- 1/(1-x)² = Σ (n+1)xⁿ
- e^x = Σ xⁿ/n!
- -ln(1-x) = Σ xⁿ/n
- 1/√(1-4x) = Σ C(2n,n) xⁿ

**Lagrange Inversion:**
If A(x) = x·B(A(x)), then:
[xⁿ]A(x) = (1/n)[x^{n-1}]B(x)ⁿ

**Applications:**
- Solving recurrence relations
- Counting trees (Cayley's formula: n^{n-2} labeled trees)
- Random walks, ballot problems

### Partitions

**Integer Partitions:**
p(n) = number of ways to write n as sum of positive integers
- p(1)=1, p(2)=2, p(3)=3, p(4)=5, p(5)=7, p(6)=11, ...
- Generating function: Σ p(n)xⁿ = ∏_{k=1}^∞ 1/(1-x^k)
- Euler's pentagonal theorem:
  p(n) = p(n-1) + p(n-2) - p(n-5) - p(n-7) + p(n-12) + ...
  where subtracted numbers are generalized pentagonal numbers (3k²±k)/2

**Young Diagrams & Tableaux:**
- Ferrers diagram: left-justified rows of boxes
- Standard Young tableau: filling with 1,...,n increasing in rows and columns
- Hook length formula: number of SYT of shape λ = n!/∏ hook lengths

**Plane Partitions:**
3D arrays decreasing in all directions.
- MacMahon's formula for generating function

### Permutation Patterns

**Pattern Avoidance:**
Permutation π avoids pattern σ if no subsequence of π has same relative order as σ.
- 231-avoiding permutations = Catalan numbers
- Stanley-Wilf conjecture (proved by Marcus-Tardos):
  For any pattern σ, ∃ L(σ) such that number of σ-avoiding permutations of length n ≤ L(σ)ⁿ

**Stack-Sortable Permutations:**
Permutations sortable by a single stack = 231-avoiding = Catalan.

**Longest Increasing Subsequence:**
For random permutation of length n:
- Expected length ~ 2√n (Vershik-Kerov, Logan-Shepp)
- Distribution: Tracy-Widom (from random matrix theory)


## Graph Theory

### Fundamentals

**Definitions:**
- Graph G = (V, E)
- Simple graph: no loops, no multiple edges
- Directed graph: edges have direction
- Weighted graph: edges have weights
- Degree d(v): number of edges incident to v
- Handshaking lemma: Σ d(v) = 2|E|

**Special Graphs:**
- Complete graph Kₙ: all pairs connected, |E| = C(n,2)
- Cycle Cₙ: n vertices in cycle
- Path Pₙ: n vertices in path
- Complete bipartite K_{m,n}: two parts, all cross edges
- Hypercube Qₙ: vertices = {0,1}ⁿ, edges differ in one coordinate
- Petersen graph: 10 vertices, 3-regular, girth 5

**Graph Isomorphism:**
G ≅ H if ∃ bijection f: V(G) → V(H) preserving adjacency.
- Graph isomorphism problem: in NP, not known to be NP-complete or in P
- Babai (2015): quasi-polynomial time algorithm

### Connectivity

**Paths & Cycles:**
- Walk: sequence of vertices with consecutive edges
- Path: walk with no repeated vertices
- Cycle: closed path (length ≥ 3 for simple graphs)
- Eulerian path/circuit: uses every edge exactly once
  - Eulerian circuit iff connected and all degrees even
- Hamiltonian path/cycle: visits every vertex exactly once
  - NP-complete to determine existence

**Connectivity:**
- κ(G): vertex connectivity (minimum vertices to remove to disconnect)
- λ(G): edge connectivity
- δ(G): minimum degree
- κ(G) ≤ λ(G) ≤ δ(G)
- Menger's theorem: κ(G) ≥ k iff there are k internally disjoint paths between any two vertices

**Trees:**
Connected acyclic graph.
- |V| = |E| + 1
- Unique path between any two vertices
- Spanning tree: subgraph that is a tree containing all vertices
- Minimum spanning tree: Kruskal's, Prim's algorithms
- Cayley's formula: n^{n-2} labeled trees on n vertices

### Coloring

**Vertex Coloring:**
χ(G) = minimum colors needed so adjacent vertices have different colors.
- χ(G) ≤ Δ(G) + 1 (greedy algorithm)
- Brooks' theorem: χ(G) ≤ Δ(G) for connected G not complete or odd cycle
- Four Color Theorem: χ(G) ≤ 4 for planar graphs (Appel-Haken, 1976)
- Chromatic polynomial: P_G(k) = number of proper k-colorings

**Edge Coloring:**
χ'(G) = minimum colors for proper edge coloring.
- Vizing's theorem: Δ(G) ≤ χ'(G) ≤ Δ(G) + 1
- Class 1: χ'(G) = Δ(G); Class 2: χ'(G) = Δ(G) + 1
- For bipartite: χ'(G) = Δ(G) (Kőnig's theorem)

**List Coloring:**
Each vertex has list of available colors.
- Choosability ch(G): minimum k such that G is k-choosable
- ch(G) ≥ χ(G)
- ch(K_{3,3}) = 3 > χ(K_{3,3}) = 2

### Planar Graphs

**Euler's Formula:**
For connected planar graph: |V| - |E| + |F| = 2
where F = faces (including outer face).

**Consequences:**
- |E| ≤ 3|V| - 6 for simple planar graph with |V| ≥ 3
- |E| ≤ 2|V| - 4 for triangle-free planar graph
- Every planar graph has vertex of degree ≤ 5
- K₅ and K_{3,3} are non-planar (Kuratowski's theorem)

**Dual Graph:**
For planar embedding, dual has vertex for each face, edge for each adjacent pair.

**Graph Minors:**
H is minor of G if H obtained from G by deleting edges/vertices and contracting edges.
- Wagner's theorem: G planar iff G has no K₅ or K_{3,3} minor
- Graph Minor Theorem (Robertson-Seymour): graphs are well-quasi-ordered by minor relation

### Extremal Graph Theory

**Turán's Theorem:**
Maximum edges in n-vertex graph without K_{r+1}:
ex(n, K_{r+1}) = (1 - 1/r)n²/2
Achieved by Turán graph T_r(n): complete r-partite graph with parts as equal as possible.

**Erdős-Stone Theorem:**
For any graph H with chromatic number χ(H) = r+1:
ex(n,H) = (1 - 1/r + o(1))n²/2

**Ramsey Theory:**
R(s,t) = minimum n such that any red-blue coloring of Kₙ contains red Kₛ or blue Kₜ.
- R(3,3) = 6
- R(4,4) = 18
- Bounds: 2^{t/2} ≤ R(t,t) ≤ 4^t
- Erdős: probabilistic method gives lower bounds

**Szemerédi's Regularity Lemma:**
Every large graph can be partitioned into a bounded number of quasi-random bipartite graphs.
- Applications: counting subgraphs, property testing, graph limits

### Random Graphs

**Erdős-Rényi Model G(n,p):**
Each edge present independently with probability p.

**Threshold Phenomena:**
For monotone property P, ∃ threshold p(n):
- p << p(n): P almost surely false
- p >> p(n): P almost surely true

**Examples:**
- Connectivity: threshold at p = (log n)/n
- Giant component: threshold at p = 1/n
- Hamiltonicity: threshold at p = (log n + log log n)/n

**Phase Transitions:**
At p = c/n:
- c < 1: all components are trees or unicyclic, largest O(log n)
- c = 1: largest component ~ n^{2/3}
- c > 1: unique giant component of size ~ α(c)n

**Random Regular Graphs:**
G(n,d): d-regular graph on n vertices chosen uniformly.
- Expansion properties
- Spectral gap: λ₂ ≤ 2√(d-1) + ε (Friedman, Alon conjecture)

### Spectral Graph Theory

**Adjacency Matrix:**
A_{ij} = 1 if (i,j) ∈ E, 0 otherwise.
- Eigenvalues: λ₁ ≥ λ₂ ≥ ... ≥ λₙ
- λ₁ ≤ Δ(G), equality iff regular
- For d-regular: λ₁ = d

**Laplacian:**
L = D - A where D = diag(d(v₁),...,d(vₙ))
- Eigenvalues: 0 = μ₁ ≤ μ₂ ≤ ... ≤ μₙ
- μ₂ > 0 iff connected
- μ₂ = algebraic connectivity (Fiedler value)

**Cheeger Inequality:**
For d-regular graph:
(d - λ₂)/2 ≤ h(G) ≤ √(2d(d - λ₂))
where h(G) = edge expansion (Cheeger constant).

**Expander Graphs:**
Sparse graphs with strong connectivity properties.
- (n,d,λ)-expander: n vertices, degree d, λ₂ ≤ λ
- Applications: derandomization, error-correcting codes, network design
- Explicit constructions: Margulis, LPS (Lubotzky-Phillips-Sarnak)

### Network Flows

**Max-Flow Min-Cut:**
For network with capacities, maximum flow = minimum cut capacity.
- Ford-Fulkerson algorithm
- Edmonds-Karp: O(VE²)
- Dinic's algorithm: O(V²E)

**Applications:**
- Bipartite matching
- Edge connectivity
- Image segmentation
- Baseball elimination


## Discrete Geometry

### Convex Geometry

**Convex Sets:**
C is convex if ∀x,y ∈ C, segment [x,y] ⊆ C.

**Carathéodory's Theorem:**
If x ∈ conv(S) in ℝᵈ, then x ∈ conv(T) for some T ⊆ S with |T| ≤ d+1.

**Helly's Theorem:**
For finite family of convex sets in ℝᵈ: if every d+1 have non-empty intersection, then all have non-empty intersection.

**Radon's Theorem:**
Any set of d+2 points in ℝᵈ can be partitioned into two subsets with intersecting convex hulls.

**Tverberg's Theorem:**
Any set of (r-1)(d+1)+1 points in ℝᵈ can be partitioned into r parts with intersecting convex hulls.

### Polytopes

**Definitions:**
- Polytope: convex hull of finitely many points (or bounded intersection of half-spaces)
- Face: intersection with supporting hyperplane
- Facet: (d-1)-dimensional face
- Vertex: 0-dimensional face
- Edge: 1-dimensional face

**Euler-Poincaré Formula:**
For d-dimensional polytope: Σ_{i=0}^{d-1} (-1)ⁱ fᵢ = 1 - (-1)ᵈ
where fᵢ = number of i-dimensional faces.

**Cyclic Polytopes:**
Vertices on moment curve (t, t², ..., tᵈ).
- Maximum number of faces for given n and d (Upper Bound Theorem)
- fᵢ(C_d(n)) = Σ_{k=0}^{⌊d/2⌋} C(k,d)C(n-d+k-1,k) for appropriate ranges

### Lattice Points

**Pick's Theorem:**
For simple lattice polygon: Area = I + B/2 - 1
where I = interior lattice points, B = boundary lattice points.

**Ehrhart Theory:**
For lattice polytope P:
L_P(t) = number of lattice points in tP = |tP ∩ ℤᵈ|
- L_P(t) is polynomial in t of degree dim(P)
- Ehrhart-Macdonald reciprocity: L_P(-t) = (-1)^{dim P} L_{P°}(t)

**Minkowski's Theorem:**
For convex symmetric body K in ℝᵈ with vol(K) > 2ᵈ:
K contains non-zero lattice point.

**Geometry of Numbers:**
- Successive minima λ₁,...,λₙ
- Minkowski's second theorem: (λ₁...λₙ)vol(K) ≤ 2ⁿdet(Λ)
- Applications to Diophantine approximation

### Incidence Geometry

**Szemerédi-Trotter Theorem:**
For n points and m lines in plane:
I(P,L) = O(n^{2/3}m^{2/3} + n + m)
where I = number of incidences.

**Crossing Number:**
cr(G) = minimum crossings in any drawing of G.
- cr(G) ≥ |E|³/(64|V|²) for |E| ≥ 4|V|
- Crossing lemma: used to prove Szemerédi-Trotter

**Unit Distances:**
Maximum number of unit distances among n points in plane: O(n^{4/3}).

**Distinct Distances:**
Minimum number of distinct distances: Erdős conjectured Ω(n/√(log n}), proved by Guth-Katz: Ω(n/log n).

### Computational Geometry

**Convex Hull:**
- Graham scan: O(n log n)
- Jarvis march (gift wrapping): O(nh) where h = number of hull vertices
- Chan's algorithm: O(n log h)

**Voronoi Diagram:**
Partition of plane into regions closest to each site.
- Dual: Delaunay triangulation
- Construction: Fortune's algorithm O(n log n)

**Delaunay Triangulation:**
Triangulation where no point is inside circumcircle of any triangle.
- Maximizes minimum angle
- Applications: mesh generation, interpolation

**Point Location:**
Preprocess planar subdivision for fast point queries.
- Kirkpatrick's method: O(n) space, O(log n) query

**Range Searching:**
Report points in query region.
- kd-trees: O(√n + k) for 2D orthogonal range queries
- Range trees: O(log²n + k) query, O(n log n) space

**Arrangements:**
Subdivision of plane by lines or curves.
- Complexity: O(n²) for n lines
- Zone theorem: complexity of zone of one line is O(n)


## Cryptography & Coding Theory

### Public Key Cryptography

**RSA:**
- Key generation: n = pq, φ(n) = (p-1)(q-1), e·d ≡ 1 (mod φ(n))
- Public key: (n,e), Private key: d
- Encryption: c = m^e mod n
- Decryption: m = c^d mod n
- Security: factoring n is hard

**Elliptic Curve Cryptography (ECC):**
- Group structure on elliptic curves over finite fields
- ECDLP: discrete log on elliptic curves
- Smaller key sizes than RSA for same security

**Lattice-Based Cryptography:**
- Learning With Errors (LWE)
- Ring-LWE
- Post-quantum secure (resistant to Shor's algorithm)
- NTRU, CRYSTALS-Kyber, CRYSTALS-Dilithium

### Coding Theory

**Linear Codes:**
Subspace of 𝔽_qⁿ.
- Parameters: [n,k,d] where n = length, k = dimension, d = minimum distance
- Rate: R = k/n
- Relative distance: δ = d/n

**Bounds:**
- Singleton bound: d ≤ n - k + 1
- MDS codes: meet Singleton bound (e.g., Reed-Solomon)
- Hamming bound: sphere-packing bound
- Gilbert-Varshamov bound: existence of good codes

**Reed-Solomon Codes:**
Evaluation of polynomials at distinct points.
- [n,k,n-k+1] code over 𝔽_q (n ≤ q)
- Optimal: MDS
- Applications: CDs, DVDs, QR codes, space communications

**LDPC Codes:**
Low-density parity-check codes.
- Sparse parity-check matrix
- Decoded by belief propagation
- Capacity-approaching on AWGN channel

**Polar Codes:**
- Channel polarization
- First codes with explicit construction achieving capacity
- Used in 5G

### Combinatorial Designs

**Block Designs:**
A t-(v,k,λ) design: v points, blocks of size k, every t-subset in exactly λ blocks.
- Steiner system S(t,k,v): λ = 1
- Fano plane: 2-(7,3,1)
- Projective plane of order n: 2-(n²+n+1, n+1, 1)

**Existence:**
- Necessary conditions on parameters
- Wilson's theorem: existence for large v given divisibility conditions
- Kirkman schoolgirl problem: resolvable Steiner triple system

**Hadamard Matrices:**
H is n×n with entries ±1 and H·H^T = n·I.
- Order 1,2 or divisible by 4 (Hadamard conjecture)
- Construction: Sylvester, Paley, Williamson
- Applications: error-correcting codes, weighing designs

**Latin Squares:**
n×n array where each symbol appears once in each row and column.
- Orthogonal Latin squares: superimposed, each ordered pair appears once
- Euler's 36 officers problem: no pair of orthogonal 6×6 Latin squares
- Existence: n-1 mutually orthogonal for prime power n


---
