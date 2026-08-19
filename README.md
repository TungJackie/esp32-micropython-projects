# ESP32 MicroPython Projects

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MicroPython](https://img.shields.io/badge/MicroPython-v1.20-blue.svg)](https://micropython.org/)

A curated collection of ESP32 MicroPython projects with reusable libraries and utilities for IoT applications.

## 📦 Projects

| Project | Description | Status |
|---------|-------------|--------|
| [OLED Clock](applications/oled_clock/) | WiFi network clock with NTP sync | ✅ Stable |

## 🚀 Quick Start

```bash
git clone https://github.com/yourusername/esp32-micropython-projects.git
cd esp32-micropython-projects/applications/oled_clock
cp config.example.py config.py
# Edit config.py with your WiFi credentials
ampy --port /dev/ttyUSB0 put boot.py
ampy --port /dev/ttyUSB0 put ../../libraries/drivers/ssd1306.py
