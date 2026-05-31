# Geometry Complete Reference

## Fundamental Concepts

A point has no size — it marks a location in space. Represented by a dot and named with a capital letter: point A.
A line extends infinitely in both directions. Determined by any two points. Line AB or ←→AB.
A line segment is part of a line with two endpoints. Segment AB has a definite length.
A ray starts at one endpoint and extends infinitely in one direction. Ray AB starts at A, goes through B and beyond.
A plane is a flat, two-dimensional surface extending infinitely. Determined by any three non-collinear points.

Collinear points: three or more points on the same line.
Coplanar points: points that lie in the same plane.
Intersection: the set of points two figures share.

Postulates (accepted without proof) vs Theorems (proven from postulates and definitions).

## Angles

An angle is formed by two rays sharing a common endpoint (vertex).
Measured in degrees (°) or radians. Full circle = 360° = 2π radians.
Conversion: degrees × (π/180) = radians; radians × (180/π) = degrees.

Types by measure:
- Acute angle: 0° < θ < 90°
- Right angle: θ = 90° (marked with a small square)
- Obtuse angle: 90° < θ < 180°
- Straight angle: θ = 180° (a straight line)
- Reflex angle: 180° < θ < 360°

Angle pairs:
- Complementary angles: sum = 90°. Example: 35° and 55°.
- Supplementary angles: sum = 180°. Example: 110° and 70°.
- Vertical angles: formed by two intersecting lines, opposite each other. Always equal.
- Adjacent angles: share a vertex and a side, no overlap.
- Linear pair: adjacent angles that form a straight line; they are supplementary.

Angles and parallel lines (cut by a transversal):
- Corresponding angles: same position at each intersection → equal.
- Alternate interior angles: between the parallel lines, opposite sides → equal.
- Alternate exterior angles: outside the parallel lines, opposite sides → equal.
- Co-interior (same-side interior / consecutive) angles: same side, between lines → supplementary (sum = 180°).

Angle bisector: a ray that divides an angle into two equal parts.
Perpendicular lines: lines that intersect at 90°. Symbol: ⊥.

## Triangles — Classification and Properties

A triangle has three sides, three vertices, and three interior angles.
Sum of interior angles of any triangle = 180°.
Exterior angle of a triangle = sum of the two non-adjacent interior angles.

Classification by sides:
- Scalene: all three sides different lengths.
- Isosceles: exactly two sides equal; base angles (opposite equal sides) are also equal.
- Equilateral: all three sides equal; all angles = 60°.

Classification by angles:
- Acute triangle: all angles < 90°.
- Right triangle: one angle = 90°. The side opposite 90° is the hypotenuse (longest side).
- Obtuse triangle: one angle > 90°.

Triangle inequality theorem: the sum of any two sides must be greater than the third side.
a + b > c, a + c > b, b + c > a.

Perimeter of a triangle: P = a + b + c
Area of a triangle: A = (1/2) × base × height = (1/2)bh
Heron's formula (when all sides known): s = (a+b+c)/2; A = √(s(s−a)(s−b)(s−c))

Medians: line segments from each vertex to the midpoint of the opposite side. Meet at the centroid (center of gravity), which divides each median in ratio 2:1 from vertex.
Altitudes: perpendicular segments from each vertex to the opposite side (or its extension). Meet at the orthocenter.
Perpendicular bisectors of sides meet at the circumcenter (center of circumscribed circle).
Angle bisectors meet at the incenter (center of inscribed circle).

Midsegment (midline): connects midpoints of two sides. Parallel to the third side and half its length.

## Congruence and Similarity

Congruent figures: same shape and same size. Symbol: ≅
Congruent triangles have equal corresponding sides and angles.

Triangle congruence theorems (postulates):
- SSS: all three pairs of sides equal → triangles congruent.
- SAS: two pairs of sides and the included angle equal → congruent.
- ASA: two pairs of angles and the included side equal → congruent.
- AAS: two pairs of angles and a non-included side equal → congruent.
- HL: hypotenuse and one leg equal in right triangles → congruent.
Note: AAA and SSA do NOT prove congruence.

Similar figures: same shape but different sizes. Symbol: ~
Corresponding angles equal; corresponding sides in the same ratio (scale factor k).

Triangle similarity:
- AA: two pairs of equal angles → similar (since the third must also match).
- SAS~: two pairs of sides in the same ratio with equal included angle → similar.
- SSS~: all three pairs of sides in the same ratio → similar.

If triangles are similar with scale factor k:
- Ratio of perimeters = k
- Ratio of areas = k²

## Pythagorean Theorem

In a right triangle with legs a, b and hypotenuse c: a² + b² = c²
Converse: if a² + b² = c² then the triangle is a right triangle.

Common Pythagorean triples (integer solutions): 3-4-5, 5-12-13, 8-15-17, 7-24-25. Multiples also work: 6-8-10, 9-12-15.

Special right triangles:
- 45°-45°-90°: legs are equal; hypotenuse = leg × √2. Sides ratio: 1 : 1 : √2.
  Example: legs = 5 → hypotenuse = 5√2.
- 30°-60°-90°: shorter leg : longer leg : hypotenuse = 1 : √3 : 2.
  Example: shorter leg = 4 → longer leg = 4√3, hypotenuse = 8.

Distance formula in 2D (from Pythagorean theorem): d = √((x₂−x₁)² + (y₂−y₁)²)
Distance in 3D: d = √((x₂−x₁)² + (y₂−y₁)² + (z₂−z₁)²)

## Trigonometry in Right Triangles

SOH-CAH-TOA (relative to angle θ, where hypotenuse is always opposite the right angle):
- sin θ = opposite / hypotenuse
- cos θ = adjacent / hypotenuse
- tan θ = opposite / adjacent = sin θ / cos θ

Reciprocal ratios:
- cosecant: csc θ = 1/sin θ = hypotenuse/opposite
- secant: sec θ = 1/cos θ = hypotenuse/adjacent
- cotangent: cot θ = 1/tan θ = adjacent/opposite

Key angle values:
- sin 0°=0, sin 30°=1/2, sin 45°=√2/2, sin 60°=√3/2, sin 90°=1
- cos 0°=1, cos 30°=√3/2, cos 45°=√2/2, cos 60°=1/2, cos 90°=0
- tan 0°=0, tan 30°=1/√3, tan 45°=1, tan 60°=√3, tan 90°=undefined

Pythagorean identity: sin²θ + cos²θ = 1 (fundamental, derives from a²+b²=c²)
Also: 1 + tan²θ = sec²θ; 1 + cot²θ = csc²θ

Law of Sines (any triangle): a/sin A = b/sin B = c/sin C
Law of Cosines (any triangle): c² = a² + b² − 2ab·cos C (generalizes Pythagorean theorem)
Area using trig: A = (1/2)ab·sin C

## Quadrilaterals

A quadrilateral has 4 sides and 4 angles. Sum of interior angles = 360°.

Parallelogram: two pairs of parallel sides.
- Opposite sides equal and parallel; opposite angles equal.
- Diagonals bisect each other.
- Area = base × height; Perimeter = 2(a+b).

Rectangle: parallelogram with all right angles.
- Diagonals equal in length and bisect each other.
- Area = length × width (A = lw); Perimeter = 2(l+w).

Rhombus: parallelogram with all sides equal.
- Diagonals bisect each other at right angles.
- Diagonals bisect the vertex angles.
- Area = (d₁ × d₂)/2 where d₁, d₂ are diagonals.

Square: rectangle AND rhombus — all sides equal, all angles 90°.
- Diagonals equal, bisect each other at 90°, and bisect the vertex angles (45° each).
- Area = s²; Perimeter = 4s; Diagonal = s√2.

Trapezoid (Trapezium in UK): exactly one pair of parallel sides (bases).
- Area = (1/2)(b₁ + b₂) × h where b₁, b₂ are the parallel bases and h is height.
- Isosceles trapezoid: non-parallel sides (legs) are equal; base angles equal; diagonals equal.
- Midsegment of trapezoid: connects midpoints of legs; length = (b₁+b₂)/2; parallel to both bases.

Kite: two pairs of consecutive equal sides (not parallel).
- Diagonals perpendicular; one diagonal bisects the other.
- Area = (d₁ × d₂)/2.

General polygon with n sides:
- Sum of interior angles = (n−2) × 180°
- Each interior angle of a regular n-gon = (n−2)×180°/n
- Sum of exterior angles (one per vertex) = always 360°
- Number of diagonals = n(n−3)/2

## Circles

Circle: set of all points equidistant from a center point. That distance = radius r.
Diameter: d = 2r (chord through center, longest chord).
Circumference: C = 2πr = πd
Area: A = πr²
π ≈ 3.14159…

Parts of a circle:
- Chord: segment connecting two points on the circle.
- Secant: a line that intersects the circle at two points.
- Tangent: a line that touches the circle at exactly one point (tangent ⊥ radius at that point).
- Arc: portion of the circle between two points.
  - Minor arc: less than semicircle (<180°).
  - Major arc: greater than semicircle (>180°).
  - Semicircle: exactly half the circle (180°).
- Sector: "pie slice" region bounded by two radii and an arc.
- Segment: region between a chord and its arc.

Arc length: L = (θ/360°) × 2πr = rθ (θ in radians)
Sector area: A = (θ/360°) × πr² = (1/2)r²θ (θ in radians)

Circle angle theorems:
- Central angle = arc it intercepts. Example: central angle 60° → arc = 60°.
- Inscribed angle = half the intercepted arc. Example: inscribed angle 30° → arc = 60°.
- Angle formed by two chords inside circle = (sum of intercepted arcs)/2.
- Angle formed by two secants from external point = (difference of arcs)/2.
- Tangent-chord angle = half the intercepted arc.

Chord theorems:
- If two chords intersect inside: (segment 1)(segment 2) = (segment 3)(segment 4).
- If two secants from external point: (outer)(whole) = (outer)(whole) for both.
- Tangent from external point: tangent² = (external segment)(whole secant).

Equation of a circle centered at (h, k) with radius r: (x−h)² + (y−k)² = r²
Standard circle (center at origin): x² + y² = r²

## Three-Dimensional Geometry (Solids)

Polyhedron: 3D solid with flat polygonal faces.
Euler's formula: Vertices − Edges + Faces = 2 (for convex polyhedra).

Prism: two congruent parallel polygonal bases connected by rectangular lateral faces.
- Volume = Base Area × Height = Bh
- Lateral surface area = Perimeter of base × Height = Ph
- Total surface area = Lateral area + 2 × Base area

Rectangular prism (cuboid / box): l×w×h
- Volume = lwh
- Surface area = 2(lw + lh + wh)
- Diagonal = √(l²+w²+h²)

Cube: all sides equal (s)
- Volume = s³
- Surface area = 6s²
- Diagonal = s√3

Cylinder: two circular bases, curved lateral surface.
- Volume = πr²h
- Lateral surface area = 2πrh
- Total surface area = 2πr² + 2πrh = 2πr(r+h)

Pyramid: polygonal base, triangular faces meeting at apex.
- Volume = (1/3) × Base Area × Height = (1/3)Bh
- Lateral surface area = (1/2) × Perimeter of base × slant height = (1/2)Pl

Cone: circular base tapering to a point (apex). Slant height l = √(r²+h²).
- Volume = (1/3)πr²h
- Lateral surface area = πrl
- Total surface area = πr² + πrl = πr(r+l)

Sphere: all points equidistant from center.
- Volume = (4/3)πr³
- Surface area = 4πr²

Hemisphere (half sphere):
- Volume = (2/3)πr³
- Total surface area = 3πr² (curved + flat circular base)

Similar solids with scale factor k:
- Ratio of surface areas = k²
- Ratio of volumes = k³

## Coordinate Geometry

The Cartesian coordinate system: x-axis (horizontal), y-axis (vertical), origin (0,0).
Four quadrants: I (+,+), II (−,+), III (−,−), IV (+,−).

Key formulas:
- Distance: d = √((x₂−x₁)² + (y₂−y₁)²)
- Midpoint: M = ((x₁+x₂)/2, (y₁+y₂)/2)
- Slope: m = (y₂−y₁)/(x₂−x₁)

Line equations:
- Slope-intercept: y = mx + b
- Point-slope: y−y₁ = m(x−x₁)
- Standard form: Ax + By = C

Parallel lines: equal slopes (m₁ = m₂).
Perpendicular lines: slopes are negative reciprocals (m₁ × m₂ = −1).

Proving geometric properties with coordinates:
- Prove sides parallel: show equal slopes.
- Prove sides perpendicular: show slopes are negative reciprocals.
- Prove sides equal: use distance formula.
- Prove diagonals bisect: show midpoints are equal.

Locus: set of all points satisfying a given condition. Example: locus equidistant from two points → perpendicular bisector of segment between them.

## Transformations

Transformations map each point of a figure to a new position.

Translation (slide): every point moves the same distance in the same direction.
(x, y) → (x+a, y+b). Preserves shape, size, and orientation. No fixed points.

Reflection (flip): mirror image over a line (line of reflection).
- Over x-axis: (x, y) → (x, −y)
- Over y-axis: (x, y) → (−x, y)
- Over y=x: (x, y) → (y, x)
- Over y=−x: (x, y) → (−y, −x)
Preserves shape and size; reverses orientation.

Rotation (turn): about a center point by an angle.
- 90° counterclockwise about origin: (x, y) → (−y, x)
- 180° about origin: (x, y) → (−x, −y)
- 270° counterclockwise (=90° clockwise): (x, y) → (y, −x)
Preserves shape, size, and orientation.

Dilation (scale): enlarges or reduces by scale factor k from a center.
(x, y) → (kx, ky) about origin. Preserves shape and angles but not size (unless k=1).
If k>1: enlargement. If 0<k<1: reduction. If k<0: also reflects.

Isometries: transformations that preserve size and shape (distance-preserving): translations, reflections, rotations.
Composition of transformations: apply one after another.
Two reflections over parallel lines = translation.
Two reflections over intersecting lines = rotation (angle = twice the angle between lines).

## Constructions and Proofs

Classical constructions use only compass and straightedge.

Key constructions:
- Bisect a segment: compass arcs from each endpoint, connect intersection points.
- Bisect an angle: compass arcs on both rays, then arc from their intersection.
- Perpendicular from a point to a line.
- Perpendicular bisector of a segment.
- Copy a line segment or angle.
- Construct parallel lines using alternate interior angles.
- Inscribe a regular hexagon in a circle.
- Inscribe a square in a circle.

Two-column proofs: statements in left column, justifications (reasons) in right.
Paragraph proofs: written in prose form.
Flowchart proofs: shows logical flow with arrows.

Common reasons used in proofs:
- Given
- Definition of (midpoint, perpendicular bisector, etc.)
- Reflexive property: any segment/angle is equal to itself. AB = AB.
- Symmetric property: if a = b then b = a.
- Transitive property: if a = b and b = c then a = c.
- Substitution property.
- Postulates and theorems (SSS, SAS, ASA, etc.).
- CPCTC: Corresponding Parts of Congruent Triangles are Congruent.

## Perimeter, Area, and Volume Summary

Perimeter and Area:
- Square (side s): P = 4s, A = s²
- Rectangle (l×w): P = 2(l+w), A = lw
- Triangle (base b, height h): A = (1/2)bh
- Parallelogram: A = bh
- Trapezoid: A = (1/2)(b₁+b₂)h
- Rhombus/Kite: A = (d₁·d₂)/2
- Circle: C = 2πr, A = πr²
- Regular polygon (n sides, side s, apothem a): A = (1/2)×perimeter×apothem = (1/2)nsa

Volume and Surface Area:
- Cube (s): V = s³, SA = 6s²
- Rectangular prism (l,w,h): V = lwh, SA = 2(lw+lh+wh)
- Cylinder (r,h): V = πr²h, SA = 2πr²+2πrh
- Pyramid (B=base area, P=perimeter, l=slant): V = (1/3)Bh, LSA = (1/2)Pl
- Cone (r,h,l=slant): V = (1/3)πr²h, SA = πr²+πrl
- Sphere (r): V = (4/3)πr³, SA = 4πr²

## Analytic and Advanced Topics

Conic sections (cross-sections of a double cone):
- Circle: (x−h)²+(y−k)² = r²
- Ellipse: (x−h)²/a² + (y−k)²/b² = 1 (a > b; a along wider axis; c² = a²−b²; foci at distance c from center)
- Parabola: y = a(x−h)²+k (opens up/down) or x = a(y−k)²+h (opens left/right); focus and directrix
- Hyperbola: (x−h)²/a² − (y−k)²/b² = 1 (opens left/right) or y version (opens up/down); c² = a²+b²

Vectors in geometry:
- Vector magnitude: |v| = √(vₓ²+vy²)
- Direction angle: θ = arctan(vy/vx)
- Vector addition: (a,b)+(c,d) = (a+c, b+d)
- Dot product: (a,b)·(c,d) = ac+bd; vectors perpendicular if dot product = 0
- Cross product (3D): gives a vector perpendicular to both

Non-Euclidean geometry basics:
- Euclidean: flat plane, parallel postulate holds. Interior angles of triangle = 180°.
- Spherical: surface of a sphere. No parallel lines; triangle angles sum > 180°.
- Hyperbolic: saddle-shaped. Multiple parallels; triangle angles sum < 180°.
