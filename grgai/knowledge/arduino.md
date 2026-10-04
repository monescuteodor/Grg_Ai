# Arduino & embedded (C/C++)

Program microcontrollers with the Arduino framework. Boards: **Uno/Nano/Mega** (AVR, 5V), **Leonardo/Micro** (native USB), **ESP32 / ESP8266** (WiFi+BLE, 3.3V — see `esp32-iot`), **RP2040/Pico**, STM32. Language: C++ (a subset, no dynamic STL by habit).

## Sketch structure
```cpp
void setup() {            // runs once at boot
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, INPUT_PULLUP);   // button to GND, internal pull-up
}
void loop() {            // runs forever
  bool pressed = digitalRead(2) == LOW;
  digitalWrite(LED_BUILTIN, pressed ? HIGH : LOW);
}
```

## Core API
- Digital: `pinMode(pin, INPUT|OUTPUT|INPUT_PULLUP)`, `digitalRead`, `digitalWrite`.
- Analog: `analogRead(A0)` (ADC, 0–1023 on AVR / 0–4095 on ESP32), `analogWrite(pin, 0-255)` (PWM).
- Serial: `Serial.begin(baud)`, `Serial.print/println`, `Serial.available()/read()`. Match the baud in the monitor.
- Time: `millis()` / `micros()` (elapsed ms/µs), `delay(ms)` **blocks — avoid in real code**.
- Interrupts: `attachInterrupt(digitalPinToInterrupt(pin), isr, RISING|FALLING|CHANGE)`; keep ISRs tiny, mark shared vars `volatile`.
- `tone(pin, freq)` for buzzers; `map(x, in_min,in_max,out_min,out_max)`, `constrain`.

## Non-blocking timing (do this instead of delay)
```cpp
unsigned long last = 0; const unsigned long PERIOD = 500;
void loop() {
  if (millis() - last >= PERIOD) { last += PERIOD; /* toggle, sample, etc. */ }
}
```

## Buses & libraries
- **I2C**: `#include <Wire.h>`, `Wire.begin()`; many sensors (BME280, MPU6050, OLED SSD1306).
- **SPI**: `#include <SPI.h>` (displays, SD, NRF24).
- Install libraries with the IDE Library Manager or `arduino-cli lib install "Adafruit BME280 Library"`.

## Toolchain — arduino-cli (scriptable; prefer for agents)
```bash
arduino-cli core update-index
arduino-cli core install arduino:avr         # Uno/Nano/Mega ; esp32:esp32 for ESP32
arduino-cli board list                        # find the port (e.g. COM5 / /dev/ttyUSB0)
arduino-cli compile --fqbn arduino:avr:uno sketch_dir
arduino-cli upload  -p COM5 --fqbn arduino:avr:uno sketch_dir
arduino-cli monitor -p COM5 -c baudrate=115200
```
FQBN examples: `arduino:avr:uno`, `arduino:avr:nano` (old bootloader: `arduino:avr:nano:cpu=atmega328old`), `esp32:esp32:esp32`, `esp8266:esp8266:nodemcuv2`, `rp2040:rp2040:rpipico`.
A sketch folder must be named like its `.ino` (e.g. `blink/blink.ino`). **PlatformIO** is the alternative (see the `platformio-esp32` template) — better for libs/CI.

## Gotchas
- **Voltage**: AVR is 5V, ESP/Pico are **3.3V** — don't feed 5V into a 3.3V pin; level-shift.
- `delay()` freezes everything (no serial, no inputs) — use `millis()`.
- Floating inputs read noise → use `INPUT_PULLUP` or an external resistor.
- Power: motors/LEDs strips need a separate supply + common ground; don't drive from the 5V pin.
- Strings: prefer `char[]` / `F("...")` (store literals in flash) over `String` to avoid heap fragmentation.
- After upload, open the Serial Monitor at the SAME baud you set.

## Checklist
Pick board + FQBN → wire with correct voltage/ground → non-blocking `loop()` → `Serial` for debug → compile → upload → monitor → iterate.
