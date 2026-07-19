# Advanced Mathematics Reference for Grg AI

## Calculus
### Differential Calculus
- **Derivative Definition**: f'(x) = lim[h→0] (f(x+h)-f(x))/h. Instantaneous rate of change.
- **Differentiation Rules**: Product (fg)'=f'g+fg'; Quotient (f/g)'=(f'g-fg')/g²; Chain [f(g)]'=f'(g)·g'.
- **Implicit Differentiation**: Differentiate both sides w.r.t. x, treat y as y(x), solve for dy/dx.
- **Taylor Series**: f(x) = Σ[n=0→∞] f⁽ⁿ⁾(a)/n! · (x-a)ⁿ. Local polynomial approximation.
- **L'Hôpital's Rule**: lim[f/g] = lim[f'/g'] for 0/0 or ∞/∞ indeterminate forms.

### Integral Calculus
- **Fundamental Theorem**: ∫[a,b] f(x)dx = F(b)-F(a). Links differentiation and integration.
- **Integration Techniques**: Substitution u=g(x); Parts ∫udv=uv-∫vdu; Partial fractions; Trig substitution.
- **Improper Integrals**: Infinite limits or discontinuous integrands. Converge if limit exists.
- **Applications**: Area between curves; Volume (disk/washer/shell); Arc length; Surface area; Work.
- **Multivariable**: Partial derivatives ∂f/∂x; Gradient ∇f; Double/triple integrals; Change of variables (Jacobian).

## Linear Algebra
### Vectors & Spaces
- **Vector Operations**: Dot product a·b=|a||b|cosθ; Cross product |a×b|=|a||b|sinθ (direction ⊥ plane).
- **Linear Independence**: Vectors v₁...vₙ independent iff c₁v₁+...+cₙvₙ=0 ⇒ all cᵢ=0.
- **Basis & Dimension**: Basis = linearly independent spanning set. Dimension = # vectors in basis.
- **Subspaces**: Null space, column space, row space. Rank-nullity: rank(A)+nullity(A)=n.

### Matrices & Transformations
- **Matrix Multiplication**: (AB)ᵢⱼ = Σₖ AᵢₖBₖⱼ. Not commutative. Associative. Distributive.
- **Determinant**: det(AB)=det(A)det(B). det≠0 ⇔ invertible. Geometric: volume scaling factor.
- **Eigenvalues/Eigenvectors**: Av=λv. Characteristic eq: det(A-λI)=0. Diagonalization A=PDP⁻¹.
- **Orthogonality**: QᵀQ=I. Orthogonal projection onto subspace W: proj_W(v)=A(AᵀA)⁻¹Aᵀv.
- **SVD**: A=UΣVᵀ. Singular values σᵢ=√(eigenvalues of AᵀA). Best low-rank approximation.

## Differential Equations
### ODEs
- **Separable**: dy/dx=g(x)h(y) ⇒ ∫dy/h(y)=∫g(x)dx.
- **Linear First Order**: y'+P(x)y=Q(x). Integrating factor μ=exp(∫Pdx). Solution y=(∫μQdx+C)/μ.
- **Second Order Linear**: ay''+by'+cy=0. Characteristic eq ar²+br+c=0. Cases: distinct real, repeated, complex.
- **Systems**: x'=Ax. Solution x(t)=e^(At)x₀. Eigenvalue method: x=c₁e^(λ₁t)v₁+c₂e^(λ₂t)v₂.
- **Nonlinear**: Phase plane analysis. Fixed points. Stability via Jacobian eigenvalues. Limit cycles.

### PDEs
- **Heat Equation**: u_t=k∇²u. Diffusion. Separation of variables. Fourier series solution.
- **Wave Equation**: u_tt=c²∇²u. Vibrations. d'Alembert solution. Standing waves.
- **Laplace/Poisson**: ∇²u=0 / ∇²u=f. Steady-state potential. Green's functions. Conformal mapping.

## Discrete Math & Number Theory
### Combinatorics
- **Counting**: Permutations P(n,r)=n!/(n-r)!; Combinations C(n,r)=n!/r!(n-r)!.
- **Binomial Theorem**: (x+y)ⁿ=Σ C(n,k)xᵏyⁿ⁻ᵏ. Pascal's triangle.
- **Recurrence Relations**: aₙ=c₁aₙ₋₁+c₂aₙ₋₂. Characteristic equation method. Generating functions.

### Number Theory
- **Divisibility**: a|b ⇔ b=ak. GCD via Euclidean algorithm. Bezout: gcd(a,b)=ax+by.
- **Modular Arithmetic**: a≡b(mod n). Fermat's Little: aᵖ⁻¹≡1(mod p) for prime p∤a.
- **Chinese Remainder Theorem**: System x≡aᵢ(mod nᵢ) has unique solution mod N=Πnᵢ if nᵢ pairwise coprime.
- **Primality**: Sieve of Eratosthenes. Miller-Rabin test. RSA relies on factoring hardness.

## Complex Analysis
- **Analytic Functions**: Cauchy-Riemann: u_x=v_y, u_y=-v_x. Holomorphic = complex differentiable.
- **Cauchy Integral Theorem**: ∮_C f(z)dz=0 for analytic f inside simply connected domain.
- **Residue Theorem**: ∮_C f(z)dz=2πi Σ Res(f,z_k). Evaluates real integrals via contour integration.
- **Conformal Mapping**: Preserves angles. Möbius transforms map circles/lines to circles/lines.

## Key Identities & Formulas
- Trig: sin²+cos²=1; e^(iθ)=cosθ+isinθ; sin(a±b)=sinacosb±cosasinb
- Log/Exp: ln(ab)=lna+lnb; e^(lnx)=x; log_b(x)=lnx/lnb
- Series: Σxⁿ=1/(1-x) |x|<1; Σ1/n²=π²/6; ζ(s)=Σ1/nˢ
- Transforms: F{f'}=iωF{f}; L{f'}=sF(s)-f(0); Convolution f*g ↔ F·G