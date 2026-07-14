Graphics Programming & Real-Time Rendering Complete Reference
CHAPTER 1: GETTING STARTED WITH GRAPHICS PROGRAMMING
Remarks
Graphics programming involves rendering 2D/3D visuals using GPUs. The graphics pipeline transforms 3D scenes into 2D images through vertex processing, rasterization, and fragment shading. Modern APIs: OpenGL (legacy/cross-platform), Vulkan (modern/low-level), DirectX 12 (Windows), Metal (Apple). Ray tracing adds photorealistic lighting.
Tools: OpenGL/GLFW/GLAD (C++), Vulkan SDK, GLSL/HLSL (shaders), Python (PyOpenGL, moderngl), Blender (asset creation), RenderDoc (debugging).
Hello Triangle (OpenGL)
# hello_triangle.py
"""
Minimal OpenGL triangle using PyOpenGL + GLFW.
"""
import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np

# Vertex shader: transforms vertices to screen space
VERTEX_SHADER = """
#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aColor;
out vec3 vColor;

void main() {
    gl_Position = vec4(aPos, 1.0);
    vColor = aColor;
}
"""

# Fragment shader: determines pixel color
FRAGMENT_SHADER = """
#version 330 core
in vec3 vColor;
out vec4 FragColor;

void main() {
    FragColor = vec4(vColor, 1.0);
}
"""

def main():
    # Initialize GLFW
    if not glfw.init():
        return
    
    # Create window
    window = glfw.create_window(800, 600, "Hello Triangle", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    # Compile shaders
    vert = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    frag = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    program = shaders.compileProgram(vert, frag)
    
    # Triangle vertices (x, y, z, r, g, b)
    vertices = np.array([
        # Position        # Color
        -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,  # Bottom-left (red)
         0.5, -0.5, 0.0,  0.0, 1.0, 0.0,  # Bottom-right (green)
         0.0,  0.5, 0.0,  0.0, 0.0, 1.0,  # Top (blue)
    ], dtype=np.float32)
    
    # Create VAO and VBO
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    
    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # Color attribute
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    
    # Render loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        
        glUseProgram(program)
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    # Cleanup
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteProgram(program)
    glfw.terminate()

if __name__ == "__main__":
    main()

The Graphics Pipeline
# Modern GPU pipeline stages:
# 1. Vertex Shader: Transform 3D vertices → 2D screen coordinates
# 2. Primitive Assembly: Group vertices into triangles/lines/points
# 3. Rasterization: Convert primitives to fragments (pixels)
# 4. Fragment Shader: Compute color for each fragment
# 5. Tests & Blending: Depth test, stencil test, alpha blending
# 6. Framebuffer: Final image displayed on screen

# Data flow:
# 3D Model → Vertex Buffer → Vertex Shader → Rasterizer → Fragment Shader → Framebuffer → Screen

# Key concepts:
# - Vertices: Points in 3D space (x, y, z)
# - Primitives: Triangles, lines, points
# - Fragments: Potential pixels (before depth test)
# - Pixels: Final colored points on screen

CHAPTER 2: LINEAR ALGEBRA FOR GRAPHICS
Vectors and Matrices
# 3D graphics relies heavily on linear algebra.
# Vectors: position, direction, normal
# Matrices: transformations (translate, rotate, scale)

import numpy as np

class Vec3:
    """3D vector for positions, directions, normals."""
    
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x, self.y, self.z = x, y, z
    
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def dot(self, other):
        """Dot product: cos(angle) * |a| * |b|"""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        """Cross product: perpendicular vector"""
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def length(self):
        """Vector magnitude"""
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        """Unit vector (direction only)"""
        l = self.length()
        if l > 0:
            return Vec3(self.x/l, self.y/l, self.z/l)
        return Vec3()
    
    def reflect(self, normal):
        """Reflect vector across normal"""
        d = 2 * self.dot(normal)
        return Vec3(self.x - d*normal.x, self.y - d*normal.y, self.z - d*normal.z)
    
    def __repr__(self):
        return f"Vec3({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

# Example
v1 = Vec3(1, 0, 0)
v2 = Vec3(0, 1, 0)
v3 = v1.cross(v2)  # (0, 0, 1) - perpendicular to both
print(f"Cross product: {v3}")
print(f"Dot product: {v1.dot(v2)}")  # 0 (perpendicular)

class Mat4:
    """4x4 transformation matrix (column-major)."""
    
    def __init__(self):
        self.data = np.eye(4, dtype=np.float32)
    
    @staticmethod
    def identity():
        return Mat4()
    
    @staticmethod
    def translate(x, y, z):
        m = Mat4()
        m.data[0, 3] = x
        m.data[1, 3] = y
        m.data[2, 3] = z
        return m
    
    @staticmethod
    def scale(x, y, z):
        m = Mat4()
        m.data[0, 0] = x
        m.data[1, 1] = y
        m.data[2, 2] = z
        return m
    
    @staticmethod
    def rotate(angle_deg, axis):
        """Rotate around axis by angle (degrees)."""
        axis = axis.normalize()
        c = np.cos(np.radians(angle_deg))
        s = np.sin(np.radians(angle_deg))
        t = 1 - c
        
        m = Mat4()
        m.data[0, 0] = t*axis.x**2 + c
        m.data[0, 1] = t*axis.x*axis.y - s*axis.z
        m.data[0, 2] = t*axis.x*axis.z + s*axis.y
        
        m.data[1, 0] = t*axis.x*axis.y + s*axis.z
        m.data[1, 1] = t*axis.y**2 + c
        m.data[1, 2] = t*axis.y*axis.z - s*axis.x
        
        m.data[2, 0] = t*axis.x*axis.z - s*axis.y
        m.data[2, 1] = t*axis.y*axis.z + s*axis.x
        m.data[2, 2] = t*axis.z**2 + c
        
        return m
    
    @staticmethod
    def perspective(fov_deg, aspect, near, far):
        """Perspective projection matrix."""
        fov_rad = np.radians(fov_deg)
        f = 1.0 / np.tan(fov_rad / 2)
        
        m = Mat4()
        m.data[0, 0] = f / aspect
        m.data[1, 1] = f
        m.data[2, 2] = (far + near) / (near - far)
        m.data[2, 3] = (2 * far * near) / (near - far)
        m.data[3, 2] = -1
        m.data[3, 3] = 0
        return m
    
    @staticmethod
    def ortho(left, right, bottom, top, near, far):
        """Orthographic projection matrix."""
        m = Mat4()
        m.data[0, 0] = 2 / (right - left)
        m.data[1, 1] = 2 / (top - bottom)
        m.data[2, 2] = -2 / (far - near)
        m.data[0, 3] = -(right + left) / (right - left)
        m.data[1, 3] = -(top + bottom) / (top - bottom)
        m.data[2, 3] = -(far + near) / (far - near)
        return m
    
    @staticmethod
    def look_at(eye, target, up):
        """View matrix (camera transformation)."""
        f = (target - eye).normalize()  # Forward
        s = f.cross(up).normalize()     # Right
        u = s.cross(f)                  # True up
        
        m = Mat4()
        m.data[0, 0] = s.x
        m.data[0, 1] = s.y
        m.data[0, 2] = s.z
        m.data[1, 0] = u.x
        m.data[1, 1] = u.y
        m.data[1, 2] = u.z
        m.data[2, 0] = -f.x
        m.data[2, 1] = -f.y
        m.data[2, 2] = -f.z
        m.data[0, 3] = -s.dot(eye)
        m.data[1, 3] = -u.dot(eye)
        m.data[2, 3] = f.dot(eye)
        return m
    
    def __matmul__(self, other):
        """Matrix multiplication."""
        result = Mat4()
        result.data = self.data @ other.data
        return result
    
    def transform_point(self, v):
        """Transform 3D point (w=1)."""
        p = np.array([v.x, v.y, v.z, 1.0])
        r = self.data @ p
        return Vec3(r[0], r[1], r[2])
    
    def to_array(self):
        """Return column-major array for OpenGL."""
        return self.data.T.flatten()

# Example: Transform a cube
model = Mat4.translate(0, 0, -5) @ Mat4.rotate(45, Vec3(0, 1, 0)) @ Mat4.scale(1, 1, 1)
view = Mat4.look_at(Vec3(0, 0, 3), Vec3(0, 0, 0), Vec3(0, 1, 0))
proj = Mat4.perspective(45, 16/9, 0.1, 100)

mvp = proj @ view @ model
print(f"MVP matrix shape: {mvp.data.shape}")

Quaternions for Rotation
# Quaternions: avoid gimbal lock, smooth interpolation.
# q = w + xi + yj + zk (4D complex number)

class Quaternion:
    """Quaternion for 3D rotations."""
    
    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        self.w, self.x, self.y, self.z = w, x, y, z
    
    @staticmethod
    def from_axis_angle(axis, angle_deg):
        """Create quaternion from axis and angle."""
        axis = axis.normalize()
        half_rad = np.radians(angle_deg) / 2
        s = np.sin(half_rad)
        return Quaternion(np.cos(half_rad), axis.x*s, axis.y*s, axis.z*s)
    
    @staticmethod
    def from_euler(pitch, yaw, roll):
        """Create from Euler angles (degrees)."""
        p, y, r = np.radians([pitch, yaw, roll]) / 2
        
        cp, sp = np.cos(p), np.sin(p)
        cy, sy = np.cos(y), np.sin(y)
        cr, sr = np.cos(r), np.sin(r)
        
        return Quaternion(
            cr*cp*cy + sr*sp*sy,
            sr*cp*cy - cr*sp*sy,
            cr*sp*cy + sr*cp*sy,
            cr*cp*sy - sr*sp*cy
        )
    
    def __mul__(self, other):
        """Quaternion multiplication (compose rotations)."""
        return Quaternion(
            self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z,
            self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y,
            self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x,
            self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w
        )
    
    def normalize(self):
        l = np.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        return Quaternion(self.w/l, self.x/l, self.y/l, self.z/l)
    
    def to_mat4(self):
        """Convert to 4x4 rotation matrix."""
        x, y, z, w = self.x, self.y, self.z, self.w
        
        m = Mat4()
        m.data[0, 0] = 1 - 2*(y*y + z*z)
        m.data[0, 1] = 2*(x*y - w*z)
        m.data[0, 2] = 2*(x*z + w*y)
        
        m.data[1, 0] = 2*(x*y + w*z)
        m.data[1, 1] = 1 - 2*(x*x + z*z)
        m.data[1, 2] = 2*(y*z - w*x)
        
        m.data[2, 0] = 2*(x*z - w*y)
        m.data[2, 1] = 2*(y*z + w*x)
        m.data[2, 2] = 1 - 2*(x*x + y*y)
        
        return m
    
    @staticmethod
    def slerp(q1, q2, t):
        """Spherical linear interpolation (smooth rotation)."""
        dot = q1.w*q2.w + q1.x*q2.x + q1.y*q2.y + q1.z*q2.z
        
        if dot < 0:
            q2 = Quaternion(-q2.w, -q2.x, -q2.y, -q2.z)
            dot = -dot
        
        if dot > 0.9995:
            # Linear interpolation for very close quaternions
            return Quaternion(
                q1.w + t*(q2.w - q1.w),
                q1.x + t*(q2.x - q1.x),
                q1.y + t*(q2.y - q1.y),
                q1.z + t*(q2.z - q1.z)
            ).normalize()
        
        theta = np.arccos(dot)
        sin_theta = np.sin(theta)
        
        w1 = np.sin((1-t)*theta) / sin_theta
        w2 = np.sin(t*theta) / sin_theta
        
        return Quaternion(
            w1*q1.w + w2*q2.w,
            w1*q1.x + w2*q2.x,
            w1*q1.y + w2*q2.y,
            w1*q1.z + w2*q2.z
        )

# Example: Smooth rotation
q1 = Quaternion.from_axis_angle(Vec3(0, 1, 0), 0)
q2 = Quaternion.from_axis_angle(Vec3(0, 1, 0), 90)

for t in np.linspace(0, 1, 5):
    q = Quaternion.slerp(q1, q2, t)
    print(f"t={t:.2f}: {q.w:.3f} + {q.x:.3f}i + {q.y:.3f}j + {q.z:.3f}k")

CHAPTER 3: SHADER PROGRAMMING (GLSL)
Vertex Shader
// vertex.glsl
#version 330 core

// Input attributes (per-vertex data)
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aNormal;
layout(location = 2) in vec2 aTexCoord;

// Uniforms (shared across all vertices)
uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProjection;
uniform mat3 uNormalMatrix;  // Inverse transpose of model matrix

// Outputs to fragment shader
out vec3 vWorldPos;
out vec3 vNormal;
out vec2 vTexCoord;

void main() {
    // Transform position to world space
    vec4 worldPos = uModel * vec4(aPos, 1.0);
    vWorldPos = worldPos.xyz;
    
    // Transform normal to world space (use normal matrix for correctness)
    vNormal = normalize(uNormalMatrix * aNormal);
    
    // Pass texture coordinates
    vTexCoord = aTexCoord;
    
    // Transform to clip space (final position)
    gl_Position = uProjection * uView * worldPos;
}

Fragment Shader
// fragment.glsl
#version 330 core

// Inputs from vertex shader
in vec3 vWorldPos;
in vec3 vNormal;
in vec2 vTexCoord;

// Uniforms
uniform vec3 uLightPos;
uniform vec3 uViewPos;
uniform vec3 uLightColor;
uniform vec3 uObjectColor;
uniform sampler2D uTexture;
uniform bool uUseTexture;

// Output
out vec4 FragColor;

void main() {
    // Ambient lighting (constant)
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * uLightColor;
    
    // Diffuse lighting (Lambertian)
    vec3 norm = normalize(vNormal);
    vec3 lightDir = normalize(uLightPos - vWorldPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * uLightColor;
    
    // Specular lighting (Blinn-Phong)
    float specularStrength = 0.5;
    vec3 viewDir = normalize(uViewPos - vWorldPos);
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(norm, halfwayDir), 0.0), 32.0);
    vec3 specular = specularStrength * spec * uLightColor;
    
    // Combine lighting
    vec3 baseColor = uObjectColor;
    if (uUseTexture) {
        baseColor = texture(uTexture, vTexCoord).rgb;
    }
    
    vec3 result = (ambient + diffuse + specular) * baseColor;
    FragColor = vec4(result, 1.0);
}

Compute Shader
// compute.glsl (for general-purpose GPU computing)
#version 430 core

layout(local_size_x = 16, local_size_y = 16) in;

layout(rgba32f, binding = 0) uniform image2D imgOutput;
layout(binding = 1) uniform sampler2D imgInput;

uniform float uTime;
uniform int uWidth;
uniform int uHeight;

void main() {
    ivec2 pos = ivec2(gl_GlobalInvocationID.xy);
    
    if (pos.x >= uWidth || pos.y >= uHeight) {
        return;
    }
    
    // Read input pixel
    vec4 color = texelFetch(imgInput, pos, 0);
    
    // Apply effect (e.g., wave distortion)
    float wave = sin(uTime + pos.x * 0.05) * 10.0;
    ivec2 distortedPos = pos + ivec2(0, int(wave));
    
    // Clamp to bounds
    distortedPos = clamp(distortedPos, ivec2(0), ivec2(uWidth-1, uHeight-1));
    
    vec4 outputColor = texelFetch(imgInput, distortedPos, 0);
    
    // Write to output
    imageStore(imgOutput, pos, outputColor);
}

Shader Compilation in Python
def compile_shader(source, shader_type):
    """Compile a GLSL shader."""
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    
    # Check for errors
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Shader compilation error:\n{error}")
    
    return shader

def create_program(vert_src, frag_src):
    """Link vertex and fragment shaders into a program."""
    vert = compile_shader(vert_src, GL_VERTEX_SHADER)
    frag = compile_shader(frag_src, GL_FRAGMENT_SHADER)
    
    program = glCreateProgram()
    glAttachShader(program, vert)
    glAttachShader(program, frag)
    glLinkProgram(program)
    
    # Check for errors
    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program).decode()
        raise RuntimeError(f"Program linking error:\n{error}")
    
    # Shaders can be deleted after linking
    glDeleteShader(vert)
    glDeleteShader(frag)
    
    return program

# Usage
program = create_program(VERTEX_SHADER, FRAGMENT_SHADER)
glUseProgram(program)

# Set uniforms
loc_model = glGetUniformLocation(program, "uModel")
loc_view = glGetUniformLocation(program, "uView")
loc_proj = glGetUniformLocation(program, "uProjection")

glUniformMatrix4fv(loc_model, 1, GL_FALSE, model.to_array())
glUniformMatrix4fv(loc_view, 1, GL_FALSE, view.to_array())
glUniformMatrix4fv(loc_proj, 1, GL_FALSE, proj.to_array())

CHAPTER 4: MESHES AND BUFFERS
Vertex Buffer Objects (VBO)
# VBO: Store vertex data in GPU memory for fast access.
# VAO: Store vertex attribute configuration.
# EBO: Store indices for indexed drawing.

class Mesh:
    """3D mesh with vertices, normals, and indices."""
    
    def __init__(self, vertices, normals, texcoords, indices):
        self.vertex_count = len(indices)
        
        # Create VAO
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
        
        # Create VBO for vertex data (interleaved: pos, normal, texcoord)
        vertex_data = []
        for i in range(len(vertices)):
            vertex_data.extend([
                vertices[i][0], vertices[i][1], vertices[i][2],  # Position
                normals[i][0], normals[i][1], normals[i][2],     # Normal
                texcoords[i][0], texcoords[i][1]                 # TexCoord
            ])
        
        vertex_data = np.array(vertex_data, dtype=np.float32)
        
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
        
        # Position attribute (location 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # Normal attribute (location 1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        
        # TexCoord attribute (location 2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)
        
        # Create EBO for indices
        indices = np.array(indices, dtype=np.uint32)
        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
        glBindVertexArray(0)
    
    def draw(self):
        """Draw the mesh."""
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, self.vertex_count, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
    
    def cleanup(self):
        """Delete GPU resources."""
        glDeleteVertexArrays(1, [self.VAO])
        glDeleteBuffers(1, [self.VBO])
        glDeleteBuffers(1, [self.EBO])

# Example: Create a cube mesh
def create_cube():
    """Generate cube geometry."""
    # 8 vertices
    vertices = [
        (-0.5, -0.5,  0.5), ( 0.5, -0.5,  0.5), ( 0.5,  0.5,  0.5), (-0.5,  0.5,  0.5),  # Front
        (-0.5, -0.5, -0.5), ( 0.5, -0.5, -0.5), ( 0.5,  0.5, -0.5), (-0.5,  0.5, -0.5),  # Back
    ]
    
    # Normals (per face)
    normals = [
        (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1),  # Front
        (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1),  # Back
        (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0),  # Left
        (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0),  # Right
        (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0),  # Top
        (0, -1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0),  # Bottom
    ]
    
    # Texture coordinates
    texcoords = [
        (0, 0), (1, 0), (1, 1), (0, 1),  # Front
        (0, 0), (1, 0), (1, 1), (0, 1),  # Back
        (0, 0), (1, 0), (1, 1), (0, 1),  # Left
        (0, 0), (1, 0), (1, 1), (0, 1),  # Right
        (0, 0), (1, 0), (1, 1), (0, 1),  # Top
        (0, 0), (1, 0), (1, 1), (0, 1),  # Bottom
    ]
    
    # Indices (12 triangles, 36 indices)
    indices = [
        0, 1, 2, 2, 3, 0,    # Front
        4, 5, 6, 6, 7, 4,    # Back
        4, 7, 3, 3, 0, 4,    # Left
        1, 5, 6, 6, 2, 1,    # Right
        3, 2, 6, 6, 7, 3,    # Top
        4, 0, 1, 1, 5, 4,    # Bottom
    ]
    
    return Mesh(vertices, normals, texcoords, indices)

# Usage
cube = create_cube()
# In render loop:
# cube.draw()

Loading OBJ Files
def load_obj(filename):
    """Load mesh from OBJ file."""
    vertices = []
    normals = []
    texcoords = []
    faces = []
    
    with open(filename, 'r') as f:
        for line in f:
            parts = line.split()
            if not parts:
                continue
            
            if parts[0] == 'v':  # Vertex
                vertices.append([float(x) for x in parts[1:4]])
            elif parts[0] == 'vn':  # Normal
                normals.append([float(x) for x in parts[1:4]])
            elif parts[0] == 'vt':  # TexCoord
                texcoords.append([float(x) for x in parts[1:3]])
            elif parts[0] == 'f':  # Face
                face = []
                for p in parts[1:]:
                    indices = p.split('/')
                    v_idx = int(indices[0]) - 1
                    face.append(v_idx)
                faces.append(face)
    
    # Triangulate faces (convert quads to triangles)
    indices = []
    for face in faces:
        for i in range(1, len(face) - 1):
            indices.extend([face[0], face[i], face[i+1]])
    
    # Generate normals if not provided
    if not normals:
        normals = [[0, 0, 0] for _ in vertices]
        # Calculate face normals (simplified)
        for i in range(0, len(indices), 3):
            v0, v1, v2 = [vertices[idx] for idx in indices[i:i+3]]
            # Cross product
            edge1 = [v1[j] - v0[j] for j in range(3)]
            edge2 = [v2[j] - v0[j] for j in range(3)]
            normal = [
                edge1[1]*edge2[2] - edge1[2]*edge2[1],
                edge1[2]*edge2[0] - edge1[0]*edge2[2],
                edge1[0]*edge2[1] - edge1[1]*edge2[0]
            ]
            # Add to vertices
            for idx in indices[i:i+3]:
                normals[idx] = [normals[idx][j] + normal[j] for j in range(3)]
        
        # Normalize
        for i in range(len(normals)):
            length = sum(x**2 for x in normals[i])**0.5
            if length > 0:
                normals[i] = [x/length for x in normals[i]]
    
    # Default texcoords
    if not texcoords:
        texcoords = [[0, 0] for _ in vertices]
    
    return Mesh(vertices, normals, texcoords, indices)

# Usage
# mesh = load_obj("model.obj")

CHAPTER 5: TEXTURES AND MATERIALS
Texture Loading
from PIL import Image

def load_texture(filename):
    """Load texture from image file."""
    img = Image.open(filename)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL expects bottom-up
    
    # Convert to RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    img_data = np.array(img, dtype=np.uint8)
    
    # Create OpenGL texture
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # Upload texture data
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    
    return texture_id

# Usage
texture = load_texture("texture.png")

# In render loop:
glActiveTexture(GL_TEXTURE0)
glBindTexture(GL_TEXTURE_2D, texture)
glUniform1i(glGetUniformLocation(program, "uTexture"), 0)

PBR Materials (Physically Based Rendering)
// pbr_fragment.glsl
#version 330 core

in vec3 vWorldPos;
in vec3 vNormal;
in vec2 vTexCoord;

out vec4 FragColor;

// PBR material properties
uniform vec3 uAlbedo;      // Base color
uniform float uMetallic;   // 0.0 (dielectric) to 1.0 (metal)
uniform float uRoughness;  // 0.0 (smooth) to 1.0 (rough)
uniform float uAO;         // Ambient occlusion

// Light sources
uniform vec3 uLightPositions[4];
uniform vec3 uLightColors[4];

uniform vec3 uViewPos;

const float PI = 3.14159265359;

// Normal Distribution Function (GGX/Trowbridge-Reitz)
float DistributionGGX(vec3 N, vec3 H, float roughness) {
    float a = roughness * roughness;
    float a2 = a * a;
    float NdotH = max(dot(N, H), 0.0);
    float NdotH2 = NdotH * NdotH;
    
    float nom = a2;
    float denom = (NdotH2 * (a2 - 1.0) + 1.0);
    denom = PI * denom * denom;
    
    return nom / denom;
}

// Geometry Function (Schlick-GGX)
float GeometrySchlickGGX(float NdotV, float roughness) {
    float r = (roughness + 1.0);
    float k = (r * r) / 8.0;
    
    float nom = NdotV;
    float denom = NdotV * (1.0 - k) + k;
    
    return nom / denom;
}

// Geometry Smith (combines view and light directions)
float GeometrySmith(vec3 N, vec3 V, vec3 L, float roughness) {
    float NdotV = max(dot(N, V), 0.0);
    float NdotL = max(dot(N, L), 0.0);
    float ggx2 = GeometrySchlickGGX(NdotV, roughness);
    float ggx1 = GeometrySchlickGGX(NdotL, roughness);
    
    return ggx1 * ggx2;
}

// Fresnel-Schlick Approximation
vec3 fresnelSchlick(float cosTheta, vec3 F0) {
    return F0 + (1.0 - F0) * pow(clamp(1.0 - cosTheta, 0.0, 1.0), 5.0);
}

void main() {
    vec3 N = normalize(vNormal);
    vec3 V = normalize(uViewPos - vWorldPos);
    
    // Calculate reflectance at normal incidence
    // If dielectric (like plastic) use 0.04, if metal use albedo
    vec3 F0 = vec3(0.04);
    F0 = mix(F0, uAlbedo, uMetallic);
    
    // Reflectance equation
    vec3 Lo = vec3(0.0);
    
    for (int i = 0; i < 4; ++i) {
        // Calculate per-light radiance
        vec3 L = normalize(uLightPositions[i] - vWorldPos);
        vec3 H = normalize(V + L);
        float distance = length(uLightPositions[i] - vWorldPos);
        float attenuation = 1.0 / (distance * distance);
        vec3 radiance = uLightColors[i] * attenuation;
        
        // Cook-Torrance BRDF
        float NDF = DistributionGGX(N, H, uRoughness);
        float G = GeometrySmith(N, V, L, uRoughness);
        vec3 F = fresnelSchlick(max(dot(H, V), 0.0), F0);
        
        vec3 numerator = NDF * G * F;
        float denominator = 4.0 * max(dot(N, V), 0.0) * max(dot(N, L), 0.0) + 0.0001;
        vec3 specular = numerator / denominator;
        
        // kS is equal to Fresnel
        vec3 kS = F;
        // For energy conservation, diffuse and specular must not exceed 1.0
        vec3 kD = vec3(1.0) - kS;
        // Multiply by metallic to remove diffuse for metals
        kD *= 1.0 - uMetallic;
        
        // Add to outgoing radiance
        float NdotL = max(dot(N, L), 0.0);
        Lo += (kD * uAlbedo / PI + specular) * radiance * NdotL;
    }
    
    // Ambient lighting (IBL would be better)
    vec3 ambient = vec3(0.03) * uAlbedo * uAO;
    vec3 color = ambient + Lo;
    
    // HDR tone mapping (Reinhard)
    color = color / (color + vec3(1.0));
    
    // Gamma correction
    color = pow(color, vec3(1.0/2.2));
    
    FragColor = vec4(color, 1.0);
}

CHAPTER 6: LIGHTING AND SHADOWS
Shadow Mapping
// shadow_vertex.glsl
#version 330 core

layout(location = 0) in vec3 aPos;

uniform mat4 uLightSpaceMatrix;
uniform mat4 uModel;

void main() {
    gl_Position = uLightSpaceMatrix * uModel * vec4(aPos, 1.0);
}

// shadow_fragment.glsl
#version 330 core

void main() {
    // Depth is written automatically to depth buffer
    // We don't need to output color
}

// main_fragment.glsl (with shadows)
#version 330 core

in vec3 vWorldPos;
in vec3 vNormal;
in vec4 vFragPosLightSpace;

uniform sampler2D uShadowMap;
uniform vec3 uLightPos;
uniform vec3 uViewPos;

out vec4 FragColor;

float calculateShadow(vec4 fragPosLightSpace) {
    // Perform perspective divide
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    
    // Transform to [0,1] range
    projCoords = projCoords * 0.5 + 0.5;
    
    // Get closest depth value from light's perspective
    float closestDepth = texture(uShadowMap, projCoords.xy).r;
    
    // Get depth of current fragment from light's perspective
    float currentDepth = projCoords.z;
    
    // Calculate bias to avoid shadow acne
    vec3 normal = normalize(vNormal);
    vec3 lightDir = normalize(uLightPos - vWorldPos);
    float bias = max(0.05 * (1.0 - dot(normal, lightDir)), 0.005);
    
    // Check whether current frag pos is in shadow
    float shadow = currentDepth - bias > closestDepth ? 1.0 : 0.0;
    
    // PCF (Percentage Closer Filtering) for softer shadows
    shadow = 0.0;
    vec2 texelSize = 1.0 / textureSize(uShadowMap, 0);
    for (int x = -1; x <= 1; ++x) {
        for (int y = -1; y <= 1; ++y) {
            float pcfDepth = texture(uShadowMap, projCoords.xy + vec2(x, y) * texelSize).r;
            shadow += currentDepth - bias > pcfDepth ? 1.0 : 0.0;
        }
    }
    shadow /= 9.0;
    
    return shadow;
}

void main() {
    float shadow = calculateShadow(vFragPosLightSpace);
    
    vec3 norm = normalize(vNormal);
    vec3 lightDir = normalize(uLightPos - vWorldPos);
    
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = vec3(1.0, 1.0, 1.0) * diff;
    
    vec3 ambient = vec3(0.2);
    vec3 color = (ambient + diffuse * (1.0 - shadow)) * vec3(1.0, 0.5, 0.3);
    
    FragColor = vec4(color, 1.0);
}

# Shadow mapping in Python
def setup_shadow_map(width=1024, height=1024):
    """Create shadow map framebuffer."""
    # Create depth texture
    depth_map = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, depth_map)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, width, height, 0,
                 GL_DEPTH_COMPONENT, GL_FLOAT, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
    # Create framebuffer
    depth_map_fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, depth_map_fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, depth_map, 0)
    glDrawBuffer(GL_NONE)
    glReadBuffer(GL_NONE)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    return depth_map_fbo, depth_map

# Render shadow pass
def render_shadow_pass(light_space_matrix, scene, shadow_fbo, shadow_shader):
    """Render scene from light's perspective."""
    glViewport(0, 0, 1024, 1024)
    glBindFramebuffer(GL_FRAMEBUFFER, shadow_fbo)
    glClear(GL_DEPTH_BUFFER_BIT)
    
    glUseProgram(shadow_shader)
    glUniformMatrix4fv(glGetUniformLocation(shadow_shader, "uLightSpaceMatrix"),
                       1, GL_FALSE, light_space_matrix.to_array())
    
    for obj in scene.objects:
        glUniformMatrix4fv(glGetUniformLocation(shadow_shader, "uModel"),
                           1, GL_FALSE, obj.model_matrix.to_array())
        obj.mesh.draw()
    
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

CHAPTER 7: POST-PROCESSING EFFECTS
Framebuffer for Post-Processing
def setup_framebuffer(width, height):
    """Create framebuffer for post-processing."""
    # Create color texture
    color_buffer = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, color_buffer)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0,
                 GL_RGB, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # Create renderbuffer for depth
    rbo = glGenRenderbuffers(1)
    glBindRenderbuffer(GL_RENDERBUFFER, rbo)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, width, height)
    
    # Create framebuffer
    fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, color_buffer, 0)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, rbo)
    
    if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        print("Framebuffer not complete!")
    
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    return fbo, color_buffer

# Post-processing shaders
BLOOM_FRAGMENT = """
#version 330 core
in vec2 vTexCoord;
out vec4 FragColor;

uniform sampler2D uScene;
uniform sampler2D uBloomBlur;
uniform float uExposure;

void main() {
    vec3 hdrColor = texture(uScene, vTexCoord).rgb;
    vec3 bloomColor = texture(uBloomBlur, vTexCoord).rgb;
    
    // Additive blending
    hdrColor += bloomColor;
    
    // Tone mapping (Reinhard)
    vec3 result = hdrColor / (hdrColor + vec3(1.0));
    
    // Gamma correction
    result = pow(result, vec3(1.0 / 2.2));
    
    FragColor = vec4(result, 1.0);
}
"""

GAUSSIAN_BLUR_FRAGMENT = """
#version 330 core
in vec2 vTexCoord;
out vec4 FragColor;

uniform sampler2D uImage;
uniform bool uHorizontal;
uniform float uWeights[5] = float[](0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);

void main() {
    vec2 tex_offset = 1.0 / textureSize(uImage, 0);
    vec3 result = texture(uImage, vTexCoord).rgb * uWeights[0];
    
    if (uHorizontal) {
        for (int i = 1; i < 5; ++i) {
            result += texture(uImage, vTexCoord + vec2(tex_offset.x * i, 0.0)).rgb * uWeights[i];
            result += texture(uImage, vTexCoord - vec2(tex_offset.x * i, 0.0)).rgb * uWeights[i];
        }
    } else {
        for (int i = 1; i < 5; ++i) {
            result += texture(uImage, vTexCoord + vec2(0.0, tex_offset.y * i)).rgb * uWeights[i];
            result += texture(uImage, vTexCoord - vec2(0.0, tex_offset.y * i)).rgb * uWeights[i];
        }
    }
    
    FragColor = vec4(result, 1.0);
}
"""

Screen-Space Ambient Occlusion (SSAO)
// ssao_fragment.glsl
#version 330 core

in vec2 vTexCoord;
out vec4 FragColor;

uniform sampler2D uPosition;
uniform sampler2D uNormal;
uniform sampler2D uSSAONoise;
uniform vec3 uSamples[64];
uniform mat4 uProjection;

uniform int uKernelSize = 64;
uniform float uRadius = 0.5;
uniform float uBias = 0.025;

uniform vec2 uNoiseScale;

void main() {
    vec3 fragPos = texture(uPosition, vTexCoord).rgb;
    vec3 normal = normalize(texture(uNormal, vTexCoord).rgb);
    vec3 randomVec = texture(uSSAONoise, vTexCoord * uNoiseScale).xyz;
    
    // Create TBN change-of-basis matrix
    vec3 tangent = normalize(randomVec - normal * dot(randomVec, normal));
    vec3 bitangent = cross(normal, tangent);
    mat3 TBN = mat3(tangent, bitangent, normal);
    
    // Calculate occlusion
    float occlusion = 0.0;
    
    for (int i = 0; i < uKernelSize; ++i) {
        // Get sample position
        vec3 samplePos = TBN * uSamples[i];
        samplePos = fragPos + samplePos * uRadius;
        
        // Project sample to screen space
        vec4 offset = vec4(samplePos, 1.0);
        offset = uProjection * offset;
        offset.xyz /= offset.w;
        offset.xyz = offset.xyz * 0.5 + 0.5;
        
        // Get depth at sample position
        float sampleDepth = texture(uPosition, offset.xy).z;
        
        // Range check and accumulate
        float rangeCheck = smoothstep(0.0, 1.0, uRadius / abs(fragPos.z - sampleDepth));
        occlusion += (sampleDepth >= samplePos.z + uBias ? 1.0 : 0.0) * rangeCheck;
    }
    
    occlusion = 1.0 - (occlusion / uKernelSize);
    
    FragColor = vec4(vec3(occlusion), 1.0);
}

CHAPTER 8: RAY TRACING FUNDAMENTALS
Ray-Sphere Intersection
import numpy as np

class Ray:
    """Ray: origin + direction * t"""
    
    def __init__(self, origin, direction):
        self.origin = np.array(origin, dtype=np.float32)
        self.direction = np.array(direction, dtype=np.float32)
        self.direction = self.direction / np.linalg.norm(self.direction)
    
    def at(self, t):
        """Point along ray at parameter t."""
        return self.origin + t * self.direction

class Sphere:
    """Sphere for ray tracing."""
    
    def __init__(self, center, radius, color):
        self.center = np.array(center, dtype=np.float32)
        self.radius = radius
        self.color = np.array(color, dtype=np.float32)
    
    def intersect(self, ray):
        """Ray-sphere intersection. Returns t or None."""
        oc = ray.origin - self.center
        a = np.dot(ray.direction, ray.direction)
        b = 2.0 * np.dot(oc, ray.direction)
        c = np.dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return None
        
        t = (-b - np.sqrt(discriminant)) / (2.0 * a)
        if t < 0:
            t = (-b + np.sqrt(discriminant)) / (2.0 * a)
            if t < 0:
                return None
        
        return t
    
    def get_normal(self, point):
        """Get surface normal at point."""
        return (point - self.center) / self.radius

# Example
ray = Ray([0, 0, 0], [0, 0, -1])
sphere = Sphere([0, 0, -5], 1.0, [1, 0, 0])

t = sphere.intersect(ray)
if t:
    hit_point = ray.at(t)
    normal = sphere.get_normal(hit_point)
    print(f"Hit at t={t:.3f}, point={hit_point}, normal={normal}")

Ray Tracing Renderer
class RayTracer:
    """Simple ray tracer."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.spheres = []
        self.image = np.zeros((height, width, 3), dtype=np.float32)
    
    def add_sphere(self, center, radius, color):
        self.spheres.append(Sphere(center, radius, color))
    
    def trace_ray(self, ray, depth=0):
        """Trace ray and return color."""
        if depth > 5:  # Max recursion depth
            return np.array([0, 0, 0])
        
        # Find closest intersection
        closest_t = float('inf')
        closest_sphere = None
        
        for sphere in self.spheres:
            t = sphere.intersect(ray)
            if t and t < closest_t:
                closest_t = t
                closest_sphere = sphere
        
        if closest_sphere is None:
            # Background gradient
            unit_dir = ray.direction / np.linalg.norm(ray.direction)
            t = 0.5 * (unit_dir[1] + 1.0)
            return (1.0 - t) * np.array([1, 1, 1]) + t * np.array([0.5, 0.7, 1.0])
        
        # Calculate hit point and normal
        hit_point = ray.at(closest_t)
        normal = closest_sphere.get_normal(hit_point)
        
        # Simple lighting (Lambertian)
        light_dir = np.array([1, 1, -1], dtype=np.float32)
        light_dir = light_dir / np.linalg.norm(light_dir)
        
        # Shadow check
        shadow_ray = Ray(hit_point + normal * 0.001, light_dir)
        in_shadow = False
        for sphere in self.spheres:
            if sphere.intersect(shadow_ray):
                in_shadow = True
                break
        
        if in_shadow:
            return closest_sphere.color * 0.2  # Ambient only
        
        # Diffuse lighting
        diffuse = max(np.dot(normal, light_dir), 0.0)
        
        # Reflection
        reflect_dir = ray.direction - 2 * np.dot(ray.direction, normal) * normal
        reflect_ray = Ray(hit_point + normal * 0.001, reflect_dir)
        reflect_color = self.trace_ray(reflect_ray, depth + 1)
        
        # Combine
        color = closest_sphere.color * diffuse * 0.8 + reflect_color * 0.2
        
        return color
    
    def render(self, camera_pos, camera_target, fov=60):
        """Render the scene."""
        # Camera setup
        aspect_ratio = self.width / self.height
        fov_rad = np.radians(fov)
        viewport_height = 2.0 * np.tan(fov_rad / 2)
        viewport_width = aspect_ratio * viewport_height
        
        # Camera basis vectors
        forward = camera_target - camera_pos
        forward = forward / np.linalg.norm(forward)
        right = np.cross(forward, np.array([0, 1, 0]))
        right = right / np.linalg.norm(right)
        up = np.cross(right, forward)
        
        viewport_upper_left = camera_pos + forward - (viewport_width/2) * right + (viewport_height/2) * up
        pixel_delta_u = viewport_width * right / self.width
        pixel_delta_v = -viewport_height * up / self.height
        
        pixel_upper_left = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)
        
        # Render each pixel
        for j in range(self.height):
            for i in range(self.width):
                pixel_center = pixel_upper_left + i * pixel_delta_u + j * pixel_delta_v
                ray_direction = pixel_center - camera_pos
                ray = Ray(camera_pos, ray_direction)
                
                color = self.trace_ray(ray)
                self.image[j, i] = color
            
            if (j + 1) % 50 == 0:
                print(f"Rendered {j+1}/{self.height} rows")
        
        return self.image
    
    def save(self, filename):
        """Save rendered image."""
        from PIL import Image
        img = (np.clip(self.image, 0, 1) * 255).astype(np.uint8)
        Image.fromarray(img).save(filename)

# Example
tracer = RayTracer(800, 600)
tracer.add_sphere([0, 0, -5], 1.0, [0.8, 0.2, 0.2])
tracer.add_sphere([-2, 0, -6], 1.0, [0.2, 0.8, 0.2])
tracer.add_sphere([2, 0, -6], 1.0, [0.2, 0.2, 0.8])
tracer.add_sphere([0, -101, -5], 100.0, [0.8, 0.8, 0.8])  # Ground

image = tracer.render([0, 0, 0], [0, 0, -1], fov=60)
tracer.save("render.png")

CHAPTER 9: ADVANCED TECHNIQUES
Level of Detail (LOD)
class LODGroup:
    """Level of Detail for mesh optimization."""
    
    def __init__(self, meshes, distances):
        """
        meshes: list of meshes (high to low detail)
        distances: list of distances where each LOD starts
        """
        self.meshes = meshes
        self.distances = distances
    
    def get_lod(self, camera_distance):
        """Select appropriate LOD based on distance."""
        for i in range(len(self.distances) - 1, -1, -1):
            if camera_distance >= self.distances[i]:
                return self.meshes[i]
        return self.meshes[0]  # Highest detail

# Example
# lod = LODGroup(
#     meshes=[high_poly_mesh, medium_poly_mesh, low_poly_mesh],
#     distances=[0, 10, 50]  # Switch at 10m and 50m
# )

Instanced Rendering
def render_instances(mesh, instance_data, program):
    """Render multiple instances of a mesh efficiently."""
    # instance_data: array of (model_matrix, color) per instance
    
    # Create instance VBO
    instance_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, instance_vbo)
    glBufferData(GL_ARRAY_BUFFER, instance_data.nbytes, instance_data, GL_STATIC_DRAW)
    
    # Set up instance attributes (mat4 = 4 vec4 attributes)
    glBindVertexArray(mesh.VAO)
    
    # Model matrix (4 attributes)
    for i in range(4):
        loc = 3 + i  # Start at location 3
        glEnableVertexAttribArray(loc)
        glVertexAttribPointer(loc, 4, GL_FLOAT, GL_FALSE, 16 * 4,
                             ctypes.c_void_p(i * 16))
        glVertexAttribDivisor(loc, 1)  # Per-instance
    
    # Instance color
    loc = 7
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, 4, GL_FLOAT, GL_FALSE, 16 * 4,
                         ctypes.c_void_p(64))
    glVertexAttribDivisor(loc, 1)
    
    # Draw instanced
    glDrawElementsInstanced(GL_TRIANGLES, mesh.vertex_count, GL_UNSIGNED_INT,
                            None, len(instance_data))
    
    # Reset divisors
    for i in range(5):
        glVertexAttribDivisor(3 + i, 0)

# Example: Render 1000 cubes
import numpy as np

instance_data = np.zeros(1000, dtype=[
    ('model', np.float32, (4, 4)),
    ('color', np.float32, 4)
])

for i in range(1000):
    x = np.random.uniform(-50, 50)
    y = np.random.uniform(-50, 50)
    z = np.random.uniform(-50, 50)
    instance_data[i]['model'] = Mat4.translate(x, y, z).data
    instance_data[i]['color'] = [np.random.rand(), np.random.rand(), np.random.rand(), 1.0]

# render_instances(cube_mesh, instance_data, program)

Deferred Rendering
// gbuffer_vertex.glsl
#version 330 core

layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aNormal;
layout(location = 2) in vec2 aTexCoord;

uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProjection;

out vec3 vWorldPos;
out vec3 vNormal;
out vec2 vTexCoord;

void main() {
    vec4 worldPos = uModel * vec4(aPos, 1.0);
    vWorldPos = worldPos.xyz;
    vNormal = mat3(transpose(inverse(uModel))) * aNormal;
    vTexCoord = aTexCoord;
    gl_Position = uProjection * uView * worldPos;
}

// gbuffer_fragment.glsl (Geometry Buffer)
#version 330 core

in vec3 vWorldPos;
in vec3 vNormal;
in vec2 vTexCoord;

layout(location = 0) out vec3 gPosition;
layout(location = 1) out vec3 gNormal;
layout(location = 2) out vec4 gAlbedoSpec;

uniform sampler2D uAlbedoTexture;
uniform float uMetallic;
uniform float uRoughness;

void main() {
    gPosition = vWorldPos;
    gNormal = normalize(vNormal);
    gAlbedoSpec.rgb = texture(uAlbedoTexture, vTexCoord).rgb;
    gAlbedoSpec.a = uMetallic;  // Store metallic in alpha
}

// deferred_lighting_fragment.glsl
#version 330 core

in vec2 vTexCoord;
out vec4 FragColor;

uniform sampler2D gPosition;
uniform sampler2D gNormal;
uniform sampler2D gAlbedoSpec;

uniform vec3 uViewPos;
uniform vec3 uLightPositions[4];
uniform vec3 uLightColors[4];

void main() {
    vec3 fragPos = texture(gPosition, vTexCoord).rgb;
    vec3 normal = texture(gNormal, vTexCoord).rgb;
    vec3 albedo = texture(gAlbedoSpec, vTexCoord).rgb;
    float metallic = texture(gAlbedoSpec, vTexCoord).a;
    
    vec3 lighting = albedo * 0.1;  // Ambient
    
    vec3 viewDir = normalize(uViewPos - fragPos);
    
    for (int i = 0; i < 4; ++i) {
        vec3 lightDir = normalize(uLightPositions[i] - fragPos);
        float distance = length(uLightPositions[i] - fragPos);
        float attenuation = 1.0 / (distance * distance);
        
        vec3 diffuse = max(dot(normal, lightDir), 0.0) * albedo;
        vec3 reflectDir = reflect(-lightDir, normal);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
        vec3 specular = vec3(0.3) * spec;
        
        lighting += (diffuse + specular) * uLightColors[i] * attenuation;
    }
    
    FragColor = vec4(lighting, 1.0);
}

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Vulkan Basics
# Vulkan: Modern low-level graphics API.
# Explicit control over GPU resources.
# More complex than OpenGL but better performance.

# Key concepts:
# - Instance: Vulkan runtime
# - Physical device: GPU
# - Logical device: Application's interface to GPU
# - Queue: Command submission
# - Command buffer: Recorded commands
# - Pipeline: Shader + state configuration
# - Descriptor set: Shader resource bindings

# Vulkan initialization (C++ pseudocode):
"""
// 1. Create instance
VkInstanceCreateInfo instanceInfo = {};
instanceInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
vkCreateInstance(&instanceInfo, nullptr, &instance);

// 2. Select physical device (GPU)
VkPhysicalDevice physicalDevice;
vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr);
vkEnumeratePhysicalDevices(instance, &deviceCount, &physicalDevice);

// 3. Create logical device
VkDeviceCreateInfo deviceInfo = {};
deviceInfo.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
vkCreateDevice(physicalDevice, &deviceInfo, nullptr, &device);

// 4. Create swapchain (for window presentation)
VkSwapchainCreateInfoKHR swapchainInfo = {};
swapchainInfo.sType = VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR;
vkCreateSwapchainKHR(device, &swapchainInfo, nullptr, &swapchain);

// 5. Create graphics pipeline
VkGraphicsPipelineCreateInfo pipelineInfo = {};
pipelineInfo.sType = VK_STRUCTURE_TYPE_GRAPHICS_PIPELINE_CREATE_INFO;
// ... configure shaders, vertex input, rasterization, etc.
vkCreateGraphicsPipelines(device, pipelineCache, 1, &pipelineInfo, nullptr, &pipeline);

// 6. Record command buffer
VkCommandBufferBeginInfo beginInfo = {};
beginInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
vkBeginCommandBuffer(commandBuffer, &beginInfo);

vkCmdBindPipeline(commandBuffer, VK_PIPELINE_BIND_POINT_GRAPHICS, pipeline);
vkCmdDraw(commandBuffer, vertexCount, instanceCount, firstVertex, firstInstance);

vkEndCommandBuffer(commandBuffer);

// 7. Submit and present
vkQueueSubmit(queue, 1, &submitInfo, fence);
vkQueuePresentKHR(presentQueue, &presentInfo);
"""

Performance Optimization
# Key techniques:
# 1. Batch rendering: Minimize state changes
# 2. Frustum culling: Don't render objects outside view
# 3. Occlusion culling: Don't render hidden objects
# 4. LOD: Use simpler meshes for distant objects
# 5. Instancing: Render multiple copies efficiently
# 6. Texture atlasing: Combine textures to reduce draw calls
# 7. Mipmapping: Use smaller textures for distant objects
# 8. Compression: Compress textures (BC/DXT, ASTC, ETC2)

# Example: Frustum culling
def frustum_culling(objects, camera):
    """Remove objects outside camera frustum."""
    visible = []
    
    for obj in objects:
        # Simple sphere-based culling
        distance = np.linalg.norm(obj.center - camera.position)
        if distance - obj.radius < camera.far_plane:
            # Check if in view cone
            direction = obj.center - camera.position
            direction = direction / np.linalg.norm(direction)
            angle = np.arccos(np.dot(direction, camera.forward))
            
            if angle < camera.fov / 2 + obj.radius / distance:
                visible.append(obj)
    
    return visible

# GPU Profiling
# Tools:
# - RenderDoc: Frame debugger (OpenGL, Vulkan, D3D)
# - NVIDIA Nsight Graphics: GPU profiling
# - AMD Radeon GPU Profiler: AMD GPU profiling
# - Intel GPA: Intel GPU profiling

# Metrics to monitor:
# - Frame time (ms)
# - Draw calls
# - Triangle count
# - Overdraw
# - Texture memory
# - GPU utilization
# - CPU-GPU sync points

Recommended Reading
# - "Real-Time Rendering" by Akenine-Möller et al.
# - "GPU Gems" series (NVIDIA)
# - "The Book of Shaders" by Patricio Gonzalez Vivo (free online)
# - "Learn OpenGL" by Joey de Vries (free online)
# - "Vulkan Programming Guide" by Sellers et al.
# - "Physically Based Rendering" by Pharr et al. (free online)

# Online Resources
# - ShaderToy: https://www.shadertoy.com/ (shader examples)
# - LearnOpenGL: https://learnopengl.com/
# - Vulkan Tutorial: https://vulkan-tutorial.com/
# - GPUOpen: https://gpuopen.com/ (AMD resources)
# - NVIDIA Developer: https://developer.nvidia.com/

# End of Graphics Programming Reference