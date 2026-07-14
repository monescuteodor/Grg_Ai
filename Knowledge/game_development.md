# Game Development Complete Reference


---

# CHAPTER 1: GAME LOOP AND ARCHITECTURE


## Remarks

Game development combines programming, math, physics, and art. The core is the game loop — a continuous cycle of input → update → render. This reference covers browser-based games (Canvas 2D, Three.js 3D) but the concepts apply to all game engines.


## The Game Loop

```javascript
// FIXED TIMESTEP game loop (professional standard)
const TICK_RATE = 60;                    // Physics updates per second
const TICK_DURATION = 1000 / TICK_RATE;  // ~16.67ms per tick

let lastTime = performance.now();
let accumulator = 0;

function gameLoop(currentTime) {
    const deltaTime = currentTime - lastTime;
    lastTime = currentTime;
    accumulator += deltaTime;

    // Process input
    handleInput();

    // Fixed timestep physics (deterministic!)
    while (accumulator >= TICK_DURATION) {
        update(TICK_DURATION / 1000);   // Update in seconds
        accumulator -= TICK_DURATION;
    }

    // Render (as fast as possible)
    const alpha = accumulator / TICK_DURATION;  // Interpolation factor
    render(alpha);

    requestAnimationFrame(gameLoop);
}
requestAnimationFrame(gameLoop);

// WHY FIXED TIMESTEP?
// Variable deltaTime: physics depends on framerate
//   60fps: ball moves 10px/frame → 600px/sec
//   30fps: ball moves 10px/frame → 300px/sec  ← WRONG!
//
// Fixed timestep: physics ALWAYS runs at 60Hz
//   60fps: 1 physics step per frame
//   30fps: 2 physics steps per frame → same result!
```


## Entity Component System (ECS)

```javascript
// Components = pure data (no logic)
class Position { constructor(x=0, y=0) { this.x = x; this.y = y; } }
class Velocity { constructor(dx=0, dy=0) { this.dx = dx; this.dy = dy; } }
class Sprite { constructor(image, w, h) { this.image = image; this.w = w; this.h = h; } }
class Health { constructor(hp=100) { this.hp = hp; this.maxHp = hp; } }
class Collider { constructor(w, h) { this.w = w; this.h = h; } }

// Entities = just IDs with components
class Entity {
    constructor(id) {
        this.id = id;
        this.components = {};
    }
    add(component) {
        this.components[component.constructor.name] = component;
        return this;
    }
    get(type) {
        return this.components[type.name];
    }
    has(type) {
        return type.name in this.components;
    }
}

// Systems = logic that operates on components
function movementSystem(entities, dt) {
    for (const entity of entities) {
        if (entity.has(Position) && entity.has(Velocity)) {
            const pos = entity.get(Position);
            const vel = entity.get(Velocity);
            pos.x += vel.dx * dt;
            pos.y += vel.dy * dt;
        }
    }
}

function collisionSystem(entities) {
    const collidable = entities.filter(e => e.has(Position) && e.has(Collider));
    for (let i = 0; i < collidable.length; i++) {
        for (let j = i + 1; j < collidable.length; j++) {
            if (aabbOverlap(collidable[i], collidable[j])) {
                handleCollision(collidable[i], collidable[j]);
            }
        }
    }
}

// Create game objects by composing components
const player = new Entity(1)
    .add(new Position(100, 200))
    .add(new Velocity(0, 0))
    .add(new Sprite(playerImg, 32, 32))
    .add(new Health(100))
    .add(new Collider(32, 32));

const bullet = new Entity(2)
    .add(new Position(100, 190))
    .add(new Velocity(0, -500))
    .add(new Collider(4, 8));
// Bullet has no Health, no Sprite needed if we draw procedurally
```


---

# CHAPTER 2: 2D GAME WITH CANVAS


## Canvas Basics

```javascript
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 600;

// Drawing primitives
ctx.fillStyle = '#ff0000';
ctx.fillRect(x, y, width, height);       // Filled rectangle

ctx.strokeStyle = '#00ff00';
ctx.strokeRect(x, y, width, height);     // Rectangle outline

ctx.beginPath();
ctx.arc(x, y, radius, 0, Math.PI * 2);  // Circle
ctx.fill();

ctx.fillStyle = 'white';
ctx.font = '24px Arial';
ctx.fillText('Score: 100', 10, 30);      // Text

// Draw image
const img = new Image();
img.src = 'player.png';
img.onload = () => {
    ctx.drawImage(img, x, y, width, height);
};

// Sprite sheet animation
function drawSprite(sheet, frameX, frameY, frameW, frameH, destX, destY) {
    ctx.drawImage(sheet,
        frameX * frameW, frameY * frameH, frameW, frameH,  // Source rect
        destX, destY, frameW, frameH                         // Dest rect
    );
}
```


## Input Handling

```javascript
// Keyboard
const keys = {};
window.addEventListener('keydown', e => { keys[e.code] = true; e.preventDefault(); });
window.addEventListener('keyup', e => { keys[e.code] = false; });

function handleInput() {
    if (keys['ArrowLeft'] || keys['KeyA'])  player.vx = -SPEED;
    else if (keys['ArrowRight'] || keys['KeyD']) player.vx = SPEED;
    else player.vx = 0;

    if (keys['Space'] && player.onGround) {
        player.vy = -JUMP_FORCE;
        player.onGround = false;
    }
}

// Mouse
let mouse = { x: 0, y: 0, down: false };
canvas.addEventListener('mousemove', e => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
});
canvas.addEventListener('mousedown', () => { mouse.down = true; });
canvas.addEventListener('mouseup', () => { mouse.down = false; });

// Touch (mobile)
canvas.addEventListener('touchstart', e => {
    e.preventDefault();
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    mouse.x = touch.clientX - rect.left;
    mouse.y = touch.clientY - rect.top;
    mouse.down = true;
});
```


---

# CHAPTER 3: 3D WITH THREE.JS


## Basic Scene

```javascript
import * as THREE from 'three';

// Scene, Camera, Renderer
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111111);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
document.body.appendChild(renderer.domElement);

// Lighting
const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 10, 5);
directionalLight.castShadow = true;
scene.add(directionalLight);

// Ground plane
const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(50, 50),
    new THREE.MeshStandardMaterial({ color: 0x228B22 })
);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// Player cube
const player = new THREE.Mesh(
    new THREE.BoxGeometry(1, 2, 1),
    new THREE.MeshStandardMaterial({ color: 0x00aaff })
);
player.position.y = 1;
player.castShadow = true;
scene.add(player);

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    
    // Update game logic
    player.rotation.y += 0.01;
    
    renderer.render(scene, camera);
}
animate();

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
```


## Physics (Simple)

```javascript
// Basic physics for platformer/racing

const GRAVITY = 20;        // m/s²
const FRICTION = 0.92;     // Velocity multiplier per frame
const TERMINAL_VEL = 50;   // Max fall speed

class PhysicsBody {
    constructor(x, y, z) {
        this.position = new THREE.Vector3(x, y, z);
        this.velocity = new THREE.Vector3(0, 0, 0);
        this.onGround = false;
    }

    update(dt) {
        // Apply gravity
        if (!this.onGround) {
            this.velocity.y -= GRAVITY * dt;
            this.velocity.y = Math.max(this.velocity.y, -TERMINAL_VEL);
        }

        // Apply friction (ground only)
        if (this.onGround) {
            this.velocity.x *= FRICTION;
            this.velocity.z *= FRICTION;
        }

        // Update position
        this.position.x += this.velocity.x * dt;
        this.position.y += this.velocity.y * dt;
        this.position.z += this.velocity.z * dt;

        // Ground collision
        if (this.position.y <= 0) {
            this.position.y = 0;
            this.velocity.y = 0;
            this.onGround = true;
        }
    }

    jump(force) {
        if (this.onGround) {
            this.velocity.y = force;
            this.onGround = false;
        }
    }
}

// AABB Collision detection
function aabbCollision(a, b) {
    return (
        a.position.x - a.size.x/2 < b.position.x + b.size.x/2 &&
        a.position.x + a.size.x/2 > b.position.x - b.size.x/2 &&
        a.position.y - a.size.y/2 < b.position.y + b.size.y/2 &&
        a.position.y + a.size.y/2 > b.position.y - b.size.y/2 &&
        a.position.z - a.size.z/2 < b.position.z + b.size.z/2 &&
        a.position.z + a.size.z/2 > b.position.z - b.size.z/2
    );
}
```


---

# CHAPTER 4: COMMON PITFALLS

```
PITFALL 1: Variable timestep physics
  Physics depends on framerate → different behavior on different machines.
  Fix: fixed timestep (accumulator pattern shown above).

PITFALL 2: Creating objects every frame
  new Vector3() in update loop → garbage collection stutter.
  Fix: pre-allocate reusable objects. Object pooling for bullets/particles.

PITFALL 3: Not using requestAnimationFrame
  setInterval(render, 16) → not synced with display refresh.
  Fix: requestAnimationFrame pauses when tab hidden, syncs with VSync.

PITFALL 4: Pixel-perfect collision with complex shapes
  Checking every pixel → extremely slow.
  Fix: use AABB (bounding box) for broad phase, precise for narrow phase.

PITFALL 5: Loading assets synchronously
  const img = new Image(); img.src = "big.png"; draw(img); → blank!
  Fix: preload all assets before game starts. Show loading screen.

PITFALL 6: Not handling window resize
  Canvas stays fixed size when window resizes → wrong aspect ratio.
  Fix: addEventListener('resize', updateCanvasSize).

PITFALL 7: Game runs too fast on powerful hardware
  No deltaTime → game speed depends on framerate.
  Fix: multiply all movement by deltaTime.
```