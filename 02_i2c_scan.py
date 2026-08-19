"""
Example 2: I2C Scanner
Scan for I2C devices on the bus
"""

from machine import I2C, Pin

# Configure I2C (adjust pins as needed)
i2c = I2C(scl=Pin(2), sda=Pin(22))

print("Scanning I2C bus...")
devices = i2c.scan()

if devices:
    print("Found devices at addresses:", [hex(d) for d in devices])
else:
    print("No I2C devices found")
