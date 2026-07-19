# Advanced Algebra & Analysis Reference

## Linear Algebra Deep Dive
### Eigenvalues & Eigenvectors
- **Definition**: Av = λv. Vector v (non-zero) is scaled by scalar λ under transformation A.
- **Characteristic Polynomial**: det(A - λI) = 0. Roots are eigenvalues.
- **Diagonalization**: A = PDP⁻¹ if A has n linearly independent eigenvectors. D is diagonal matrix of eigenvalues.
- **Spectral Theorem**: Symmetric real matrices have orthogonal eigenvectors and real eigenvalues.
- **Applications**: Principal Component Analysis (PCA), stability analysis in ODEs, quantum mechanics operators.

### Vector Spaces & Subspaces
- **Basis**: Minimal spanning set. Dimension = number of vectors in basis.
- **Rank**: Dimension of column space (image). Nullity = dimension of null space (kernel).
- **Rank-Nullity Theorem**: rank(A) + nullity(A) = n (number of columns).
- **Orthogonal Projection**: proj_u(v) = ((v·u)/(u·u))u. Gram-Schmidt process orthogonalizes bases.

### Matrix Decompositions
- **LU Decomposition**: A = LU. Lower triangular L, Upper triangular U. Used for solving linear systems efficiently.
- **QR Decomposition**: A = QR. Orthogonal Q, Upper triangular R. Used for least squares problems.
- **Singular Value Decomposition (SVD)**: A = UΣVᵀ. U, V orthogonal; Σ diagonal with singular values. Best low-rank approximation.

## Multivariable Calculus
### Partial Derivatives & Gradient
- **Gradient**: ∇f = <∂f/∂x, ∂f/∂y, ∂f/∂z>. Points in direction of steepest ascent.
- **Directional Derivative**: D_u f = ∇f · u (u is unit vector). Rate of change in direction u.
- **Chain Rule**: dz/dt = (∂z/∂x)(dx/dt) + (∂z/∂y)(dy/dt).

### Multiple Integrals
- **Double Integral**: ∬_R f(x,y)dA. Area under surface z=f(x,y) over region R.
- **Change of Variables (Jacobian)**: ∬_R f(x,y)dxdy = ∬_S f(x(u,v), y(u,v)) |∂(x,y)/∂(u,v)| dudv.
- **Polar Coordinates**: x=r cosθ, y=r sinθ. dA = r dr dθ.
- **Triple Integral**: ∭_E f(x,y,z)dV. Volume/mass calculations. Cylindrical/Spherical coordinates.

### Vector Calculus
- **Line Integral**: ∫_C F·dr. Work done by force field F along curve C.
- **Green's Theorem**: ∮_C (L dx + M dy) = ∬_D (∂M/∂x - ∂L/∂y) dA. Relates line integral to double integral.
- **Stokes' Theorem**: ∮_C F·dr = ∬_S (curl F)·n dS. Relates line integral to surface integral.
- **Divergence Theorem (Gauss)**: ∭_V (div F) dV = ∬_S F·n dS. Relates volume integral to flux through boundary.
- **Curl**: ∇ × F. Measures rotation/circulation density.
- **Divergence**: ∇ · F. Measures source/sink strength.

## Differential Equations Advanced
### Systems of ODEs
- **Matrix Form**: x' = Ax. Solution x(t) = e^(At)x₀.
- **Eigenvalue Method**: If A has distinct real eigenvalues λ₁, λ₂ with eigenvectors v₁, v₂: x(t) = c₁e^(λ₁t)v₁ + c₂e^(λ₂t)v₂.
- **Complex Eigenvalues**: α ± iβ → Oscillatory solutions involving e^(αt)cos(βt) and e^(αt)sin(βt).
- **Phase Plane Analysis**: Trajectories, fixed points (nodes, saddles, spirals), stability.

### Laplace Transforms
- **Definition**: L{f(t)} = ∫₀^∞ e^(-st)f(t)dt. Converts differential equations to algebraic equations.
- **Properties**: L{f'} = sF(s) - f(0); L{f''} = s²F(s) - sf(0) - f'(0).
- **Inverse Laplace**: Use partial fraction decomposition to find f(t) from F(s).
- **Convolution**: L{f * g} = F(s)G(s). Useful for non-homogeneous terms.

### Fourier Series & Transforms
- **Fourier Series**: Periodic function f(x) = a₀/2 + Σ[aₙcos(nπx/L) + bₙsin(nπx/L)].
- **Coefficients**: aₙ = (1/L)∫f(x)cos(nπx/L)dx; bₙ = (1/L)∫f(x)sin(nπx/L)dx.
- **Fourier Transform**: F(ω) = ∫f(t)e^(-iωt)dt. Decomposes signal into frequencies.
- **Parseval's Theorem**: Energy in time domain = Energy in frequency domain.