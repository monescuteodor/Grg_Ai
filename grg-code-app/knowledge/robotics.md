# Robotics — motors, servos, sensors, drive

Actuators + feedback for robots on Arduino/ESP32. For the control math see `pid-control`; for boards see `arduino` / `microcontrollers`.

## Motors & drivers (never drive a motor from a logic pin!)
A microcontroller pin gives ~20–40mA; motors need a **driver** (H-bridge) + a **separate motor supply** with a **common ground**.
- **Brushed DC** — speed by PWM, direction by an H-bridge:
  - **L298N** (cheap, lossy, ~2A), **TB6612FNG** (efficient, 1.2A/ch), **DRV8833** (small, 1.5A), **BTS7960** (big, ~40A).
  - Control = 2 direction pins + 1 PWM (enable) per motor.
- **Stepper** — precise position, no feedback needed. Drivers: **A4988 / DRV8825 / TMC2209** (STEP + DIR pins, microstepping). Use **AccelStepper** for accel/decel and multi-motor.
- **BLDC** — via an **ESC**; drive it like a servo signal (`Servo`/`ESP32Servo`, `writeMicroseconds(1000..2000)`), arm at min throttle first.
- **Servo geared motors** with encoders → closed-loop position (PID).

### DC motor with TB6612/L298N (Arduino)
```cpp
const int AIN1=7, AIN2=8, PWMA=9;   // one motor
void motor(int speed){                // speed -127..127
  bool fwd = speed >= 0; int pwm = constrain(abs(speed)*2, 0, 255);
  digitalWrite(AIN1, fwd); digitalWrite(AIN2, !fwd);
  analogWrite(PWMA, pwm);
}
void setup(){ pinMode(AIN1,OUTPUT); pinMode(AIN2,OUTPUT); pinMode(PWMA,OUTPUT); }
```
ESP32 has no `analogWrite` for motors — use LEDC: `ledcSetup(0,20000,8); ledcAttachPin(PWMA,0); ledcWrite(0,pwm);` (20kHz = silent).

## Servos (position 0–180°)
Hobby servos take a **50Hz PWM**, 1.0–2.0ms pulse = 0–180°. Use the library, not raw PWM.
```cpp
#include <Servo.h>          // ESP32: #include <ESP32Servo.h>
Servo s;
void setup(){ s.attach(6); }         // signal pin
void loop(){ s.write(90);            // angle
  // s.writeMicroseconds(1500);      // finer; 500..2500us on many servos
}
```
- **Power**: servos spike amps — use a **separate 5–6V supply**, common ground with the MCU. Never power from the board's 5V for anything but a micro servo.
- **Continuous-rotation servos**: `write(90)`=stop, `<90`/`>90` = speed/direction (they're not positional).
- Jitter? add a capacitor across servo power, keep signal wires short, avoid `delay()` starving the refresh.
- Many servos: **PCA9685** (16-ch I2C PWM driver) — ideal for robot arms/hexapods (`Adafruit_PWMServoDriver`).

## Feedback sensors
- **Quadrature encoder** (motor position/speed): two channels A/B; count edges on interrupts. Use the **Encoder** or **ESP32Encoder** lib. Speed = Δcount / Δt.
```cpp
volatile long ticks=0;
void isrA(){ ticks += digitalRead(ENC_B) ? +1 : -1; }
// attachInterrupt(digitalPinToInterrupt(ENC_A), isrA, RISING);
```
- **IMU** (MPU6050 / MPU9250, I2C): accel+gyro for tilt/heading → fuse with a complementary or Kalman filter (balancing robots).
- **IR line sensors** (analog/digital array) for line followers; **HC-SR04** ultrasonic for distance; **limit switches** for homing; **ToF (VL53L0X)** for precise range.

## Differential drive (2 wheels) — motor mixing
```cpp
void drive(int throttle, int steer){        // -127..127 each
  motorL(constrain(throttle + steer, -127, 127));
  motorR(constrain(throttle - steer, -127, 127));
}
```
`steer` typically comes from a **PID** on a line/heading error (see `pid-control`). For arms, do inverse kinematics per joint; for omni/mecanum, mix 3–4 wheels.

## Power & safety
- Motor supply separate from logic; **common ground** is mandatory. Add bulk + decoupling caps; put a diode/flyback where the driver lacks one.
- Size the battery to stall current; add a fuse and an **e-stop**/kill switch. Current-limit steppers (set Vref on A4988/DRV8825).
- Start motors at low PWM, ramp up; brake by shorting the H-bridge (both low) — do it gently.

## Checklist
Pick motor type → matching driver + separate supply + common ground → PWM/step/servo signal → add encoder/IMU feedback → close the loop with PID → mix for drive/kinematics → tune → add e-stop.
