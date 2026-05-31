# Physics Complete Reference


---

# CHAPTER 1: CLASSICAL MECHANICS


## Newtonian Mechanics

```
=== KINEMATICS (1D) ===
Position:     x(t)
Velocity:     v = dx/dt = Δx/Δt
Acceleration: a = dv/dt = d²x/dt²

Kinematic equations (constant acceleration):
  v = v₀ + at
  x = x₀ + v₀t + ½at²
  v² = v₀² + 2a(x-x₀)
  x = x₀ + ½(v₀+v)t

Free fall: a = g = 9.8 m/s² (downward)
Projectile (2D):
  x = v₀cosθ·t
  y = v₀sinθ·t - ½gt²
  Range = v₀²sin(2θ)/g  (max at θ=45°)
  Max height = v₀²sin²θ/(2g)

=== NEWTON'S LAWS ===
1st (Inertia): Object at rest stays at rest; in motion stays in motion (ΣF=0)
2nd (F=ma): ΣF = ma  (net force = mass × acceleration)
3rd (Action-Reaction): F₁₂ = -F₂₁

=== COMMON FORCES ===
Weight:         W = mg  (g = 9.8 m/s²)
Normal force:   N (perpendicular to surface)
Friction:       f = μN  (μₛ > μₖ, static vs kinetic)
Spring (Hooke): F = -kx  (k = spring constant, x = displacement)
Drag:           F = ½ρCᴅAv²  (ρ=fluid density, Cᴅ=drag coeff, A=area)

=== WORK AND ENERGY ===
Work:           W = F·d·cosθ  (joules, J)
Kinetic energy: KE = ½mv²
Potential energy (gravity): PE = mgh
Potential energy (spring): PE = ½kx²
Work-energy theorem: Wnet = ΔKE
Conservation of energy: KE₁ + PE₁ = KE₂ + PE₂ (no friction)
Power:          P = W/t = F·v  (watts, W)

=== MOMENTUM AND COLLISIONS ===
Momentum:       p = mv  (kg·m/s)
Impulse:        J = FΔt = Δp
Conservation of momentum: p₁ + p₂ = p₁' + p₂' (isolated system)
Elastic collision: KE conserved; inelastic: KE not conserved
Perfectly inelastic: objects stick together

=== ROTATIONAL MECHANICS ===
Angular position: θ (rad)
Angular velocity: ω = dθ/dt  (rad/s)
Angular acceleration: α = dω/dt  (rad/s²)

Relationships: v = rω,  a_tangential = rα,  a_centripetal = v²/r = rω²

Torque: τ = r × F = rFsinθ  (N·m)
Newton 2nd (rotation): τ = Iα
Moment of inertia: I = Σmᵢrᵢ²
  Solid disk: I = ½MR²
  Solid sphere: I = ⅖MR²
  Hollow sphere: I = ⅔MR²
  Rod (center): I = ¹⁄₁₂ML²
  Rod (end): I = ⅓ML²

Angular momentum: L = Iω = r×p
Conservation: L₁ = L₂ (no external torque)
Rotational KE: ½Iω²
```


---

# CHAPTER 2: THERMODYNAMICS


## Heat and Statistical Mechanics

```
=== TEMPERATURE AND HEAT ===
Temperature conversions:
  K = °C + 273.15
  °F = (9/5)°C + 32
  °C = (5/9)(°F - 32)

Heat transfer: Q = mcΔT  (m=mass, c=specific heat, ΔT=temp change)
  Water: c = 4186 J/(kg·K)
  Aluminum: c = 900 J/(kg·K)
  Iron: c = 450 J/(kg·K)

Phase changes: Q = mL
  Latent heat of fusion (water): L_f = 334,000 J/kg
  Latent heat of vaporization (water): L_v = 2,260,000 J/kg

Heat transfer mechanisms:
  Conduction: Q/t = kA(ΔT/d)  (k=thermal conductivity)
  Convection: Q = hA(T_surface - T_fluid)
  Radiation: P = εσAT⁴  (σ=5.67×10⁻⁸ W/m²K⁴, Stefan-Boltzmann)

=== LAWS OF THERMODYNAMICS ===
Zeroth: Thermal equilibrium is transitive (defines temperature)
First: ΔU = Q - W  (U=internal energy, Q=heat added, W=work done by system)
Second: Entropy of isolated system never decreases (ΔS ≥ 0)
Third: Entropy → 0 as T → 0 K

=== IDEAL GAS LAW ===
PV = nRT  (n=moles, R=8.314 J/mol·K)
PV = NkT  (N=molecules, k=1.38×10⁻²³ J/K, Boltzmann constant)
Boyle's: P₁V₁ = P₂V₂  (constant T)
Charles': V₁/T₁ = V₂/T₂  (constant P)
Gay-Lussac: P₁/T₁ = P₂/T₂  (constant V)

Internal energy (monatomic ideal gas): U = (3/2)NkT = (3/2)nRT
rms speed: v_rms = √(3kT/m) = √(3RT/M)  (M=molar mass)

=== PROCESSES AND EFFICIENCY ===
Isothermal: ΔT=0, W=nRT·ln(V₂/V₁), ΔU=0
Adiabatic: Q=0, TV^(γ-1)=const, γ=Cp/Cv (1.4 for diatomic)
Isobaric: ΔP=0, W=PΔV, Q=nCpΔT
Isochoric: ΔV=0, W=0, Q=ΔU=nCvΔT

Carnot efficiency: η = 1 - T_cold/T_hot  (maximum possible)
Entropy: ΔS = Q_rev/T  (reversible process)
  ΔS = nR·ln(V₂/V₁) + nCv·ln(T₂/T₁)  (ideal gas)
```


---

# CHAPTER 3: ELECTROMAGNETISM


## Electric and Magnetic Fields

```
=== ELECTRIC FORCE AND FIELD ===
Coulomb's law: F = kq₁q₂/r²  (k=8.99×10⁹ N·m²/C²)
  k = 1/(4πε₀),  ε₀ = 8.85×10⁻¹² C²/(N·m²)

Electric field: E = F/q = kQ/r²  (N/C or V/m)
  Field lines: from +, to -; density = field strength
  Superposition: E_total = Σ Eᵢ

Electric potential: V = kQ/r  (volts, V)
  E = -dV/dx  (gradient)
  V = -∫E·dr
  Work: W = qΔV
  Potential energy: U = qV = kq₁q₂/r

=== CIRCUITS ===
Ohm's law: V = IR  (V=volts, I=amps, R=ohms)
Power: P = IV = I²R = V²/R  (watts)

Series: R_total = R₁+R₂+..., I same, V divides
Parallel: 1/R_total = 1/R₁+1/R₂+..., V same, I divides

Kirchhoff's laws:
  KCL (junction): ΣI_in = ΣI_out
  KVL (loop): ΣV = 0  (sum around any loop)

Capacitor: C = Q/V  (farads, F)
  Energy: U = ½CV² = Q²/(2C)
  Series: 1/C = Σ1/Cᵢ
  Parallel: C = ΣCᵢ
  Charging: V(t) = V₀(1-e^(-t/RC))

Inductor: V = L·dI/dt  (L in henries, H)
  Energy: U = ½LI²
  Time constant: τ = L/R

=== MAXWELL'S EQUATIONS ===
Gauss's law (E): ∮E·dA = Q_enc/ε₀
Gauss's law (B): ∮B·dA = 0  (no magnetic monopoles)
Faraday's law: ∮E·dl = -dΦ_B/dt  (changing B creates E)
Ampere-Maxwell: ∮B·dl = μ₀(I + ε₀dΦ_E/dt)

EM waves: c = 1/√(μ₀ε₀) = 3×10⁸ m/s
  c = fλ
  Energy density: u = ½(ε₀E² + B²/μ₀)
  Intensity: I = power/area = u·c

Lorentz force: F = q(E + v×B)
Magnetic force on wire: F = IL×B

=== OPTICS ===
Snell's law: n₁sinθ₁ = n₂sinθ₂
  n = c/v  (index of refraction; n_air≈1, n_glass≈1.5, n_water=1.33)
Total internal reflection: sinθ_c = n₂/n₁ (when n₁>n₂)

Mirror/Lens equation: 1/f = 1/dₒ + 1/dᵢ
  f: focal length, dₒ: object distance, dᵢ: image distance
Magnification: m = -dᵢ/dₒ = hᵢ/hₒ

Diffraction grating: d·sinθ = mλ  (m=0,±1,±2,...)
Young's double slit: constructive at d·sinθ = mλ
```


---

# CHAPTER 4: QUANTUM MECHANICS


## Wave-Particle Duality and Quantum Theory

```
=== QUANTUM BASICS ===
Planck's constant: h = 6.626×10⁻³⁴ J·s
  ℏ = h/(2π) = 1.055×10⁻³⁴ J·s

Photon energy: E = hf = ℏω  (f=frequency, ω=angular frequency)
Photon momentum: p = h/λ = E/c

de Broglie wavelength: λ = h/p = h/(mv)
  Electron at 1 eV: λ ≈ 1.2 nm

Heisenberg uncertainty principle:
  Δx·Δp ≥ ℏ/2
  ΔE·Δt ≥ ℏ/2

=== SCHRÖDINGER EQUATION ===
Time-dependent: iℏ∂ψ/∂t = Ĥψ
Time-independent: Ĥψ = Eψ  (for stationary states)
  Ĥ = -ℏ²/(2m)∇² + V(x)

Born interpretation: |ψ|² = probability density
Normalization: ∫|ψ|²dx = 1

Infinite square well (0<x<L):
  ψₙ = √(2/L)sin(nπx/L)
  Eₙ = n²π²ℏ²/(2mL²) = n²E₁

Harmonic oscillator:
  Eₙ = (n+½)ℏω  (n=0,1,2,...)
  Zero-point energy: E₀ = ℏω/2

=== HYDROGEN ATOM ===
Energy levels: Eₙ = -13.6 eV/n²  (n=1,2,3,...)
Bohr radius: a₀ = 0.529 Å = 5.29×10⁻¹¹ m

Quantum numbers:
  n (principal): 1, 2, 3, ...  (shell)
  l (angular): 0 to n-1  (0=s, 1=p, 2=d, 3=f)
  mₗ (magnetic): -l to +l
  mₛ (spin): ±½

Pauli exclusion: no two electrons have same 4 quantum numbers

Electron configuration example:
  Carbon (Z=6): 1s² 2s² 2p²
  Iron (Z=26): [Ar] 3d⁶ 4s²

=== PARTICLE PHYSICS ===
E = mc²  (mass-energy equivalence)
Relativistic energy: E² = (pc)² + (mc²)²
  Total energy: E = γmc²  (γ=1/√(1-v²/c²))
  Kinetic: K = (γ-1)mc²

Fundamental particles:
  Quarks: up, down, strange, charm, bottom, top
  Leptons: electron, muon, tau + 3 neutrinos
  Gauge bosons: photon (EM), W/Z (weak), gluons (strong), graviton (gravity)

Radioactive decay:
  N(t) = N₀e^(-λt)
  Half-life: t₁/₂ = ln2/λ
  Activity: A = λN = A₀e^(-λt)
  Alpha (α): emit ⁴He nucleus
  Beta (β): emit e⁻ or e⁺ + neutrino
  Gamma (γ): emit photon
```


---

# CHAPTER 5: RELATIVITY


## Special and General Relativity

```
=== SPECIAL RELATIVITY ===
Postulates:
  1. Laws of physics same in all inertial frames
  2. Speed of light c = 3×10⁸ m/s in all inertial frames

Lorentz factor: γ = 1/√(1-β²)  where β = v/c
  γ > 1 always, → ∞ as v → c

Time dilation: Δt = γΔt₀  (moving clock runs slow)
  Δt₀ = proper time (same location)

Length contraction: L = L₀/γ  (moving objects shortened in direction of motion)
  L₀ = proper length

Relativistic momentum: p = γmv
Relativistic energy: E = γmc²
  Rest energy: E₀ = mc²
  Kinetic: K = (γ-1)mc²

Relativistic addition of velocities:
  v' = (v + u)/(1 + vu/c²)  (u = frame velocity)

=== LORENTZ TRANSFORMATION ===
t' = γ(t - vx/c²)
x' = γ(x - vt)
y' = y
z' = z

Spacetime interval: s² = c²t² - x² - y² - z²  (invariant)
  Timelike (s²>0): causally connected events
  Spacelike (s²<0): no causal connection possible
  Lightlike (s²=0): connected by light signal

=== GENERAL RELATIVITY (overview) ===
Equivalence principle: gravity = acceleration locally
Einstein field equations: G_μν = 8πG/c⁴ · T_μν
  G_μν = Einstein tensor (spacetime curvature)
  T_μν = stress-energy tensor (matter/energy)

Geodesic: path of free-falling object in curved spacetime

Predictions (confirmed):
  - Light deflection by gravity (gravitational lensing)
  - Gravitational time dilation: clocks run slower in strong gravity
  - Gravitational redshift: photons lose energy climbing out of gravity well
  - Precession of Mercury's perihelion
  - Gravitational waves (LIGO detected 2015)
  - Black holes: r_s = 2GM/c² (Schwarzschild radius)

GPS correction: must account for both SR (-7 μs/day) and GR (+45 μs/day)
  Net: clocks run fast by ~38 μs/day without correction
```


---

# CHAPTER 6: WAVES AND OSCILLATIONS


## Wave Phenomena

```
=== SIMPLE HARMONIC MOTION ===
x(t) = A cos(ωt + φ)
v(t) = -Aω sin(ωt + φ)
a(t) = -Aω² cos(ωt + φ) = -ω²x

ω = 2πf = 2π/T  (angular frequency)
Period T = 1/f
Energy: E = ½kA²  (k=spring constant, A=amplitude)

Spring: ω = √(k/m)  →  T = 2π√(m/k)
Pendulum: ω = √(g/L)  →  T = 2π√(L/g)  (small angle)

Damped oscillator: x = Ae^(-γt)cos(ω't + φ)
  γ = b/(2m) (damping coefficient)
  ω' = √(ω₀² - γ²)

Resonance: maximum response when driving frequency ≈ natural frequency

=== WAVES ===
Wave equation: ∂²y/∂t² = v²·∂²y/∂x²
Transverse wave: y(x,t) = A sin(kx - ωt + φ)
  k = 2π/λ  (wave number)
  v = ω/k = fλ = λ/T  (wave speed)

String wave speed: v = √(T/μ)  (T=tension, μ=linear density)
Sound speed (air): v = √(γP/ρ) ≈ 343 m/s at 20°C
  v ≈ 331 + 0.6T  (T in °C)

Energy: I = ½ρω²A²v  (intensity)
  Intensity (spherical): I = P/(4πr²)  (falls as 1/r²)

Doppler effect:
  f_observed = f_source · (v ± v_observer)/(v ∓ v_source)
  + for approaching, - for receding

=== INTERFERENCE AND DIFFRACTION ===
Superposition: y_total = y₁ + y₂
Constructive: path difference = mλ
Destructive: path difference = (m+½)λ

Standing waves on string (fixed ends):
  fₙ = n·v/(2L) = n·f₁  (harmonics)
  Nodes at x = nL/N; antinodes between

Sound in pipes:
  Open-open: fₙ = nv/(2L)
  Closed-one: fₙ = (2n-1)v/(4L)  (odd harmonics only)

=== FLUID MECHANICS ===
Pressure: P = F/A  (Pa = N/m²)
  Hydrostatic: P = P₀ + ρgh
  Atmospheric: P₀ ≈ 101,325 Pa = 1 atm

Archimedes: F_buoy = ρ_fluid · V_submerged · g
Bernoulli: P + ½ρv² + ρgh = constant
Continuity (incompressible): A₁v₁ = A₂v₂

Viscosity: F = η·A·(dv/dy)  (η=dynamic viscosity)
Reynolds number: Re = ρvL/η  (laminar <2300, turbulent >4000)
```


---

# CHAPTER 7: PHYSICAL CONSTANTS AND UNITS


## Constants and Conversions

```
=== FUNDAMENTAL CONSTANTS ===
Speed of light:         c  = 2.998×10⁸ m/s
Planck constant:        h  = 6.626×10⁻³⁴ J·s
  ℏ = h/2π           = 1.055×10⁻³⁴ J·s
Boltzmann constant:     k  = 1.381×10⁻²³ J/K
Elementary charge:      e  = 1.602×10⁻¹⁹ C
Electron mass:          mₑ = 9.109×10⁻³¹ kg
Proton mass:            mₚ = 1.673×10⁻²⁷ kg
Neutron mass:           mₙ = 1.675×10⁻²⁷ kg
Avogadro's number:      Nₐ = 6.022×10²³ mol⁻¹
Gas constant:           R  = 8.314 J/(mol·K)
Gravitational constant: G  = 6.674×10⁻¹¹ N·m²/kg²
g (Earth surface):         = 9.807 m/s²
Coulomb constant:       k  = 8.988×10⁹ N·m²/C²
Permittivity of free space: ε₀ = 8.854×10⁻¹² C²/(N·m²)
Permeability of free space: μ₀ = 4π×10⁻⁷ T·m/A
Fine structure constant:  α  = 1/137.036
Bohr radius:            a₀ = 5.292×10⁻¹¹ m
Stefan-Boltzmann:       σ  = 5.671×10⁻⁸ W/(m²·K⁴)

=== SI UNITS ===
Length:        meter (m)
Mass:          kilogram (kg)
Time:          second (s)
Current:       ampere (A)
Temperature:   kelvin (K)
Amount:        mole (mol)
Luminosity:    candela (cd)

Derived:
  Force:       N = kg·m/s²
  Energy:      J = N·m = kg·m²/s²
  Power:       W = J/s
  Pressure:    Pa = N/m²
  Charge:      C = A·s
  Voltage:     V = J/C
  Resistance:  Ω = V/A
  Capacitance: F = C/V
  Inductance:  H = V·s/A
  Frequency:   Hz = s⁻¹
  Magnetic field: T = kg/(A·s²)

=== UNIT PREFIXES ===
tera  (T)  = 10¹²    femto (f)  = 10⁻¹⁵
giga  (G)  = 10⁹     pico  (p)  = 10⁻¹²
mega  (M)  = 10⁶     nano  (n)  = 10⁻⁹
kilo  (k)  = 10³     micro (μ)  = 10⁻⁶
hecto (h)  = 10²     milli (m)  = 10⁻³
deca  (da) = 10¹     centi (c)  = 10⁻²
                      deci  (d)  = 10⁻¹

=== COMMON CONVERSIONS ===
1 eV = 1.602×10⁻¹⁹ J
1 atm = 101325 Pa
1 cal = 4.186 J
1 kWh = 3.6×10⁶ J
1 light-year = 9.461×10¹⁵ m
1 parsec = 3.086×10¹⁶ m = 3.26 light-years
1 AU = 1.496×10¹¹ m
```


---

# CHAPTER 8: MODERN PHYSICS AND ASTROPHYSICS


## Modern Topics

```
=== SOLID STATE PHYSICS ===
Crystal lattice: periodic arrangement of atoms
Lattice types: simple cubic, BCC, FCC, HCP

Band theory:
  Valence band: filled electron states
  Conduction band: empty electron states
  Band gap (E_g): energy between bands
  
  Conductor: no gap (bands overlap)
  Semiconductor: small gap (~1 eV: Si=1.1, Ge=0.67, GaAs=1.4)
  Insulator: large gap (>4 eV: diamond=5.5)

Fermi energy: highest occupied energy at T=0
  Fermi-Dirac distribution: f(E) = 1/(exp((E-E_F)/kT)+1)

Semiconductors:
  Intrinsic: pure, ni = √(NcNv)·exp(-E_g/2kT)
  n-type: donor atoms (extra electrons)
  p-type: acceptor atoms (holes)
  p-n junction: rectifier, depletion zone
  Diode forward bias: I = I₀(e^(qV/kT) - 1)

Hall effect: V_H = IB/(nqt)  (measures carrier density)

=== NUCLEAR PHYSICS ===
Binding energy: B = (Zm_p + Nm_n - m_nucleus)c²
Binding energy per nucleon: peaks at Fe-56

Fission: heavy nucleus splits (U-235, Pu-239)
  n + ²³⁵U → ¹⁴¹Ba + ⁹²Kr + 3n  (chain reaction)
Fusion: light nuclei combine (stars, tokamaks)
  ²H + ³H → ⁴He + n  (+ 17.6 MeV)

Radioactive series: U-238 → ... → Pb-206 (14 steps)

=== COSMOLOGY ===
Big Bang: ~13.8 billion years ago
Hubble's law: v = H₀d  (H₀ ≈ 70 km/s/Mpc)
Dark matter: ~27% of universe energy
Dark energy: ~68% of universe energy (drives acceleration)
Normal matter: ~5%

Cosmic Microwave Background (CMB): T = 2.725 K
  Relic radiation from recombination (~380,000 years after BB)

Stellar evolution:
  Main sequence → Red giant → (low mass: white dwarf)
                            → (high mass: supernova → neutron star/black hole)

Black holes:
  Schwarzschild radius: r_s = 2GM/c²  (event horizon)
  Earth: r_s ≈ 9 mm
  Sun: r_s ≈ 3 km
  Hawking radiation: T_H = ℏc³/(8πGMk)  (tiny for large BH)

=== COMPUTATIONAL PHYSICS ===
Molecular dynamics: simulate atoms via Newton's laws
  Lennard-Jones potential: V(r) = 4ε[(σ/r)¹² - (σ/r)⁶]

Monte Carlo methods: random sampling for integration and simulation
  Error: O(1/√N) regardless of dimension

Finite element method (FEM): solve PDEs on mesh
Finite difference method: approximate derivatives on grid

Density Functional Theory (DFT): quantum many-body systems
  Ground state energy from electron density (not wavefunction)
  Kohn-Sham equations: practical calculation method
```
