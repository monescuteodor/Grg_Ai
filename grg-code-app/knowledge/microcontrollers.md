# Microcontrollers — the whole map (all families)

Pick the family, the language, and the toolchain. Deep dives: `arduino` (AVR + arduino-cli), `esp32-iot` (WiFi/BLE). This is the umbrella for everything else.

## Families (how to choose)
- **AVR** (ATmega328 = Uno/Nano, ATtiny) — 8-bit, 5V, simple, cheap, huge community. Arduino.
- **ESP32 / ESP8266** (Espressif) — WiFi+BLE, 3.3V, cheap, IoT king. Arduino / ESP-IDF. → `esp32-iot`.
- **RP2040** (Raspberry Pi Pico / Pico W) — dual-core M0+, PIO state machines, cheap, 3.3V. Arduino / Pico SDK / **MicroPython** / CircuitPython.
- **STM32** (ARM Cortex-M0…M7) — powerful, tons of peripherals, industrial. STM32Cube/HAL, Arduino core, PlatformIO.
- **nRF52 / nRF53** (Nordic) — best-in-class BLE / Thread / Matter. Zephyr (nRF Connect SDK), Arduino.
- **SAMD21/51** (Microchip, Adafruit boards), **Teensy** (fast M7, audio/USB), **ESP32-C/S** (RISC-V/USB).
- **Raspberry Pi (Zero/3/4/5)** — a Linux SBC, NOT an MCU: run full Python/Node, GPIO via `gpiozero`/`lgpio`. Use for camera/AI/networking; use an MCU for hard-real-time I/O.
Rule of thumb: need WiFi → ESP32; need BLE/low-power → nRF52; cheap & simple → AVR/RP2040; lots of peripherals/industrial → STM32; Linux+camera → Raspberry Pi.

## Languages
- **C/C++ (Arduino or vendor SDK)** — the default; max control and performance.
- **MicroPython** — Python on the chip (RP2040, ESP32, STM32, nRF). Fast to iterate, REPL over USB. Flash the MicroPython firmware, then push `main.py`. Tools: `mpremote` (`mpremote connect COM5 fs cp main.py :`), Thonny IDE, `ampy`. Example:
  ```python
  from machine import Pin; import time
  led = Pin("LED", Pin.OUT)
  while True: led.toggle(); time.sleep(0.5)
  ```
- **CircuitPython** (Adafruit) — MicroPython fork; the board mounts as a USB drive, edit `code.py`, it reloads. Beginner-friendly, huge driver library (`adafruit_*`).
- **Rust (embedded)** — `embedded-hal`, `probe-rs` to flash, **Embassy** async framework or RTIC. Memory-safe firmware; growing fast.
- **TinyGo** — Go for microcontrollers.

## Toolchains / frameworks
- **Arduino** (arduino-cli) — easiest, cross-vendor. → see `arduino`.
- **PlatformIO** (VS Code / CLI) — multi-platform build+lib+CI manager over Arduino/ESP-IDF/STM32/etc. `pio run`, `pio run -t upload`, `pio device monitor`. Best for real projects (see `platformio-esp32` template).
- **ESP-IDF** (Espressif), **Pico SDK** (CMake for RP2040), **STM32Cube** (CubeMX generates init + HAL), **Zephyr RTOS** (`west build -b <board>`; nRF Connect SDK) — vendor/native SDKs for full control + RTOS.

## Peripherals & protocols (common across all)
GPIO (digital in/out), **ADC** (analog in), **PWM** (analog out / motors / LED dimming), **UART** (serial), **I2C** (many sensors on 2 wires), **SPI** (displays/SD, fast), **CAN** (automotive/industrial), **USB**, **BLE / WiFi / LoRa / Zigbee** (wireless), timers/interrupts, DMA. Sensors talk I2C/SPI/analog; motors use PWM + a driver (H-bridge/ESC); check the datasheet for the bus + address.

## RTOS
For many concurrent tasks use an RTOS: **FreeRTOS** (built into ESP-IDF/Arduino-ESP32; `xTaskCreate`, queues, semaphores) or **Zephyr** (modular, nRF/STM32). Otherwise a non-blocking `loop()` with `millis()` state machines is enough.

## Universal workflow & gotchas
1. Choose board → language → toolchain. 2. Wire at the RIGHT voltage (3.3V vs 5V) with a common ground. 3. Blink an LED first (proves toolchain+upload). 4. Add peripherals one at a time, verify over serial. 5. Make timing non-blocking; sleep for battery.
Gotchas: voltage mismatch, floating inputs (pull-ups), blocking delays, brown-outs from weak USB power, wrong serial baud, forgetting the bootloader/BOOT button, driving motors/LEDs off the logic supply.
