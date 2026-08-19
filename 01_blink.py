"""
Example 1: LED Blink
Blink the built-in LED on ESP32
"""

from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.value(not led.value())
    time.sleep(1)
