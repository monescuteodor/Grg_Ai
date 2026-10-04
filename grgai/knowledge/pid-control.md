# PID control

Closed-loop control: drive an **error** (setpoint − measurement) to zero. Used for motor speed/position, line following, balancing, temperature, drones, cruise. Pairs with `robotics`.

## The idea
output = **Kp·e** + **Ki·∫e dt** + **Kd·de/dt**
- **P** (proportional): react to the current error. Higher Kp = faster but oscillates.
- **I** (integral): erase steady-state error (accumulated past error). Too much = slow oscillation + windup.
- **D** (derivative): damp/anticipate (rate of change). Reduces overshoot; amplifies noise.

## Discrete implementation (what runs on an MCU)
Run at a **fixed sample time** dt. Key robustness tricks: **derivative on measurement** (not on error → no "derivative kick" on setpoint changes) and **anti-windup** (clamp the integral).
```cpp
struct PID {
  float Kp, Ki, Kd;
  float integ = 0, prevMeas = 0;
  float outMin = -255, outMax = 255;
  float compute(float setpoint, float meas, float dt){
    float error = setpoint - meas;
    integ += Ki * error * dt;                       // integral
    integ = constrain(integ, outMin, outMax);       // anti-windup clamp
    float deriv = (meas - prevMeas) / dt;           // derivative on measurement
    prevMeas = meas;
    float out = Kp*error + integ - Kd*deriv;        // note: minus, since deriv is on meas
    return constrain(out, outMin, outMax);
  }
};
```
Call it on a steady timer:
```cpp
PID pid{2.0, 0.5, 0.1};
unsigned long last=0; const float DT=0.01;   // 100 Hz
void loop(){
  if (millis() - last >= DT*1000) { last += DT*1000;
    float meas = readSpeed();                  // e.g. encoder ticks/sec
    float u = pid.compute(targetSpeed, meas, DT);
    motor((int)u);
  }
}
```

## Tuning
1. **Ki=Kd=0.** Raise **Kp** until it responds fast and *just* starts to oscillate; back off ~30%.
2. Add **Kd** to damp overshoot/oscillation (small; raise until smooth, stop before it gets jittery from noise).
3. Add **Ki** slowly to remove any steady offset; too much = slow wobble/windup.
- **Ziegler–Nichols**: find Ku (Kp where it oscillates steadily) and period Tu, then classic PID: Kp=0.6·Ku, Ki=1.2·Ku/Tu, Kd=0.075·Ku·Tu (a starting point; hand-tune after).
- Keep **dt constant**; if you change the loop rate, re-tune. Filter noisy measurements before D.

## Common uses
- **Line follower**: error = weighted position of the line under an IR array (e.g. −2..+2). `steer = pid.compute(0, error, dt)` → differential `drive(base, steer)`.
- **Motor speed**: measure with an encoder (ticks/sec), output = PWM. Position control: error in encoder counts.
- **Balancing robot / drone**: PID on tilt angle from an IMU; output to motors. Often cascaded (angle PID → rate PID).
- **Temperature**: slow plant; mostly P+I, small/no D; watch integral windup during warm-up.

## Pitfalls
- **Integral windup** (actuator saturates, integral keeps growing) → clamp it (above) or stop integrating when saturated.
- **Derivative kick** on setpoint steps → use derivative-on-measurement (above).
- **Noise** → D amplifies it; low-pass the measurement or lower Kd.
- **Non-constant dt** → jittery output; use a fixed-rate loop/timer.
- Match output limits to the actuator (PWM 0–255, servo µs, etc.). Consider a feed-forward term for fast tracking.
Libraries: **PID by Brett Beauregard** (`Arduino-PID-Library`, `QuickPID`) do all this — good default; the class above shows what they do.
