# Mathematical Analysis Complete Reference

## Real Numbers and the Real Line

The real number system ℝ is a complete ordered field. Every non-empty subset bounded above has a least upper bound (supremum) — this is the completeness axiom.

Supremum (sup): least upper bound of a set. Infimum (inf): greatest lower bound.
Example: sup{1 − 1/n : n ∈ ℕ} = 1 (never reached but approached arbitrarily closely).

Absolute value: |x| = x if x ≥ 0, −x if x < 0. Distance between a and b on ℝ is |a − b|.
Triangle inequality: |a + b| ≤ |a| + |b|. Also: ||a| − |b|| ≤ |a − b|.

Intervals:
- Open: (a, b) = {x : a < x < b}
- Closed: [a, b] = {x : a ≤ x ≤ b}
- Half-open: [a, b) or (a, b]
- Unbounded: (a, ∞), (−∞, b], (−∞, ∞) = ℝ

Neighborhoods: an ε-neighborhood of point a is the open interval (a−ε, a+ε), all points within distance ε of a.

Density of ℚ in ℝ: between any two real numbers there is a rational number and an irrational number.

## Sequences

A sequence is a function f: ℕ → ℝ, written as {aₙ} or a₁, a₂, a₃, …

Limit of a sequence: lim(n→∞) aₙ = L means for every ε > 0, there exists N such that for all n > N, |aₙ − L| < ε.
A sequence that has a limit is called convergent; otherwise divergent.

Uniqueness: a convergent sequence has exactly one limit.
Boundedness: every convergent sequence is bounded.

Arithmetic rules for limits (if lim aₙ = L and lim bₙ = M):
- lim(aₙ ± bₙ) = L ± M
- lim(aₙ · bₙ) = L · M
- lim(aₙ/bₙ) = L/M provided M ≠ 0
- lim(c · aₙ) = c · L
- lim|aₙ| = |L|

Squeeze theorem (sandwich theorem): if aₙ ≤ bₙ ≤ cₙ and lim aₙ = lim cₙ = L, then lim bₙ = L.

Monotone Convergence Theorem: a monotone increasing sequence bounded above converges; a monotone decreasing sequence bounded below converges.

Subsequences: a subsequence of {aₙ} is formed by taking elements at increasing indices n₁ < n₂ < n₃ < …
If {aₙ} converges to L, every subsequence also converges to L.
Bolzano-Weierstrass theorem: every bounded sequence has a convergent subsequence.

Cauchy sequences: {aₙ} is Cauchy if for every ε > 0 there exists N such that for all m, n > N, |aₙ − aₘ| < ε.
A sequence in ℝ is convergent if and only if it is Cauchy.

Important limits:
- lim(n→∞) 1/n = 0
- lim(n→∞) rⁿ = 0 if |r| < 1; diverges if |r| > 1
- lim(n→∞) n^(1/n) = 1
- lim(n→∞) (1 + 1/n)ⁿ = e
- lim(n→∞) xⁿ/n! = 0 for all x
- lim(n→∞) (ln n)/n = 0

## Limits of Functions

Formal definition (epsilon-delta): lim(x→a) f(x) = L means for every ε > 0, there exists δ > 0 such that 0 < |x − a| < δ implies |f(x) − L| < ε.
Note: the value at x = a does not matter (or need not exist).

One-sided limits:
- Right-hand limit: lim(x→a⁺) f(x) = L (approach from x > a)
- Left-hand limit: lim(x→a⁻) f(x) = L (approach from x < a)
lim(x→a) f(x) exists if and only if both one-sided limits exist and are equal.

Limits at infinity: lim(x→∞) f(x) = L means f(x) can be made arbitrarily close to L for all sufficiently large x.
Vertical asymptote at x = a: lim(x→a) |f(x)| = ∞.
Horizontal asymptote y = L: lim(x→±∞) f(x) = L.

Limit laws (same as for sequences): sum, difference, product, quotient, constant multiple, power.

Squeeze theorem for functions: if g(x) ≤ f(x) ≤ h(x) near a and lim g(x) = lim h(x) = L, then lim f(x) = L.

Important limits:
- lim(x→0) sin x / x = 1 (must memorize)
- lim(x→0) (1 − cos x) / x = 0
- lim(x→0) (eˣ − 1) / x = 1
- lim(x→0) ln(1 + x) / x = 1
- lim(x→0) (aˣ − 1) / x = ln a
- lim(x→∞) (1 + 1/x)ˣ = e

L'Hôpital's Rule: if lim f(x) = lim g(x) = 0 or ±∞, then lim f(x)/g(x) = lim f'(x)/g'(x), provided the latter limit exists.
Applicable to indeterminate forms: 0/0, ∞/∞. For forms 0·∞, ∞−∞, 0⁰, 1^∞, ∞⁰, rewrite first.

## Continuity

f is continuous at a if: (1) f(a) is defined, (2) lim(x→a) f(x) exists, (3) lim(x→a) f(x) = f(a).

Types of discontinuity:
- Removable: limit exists but ≠ f(a) or f(a) undefined. Fix by redefining f(a).
- Jump: left and right limits both exist but differ.
- Infinite: limit is ±∞.
- Oscillatory: limit does not exist (e.g., sin(1/x) as x→0).

Continuity on intervals: f is continuous on [a,b] if continuous at every interior point and continuous from the right at a, from the left at b.

Properties of continuous functions:
- Sums, differences, products, quotients (g≠0), compositions of continuous functions are continuous.
- Polynomials and rational functions (where denominator ≠ 0) are continuous everywhere.
- sin, cos, eˣ, ln x are continuous on their domains.

Intermediate Value Theorem (IVT): if f is continuous on [a, b] and k is any value between f(a) and f(b), then there exists c ∈ (a, b) with f(c) = k.
Application: root finding — if f(a) and f(b) have opposite signs, f has a root in (a, b).

Extreme Value Theorem (EVT): if f is continuous on [a, b], then f attains both a maximum value and a minimum value on [a, b].

Uniform continuity: f is uniformly continuous on an interval if δ depends only on ε, not on the point x.
Every continuous function on a closed bounded interval [a, b] is uniformly continuous (Heine-Cantor theorem).

## Differentiation

The derivative of f at x = a is f'(a) = lim(h→0) [f(a+h) − f(a)] / h, provided the limit exists.
Geometrically: slope of the tangent line to the graph at (a, f(a)).
If the derivative exists at a point, the function is differentiable there. Differentiability implies continuity (not vice versa).

Notation: f'(x), df/dx, dy/dx, Df(x), ẋ (Newton), all mean the same.

Basic differentiation rules:
- Constant: d/dx[c] = 0
- Power rule: d/dx[xⁿ] = nxⁿ⁻¹ (works for all real n)
- Constant multiple: d/dx[cf(x)] = c·f'(x)
- Sum/difference: d/dx[f ± g] = f' ± g'
- Product rule: d/dx[fg] = f'g + fg'
- Quotient rule: d/dx[f/g] = (f'g − fg')/g²
- Chain rule: d/dx[f(g(x))] = f'(g(x))·g'(x)

Derivatives of elementary functions:
- d/dx[xⁿ] = nxⁿ⁻¹
- d/dx[eˣ] = eˣ; d/dx[aˣ] = aˣ ln a
- d/dx[ln x] = 1/x; d/dx[logₐx] = 1/(x ln a)
- d/dx[sin x] = cos x; d/dx[cos x] = −sin x
- d/dx[tan x] = sec²x; d/dx[cot x] = −csc²x
- d/dx[sec x] = sec x tan x; d/dx[csc x] = −csc x cot x
- d/dx[arcsin x] = 1/√(1−x²); d/dx[arccos x] = −1/√(1−x²)
- d/dx[arctan x] = 1/(1+x²); d/dx[arccot x] = −1/(1+x²)
- d/dx[sinh x] = cosh x; d/dx[cosh x] = sinh x; d/dx[tanh x] = sech²x

Implicit differentiation: differentiate both sides with respect to x; treat y as a function of x and use chain rule.
Example: x² + y² = 25 → 2x + 2y(dy/dx) = 0 → dy/dx = −x/y.

Logarithmic differentiation: take ln of both sides before differentiating. Useful for products, quotients, or variable exponents.
Example: y = xˣ → ln y = x ln x → (1/y)y' = ln x + 1 → y' = xˣ(ln x + 1).

Higher-order derivatives: f''(x) = d²f/dx² (second derivative), f⁽ⁿ⁾(x) = nth derivative.
Second derivative measures concavity; acceleration if x = position.

## Mean Value Theorem and Applications

Rolle's Theorem: if f is continuous on [a,b], differentiable on (a,b), and f(a) = f(b), then there exists c ∈ (a,b) with f'(c) = 0.

Mean Value Theorem (MVT): if f is continuous on [a,b] and differentiable on (a,b), then there exists c ∈ (a,b) with f'(c) = (f(b)−f(a))/(b−a).
Geometrically: there is a tangent line parallel to the secant line through (a,f(a)) and (b,f(b)).

Consequences:
- If f'(x) = 0 on (a,b), then f is constant on [a,b].
- If f'(x) > 0 on (a,b), then f is strictly increasing.
- If f'(x) < 0 on (a,b), then f is strictly decreasing.

Monotonicity test: find critical points (where f'=0 or undefined), test sign of f' on each interval.

Concavity and inflection points:
- f''(x) > 0 on (a,b): f is concave up (smile shape) on that interval.
- f''(x) < 0 on (a,b): f is concave down (frown shape).
- Inflection point: where concavity changes (f'' changes sign).

Critical points: where f'(x) = 0 or f'(x) does not exist.
First derivative test: sign of f' changes from + to − → local max; from − to + → local min.
Second derivative test: f'(c) = 0 and f''(c) < 0 → local max; f''(c) > 0 → local min; f''(c) = 0 → inconclusive.

Absolute (global) extrema on [a,b]: compare values at all critical points and endpoints; the largest is the absolute max, smallest is the absolute min.

Optimization: find the quantity to maximize/minimize, express it as a function of one variable, find critical points, check endpoints and second derivative.

## Integration — Antiderivatives and Indefinite Integrals

An antiderivative of f is a function F such that F'(x) = f(x).
The indefinite integral: ∫ f(x) dx = F(x) + C, where C is an arbitrary constant.

Basic integration rules:
- ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C (n ≠ −1)
- ∫ x⁻¹ dx = ∫ 1/x dx = ln|x| + C
- ∫ eˣ dx = eˣ + C; ∫ aˣ dx = aˣ/(ln a) + C
- ∫ sin x dx = −cos x + C; ∫ cos x dx = sin x + C
- ∫ tan x dx = ln|sec x| + C = −ln|cos x| + C
- ∫ sec²x dx = tan x + C; ∫ csc²x dx = −cot x + C
- ∫ sec x tan x dx = sec x + C; ∫ csc x cot x dx = −csc x + C
- ∫ 1/√(1−x²) dx = arcsin x + C; ∫ −1/√(1−x²) dx = arccos x + C
- ∫ 1/(1+x²) dx = arctan x + C
- ∫ sinh x dx = cosh x + C; ∫ cosh x dx = sinh x + C

Integration techniques:

1. Substitution (u-substitution): let u = g(x), du = g'(x)dx. Replaces complex integrals with simpler ones.
   Example: ∫ 2x(x²+1)⁵ dx. Let u = x²+1, du = 2x dx. → ∫ u⁵ du = u⁶/6 + C = (x²+1)⁶/6 + C.

2. Integration by parts: ∫ u dv = uv − ∫ v du. Choose u and dv wisely (LIATE: Logarithmic, Inverse trig, Algebraic, Trig, Exponential — prefer u from left).
   Example: ∫ x eˣ dx. u = x, dv = eˣ dx → du = dx, v = eˣ. = xeˣ − ∫ eˣ dx = xeˣ − eˣ + C.

3. Trigonometric integrals: use identities to simplify.
   ∫ sinⁿx cosᵐx dx: if n or m is odd, save one factor and convert rest using sin²+cos²=1; if both even, use power-reducing formulas.

4. Trigonometric substitution:
   √(a²−x²): let x = a sinθ; √(a²+x²): let x = a tanθ; √(x²−a²): let x = a secθ.

5. Partial fractions: for rational functions P(x)/Q(x) where deg P < deg Q, decompose into simpler fractions.
   Linear factors: A/(x−r); repeated: A/(x−r) + B/(x−r)²; irreducible quadratic: (Ax+B)/(x²+bx+c).

## The Definite Integral and Fundamental Theorem

Riemann sums: partition [a,b] into n subintervals, pick sample points xᵢ*, sum f(xᵢ*)Δxᵢ.
Definite integral: ∫ₐᵇ f(x) dx = lim(n→∞) Σ f(xᵢ*)Δxᵢ (if the limit exists, f is integrable).
Every continuous function on [a,b] is Riemann integrable.

Geometric interpretation: ∫ₐᵇ f(x) dx = signed area between the graph and the x-axis.
Area above x-axis contributes positively; area below contributes negatively.

Properties of the definite integral:
- ∫ₐᵃ f dx = 0
- ∫ₐᵇ f dx = −∫ᵦₐ f dx
- ∫ₐᵇ (f ± g) dx = ∫ₐᵇ f dx ± ∫ₐᵇ g dx
- ∫ₐᵇ cf dx = c∫ₐᵇ f dx
- ∫ₐᵇ f dx = ∫ₐᶜ f dx + ∫ᶜᵇ f dx (additivity)
- If f ≥ 0 on [a,b], then ∫ₐᵇ f dx ≥ 0
- |∫ₐᵇ f dx| ≤ ∫ₐᵇ |f| dx

Fundamental Theorem of Calculus (FTC):
Part 1: if F(x) = ∫ₐˣ f(t) dt, then F'(x) = f(x). (Differentiation undoes integration.)
Part 2: if F is an antiderivative of f on [a,b], then ∫ₐᵇ f(x) dx = F(b) − F(a). (Evaluation theorem.)

Mean Value Theorem for Integrals: if f is continuous on [a,b], there exists c ∈ (a,b) with f(c) = (1/(b−a))∫ₐᵇ f(x) dx. The average value of f on [a,b] is f_avg = (1/(b−a))∫ₐᵇ f(x) dx.

## Applications of Integration

Area between two curves: A = ∫ₐᵇ [f(x) − g(x)] dx where f(x) ≥ g(x) on [a,b].
If curves cross, split integral at intersection points.

Volumes of solids of revolution:
- Disk method (axis is the x-axis or y-axis): V = π∫ₐᵇ [f(x)]² dx
- Washer method (hole in solid): V = π∫ₐᵇ ([f(x)]² − [g(x)]²) dx
- Shell method (cylindrical shells): V = 2π∫ₐᵇ x·f(x) dx

Arc length: L = ∫ₐᵇ √(1 + [f'(x)]²) dx

Surface area of revolution: SA = 2π∫ₐᵇ f(x)√(1 + [f'(x)]²) dx

Work: W = ∫ₐᵇ F(x) dx (force as a function of position)
Hooke's Law: F = kx; W = ∫₀ᵈ kx dx = kd²/2

Improper integrals:
Type 1 (infinite limits): ∫ₐ^∞ f dx = lim(b→∞) ∫ₐᵇ f dx
Type 2 (unbounded integrand): ∫ₐᵇ f dx = lim(c→a⁺) ∫ᶜᵇ f dx if f unbounded near a.
Convergent if the limit exists and is finite; divergent otherwise.
Example: ∫₁^∞ 1/xᵖ dx converges if p > 1, diverges if p ≤ 1.
Comparison test for improper integrals: if 0 ≤ f ≤ g and ∫g converges, then ∫f converges.

## Infinite Series

A series is the sum Σₙ₌₁^∞ aₙ = lim(n→∞) Sₙ where Sₙ = a₁ + a₂ + … + aₙ (partial sums).
Convergent series: the sequence of partial sums converges to a finite limit.
Divergent series: partial sums diverge (go to ∞, −∞, or oscillate).

nth-term test (divergence test): if lim(n→∞) aₙ ≠ 0, then Σaₙ diverges. (If lim aₙ = 0, the test is inconclusive.)

Geometric series: Σₙ₌₀^∞ arⁿ = a/(1−r) if |r| < 1; diverges if |r| ≥ 1.
Example: Σ (1/2)ⁿ = 1/(1−1/2) = 2.

p-series: Σ 1/nᵖ converges if p > 1, diverges if p ≤ 1.
Harmonic series: Σ 1/n diverges (p = 1).

Convergence tests:

1. Integral test: if f is positive, continuous, decreasing on [1,∞) and aₙ = f(n), then Σaₙ and ∫₁^∞ f(x)dx either both converge or both diverge.

2. Comparison test: if 0 ≤ aₙ ≤ bₙ, then: Σbₙ converges → Σaₙ converges; Σaₙ diverges → Σbₙ diverges.

3. Limit comparison test: if lim(n→∞) aₙ/bₙ = c where 0 < c < ∞, then Σaₙ and Σbₙ either both converge or both diverge.

4. Ratio test: let L = lim|aₙ₊₁/aₙ|. If L < 1: converges absolutely. If L > 1: diverges. If L = 1: inconclusive.

5. Root test: let L = lim|aₙ|^(1/n). Same conclusions as ratio test.

6. Alternating series test (Leibniz): Σ(−1)ⁿaₙ converges if aₙ decreasing and lim aₙ = 0.
   Error bound: |Sₙ − S| ≤ aₙ₊₁.

Absolute vs conditional convergence:
- Absolutely convergent: Σ|aₙ| converges → Σaₙ also converges.
- Conditionally convergent: Σaₙ converges but Σ|aₙ| diverges.
- Example: Σ(−1)ⁿ/n converges conditionally; Σ(−1)ⁿ/n² converges absolutely.

## Power Series and Taylor Series

A power series centered at a: Σₙ₌₀^∞ cₙ(x−a)ⁿ = c₀ + c₁(x−a) + c₂(x−a)² + …

Radius of convergence R: the series converges for |x−a| < R and diverges for |x−a| > R.
Found via: R = lim|cₙ/cₙ₊₁| or R = 1/lim|cₙ|^(1/n).
At endpoints x = a ± R, check convergence separately.

Within its interval of convergence, a power series defines a continuous, differentiable, integrable function.
Differentiation and integration are done term by term.

Taylor series of f at a: f(x) = Σₙ₌₀^∞ f⁽ⁿ⁾(a)/n! · (x−a)ⁿ
Maclaurin series (centered at 0): f(x) = Σₙ₌₀^∞ f⁽ⁿ⁾(0)/n! · xⁿ

Essential Maclaurin series (memorize):
- eˣ = 1 + x + x²/2! + x³/3! + x⁴/4! + … = Σ xⁿ/n!, for all x
- sin x = x − x³/3! + x⁵/5! − x⁷/7! + … = Σ (−1)ⁿx^(2n+1)/(2n+1)!, for all x
- cos x = 1 − x²/2! + x⁴/4! − x⁶/6! + … = Σ (−1)ⁿx^(2n)/(2n)!, for all x
- ln(1+x) = x − x²/2 + x³/3 − x⁴/4 + … = Σ (−1)ⁿ⁺¹xⁿ/n, for −1 < x ≤ 1
- 1/(1−x) = 1 + x + x² + x³ + … = Σ xⁿ, for |x| < 1
- arctan x = x − x³/3 + x⁵/5 − … = Σ (−1)ⁿx^(2n+1)/(2n+1), for |x| ≤ 1
- (1+x)ᵏ = 1 + kx + k(k−1)x²/2! + … (binomial series), for |x| < 1

Taylor's remainder theorem: Rₙ(x) = f⁽ⁿ⁺¹⁾(c)/(n+1)! · (x−a)ⁿ⁺¹ for some c between a and x.
Use to bound the error when approximating f by a partial sum.

## Multivariable Functions and Partial Derivatives

A function of two variables: f(x, y) maps a point in ℝ² to a value in ℝ. Graph is a surface in ℝ³.
Level curves (contour lines): f(x, y) = c for various constants c.
Domain: set of all (x, y) where f is defined. Range: set of all output values.

Limits: lim(x,y)→(a,b) f(x,y) = L if f(x,y) → L along every path.
To show a limit does NOT exist: find two paths giving different limits.

Continuity: f is continuous at (a,b) if lim(x,y)→(a,b) f(x,y) = f(a,b).

Partial derivatives:
∂f/∂x = fₓ = lim(h→0) [f(x+h,y) − f(x,y)] / h (treat y as constant, differentiate with respect to x)
∂f/∂y = f_y = lim(h→0) [f(x,y+h) − f(x,y)] / h (treat x as constant, differentiate with respect to y)

Higher partial derivatives: fₓₓ, f_yy, fₓ_y = f_yₓ (mixed partials).
Clairaut's theorem: if fₓ_y and f_yₓ are continuous, then fₓ_y = f_yₓ.

The gradient vector: ∇f = (∂f/∂x, ∂f/∂y) = fₓ î + f_y ĵ
Points in the direction of steepest ascent. Perpendicular to level curves.

Directional derivative: D_u f(a,b) = ∇f · u (u is a unit vector in the desired direction).
Maximum rate of increase = |∇f|, in the direction of ∇f.

Tangent plane to z = f(x,y) at point (a,b,f(a,b)):
z = f(a,b) + fₓ(a,b)(x−a) + f_y(a,b)(y−b)

Chain rule for multivariable functions:
If z = f(x,y) and x = x(t), y = y(t), then dz/dt = (∂f/∂x)(dx/dt) + (∂f/∂y)(dy/dt).

## Optimization of Multivariable Functions

Critical points: where ∇f = 0 (both fₓ = 0 and f_y = 0) or a partial derivative does not exist.

Second derivative test: compute discriminant D = fₓₓ f_yy − (fₓ_y)²:
- D > 0 and fₓₓ > 0: local minimum
- D > 0 and fₓₓ < 0: local maximum
- D < 0: saddle point
- D = 0: inconclusive

Lagrange multipliers: for maximizing/minimizing f(x,y) subject to constraint g(x,y) = 0.
Solve: ∇f = λ∇g and g(x,y) = 0. The critical points are among the solutions.

## Multiple Integrals

Double integral ∬_R f(x,y) dA: volume under surface z = f(x,y) above region R.

Iterated integrals (Fubini's theorem — if f is continuous on rectangle R=[a,b]×[c,d]):
∬_R f(x,y) dA = ∫ₐᵇ ∫ᶜᵈ f(x,y) dy dx = ∫ᶜᵈ ∫ₐᵇ f(x,y) dx dy

For non-rectangular regions:
Type I (between functions of x): ∫ₐᵇ ∫_{g₁(x)}^{g₂(x)} f(x,y) dy dx
Type II (between functions of y): ∫ᶜᵈ ∫_{h₁(y)}^{h₂(y)} f(x,y) dx dy

Polar coordinates (x = r cosθ, y = r sinθ, dA = r dr dθ):
∬_R f(x,y) dA = ∫∫ f(r cosθ, r sinθ) r dr dθ
Useful for circles, rings, and regions with angular symmetry.

Triple integral ∭_E f(x,y,z) dV: integrate over a 3D region E.
Cylindrical coordinates: x = r cosθ, y = r sinθ, z = z; dV = r dz dr dθ
Spherical coordinates: x = ρ sinφ cosθ, y = ρ sinφ sinθ, z = ρ cosφ; dV = ρ² sinφ dρ dφ dθ (ρ = distance from origin, φ = polar angle from z-axis, θ = azimuthal angle)

Applications:
- Area of region: A = ∬_R 1 dA
- Volume: V = ∭_E 1 dV
- Average value: f_avg = (1/Volume) ∭_E f dV
- Mass with density ρ(x,y,z): m = ∭ ρ dV
- Center of mass: x̄ = (1/m)∭ xρ dV, ȳ = (1/m)∭ yρ dV

## Vector Calculus

Vector fields: F(x,y) = P(x,y)î + Q(x,y)ĵ; assigns a vector to each point in space.
Examples: gravitational field, electric field, velocity field of a fluid.

Line integrals:
Scalar field: ∫_C f ds = ∫ₐᵇ f(r(t)) |r'(t)| dt (arc length weighted)
Vector field: ∫_C F·dr = ∫ₐᵇ F(r(t))·r'(t) dt (work done by force F along curve C)

Conservative vector fields: F = ∇f for some scalar potential f.
Test: ∂P/∂y = ∂Q/∂x (in 2D). If conservative, ∫_C F·dr = f(end) − f(start) (path-independent).

Green's theorem: ∮_C P dx + Q dy = ∬_D (∂Q/∂x − ∂P/∂y) dA
Relates line integral around closed curve C to double integral over region D it encloses.

Divergence: div F = ∇·F = ∂P/∂x + ∂Q/∂y + ∂R/∂z. Measures source/sink strength.
Curl: curl F = ∇×F. Measures rotational tendency. (In 2D, curl F = ∂Q/∂x − ∂P/∂y.)

Stokes' theorem: ∬_S (curl F)·dS = ∮_C F·dr (generalizes Green's to surfaces in 3D)
Divergence theorem (Gauss): ∯_S F·dS = ∭_E div F dV (flux through closed surface = integral of divergence)

## Differential Equations (Introduction)

An ordinary differential equation (ODE) relates a function y(x) to its derivatives.
Order: the highest derivative appearing. Degree: power of the highest derivative.

First-order separable equations: dy/dx = f(x)g(y). Separate: dy/g(y) = f(x)dx, then integrate both sides.
Example: dy/dx = xy → dy/y = x dx → ln|y| = x²/2 + C → y = Ae^(x²/2).

First-order linear equations: dy/dx + P(x)y = Q(x).
Integrating factor: μ(x) = e^(∫P(x)dx). Multiply both sides by μ; left side becomes d/dx[μy].
Solution: y = (1/μ)∫μQ dx + C/μ.

Exact equations: M dx + N dy = 0 where ∂M/∂y = ∂N/∂x. Find f such that fₓ = M, f_y = N; solution is f(x,y) = C.

Second-order linear constant-coefficient: ay'' + by' + cy = 0.
Characteristic equation: ar² + br + c = 0. Solutions depend on discriminant Δ = b²−4ac:
- Δ > 0: two real roots r₁, r₂. General solution: y = C₁e^(r₁x) + C₂e^(r₂x).
- Δ = 0: repeated root r. General solution: y = (C₁ + C₂x)eʳˣ.
- Δ < 0: complex roots r = α ± βi. General solution: y = eᵅˣ(C₁cosβx + C₂sinβx).

Non-homogeneous: ay'' + by' + cy = g(x). General solution = homogeneous solution + particular solution.
Method of undetermined coefficients: guess the form of the particular solution based on g(x).
Variation of parameters: general method for particular solutions.

## Important Theorems Summary

Extreme Value Theorem: continuous f on [a,b] attains max and min.
Intermediate Value Theorem: continuous f on [a,b] takes all values between f(a) and f(b).
Mean Value Theorem: differentiable f on (a,b), ∃c with f'(c) = (f(b)−f(a))/(b−a).
Fundamental Theorem of Calculus: d/dx[∫ₐˣ f dt] = f(x); ∫ₐᵇ f dx = F(b)−F(a).
Fubini's Theorem: double integrals over rectangles can be evaluated as iterated integrals.
Green's, Stokes', Divergence theorems: connect integrals of different dimensions.
Taylor's theorem: smooth functions can be approximated by polynomials with controlled error.
Bolzano-Weierstrass: bounded sequence has convergent subsequence.
Heine-Cantor: continuous function on closed bounded interval is uniformly continuous.
