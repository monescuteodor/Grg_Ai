# Games

## Pick engine
- **Web / 2D**: HTML5 Canvas + JS, or **Phaser** (2D framework). Ship anywhere instantly.
- **Godot 4** (GDScript/C#) — free, open-source, great 2D + capable 3D, exports to desktop/mobile/web.
- **Unity** (C#) — huge ecosystem, mobile/console, steeper + licensing at scale.
- **Bevy** (Rust) — code-first ECS, modern.

## Canvas game loop
```js
const ctx = canvas.getContext('2d'); let x=0;
function loop(t){ ctx.clearRect(0,0,canvas.width,canvas.height);
  x=(x+2)%canvas.width; ctx.fillRect(x,100,30,30); requestAnimationFrame(loop); }
requestAnimationFrame(loop);
```

## Core concepts
- Fixed update vs render; delta-time movement (`v * dt`) for frame-rate independence.
- Input handling, collision (AABB/circle), sprite sheets + animation, audio.
- State machine for scenes (menu/play/gameover). Object pooling for performance.
- Save/load progress; keep assets optimized; target 60fps.
