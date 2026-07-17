Advanced Game Engine Architecture Complete Reference
CHAPTER 1: GETTING STARTED WITH GAME ENGINES
Remarks
A game engine is a software framework designed for the creation and development of video games. It provides core functionalities like rendering, physics, audio, input, and scripting. Modern engines (Unreal, Unity, Godot) use Component-Based or Entity-Component-System (ECS) architectures to handle complexity and performance. Key concepts: Game Loop, Resource Management, Scene Graph, ECS, Data-Oriented Design.
Tools: C++ (industry standard), Rust (emerging), OpenGL/Vulkan/DirectX (graphics), FMOD/Wwise (audio), PhysX/Bullet (physics).
Hello Game Loop
# hello_gameloop.py
"""
First engine program: The fundamental Game Loop.
"""
import time

class GameEngine:
    def __init__(self):
        self.is_running = False
        self.last_time = 0.0
        self.delta_time = 0.0
        
    def initialize(self):
        print("Engine initialized.")
        self.is_running = True
        self.last_time = time.perf_counter()
        
    def update(self):
        """Update game logic (AI, Physics, Input)."""
        pass
        
    def render(self):
        """Draw the frame."""
        pass
        
    def shutdown(self):
        print("Engine shutdown.")
        self.is_running = False
        
    def run(self):
        self.initialize()
        
        while self.is_running:
            # Calculate Delta Time
            current_time = time.perf_counter()
            self.delta_time = current_time - self.last_time
            self.last_time = current_time
            
            # Process Input
            self.process_input()
            
            # Update Logic
            self.update()
            
            # Render Frame
            self.render()
            
        self.shutdown()
        
    def process_input(self):
        pass

engine = GameEngine()
# engine.run() # Uncomment to run infinite loop

Fixed vs Variable Time Step
# Variable: Delta time varies per frame. Simple, but physics can be unstable.
# Fixed: Update logic at constant intervals (e.g., 60Hz). Stable physics, requires interpolation for rendering.

def fixed_step_loop():
    dt = 1/60.0  # 60 updates per second
    accumulator = 0.0
    
    while True:
        frame_start = time.perf_counter()
        new_time = frame_start
        
        accumulator += new_time - last_time
        last_time = new_time
        
        while accumulator >= dt:
            update(dt)  # Fixed step update
            accumulator -= dt
            
        render(accumulator / dt)  # Interpolate for smooth rendering

CHAPTER 2: ENTITY COMPONENT SYSTEM (ECS)
Architecture Overview
# Traditional OOP: Deep inheritance hierarchies (Entity -> Actor -> Character -> Enemy).
# Problems: Fragile base class, cache misses, rigid structure.
# ECS: Composition over Inheritance.
# Entity: Just an ID.
# Component: Pure data (structs).
# System: Logic that operates on entities with specific components.

import uuid

class Component:
    pass

class Position(Component):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class Velocity(Component):
    def __init__(self, vx=0.0, vy=0.0):
        self.vx = vx
        self.vy = vy

class Renderable(Component):
    def __init__(self, sprite_id):
        self.sprite_id = sprite_id

class EntityManager:
    def __init__(self):
        self.entities = {}
        self.components = {}
        
    def create_entity(self):
        eid = str(uuid.uuid4())
        self.entities[eid] = set()
        return eid
        
    def add_component(self, eid, component):
        if eid not in self.entities:
            raise ValueError("Entity does not exist")
        comp_type = type(component)
        if comp_type not in self.components:
            self.components[comp_type] = {}
        self.components[comp_type][eid] = component
        self.entities[eid].add(comp_type)
        
    def get_components(self, *types):
        """Get all entities that have ALL specified components."""
        if not types:
            return []
        
        # Find entities with first component type
        if types[0] not in self.components:
            return []
            
        candidate_eids = set(self.components[types[0]].keys())
        
        # Intersect with other component types
        for t in types[1:]:
            if t not in self.components:
                return []
            candidate_eids &= set(self.components[t].keys())
            
        # Return dict of components for each entity
        result = {}
        for eid in candidate_eids:
            comps = {}
            for t in types:
                comps[t] = self.components[t][eid]
            result[eid] = comps
            
        return result

class MovementSystem:
    def update(self, entity_manager, dt):
        # Get all entities with Position and Velocity
        entities = entity_manager.get_components(Position, Velocity)
        
        for eid, comps in entities.items():
            pos = comps[Position]
            vel = comps[Velocity]
            
            pos.x += vel.vx * dt
            pos.y += vel.vy * dt

# Usage
em = EntityManager()
e1 = em.create_entity()
em.add_component(e1, Position(0, 0))
em.add_component(e1, Velocity(10, 5))

sys = MovementSystem()
sys.update(em, 0.016) # 60 FPS

pos_comp = em.components[Position][e1]
print(f"New Position: ({pos_comp.x:.2f}, {pos_comp.y:.2f})")

Data-Oriented Design (DOD)
# Focus on data layout in memory to maximize CPU cache efficiency.
# Array of Structures (AoS) vs Structure of Arrays (SoA).
# ECS naturally leads to SoA: All Positions in one array, all Velocities in another.

CHAPTER 3: RENDERING PIPELINE
Graphics API Abstraction
# Hide backend differences (OpenGL, Vulkan, DirectX, Metal).

class GraphicsDevice:
    def __init__(self):
        self.backend = None # "OpenGL", "Vulkan", etc.
        
    def create_buffer(self, data, usage):
        pass
        
    def draw_mesh(self, mesh, material):
        pass

class Mesh:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices
        
class Material:
    def __init__(self, shader, textures):
        self.shader = shader
        self.textures = textures

Scene Graph
# Hierarchical representation of the scene.
# Transform propagation: Parent rotation/scale affects children.

class Transform:
    def __init__(self, parent=None):
        self.position = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]
        self.parent = parent
        self.children = []
        
    def get_world_matrix(self):
        # Calculate local matrix
        # Multiply by parent's world matrix if exists
        pass

Rendering Techniques
# Forward Rendering: Draw objects directly. Simple, but many lights are expensive.
# Deferred Rendering: Store geometry info in G-Buffers, then light in screen space. Good for many lights.
# PBR (Physically Based Rendering): Realistic lighting using energy conservation.

CHAPTER 4: PHYSICS ENGINE
Collision Detection
# Broad Phase: Quickly eliminate pairs that don't collide (Spatial Partitioning).
# Narrow Phase: Precise collision test between remaining pairs.

class AABB:
    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        
    def intersects(self, other):
        return not (self.max_x < other.min_x or 
                    self.min_x > other.max_x or 
                    self.max_y < other.min_y or 
                    self.min_y > other.max_y)

# Spatial Partitioning: Quadtree (2D), Octree (3D), BVH (Bounding Volume Hierarchy).

Collision Resolution
# Impulse-based resolution.
# Calculate normal, penetration depth, and apply impulses to separate objects.

def resolve_collision(body_a, body_b, normal, penetration):
    # Calculate relative velocity
    rel_vel = body_b.velocity - body_a.velocity
    
    # Velocity along normal
    vel_along_normal = rel_vel.dot(normal)
    
    # Do not resolve if velocities are separating
    if vel_along_normal > 0:
        return
        
    # Calculate restitution (bounciness)
    e = min(body_a.restitution, body_b.restitution)
    
    # Calculate impulse scalar
    j = -(1 + e) * vel_along_normal
    j /= (1/body_a.mass + 1/body_b.mass)
    
    # Apply impulse
    impulse = normal * j
    body_a.velocity -= impulse / body_a.mass
    body_b.velocity += impulse / body_b.mass

Integration Methods
# Euler: Simple, but inaccurate and unstable.
# Verlet: Better stability, good for constraints.
# Runge-Kutta (RK4): High accuracy, expensive.

CHAPTER 5: AUDIO SYSTEM
Sound Engine Basics
# Sources: Sound emitters in 3D space.
# Listener: The camera/player position.
# Mixing: Combining multiple audio streams.

class AudioSource:
    def __init__(self, clip):
        self.clip = clip
        self.position = [0, 0, 0]
        self.volume = 1.0
        self.pitch = 1.0
        self.loop = False
        
    def play(self):
        pass
        
    def stop(self):
        pass

class AudioEngine:
    def __init__(self):
        self.sources = []
        self.listener_pos = [0, 0, 0]
        
    def update(self):
        # Update 3D spatialization (Doppler, attenuation)
        for source in self.sources:
            dist = distance(source.position, self.listener_pos)
            # Apply attenuation formula
            gain = 1.0 / (1.0 + dist * 0.1)
            source.set_volume(source.volume * gain)

Audio Formats
# WAV: Uncompressed, large size.
# MP3/OGG: Compressed, smaller size, CPU overhead for decoding.
# ADPCM: Compressed, fast decoding, good for consoles.

CHAPTER 6: SCRIPTING AND MODDING
Embedding Scripting Languages
# Allow designers to define behavior without recompiling C++.
# Common choices: Lua, Python, C#.

# Example: Binding Python to C++ Engine (using pybind11 concept)
"""
// C++ Side
#include <pybind11/pybind11.h>

class GameObject {
public:
    void move(float x, float y) { ... }
};

PYBIND11_MODULE(engine, m) {
    py::class_<GameObject>(m, "GameObject")
        .def("move", &GameObject::move);
}
"""

# Python Side
# import engine
# player = engine.GameObject()
# player.move(10, 0)

Hot Reloading
# Reload scripts/assets while the game is running.
# Requires careful memory management and state preservation.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Networking for Multiplayer
# Client-Server Architecture.
# Prediction: Client predicts movement to hide latency.
# Reconciliation: Server corrects client if prediction was wrong.
# Interpolation: Smooth out other players' movements.

Asset Pipeline
# Importing raw assets (FBX, PNG) and converting to engine-specific formats.
# Compression: Texture compression (BC7, ASTC), Mesh optimization.

Profiling and Optimization
# GPU Profiling: RenderDoc, NVIDIA Nsight.
# CPU Profiling: VTune, Perf.
# Memory Profiling: Valgrind, AddressSanitizer.

Recommended Reading
# - "Game Engine Architecture" by Jason Gregory
# - "Real-Time Rendering" by Akenine-Möller et al.
# - "Physics for Game Developers" by David M. Bourg
# - Unreal Engine Source Code: https://github.com/EpicGames/UnrealEngine
# - Godot Engine Source Code: https://github.com/godotengine/godot

# End of Game Engine Architecture Reference