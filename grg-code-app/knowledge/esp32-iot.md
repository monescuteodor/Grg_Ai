# ESP32 / ESP8266 — WiFi & IoT

Espressif SoCs run the Arduino framework or **ESP-IDF** (native, FreeRTOS). **3.3V logic.** Great for IoT: WiFi, BLE (ESP32), deep sleep, OTA. FQBN: `esp32:esp32:esp32`, `esp8266:esp8266:nodemcuv2`. Install core: `arduino-cli core install esp32:esp32` (board URL `https://espressif.github.io/arduino-esp32/package_esp32_index.json`).

## WiFi + web server + sensor (Arduino framework)
```cpp
#include <WiFi.h>          // <ESP8266WiFi.h> on ESP8266
#include <WebServer.h>     // ESP8266WebServer on ESP8266
const char* SSID = "yourssid"; const char* PASS = "yourpass";
WebServer server(80);
void handleRoot() {
  int v = analogRead(34);                      // ADC1 pin
  server.send(200, "text/html",
    "<h1>ESP32</h1><p>sensor: " + String(v) + "</p>");
}
void setup() {
  Serial.begin(115200);
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) { delay(300); Serial.print("."); }
  Serial.println(WiFi.localIP());
  server.on("/", handleRoot);
  server.begin();
}
void loop() { server.handleClient(); }
```
For many concurrent clients / async use **ESPAsyncWebServer** + AsyncTCP.

## IoT building blocks
- **HTTP client**: `HTTPClient http; http.begin(url); http.GET();`.
- **MQTT**: PubSubClient or AsyncMqttClient → brokers (Mosquitto, HiveMQ). Great for home automation.
- **BLE** (ESP32): `BLEDevice` (server/characteristics) or NimBLE-Arduino (smaller).
- **OTA updates**: ArduinoOTA (local) or HTTP/HTTPS OTA (`Update` library) for field devices.
- **Deep sleep**: `esp_deep_sleep_start()`, wake on timer/GPIO — mandatory for battery. Currents drop to µA.
- **Storage**: `Preferences` (NVS key/value) or SPIFFS/LittleFS for files.
- **Time**: `configTime()` + NTP.
- **Home Assistant**: expose via MQTT discovery or ESPHome (YAML, no code) for the fast path.

## ESP-IDF (when you outgrow Arduino)
Native SDK, FreeRTOS tasks, full peripheral control. `idf.py set-target esp32 && idf.py build flash monitor`. Use it for RTOS scheduling, power tuning, secure boot, or components Arduino lacks.

## Gotchas
- **3.3V only** — 5V kills pins. Many sensors are 3.3V; level-shift 5V ones.
- **ADC2 can't be used while WiFi is on** — use ADC1 pins (GPIO 32–39) for analog.
- Some GPIOs are input-only (34–39) or strapping pins (0, 2, 15) — don't hang loads on boot pins.
- Brownout resets = weak USB power; use a good cable/supply, add a cap.
- Feed the watchdog: don't block long in `loop()`/tasks; `delay()` yields on ESP, tight `while` loops don't.
- Put big const strings in flash; enable `CORE_DEBUG_LEVEL` for logs.

## Checklist
Pick ESP32 vs ESP8266 (BLE? → ESP32) → 3.3V wiring → WiFi connect → add HTTP/MQTT/BLE → deep sleep if battery → OTA for deployed devices → verify with Serial + the device's IP.
