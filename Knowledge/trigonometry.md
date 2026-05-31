# Trigonometry Complete Reference

## Angles and Measurement

An angle is formed by two rays sharing a common endpoint (vertex). The initial side is the starting ray; the terminal side is where the angle ends after rotation.
Standard position: vertex at origin, initial side along positive x-axis.

Degree measure: full rotation = 360°. One degree = 1/360 of a full rotation.
Radian measure: angle whose arc length equals the radius. Full rotation = 2π radians.

Conversion formulas:
- Degrees to radians: multiply by π/180
- Radians to degrees: multiply by 180/π
- Examples: 180° = π rad; 90° = π/2 rad; 45° = π/4 rad; 60° = π/3 rad; 30° = π/6 rad; 270° = 3π/2 rad; 360° = 2π rad

Coterminal angles: angles in standard position that share the same terminal side.
Add or subtract multiples of 360° (or 2π): θ + 360°k for any integer k.
Example: 30° and 390° and −330° are all coterminal.

Reference angle: the positive acute angle between the terminal side and the x-axis. Always between 0° and 90°.
- Quadrant I: reference angle = θ
- Quadrant II: reference angle = 180° − θ
- Quadrant III: reference angle = θ − 180°
- Quadrant IV: reference angle = 360° − θ

Arc length formula: s = rθ (θ must be in radians, r = radius, s = arc length)
Sector area: A = (1/2)r²θ (θ in radians)
Linear speed: v = s/t = rω; Angular speed: ω = θ/t (radians per unit time)

## The Six Trigonometric Functions

For a right triangle with angle θ, hypotenuse c, opposite side a, adjacent side b:

SOH-CAH-TOA:
- sin θ = opposite / hypotenuse = a/c
- cos θ = adjacent / hypotenuse = b/c
- tan θ = opposite / adjacent = a/b = sin θ / cos θ

Reciprocal functions:
- csc θ = 1/sin θ = c/a (cosecant)
- sec θ = 1/cos θ = c/b (secant)
- cot θ = 1/tan θ = b/a = cos θ / sin θ (cotangent)

Co-function identities (complementary angles sum to 90°):
- sin θ = cos(90°−θ)
- cos θ = sin(90°−θ)
- tan θ = cot(90°−θ)
- csc θ = sec(90°−θ)
- sec θ = csc(90°−θ)
- cot θ = tan(90°−θ)

## The Unit Circle

The unit circle has center at origin and radius = 1. A point (x, y) on the unit circle satisfies x² + y² = 1.
For angle θ in standard position: the terminal side intersects the unit circle at (cos θ, sin θ).
So: cos θ = x-coordinate, sin θ = y-coordinate, tan θ = y/x.

Key points on the unit circle (angle → (cos, sin)):
- 0° (0): (1, 0)
- 30° (π/6): (√3/2, 1/2)
- 45° (π/4): (√2/2, √2/2)
- 60° (π/3): (1/2, √3/2)
- 90° (π/2): (0, 1)
- 120° (2π/3): (−1/2, √3/2)
- 135° (3π/4): (−√2/2, √2/2)
- 150° (5π/6): (−√3/2, 1/2)
- 180° (π): (−1, 0)
- 210° (7π/6): (−√3/2, −1/2)
- 225° (5π/4): (−√2/2, −√2/2)
- 240° (4π/3): (−1/2, −√3/2)
- 270° (3π/2): (0, −1)
- 300° (5π/3): (1/2, −√3/2)
- 315° (7π/4): (√2/2, −√2/2)
- 330° (11π/6): (√3/2, −1/2)
- 360° (2π): (1, 0)

Memory tip: for 30-45-60, sin values are 1/2, √2/2, √3/2 (numerators 1, √2, √3 increasing).

## Signs in Each Quadrant (ASTC Rule)

"All Students Take Calculus" (or "Add Sugar To Coffee"):
- Quadrant I (0° to 90°): All functions positive (sin+, cos+, tan+)
- Quadrant II (90° to 180°): Sine positive only (sin+, cos−, tan−)
- Quadrant III (180° to 270°): Tangent positive only (sin−, cos−, tan+)
- Quadrant IV (270° to 360°): Cosine positive only (sin−, cos+, tan−)

Reciprocals follow the same sign as their base function:
csc has same sign as sin; sec same sign as cos; cot same sign as tan.

## Exact Values — Complete Table

| Angle | Degrees | sin | cos | tan | csc | sec | cot |
|-------|---------|-----|-----|-----|-----|-----|-----|
| 0 | 0° | 0 | 1 | 0 | undef | 1 | undef |
| π/6 | 30° | 1/2 | √3/2 | 1/√3=√3/3 | 2 | 2√3/3 | √3 |
| π/4 | 45° | √2/2 | √2/2 | 1 | √2 | √2 | 1 |
| π/3 | 60° | √3/2 | 1/2 | √3 | 2√3/3 | 2 | 1/√3=√3/3 |
| π/2 | 90° | 1 | 0 | undef | 1 | undef | 0 |
| π | 180° | 0 | −1 | 0 | undef | −1 | undef |
| 3π/2 | 270° | −1 | 0 | undef | −1 | undef | 0 |
| 2π | 360° | 0 | 1 | 0 | undef | 1 | undef |

## Pythagorean Identities

These come directly from x² + y² = 1 on the unit circle:

Fundamental: sin²θ + cos²θ = 1
Divide by cos²θ: tan²θ + 1 = sec²θ → sec²θ − tan²θ = 1
Divide by sin²θ: 1 + cot²θ = csc²θ → csc²θ − cot²θ = 1

Useful rearrangements:
- sin²θ = 1 − cos²θ
- cos²θ = 1 − sin²θ
- tan²θ = sec²θ − 1
- cot²θ = csc²θ − 1

## Even and Odd Identities

Even functions (symmetric about y-axis, f(−x) = f(x)):
- cos(−θ) = cos θ
- sec(−θ) = sec θ

Odd functions (symmetric about origin, f(−x) = −f(x)):
- sin(−θ) = −sin θ
- tan(−θ) = −tan θ
- csc(−θ) = −csc θ
- cot(−θ) = −cot θ

## Sum and Difference Formulas

sin(A + B) = sin A cos B + cos A sin B
sin(A − B) = sin A cos B − cos A sin B
cos(A + B) = cos A cos B − sin A sin B
cos(A − B) = cos A cos B + sin A sin B
tan(A + B) = (tan A + tan B) / (1 − tan A tan B)
tan(A − B) = (tan A − tan B) / (1 + tan A tan B)

Example: sin 75° = sin(45°+30°) = sin45·cos30 + cos45·sin30
= (√2/2)(√3/2) + (√2/2)(1/2) = √6/4 + √2/4 = (√6+√2)/4

## Double Angle Formulas

sin 2θ = 2 sin θ cos θ
cos 2θ = cos²θ − sin²θ = 1 − 2sin²θ = 2cos²θ − 1
tan 2θ = 2tan θ / (1 − tan²θ)

Example: if sin θ = 3/5 (Quadrant I), cos θ = 4/5:
sin 2θ = 2(3/5)(4/5) = 24/25
cos 2θ = (4/5)² − (3/5)² = 16/25 − 9/25 = 7/25

## Half Angle Formulas

sin(θ/2) = ±√((1 − cos θ)/2)
cos(θ/2) = ±√((1 + cos θ)/2)
tan(θ/2) = ±√((1 − cos θ)/(1 + cos θ)) = sin θ/(1 + cos θ) = (1 − cos θ)/sin θ

The sign (±) depends on the quadrant of θ/2.

Power-reducing formulas (useful in calculus):
sin²θ = (1 − cos 2θ)/2
cos²θ = (1 + cos 2θ)/2
tan²θ = (1 − cos 2θ)/(1 + cos 2θ)

## Product-to-Sum and Sum-to-Product Formulas

Product-to-sum:
sin A · sin B = (1/2)[cos(A−B) − cos(A+B)]
cos A · cos B = (1/2)[cos(A−B) + cos(A+B)]
sin A · cos B = (1/2)[sin(A+B) + sin(A−B)]
cos A · sin B = (1/2)[sin(A+B) − sin(A−B)]

Sum-to-product:
sin A + sin B = 2 sin((A+B)/2) cos((A−B)/2)
sin A − sin B = 2 cos((A+B)/2) sin((A−B)/2)
cos A + cos B = 2 cos((A+B)/2) cos((A−B)/2)
cos A − cos B = −2 sin((A+B)/2) sin((A−B)/2)

## Graphs of Trigonometric Functions

General sinusoidal form: y = A sin(Bx − C) + D or y = A cos(Bx − C) + D

Key parameters:
- Amplitude: |A| — maximum distance from midline (not defined for tan/cot/csc/sec)
- Period: T = 2π/|B| for sin and cos; T = π/|B| for tan and cot
- Phase shift: C/B (shift right if positive, left if negative)
- Vertical shift: D (midline at y = D)
- Frequency: f = 1/T = |B|/(2π)

y = sin x: period 2π, amplitude 1, passes through (0,0), max at π/2, min at 3π/2.
y = cos x: period 2π, amplitude 1, starts at max (0,1), zero at π/2.
y = tan x: period π, undefined at x = π/2 + nπ, passes through (0,0), no amplitude.
y = cot x: period π, undefined at x = nπ.
y = csc x: period 2π, undefined where sin x = 0, U-shaped curves, min 1 max −1.
y = sec x: period 2π, undefined where cos x = 0, U-shaped curves.

Example: y = 3 sin(2x − π/4) + 1
- Amplitude = 3
- Period = 2π/2 = π
- Phase shift = (π/4)/2 = π/8 to the right
- Vertical shift = 1 (midline y = 1)
- Range: [1−3, 1+3] = [−2, 4]

Transformations:
- Vertical stretch/compress: multiply by |A|
- Horizontal stretch/compress: replace x with Bx
- Reflection over x-axis: A < 0
- Reflection over y-axis: replace x with −x

## Inverse Trigonometric Functions

Inverse trig functions give the angle whose trig value is a given number.

Definitions and restricted domains (needed to make them functions):
- arcsin(x) = sin⁻¹(x): domain [−1,1], range [−π/2, π/2] (−90° to 90°)
- arccos(x) = cos⁻¹(x): domain [−1,1], range [0, π] (0° to 180°)
- arctan(x) = tan⁻¹(x): domain all reals, range (−π/2, π/2) (−90° to 90°), excludes endpoints

Examples:
- arcsin(1/2) = 30° = π/6 (because sin 30° = 1/2)
- arccos(−√2/2) = 135° = 3π/4 (because cos 135° = −√2/2)
- arctan(1) = 45° = π/4 (because tan 45° = 1)
- arctan(−√3) = −60° = −π/3

Compositions:
- sin(arcsin(x)) = x for x ∈ [−1,1]
- arcsin(sin(x)) = x only for x ∈ [−π/2, π/2]; otherwise you get the reference angle
- cos(arccos(x)) = x; arccos(cos(x)) = x only for x ∈ [0,π]

Evaluating expressions like cos(arcsin(3/5)):
Draw a right triangle: sin θ = 3/5, so opposite=3, hyp=5, adjacent=4 (3-4-5 triple).
cos(arcsin(3/5)) = 4/5.

Inverse reciprocal functions:
- arccsc(x) = arcsin(1/x)
- arcsec(x) = arccos(1/x)
- arccot(x) = arctan(1/x) adjusted for range

## Solving Trigonometric Equations

Goal: find all angles satisfying a trig equation, usually within [0°, 360°) or [0, 2π).
Then add the period to find all general solutions.

Strategy:
1. Isolate the trig function.
2. Find the reference angle.
3. Determine which quadrants give the correct sign.
4. List all solutions in the given interval.
5. For general solution, add period × n.

Example 1: sin θ = 1/2, θ ∈ [0°, 360°)
Reference angle = 30°. sin is positive in Q I and Q II.
θ = 30° or θ = 150°
General solution: θ = 30° + 360°n or θ = 150° + 360°n

Example 2: tan θ = −1, θ ∈ [0°, 360°)
Reference angle = 45°. tan is negative in Q II and Q IV.
θ = 135° or θ = 315°
General solution: θ = 135° + 180°n (tan has period 180°)

Example 3: 2cos²θ − cosθ − 1 = 0
Factor: (2cosθ + 1)(cosθ − 1) = 0
cosθ = −1/2 → θ = 120°, 240°; cosθ = 1 → θ = 0°

Example 4: sin 2θ = cos θ, θ ∈ [0, 2π)
2 sin θ cos θ = cos θ → 2 sin θ cos θ − cos θ = 0 → cos θ(2sin θ − 1) = 0
cos θ = 0 → θ = π/2, 3π/2; sin θ = 1/2 → θ = π/6, 5π/6

Always verify solutions in the original equation (extraneous solutions can arise).

## Law of Sines

Used for any triangle (not just right triangles). Works with AAS, ASA, or SSA.

a/sin A = b/sin B = c/sin C

where a, b, c are sides and A, B, C are opposite angles.

Solving a triangle (find all missing parts):
AAS or ASA: find missing angle (angle sum = 180°), then use Law of Sines for sides.
SSA (ambiguous case): given two sides and a non-included angle.
- If a < b sin A: no triangle.
- If a = b sin A: one right triangle.
- If b sin A < a < b: two possible triangles (both valid).
- If a ≥ b: one triangle.

Example (AAS): A = 40°, B = 75°, a = 10.
C = 180° − 40° − 75° = 65°
b = a·sin B/sin A = 10·sin75°/sin40° ≈ 10(0.9659)/(0.6428) ≈ 15.03
c = a·sin C/sin A = 10·sin65°/sin40° ≈ 14.10

Area using Law of Sines: A = (1/2)ab sin C = (1/2)bc sin A = (1/2)ac sin B

## Law of Cosines

Used when you have SSS or SAS (Law of Sines doesn't apply directly).

c² = a² + b² − 2ab cos C
b² = a² + c² − 2ac cos B
a² = b² + c² − 2bc cos A

Solving for angles:
cos C = (a² + b² − c²) / (2ab)

Note: if C = 90°, then cos C = 0 and the formula reduces to the Pythagorean theorem.

Example (SAS): a = 8, b = 11, C = 35°
c² = 64 + 121 − 2(8)(11)cos35° = 185 − 176(0.8192) ≈ 185 − 144.2 = 40.8
c ≈ 6.39

Finding angles from SSS: use the cosine formula rearranged:
a = 5, b = 7, c = 9. cos C = (25+49−81)/(2·5·7) = −7/70 = −0.1 → C ≈ 95.7°

Heron's formula (area from SSS): s = (a+b+c)/2; Area = √(s(s−a)(s−b)(s−c))

## Trigonometric Identities — Proving

To prove an identity, work on one side only (usually the more complex side) and transform it to look like the other side. Do not move terms across the equals sign.

Strategies:
- Convert everything to sin and cos.
- Factor expressions.
- Multiply numerator and denominator by a conjugate.
- Use Pythagorean identities to substitute.
- Split fractions or combine fractions.
- Look for common patterns.

Example: Prove sin²x/(1−cosx) = 1+cosx
LHS = (1−cos²x)/(1−cosx) = (1−cosx)(1+cosx)/(1−cosx) = 1+cosx = RHS ✓

Example: Prove (sinx + cosx)² = 1 + 2sinx cosx
LHS = sin²x + 2sinx cosx + cos²x = (sin²x + cos²x) + 2sinx cosx = 1 + 2sinx cosx = RHS ✓

Example: Prove tanx + cotx = secx cscx
LHS = sinx/cosx + cosx/sinx = (sin²x + cos²x)/(sinx cosx) = 1/(sinx cosx) = secx cscx = RHS ✓

## Polar Coordinates and Complex Numbers in Polar Form

Polar coordinates (r, θ): r = distance from origin; θ = angle from positive x-axis.
Converting polar to rectangular: x = r cosθ, y = r sinθ
Converting rectangular to polar: r = √(x²+y²), θ = arctan(y/x) (adjust quadrant)

Example: (r,θ) = (4, π/3) → x = 4cos(π/3) = 2, y = 4sin(π/3) = 2√3. Point: (2, 2√3).
Example: (x,y) = (−3, 3) → r = √(9+9) = 3√2, θ = arctan(3/−3) = arctan(−1) in Q II = 135°.

Polar form of complex numbers:
z = a + bi = r(cosθ + i sinθ) = r cis θ = re^(iθ)
where r = |z| = √(a²+b²) is the modulus, θ = arg(z) = arctan(b/a) is the argument.

Euler's formula: e^(iθ) = cosθ + i sinθ (fundamental result connecting e, i, trig)
Euler's identity: e^(iπ) + 1 = 0

Multiplication in polar form: r₁cis θ₁ · r₂cis θ₂ = r₁r₂ · cis(θ₁+θ₂)
Division in polar form: (r₁/r₂) · cis(θ₁−θ₂)

De Moivre's Theorem: (r cis θ)ⁿ = rⁿ cis(nθ)
Powers: (2 cis 30°)³ = 8 cis 90° = 8i

nth roots of a complex number: z^(1/n) = r^(1/n) cis((θ + 360°k)/n) for k = 0,1,…,n−1.
There are always exactly n distinct nth roots.
Roots of unity: nth roots of 1 are cis(360°k/n) for k = 0,…,n−1. Equally spaced on the unit circle.

## Hyperbolic Functions

Hyperbolic functions are analogs of trig functions defined using the exponential function.

Definitions:
- sinh x = (eˣ − e⁻ˣ)/2
- cosh x = (eˣ + e⁻ˣ)/2
- tanh x = sinh x / cosh x = (eˣ − e⁻ˣ)/(eˣ + e⁻ˣ)
- csch x = 1/sinh x; sech x = 1/cosh x; coth x = 1/tanh x

Key identity: cosh²x − sinh²x = 1 (compare sin²+cos²=1)

Properties:
- cosh(−x) = cosh x (even); sinh(−x) = −sinh x (odd)
- sinh(A+B) = sinh A cosh B + cosh A sinh B
- cosh(A+B) = cosh A cosh B + sinh A sinh B

Graphs: sinh has range all reals, passes through origin. cosh has minimum of 1 at x=0 (catenary curve — shape of a hanging chain).

## Trigonometry in Calculus (Preview)

Derivatives:
d/dx[sin x] = cos x
d/dx[cos x] = −sin x
d/dx[tan x] = sec²x
d/dx[csc x] = −csc x cot x
d/dx[sec x] = sec x tan x
d/dx[cot x] = −csc²x

Integrals:
∫ sin x dx = −cos x + C
∫ cos x dx = sin x + C
∫ tan x dx = ln|sec x| + C
∫ sec²x dx = tan x + C
∫ sec x tan x dx = sec x + C

Key limits:
lim(x→0) sin x / x = 1 (fundamental limit in calculus)
lim(x→0) (1 − cos x) / x = 0

Trig substitutions (for integrals with square roots):
- √(a²−x²): let x = a sin θ
- √(a²+x²): let x = a tan θ
- √(x²−a²): let x = a sec θ

## Quick Reference — Key Identities Summary

Reciprocal: csc=1/sin, sec=1/cos, cot=1/tan
Quotient: tan=sin/cos, cot=cos/sin
Pythagorean: sin²+cos²=1; tan²+1=sec²; 1+cot²=csc²
Even/Odd: cos(−x)=cosx; sin(−x)=−sinx; tan(−x)=−tanx
Cofunction: sin(90°−x)=cosx; tan(90°−x)=cotx; sec(90°−x)=cscx
Sum: sin(A±B)=sinAcosB±cosAsinB; cos(A±B)=cosAcosB∓sinAsinB
Double: sin2x=2sinxcosx; cos2x=cos²x−sin²x=1−2sin²x=2cos²x−1
Half: sin²x=(1−cos2x)/2; cos²x=(1+cos2x)/2
Law of Sines: a/sinA = b/sinB = c/sinC
Law of Cosines: c²=a²+b²−2ab·cosC
Area: A=(1/2)absinC
Polar: x=rcosθ, y=rsinθ, r=√(x²+y²)
De Moivre: (rcisθ)ⁿ = rⁿcis(nθ)
Euler: e^(iθ) = cosθ + i sinθ
