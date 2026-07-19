# Condensed Matter Physics Reference

## Crystal Structure
### Lattices & Unit Cells
- **Bravais Lattices**: 14 types in 3D (Cubic, Tetragonal, Orthorhombic, etc.).
- **Miller Indices (hkl)**: Describe crystal planes. Reciprocal intercepts.
- **Reciprocal Lattice**: Defined by basis vectors bᵢ such that aᵢ·bⱼ = 2πδᵢⱼ. Crucial for diffraction.

### Diffraction
- **Bragg's Law**: nλ = 2d sinθ. Constructive interference from crystal planes.
- **Laue Condition**: Δk = G (reciprocal lattice vector). Momentum conservation in scattering.
- **Structure Factor**: F(G) = Σ fⱼ e^{-iG·rⱼ}. Determines intensity of diffraction peaks.

## Band Theory
### Bloch's Theorem
- **Wavefunction**: ψ_k(r) = e^{ik·r} u_k(r). u_k(r) has periodicity of lattice.
- **Band Structure**: E(k) vs k in Brillouin zone. Allowed energy levels.

### Metals, Insulators, Semiconductors
- **Fermi Level E_F**: Highest occupied energy at T=0.
- **Metal**: Partially filled band. E_F intersects band. High conductivity.
- **Insulator**: Full valence band, empty conduction band. Large gap (>3 eV).
- **Semiconductor**: Small gap (~1 eV). Conductivity increases with T. Doping modifies carrier concentration.

### Effective Mass
- **Concept**: Electron responds to external field as if it had mass m*.
- **Formula**: 1/m* = (1/ℏ²) d²E/dk². Curvature of band determines mass.

## Magnetism
### Types
- **Diamagnetism**: Weak repulsion from magnetic field. All materials have it. Lenz's law at atomic scale.
- **Paramagnetism**: Weak attraction. Unpaired spins align with field. Curie Law: χ ∝ 1/T.
- **Ferromagnetism**: Strong attraction. Spontaneous alignment below Curie temperature T_C. Domains.
- **Antiferromagnetism**: Adjacent spins anti-align. Net magnetization zero.
- **Ferrimagnetism**: Anti-aligned spins of unequal magnitude. Net magnetization.

### Exchange Interaction
- **Quantum Origin**: Pauli exclusion + Coulomb repulsion.
- **Heisenberg Model**: H = -J Σ Sᵢ·Sⱼ. J>0 ferromagnetic, J<0 antiferromagnetic.

## Superconductivity
### Phenomenology
- **Zero Resistance**: Below critical temperature T_C.
- **Meissner Effect**: Expulsion of magnetic field. Perfect diamagnetism.
- **Critical Field H_C**: Magnetic field destroys superconductivity.

### BCS Theory
- **Cooper Pairs**: Two electrons with opposite momentum/spin bind via phonon exchange.
- **Energy Gap**: Δ opens at Fermi surface. Excitations require energy ≥ 2Δ.
- **Coherence Length ξ**: Size of Cooper pair.

### Type I vs Type II
- **Type I**: Single critical field. Complete Meissner effect. Pure metals.
- **Type II**: Two critical fields H_C1, H_C2. Mixed state (vortices) between them. Alloys/High-T_C.