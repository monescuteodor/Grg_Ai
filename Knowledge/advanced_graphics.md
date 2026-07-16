Advanced Computer Graphics & Physically Based Rendering Complete Reference
CHAPTER 1: GETTING STARTED WITH ADVANCED GRAPHICS
Remarks
Advanced computer graphics focuses on photorealistic rendering, global illumination, and physically accurate light simulation. Key concepts: Ray Tracing (whitted-style), Path Tracing (Monte Carlo integration), Radiometry (light measurement), BRDFs (material models), Importance Sampling, Denoising. Modern APIs: Vulkan RT, DirectX Raytracing (DXR), OptiX. Used in: Film VFX, AAA Games, Architectural Visualization, Product Design.
Tools: C++ (performance), GLSL/HLSL (shaders), Python (prototyping), Blender/Cycles (reference implementation), NVIDIA OptiX, Intel Embree (ray traversal).
Hello Ray Tracing
# hello_raytracer.py
"""
Minimal CPU ray tracer: renders a sphere with shadows.
"""
import numpy as np
import matplotlib.pyplot as plt

class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z
    
    def __add__(self, other): return Vec3(self.x+other.x, self.y+other.y, self.z+other.z)
    def __sub__(self, other): return Vec3(self.x-other.x, self.y-other.y, self.z-other.z)
    def __mul__(self, t): return Vec3(self.x*t, self.y*t, self.z*t)
    def dot(self, other): return self.x*other.x + self.y*other.y + self.z*other.z
    def norm(self): return np.sqrt(self.dot(self))
    def normalized(self):
        n = self.norm()
        return Vec3(self.x/n, self.y/n, self.z/n) if n > 0 else Vec3()

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalized()
    
    def at(self, t):
        return self.origin + self.direction * t

class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color # Vec3
    
    def hit(self, ray, t_min=0.001, t_max=np.inf):
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius**2
        discriminant = b*b - 4*a*c
        
        if discriminant < 0:
            return None
        
        sqrt_disc = np.sqrt(discriminant)
        root = (-b - sqrt_disc) / (2*a)
        
        if root < t_min or root > t_max:
            root = (-b + sqrt_disc) / (2*a)
            if root < t_min or root > t_max:
                return None
        
        point = ray.at(root)
        normal = (point - self.center) / self.radius
        return {'t': root, 'point': point, 'normal': normal, 'color': self.color}

def trace_ray(ray, objects, light_pos, depth=0):
    if depth > 3:
        return Vec3(0, 0, 0)
    
    closest_hit = None
    min_t = np.inf
    
    for obj in objects:
        hit = obj.hit(ray)
        if hit and hit['t'] < min_t:
            min_t = hit['t']
            closest_hit = hit
    
    if not closest_hit:
        # Sky gradient
        t = 0.5 * (ray.direction.y + 1.0)
        return Vec3(1,1,1)*(1-t) + Vec3(0.5, 0.7, 1.0)*t
    
    # Lighting calculation (Lambertian diffuse + Shadow)
    light_dir = (light_pos - closest_hit['point']).normalized()
    
    # Shadow ray
    shadow_ray = Ray(closest_hit['point'] + closest_hit['normal']*0.001, light_dir)
    in_shadow = False
    for obj in objects:
        if obj.hit(shadow_ray, 0.001, np.inf):
            in_shadow = True
            break
    
    if in_shadow:
        return closest_hit['color'] * 0.1 # Ambient only
    
    # Diffuse
    diff = max(closest_hit['normal'].dot(light_dir), 0)
    return closest_hit['color'] * diff

# Scene setup
width, height = 400, 300
image = np.zeros((height, width, 3))

objects = [
    Sphere(Vec3(0, 0, -3), 1.0, Vec3(0.8, 0.2, 0.2)), # Red sphere
    Sphere(Vec3(-2, 0, -4), 1.0, Vec3(0.2, 0.8, 0.2)), # Green sphere
    Sphere(Vec3(2, 0, -4), 1.0, Vec3(0.2, 0.2, 0.8)), # Blue sphere
]
light_pos = Vec3(5, 5, -5)

camera_pos = Vec3(0, 0, 0)

print("Rendering...")
for y in range(height):
    for x in range(width):
        # Normalized device coordinates
        u = (x / width) * 2 - 1
        v = -(y / height) * 2 + 1
        
        # Ray direction (simple pinhole camera)
        direction = Vec3(u, v, -1)
        ray = Ray(camera_pos, direction)
        
        color = trace_ray(ray, objects, light_pos)
        image[y, x] = [color.x, color.y, color.z]

plt.imshow(image)
plt.axis('off')
plt.title("Simple Ray Tracer with Shadows")
plt.show()

Radiometry Basics
# Radiometric quantities:
# 1. Radiant Energy (Q): Joules
# 2. Radiant Flux (Power, Φ): Watts (J/s)
# 3. Irradiance (E): W/m² (incident power per area)
# 4. Radiance (L): W/(m²·sr) (power per projected area per solid angle)
#    - This is what cameras measure and what we simulate in rendering.

# Solid Angle (Ω): Area on unit sphere (steradians)
# dΩ = sin(θ) dθ dφ

# Cosine Law (Lambert's Cosine Law):
# Apparent brightness of a surface falls off as cos(θ) where θ is angle between normal and view/light direction.

CHAPTER 2: MONTE CARLO INTEGRATION
Monte Carlo Estimator
# Rendering Equation is an integral over the hemisphere.
# I = ∫ f(x) dx ≈ (1/N) Σ f(xi) / p(xi)
# where xi are samples drawn from PDF p(x)

import numpy as np

def estimate_pi_mc(N=100000):
    """Estimate Pi using Monte Carlo dart throwing."""
    points_inside = 0
    for _ in range(N):
        x, y = np.random.uniform(-1, 1), np.random.uniform(-1, 1)
        if x*x + y*y <= 1:
            points_inside += 1
    return 4 * points_inside / N

print(f"Pi Estimate (N={100000}): {estimate_pi_mc()}")

Importance Sampling
# Reduce variance by sampling more frequently where the function contributes most.
# For rendering: sample light sources or BRDF lobes proportionally to their intensity.

def importance_sample_cosine_hemisphere(N=1000):
    """Generate directions biased towards the normal (cosine weighted)."""
    directions = []
    for _ in range(N):
        # Uniform random numbers
        r1, r2 = np.random.random(), np.random.random()
        
        # Cosine-weighted hemisphere sampling
        phi = 2 * np.pi * r1
        r_sq = r2
        x = np.cos(phi) * np.sqrt(r_sq)
        y = np.sin(phi) * np.sqrt(r_sq)
        z = np.sqrt(1 - r_sq) # Cosine term implicitly handled
        
        directions.append(np.array([x, y, z]))
    return np.array(directions)

# Visualize distribution
dirs = importance_sample_cosine_hemisphere(5000)
plt.figure(figsize=(6,6))
plt.scatter(dirs[:,0], dirs[:,1], s=1, alpha=0.5)
plt.title("Cosine-Weighted Hemisphere Projection")
plt.axis('equal')
plt.show()

Stratified Sampling
# Divide domain into strata (buckets) and sample once per stratum.
# Reduces clumping and improves convergence compared to pure random.

def stratified_samples(n_strata):
    samples = []
    stride = 1.0 / n_strata
    for i in range(n_strata):
        # Random offset within the stratum
        sample = (i + np.random.random()) * stride
        samples.append(sample)
    return samples

print("Pure Random:", sorted([np.random.random() for _ in range(10)]))
print("Stratified: ", sorted(stratified_samples(10)))

CHAPTER 3: LIGHT TRANSPORT & MATERIALS
The Rendering Equation
# Kajiya (1986):
# Lo(x, ωo) = Le(x, ωo) + ∫Ω fr(x, ωi, ωo) Li(x, ωi) (n·ωi) dωi
# Lo: Outgoing radiance
# Le: Emitted radiance
# fr: BRDF (Bidirectional Reflectance Distribution Function)
# Li: Incoming radiance
# n·ωi: Cosine foreshortening term

BRDF Models
# 1. Lambertian (Diffuse):
#    fr = kd / π
#    Perfectly matte surface. Energy conserved if kd <= 1.

# 2. Phong/Blinn-Phong (Specular):
#    Empirical model. Not energy conserving by default.
#    Blinn-Phong uses Halfway vector H = normalize(ωi + ωo)
#    Specular = ks * (n·H)^shininess

# 3. Microfacet Models (GGX/Trowbridge-Reitz):
#    Physically based. Assumes surface is made of tiny mirrors.
#    D(h): Normal Distribution Function (NDF) - how many microfacets align with h.
#    G(l,v): Geometry Function (Shadowing/Masking).
#    F(v): Fresnel Effect (reflectivity at grazing angles).

def ggx_ndf(n_dot_h, alpha):
    """Trowbridge-Reitz GGX Normal Distribution Function."""
    a_sq = alpha * alpha
    denom = (n_dot_h * n_dot_h) * (a_sq - 1) + 1
    return a_sq / (np.pi * denom * denom)

def schlick_fresnel(cos_theta, f0):
    """Schlick approximation for Fresnel effect."""
    return f0 + (1 - f0) * (1 - cos_theta)**5

# Example: Plotting GGX NDF for different roughness
alphas = [0.1, 0.3, 0.5, 0.9] # Roughness
n_dot_h = np.linspace(0, 1, 100)

plt.figure()
for a in alphas:
    plt.plot(n_dot_h, ggx_ndf(n_dot_h, a), label=f'Roughness={a}')
plt.title("GGX Normal Distribution Function")
plt.xlabel("N · H")
plt.ylabel("D(h)")
plt.legend()
plt.grid(True)
plt.show()

Fresnel Effect
# Light reflects more at grazing angles.
# Conductors (metals) have high F0 (base reflectivity).
# Dielectrics (plastic, wood) have low F0 (~0.04).
# Crucial for realistic PBR materials.

CHAPTER 4: PATH TRACING
Basic Path Tracer
# Unbiased global illumination.
# Trace random paths from camera, bounce around scene, accumulate light.

class PathTracer:
    def __init__(self, width, height, samples_per_pixel):
        self.width = width
        self.height = height
        self.spp = samples_per_pixel
        self.image = np.zeros((height, width, 3))
        
    def render(self, scene):
        for y in range(self.height):
            for x in range(self.width):
                color = Vec3(0,0,0)
                for s in range(self.spp):
                    # Jitter pixel coordinate for anti-aliasing
                    u = (x + np.random.random()) / self.width
                    v = (y + np.random.random()) / self.height
                    
                    ray = scene.camera.get_ray(u, v)
                    color += self.trace(ray, scene, depth=0)
                
                self.image[y, x] = color / self.spp
            
            if y % 10 == 0: print(f"Row {y}/{self.height}")

    def trace(self, ray, scene, depth, max_depth=5):
        if depth > max_depth:
            return Vec3(0,0,0)
            
        hit = scene.intersect(ray)
        if not hit:
            return Vec3(0,0,0) # Or sky color
            
        # Russian Roulette termination could go here
        
        # Sample new direction based on material
        # For now, simple diffuse bounce
        target = hit.point + hit.normal + random_in_unit_sphere()
        new_dir = (target - hit.point).normalized()
        
        incoming = self.trace(Ray(hit.point, new_dir), scene, depth+1)
        
        return hit.material.albedo * incoming # Simplified

    def random_in_unit_sphere():
        while True:
            p = Vec3(np.random.uniform(-1,1), np.random.uniform(-1,1), np.random.uniform(-1,1))
            if p.norm() < 1: return p

# Note: Full implementation requires robust BVH acceleration structure.

Acceleration Structures (BVH)
# Bounding Volume Hierarchy.
# Binary tree of AABBs (Axis-Aligned Bounding Boxes).
# Reduces intersection tests from O(N) to O(log N).

class AABB:
    def __init__(self, min_pt, max_pt):
        self.min = min_pt
        self.max = max_pt
    
    def hit(self, ray, t_min, t_max):
        for i in range(3):
            inv_d = 1.0 / ray.direction[i] # Component-wise
            t0 = (self.min[i] - ray.origin[i]) * inv_d
            t1 = (self.max[i] - ray.origin[i]) * inv_d
            if inv_d < 0: t0, t1 = t1, t0
            t_min = max(t0, t_min)
            t_max = min(t1, t_max)
            if t_max <= t_min: return False
        return True

class BVHNode:
    def __init__(self, left, right, bbox):
        self.left = left
        self.right = right
        self.bbox = bbox
    
    def hit(self, ray, t_min, t_max):
        if not self.bbox.hit(ray, t_min, t_max):
            return None
        
        hit_left = self.left.hit(ray, t_min, t_max) if self.left else None
        hit_right = self.right.hit(ray, t_min, t_max) if self.right else None
        
        if hit_left and hit_right:
            return hit_left if hit_left.t < hit_right.t else hit_right
        elif hit_left:
            return hit_left
        else:
            return hit_right

CHAPTER 5: MODERN REAL-TIME RAY TRACING
Hybrid Rendering
# Rasterization for primary visibility (fast).
# Ray Tracing for secondary effects:
# - Reflections
# - Shadows
# - Global Illumination (GI)
# - Ambient Occlusion

DXR / Vulkan RT Pipeline
# 1. Acceleration Structure Build (Top-Level & Bottom-Level AS)
# 2. Ray Generation Shader (Launch rays)
# 3. Intersection Shader (Custom geometry) or Triangle Intersection
# 4. Any-Hit Shader (Alpha testing, decals)
# 5. Closest-Hit Shader (Shading)
# 6. Miss Shader (Skybox, fog)

Denoising
# Path tracing produces noisy images at low sample counts.
# AI Denoisers: NVIDIA OptiX Denoiser, Intel Open Image Denoise (OIDN).
# Inputs: Albedo, Normal, Depth, Variance.
# Technique: Temporal accumulation + Spatial filtering.

CHAPTER 6: ADVANCED TOPICS
Subsurface Scattering (SSS)
# Light enters surface, scatters internally, exits at different point.
# Materials: Skin, Wax, Milk, Marble.
# Approximation: Screen-space blur, Pre-integrated skin shading.

Volumetric Rendering
# Participating media: Fog, Smoke, Fire.
# Beer-Lambert Law: Transmission T = exp(-σt * distance)
# In-scattering: Light added along the ray path.
# Method: Ray marching through density field.

Caustics
# Focused light patterns formed by refraction/reflection.
# Hard for standard path tracing (rare samples).
# Solutions: Photon Mapping, Bidirectional Path Tracing (BDPT), Manifold Exploration.

Recommended Reading
# - "Physically Based Rendering: From Theory To Implementation" (Pharr, Jakob, Humphreys)
# - "Real-Time Rendering" (Akenine-Möller et al.)
# - Ray Tracing in One Weekend Series (Peter Shirley)
# - SIGGRAPH Course Notes (Advances in Real-Time Ray Tracing)

# End of Advanced Computer Graphics Reference