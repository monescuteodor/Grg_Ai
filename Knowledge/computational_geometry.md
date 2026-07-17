Advanced Computational Geometry Complete Reference
CHAPTER 1: GETTING STARTED WITH COMPUTATIONAL GEOMETRY
Remarks
Computational geometry focuses on algorithms for solving geometric problems. It is fundamental in computer graphics, robotics, GIS, CAD, and scientific computing. Key areas: Convex Hulls, Voronoi Diagrams, Delaunay Triangulation, Mesh Generation, Point Location, and Intersection Detection. Challenges: Numerical precision (floating point errors), degeneracy (collinear points), and efficiency (O(n log n) vs O(n²)).
Tools: Python (SciPy, Shapely, CGAL bindings, PyVista), C++ (CGAL, Boost.Geometry), MATLAB.
Hello Convex Hull
# hello_geom.py
"""
First geometry program: Compute the Convex Hull of a set of points.
"""
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

# Generate random points
points = np.random.rand(30, 2)

# Compute convex hull
hull = ConvexHull(points)

# Plot
plt.figure(figsize=(8, 6))
plt.plot(points[:, 0], points[:, 1], 'o', label='Points')
for simplex in hull.simplices:
    plt.plot(points[simplex, 0], points[simplex, 1], 'k-', linewidth=2)
    
# Highlight vertices
plt.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'r--', lw=2, label='Hull Boundary')
plt.title("Convex Hull of Random Points")
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()

print(f"Number of points: {len(points)}")
print(f"Hull vertices: {len(hull.vertices)}")

Geometric Primitives
# Point: (x, y) or (x, y, z)
# Line Segment: Defined by two endpoints.
# Polygon: Ordered list of vertices. Simple (no self-intersection) vs Complex.
# Circle/Sphere: Center + Radius.
# Bounding Box: Axis-Aligned (AABB) or Oriented (OBB).

CHAPTER 2: CONVEX HULL ALGORITHMS
Graham Scan
# Complexity: O(n log n) due to sorting.
# Steps:
# 1. Find the lowest point (pivot).
# 2. Sort other points by polar angle relative to pivot.
# 3. Iterate through sorted points, using a stack to remove non-left turns.

def cross_product(o, a, b):
    """Return positive if counter-clockwise, negative if clockwise, 0 if collinear."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def graham_scan(points):
    """Compute convex hull using Graham Scan."""
    if len(points) < 3:
        return points
        
    # Find pivot (lowest y, then lowest x)
    pivot = min(points, key=lambda p: (p[1], p[0]))
    
    # Sort by polar angle
    def polar_angle_key(p):
        if p == pivot:
            return (-float('inf'), 0)
        angle = np.arctan2(p[1] - pivot[1], p[0] - pivot[0])
        dist = (p[0] - pivot[0])**2 + (p[1] - pivot[1])**2
        return (angle, dist)
        
    sorted_points = sorted(points, key=polar_angle_key)
    
    # Build hull
    hull = []
    for p in sorted_points:
        while len(hull) >= 2 and cross_product(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
        
    return hull

# Example
pts = [(0,0), (1,1), (2,0), (1,2), (0.5, 0.5)]
hull_pts = graham_scan(pts)
print(f"Graham Scan Hull: {hull_pts}")

Jarvis March (Gift Wrapping)
# Complexity: O(nh), where h is number of hull vertices.
# Good for small h, bad for large h (worst case O(n²)).
# Simpler to implement than Graham Scan.

QuickHull
# Divide and conquer approach.
# Similar to QuickSort.
# Average case O(n log n), worst case O(n²).

CHAPTER 3: VORONOI DIAGRAMS & DELAUNAY TRIANGULATION
Duality
# Delaunay Triangulation and Voronoi Diagram are dual graphs.
# Vertices of Voronoi = Circumcenters of Delaunay triangles.
# Edges of Voronoi are perpendicular bisectors of Delaunay edges.

Properties of Delaunay
# Empty Circle Property: No point lies inside the circumcircle of any triangle.
# Maximizes the minimum angle: Avoids "sliver" triangles.
# Unique if no four points are cocircular.

Computing with SciPy
from scipy.spatial import Delaunay, Voronoi

points = np.random.rand(20, 2)

# Delaunay
tri = Delaunay(points)
plt.triplot(points[:, 0], points[:, 1], tri.simplices)
plt.plot(points[:, 0], points[:, 1], 'o')
plt.title("Delaunay Triangulation")
plt.show()

# Voronoi
vor = Voronoi(points)
# Plotting Voronoi requires handling infinite regions, which is more complex.
# SciPy provides vor.vertices and vor.regions.

Applications
# Voronoi: Nearest neighbor search, facility location, natural patterns (cell structures).
# Delaunay: Mesh generation for FEM, terrain modeling, interpolation.

CHAPTER 4: MESH GENERATION
Triangulation of Polygons
# Ear Clipping: O(n²). Simple but slow.
# Seidel's Algorithm: O(n log n). Complex.
# Constrained Delaunay: Respects boundary edges.

Quality Meshing
# Goal: Generate triangles with good aspect ratios.
# Ruppert's Algorithm: Refines Delaunay triangulation by inserting points at circumcenters of bad triangles.
# Delaunay Refinement: Ensures minimum angle bound.

Mesh Formats
# OBJ: Wavefront object file.
# STL: Stereolithography (triangles only).
# VTK: Visualization Toolkit format.
# MSH: Gmsh format.

Using PyVista/Gmsh
# import gmsh
# gmsh.initialize()
# gmsh.model.add("triangle")
# gmsh.model.geo.addPoint(0, 0, 0, 0.1, 1)
# ... define geometry ...
# gmsh.model.mesh.generate(2)
# gmsh.write("mesh.msh")

CHAPTER 5: POINT LOCATION & SPATIAL INDEXING
K-D Trees
# Binary space partitioning tree.
# Split space alternating between dimensions.
# Efficient for nearest neighbor search and range search.
# Build: O(n log n), Query: O(log n).

from scipy.spatial import KDTree

tree = KDTree(points)
dist, idx = tree.query([0.5, 0.5])
print(f"Nearest point to (0.5, 0.5) is index {idx} with distance {dist:.4f}")

QuadTrees / Octrees
# Recursive subdivision of space into 4 (2D) or 8 (3D) quadrants/octants.
# Used in graphics for visibility culling, collision detection.

R-Trees
# Group nearby objects using Minimum Bounding Rectangles (MBRs).
# Standard for spatial databases (PostGIS, SQLite R*Tree).
# Efficient for dynamic data (insertions/deletions).

CHAPTER 6: INTERSECTION & COLLISION DETECTION
Line Segment Intersection
# Check if two segments intersect.
# Use orientation tests (cross products).

def do_segments_intersect(p1, p2, p3, p4):
    """Check if segment p1-p2 intersects p3-p4."""
    d1 = cross_product(p3, p4, p1)
    d2 = cross_product(p3, p4, p2)
    d3 = cross_product(p1, p2, p3)
    d4 = cross_product(p1, p2, p4)
    
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    elif d1 == 0 and on_segment(p3, p4, p1): return True
    elif d2 == 0 and on_segment(p3, p4, p2): return True
    elif d3 == 0 and on_segment(p1, p2, p3): return True
    elif d4 == 0 and on_segment(p1, p2, p4): return True
    else:
        return False

def on_segment(p, q, r):
    """Check if point q lies on segment pr."""
    if (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
        min(p[1], r[1]) <= q[1] <= max(p[1], r[1])):
        return True
    return False

Bounding Volume Hierarchies (BVH)
# Accelerate collision detection for complex objects.
# Wrap objects in simple volumes (Spheres, AABBs, OBBs).
# Test volume intersections first before detailed geometry checks.

Separating Axis Theorem (SAT)
# For convex polygons/polyhedra.
# If there exists an axis where projections do not overlap, objects do not intersect.
# Axes to test: Normals of faces/edges.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Arrangements of Lines
# Decomposition of plane by a set of lines.
# Complexity: O(n²).
# Used in motion planning, visibility problems.

Minkowski Sums
# A ⊕ B = {a + b | a ∈ A, b ∈ B}
# Used for robot motion planning (configuration space obstacles).
# Convolution of shapes.

Robust Geometric Predicates
# Floating point errors cause topological inconsistencies.
# Solutions: Exact arithmetic (GMP, MPFR), Epsilon heuristics, Symbolic perturbation.
# Libraries: CGAL uses exact arithmetic internally.

Recommended Reading
# - "Computational Geometry: Algorithms and Applications" by de Berg et al.
# - "Introduction to Algorithms" (CLRS) - Chapter on Geometry.
# - CGAL Documentation: https://www.cgal.org/
# - SciPy Spatial Documentation: https://docs.scipy.org/doc/scipy/reference/spatial.html

# End of Computational Geometry Reference