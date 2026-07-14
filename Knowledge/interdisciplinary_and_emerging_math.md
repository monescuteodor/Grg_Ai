# CHAPTER 16: INTERDISCIPLINARY & EMERGING MATHEMATICS


## Mathematical Biology

### Population Dynamics

**Lotka-Volterra Equations:**
dx/dt = αx - βxy
 dy/dt = δxy - γy
- Predator-prey model
- Periodic solutions
- Lyapunov stability analysis

**Logistic Growth:**
dN/dt = rN(1 - N/K)
- Carrying capacity K
- Allee effect: positive density dependence at low population

**Structured Populations:**
- Age-structured: McKendrick-von Foerster equation
- Size-structured
- Stage-structured matrix models (Leslie matrix)

**Epidemic Models:**
- SIR: dS/dt = -βSI, dI/dt = βSI - γI, dR/dt = γI
- SEIR, SIRS extensions
- Basic reproduction number R₀
- Herd immunity threshold
- Network epidemiology

**Evolutionary Game Theory:**
- Replicator dynamics: dxᵢ/dt = xᵢ(fᵢ - φ̄)
- Evolutionarily stable strategies (ESS)
- Hawk-Dove game
- Prisoner's dilemma
- Evolution of cooperation

### Systems Biology

**Reaction Networks:**
- Mass action kinetics
- Deficiency zero theorem (Feinberg-Horn-Jackson)
- Persistence and global attractor conjecture

**Gene Regulatory Networks:**
- Boolean networks
- Ordinary differential equation models
- Stochastic models (Gillespie algorithm)
- Bifurcation analysis

**Morphogen Gradients:**
- French flag model
- Turing patterns: reaction-diffusion systems
- Mechanochemical models

**Neural Dynamics:**
- Hodgkin-Huxley model
- FitzHugh-Nagumo simplification
- Wilson-Cowan equations
- Neural field equations

### Mathematical Neuroscience

**Single Neuron Models:**
- Integrate-and-fire
- Leaky integrate-and-fire
- Izhikevich model
- Hindmarsh-Rose model

**Network Models:**
- Kuramoto model: dθᵢ/dt = ωᵢ + (K/N)Σ sin(θⱼ - θᵢ)
- Synchronization transitions
- Master stability function
- Graph Laplacian and dynamics

**Mean Field Models:**
- Wilson-Cowan: rate equations
- Brunel's balanced network
- Chaotic balanced state

**Information Processing:**
- Mutual information between stimuli and responses
- Fisher information in neural populations
- Efficient coding hypothesis
- Predictive coding

## Mathematical Economics & Game Theory

### General Equilibrium

**Arrow-Debreu Model:**
- Commodities, consumers, producers
- Walrasian equilibrium: prices clear all markets
- Existence: Brouwer/Kakutani fixed point
- Welfare theorems

**Mechanism Design:**
- Revelation principle
- Vickrey-Clarke-Groves (VCG) mechanism
- Myerson's optimal auction
- Border's theorem

**Market Design:**
- Matching markets (Gale-Shapley)
- School choice
- Kidney exchange
- Spectrum auctions

### Financial Mathematics

**Stochastic Calculus in Finance:**
- Black-Scholes model: dS = μS dt + σS dW
- Risk-neutral pricing
- Martingale representation theorem
- Girsanov theorem

**Derivatives Pricing:**
- European options: closed form (Black-Scholes formula)
- American options: free boundary problem
- Exotic options: path-dependent
- Interest rate models (Vasicek, CIR, HJM)

**Risk Measures:**
- Value at Risk (VaR)
- Expected Shortfall (CVaR)
- Coherent risk measures (Artzner et al.)
- Spectral risk measures

**Optimal Investment:**
- Merton's problem: utility maximization
- Dynamic programming (HJB equation)
- Martingale method
- Transaction costs

### Algorithmic Game Theory

**Price of Anarchy:**
Ratio of worst Nash equilibrium to social optimum.
- Routing games
- Auctions
- Coordination mechanisms

**Complexity of Equilibria:**
- PPAD-completeness of Nash equilibrium
- PLS-completeness of pure Nash
- Approximation algorithms

**Online Algorithms:**
- Competitive analysis
- Secretary problem
- Prophet inequalities
- Online matching

## Mathematical Linguistics & Formal Languages

### Formal Language Theory

**Chomsky Hierarchy:**
- Type 0: Recursively enumerable (Turing machines)
- Type 1: Context-sensitive (linear bounded automata)
- Type 2: Context-free (pushdown automata)
- Type 3: Regular (finite automata)

**Context-Free Grammars:**
- Parsing: CYK, Earley, LR(k)
- Ambiguity
- Pumping lemma
- Parikh's theorem

**Tree Automata:**
- Recognize tree languages
- Applications: XML, term rewriting
- Monadic second-order logic on trees

### Categorial Grammar

**Lambek Calculus:**
- Types: A/B (looking for B on right to form A)
- A\B (looking for A on left to form B)
- Cut elimination
- Pentus' theorem: equivalence to context-free

**Combinatory Categorial Grammar (CCG):**
- Forward application: >
- Backward application: <
- Harmonic/crossed composition rules
- Polynomial parsing

### Formal Semantics

**Montague Grammar:**
- PTQ (Proper Treatment of Quantification)
- Typed lambda calculus
- Intensional logic
- Compositionality principle

**Dynamic Semantics:**
- Discourse Representation Theory (DRT)
- File Change Semantics
- Dynamic Predicate Logic
- Anaphora resolution

**Probabilistic Semantics:**
- Vector space models
- Word embeddings (Word2Vec, GloVe, BERT)
- Compositional distributional semantics
- Quantum natural language processing

## Quantum Mathematics

### Quantum Information Theory

**Quantum States:**
- Density matrices: ρ ≥ 0, tr(ρ) = 1
- Pure states: ρ = |ψ⟩⟨ψ|
- Mixed states: ρ = Σ pᵢ |ψᵢ⟩⟨ψᵢ|

**Quantum Channels:**
- Completely positive trace-preserving (CPTP) maps
- Kraus representation: E(ρ) = Σ Kᵢ ρ Kᵢ*
- Stinespring dilation
- Choi-Jamiołkowski isomorphism

**Entanglement Theory:**
- Separable vs entangled states
- Entanglement measures: entropy of entanglement, concurrence, negativity
- Distillation and dilution
- Bound entanglement

**Quantum Error Correction:**
- Knill-Laflamme conditions
- Stabilizer codes
- CSS codes
- Topological codes (surface, color, toric)
- Threshold theorem

### Quantum Topology

**Topological Quantum Field Theory (TQFT):**
- Atiyah's axioms
- Functor from cobordism category to vector spaces
- 2D TQFT = commutative Frobenius algebra
- 3D TQFT: Reshetikhin-Turaev from quantum groups

**Knot Invariants:**
- Jones polynomial from quantum groups
- HOMFLY polynomial
- Kauffman bracket
- Khovanov homology: categorification of Jones polynomial
- Witten's path integral interpretation

**Anyons & Braiding:**
- Fractional statistics
- Braid group representations
- Fibonacci anyons
- Universal quantum computing

### Quantum Gravity Mathematics

**Loop Quantum Gravity:**
- Spin networks
- Spin foam models
- Area and volume quantization
- Ashtekar variables

**String Theory Mathematics:**
- Calabi-Yau manifolds
- Mirror symmetry
- Gromov-Witten invariants
- Topological string theory
- AdS/CFT correspondence

**Conformal Field Theory:**
- Virasoro algebra
- Vertex operator algebras
- Modular tensor categories
- Rational CFT classification

## Fractals & Complex Systems

### Fractal Geometry

**Hausdorff Dimension:**
For S ⊆ ℝⁿ:
dim_H(S) = inf{s : H^s(S) = 0} = sup{s : H^s(S) = ∞}
where H^s is s-dimensional Hausdorff measure.

**Examples:**
- Cantor set: log(2)/log(3) ≈ 0.63
- Koch snowflake: log(4)/log(3) ≈ 1.26
- Sierpinski triangle: log(3)/log(2) ≈ 1.58
- Mandelbrot set: boundary has dimension 2

**Box-Counting Dimension:**
dim_B(S) = lim_{ε→0} log N(ε)/log(1/ε)
where N(ε) = number of boxes of size ε needed to cover S.

**Iterated Function Systems (IFS):**
S = ∪ fᵢ(S) for contractions fᵢ.
- Hutchinson's theorem: unique attractor
- Barnsley fern
- Fractal compression

**Multifractal Analysis:**
- Singularity spectrum f(α)
- Large deviations formalism
- Applications: turbulence, finance, neural activity

### Complex Networks

**Random Graph Models:**
- Erdős-Rényi G(n,p)
- Configuration model
- Preferential attachment (Barabási-Albert)
- Stochastic block models
- Hyperbolic random graphs

**Network Properties:**
- Degree distribution: power law, exponential
- Clustering coefficient
- Shortest path lengths
- Centrality measures
- Community detection

**Percolation:**
- Phase transition at critical probability p_c
- Critical exponents
- Universality classes
- Bootstrap percolation
- Explosive percolation

**Synchronization:**
- Kuramoto model on networks
- Master stability function
- Laplacian eigenvalues and synchronizability
- Chimera states

### Self-Organized Criticality

**Bak-Tang-Wiesenfeld Model:**
- Sandpile model
- Abelian property
- Critical state without tuning
- 1/f noise

**Applications:**
- Earthquakes (Gutenberg-Richter law)
- Forest fires
- Neural avalanches
- Traffic jams
- Financial markets

## Origami & Discrete Differential Geometry

### Mathematical Origami

**Huzita-Hatori Axioms:**
Seven (plus one) axioms for paper folding.
- More powerful than straightedge and compass
- Can trisect angles, double cube
- Equivalent to solving cubic equations

**Flat-Foldability:**
- Maekawa-Justin theorem: M-V = ±2 at vertex
- Kawasaki-Justin theorem: alternating sum of angles = 0
- Global flat-foldability: NP-hard

**Rigid Origami:**
- Rigid foldability
- Bellows theorem: volume invariant (Cauchy-style)
- Thick origami
- Applications: deployable structures

### Discrete Differential Geometry

**Discrete Surfaces:**
- Simplicial surfaces
- Circle packings
- Discrete minimal surfaces
- Discrete integrable systems

**Discrete Curvature:**
- Angle defect: K(v) = 2π - Σ angles at v
- Discrete Gauss-Bonnet
- Discrete mean curvature
- Steiner's formula

**Discrete Exterior Calculus (DEC):**
- Discrete differential forms on simplicial complexes
- Discrete exterior derivative
- Discrete Hodge star
- Discrete Laplacian
- Applications: geometry processing, simulation

**Discrete Conformal Maps:**
- Circle packing approach (Thurston, Rodin-Sullivan)
- Discrete Ricci flow
- Conformal equivalence of triangle meshes
- Applications: parameterization, remeshing

## Mathematics of AI & Deep Learning

### Neural Network Theory

**Universal Approximation:**
- Cybenko (1989): single hidden layer neural networks approximate continuous functions on compact sets
- Hornik et al.: approximation in L^p
- Barron's theorem: approximation rates for functions with bounded Fourier moments

**Neural Tangent Kernel (NTK):**
- In infinite width limit, training dynamics are kernel regression
- NTK: Θ(x,x') = E[∇_θ f(x;θ) · ∇_θ f(x';θ)]
- Lazy training regime
- Feature learning regime (beyond NTK)

**Mean Field Theory:**
- McKean-Vlasov equation for neural networks
- Wasserstein gradient flow
- Global convergence for certain architectures

**Landscape Analysis:**
- Spurious local minima
- Saddle points (escaped by noise)
- No bad local valleys for overparameterized networks
- PL condition (Polyak-Łojasiewicz)

### Optimization Theory

**Implicit Regularization:**
- Gradient descent converges to minimum norm solution
- Matrix factorization: low rank
- Linear networks: implicit rank regularization
- Max-margin in classification

**Sharpness-Aware Minimization (SAM):**
- Minimize max_{||ε||≤ρ} L(w+ε)
- Flat minima generalize better
- Connection to PAC-Bayes bounds

**Generalization Bounds:**
- Rademacher complexity
- VC dimension (too loose for deep nets)
- PAC-Bayes bounds
- Uniform stability
- Neural network Gaussian process (NNGP)

### Geometric Deep Learning

**Graph Neural Networks:**
- Message passing: hᵥ^{(l+1)} = UPDATE(hᵥ^{(l)}, AGGREGATE({hᵤ^{(l)} : u ∈ N(v)}))
- GCN, GAT, GraphSAGE
- Weisfeiler-Lehman test
- Expressive power limitations

**Equivariant Networks:**
- E(n)-equivariant: EGNN
- SE(3)-equivariant: Tensor Field Networks
- Steerable CNNs
- Spherical CNNs

**Manifold Learning:**
- Isomap, LLE, t-SNE, UMAP
- Diffusion maps
- Laplacian eigenmaps
- Persistent homology for data

### Generative Models

**Normalizing Flows:**
- Invertible neural networks
- Change of variables formula
- NICE, RealNVP, Glow
- Continuous normalizing flows (FFJORD)

**Diffusion Models:**
- Forward: add noise gradually
- Reverse: learn denoising
- Score matching
- DDPM, DDIM sampling
- Connections to stochastic differential equations

**Energy-Based Models:**
- p(x) = exp(-E(x))/Z
- Contrastive divergence
- Score matching
- Langevin dynamics

### Reinforcement Learning Theory

**Markov Decision Processes:**
- Bellman equation: V*(s) = max_a [R(s,a) + γΣ P(s'|s,a)V*(s')]
- Policy iteration, value iteration
- Q-learning: Q*(s,a) = R(s,a) + γΣ P(s'|s,a) max_a' Q*(s',a')

**Sample Complexity:**
- PAC-MDP: probably approximately correct
- UCB algorithms
- Thompson sampling
- Lower bounds

**Function Approximation:**
- Linear function approximation
- Neural network approximation
- Fitted Q-iteration
- Actor-critic methods

**Multi-Agent RL:**
- Markov games
- Nash equilibrium learning
- Mean field games
- V-learning


---
