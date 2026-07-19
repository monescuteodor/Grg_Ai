# Topology & Differential Geometry Reference

## General Topology
### Basic Concepts
- **Topological Space**: Set X with collection of open sets satisfying axioms (union, intersection, empty/full set).
- **Homeomorphism**: Continuous bijection with continuous inverse. Preserves topological properties.
- **Compactness**: Every open cover has finite subcover. Generalizes "closed and bounded".
- **Connectedness**: Cannot be divided into two disjoint non-empty open sets. Path-connected implies connected.
- **Hausdorff Space**: Distinct points have disjoint neighborhoods. Most spaces in analysis are Hausdorff.

### Fundamental Group
- **Homotopy**: Continuous deformation of paths. γ₀ ~ γ₁ if one can be shrunk to other.
- **Fundamental Group π₁(X,x₀)**: Group of loops based at x₀ under concatenation.
- **Simply Connected**: π₁(X) = {0}. Every loop contracts to point. Example: Sphere S².
- **Non-Simply Connected**: Torus T² has π₁ = ℤ × ℤ. Circle S¹ has π₁ = ℤ.

### Covering Spaces
- **Covering Map**: p: E → B such that each b ∈ B has neighborhood evenly covered.
- **Universal Cover**: Simply connected covering space. Unique up to homeomorphism.
- **Example**: ℝ covers S¹ via p(t) = e^{2πit}. ℂ\{0} covered by ℂ via exp(z).

## Differential Geometry
### Curves in Space
- **Parametrization**: r(t) = (x(t), y(t), z(t)).
- **Arc Length**: s = ∫ |r'(t)| dt.
- **Curvature κ**: |dT/ds|. Measures how fast tangent vector changes.
- **Torsion τ**: Measures twisting out of osculating plane.
- **Frenet-Serret Formulas**: dT/ds = κN, dN/ds = -κT + τB, dB/ds = -τN.

### Surfaces
- **First Fundamental Form**: I = E du² + 2F du dv + G dv². Metric tensor. Measures lengths/angles on surface.
- **Second Fundamental Form**: II = L du² + 2M du dv + N dv². Shape operator. Measures curvature.
- **Gaussian Curvature K**: (LN - M²)/(EG - F²). Intrinsic property. K > 0 (sphere), K < 0 (saddle), K = 0 (plane/cylinder).
- **Mean Curvature H**: (EN + GL - 2FM)/(2(EG - F²)). Extrinsic property. Minimal surfaces have H = 0.

### Gauss-Bonnet Theorem
- **Statement**: ∫∫_S K dA + ∫_∂S κ_g ds = 2π χ(S).
- **χ(S)**: Euler characteristic. Topological invariant.
- **Implication**: Total curvature depends only on topology, not geometry.

## Manifolds
- **Definition**: Space locally homeomorphic to ℝⁿ. Smooth manifold has differentiable transition maps.
- **Tangent Space T_p M**: Vector space of tangent vectors at point p. Dimension = dim(M).
- **Vector Fields**: Assignment of tangent vector to each point. Lie bracket [X,Y] measures non-commutativity.
- **Differential Forms**: Antisymmetric tensors. Exterior derivative d. Stokes' Theorem: ∫_M dω = ∫_∂M ω.
- **Riemannian Manifold**: Manifold with metric tensor g_ij. Defines distances, angles, geodesics.
- **Geodesics**: Curves minimizing distance. Satisfy geodesic equation: d²xᵏ/ds² + Γᵏ_ij dxⁱ/ds dxʲ/ds = 0.