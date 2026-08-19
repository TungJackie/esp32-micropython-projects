"""
MicroPython SSD1306 OLED Display Driver
Version: 1.0.0
License: MIT
Jackie Tung 10/8/2026
"""

from machine import Pin, I2C
import time


class SSD1306_I2C:
    WIDTH = 128
    HEIGHT = 64
    PAGES = HEIGHT // 8

    def __init__(self, width=128, height=64, i2c=None, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.buffer = bytearray((height // 8) * width)
        self._init_display()

    def _write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x00, cmd]))

    def _write_data(self, data):
        self.i2c.writeto(self.addr, bytearray([0x40] + list(data)))

    def _init_display(self):
        self._write_cmd(0xAE)
        self._write_cmd(0xD5)
        self._write_cmd(0x80)
        self._write_cmd(0xA8)
        self._write_cmd(0x3F)
        self._write_cmd(0xD3)
        self._write_cmd(0x00)
        self._write_cmd(0x40 | 0x00)
        self._write_cmd(0x8D)
        self._write_cmd(0x14)
        self._write_cmd(0x20)
        self._write_cmd(0x00)
        self._write_cmd(0xA0 | 0x01)
        self._write_cmd(0xC8)
        self._write_cmd(0xDA)
        self._write_cmd(0x12)
        self._write_cmd(0x81)
        self._write_cmd(0xCF)
        self._write_cmd(0xD9)
        self._write_cmd(0xF1)
        self._write_cmd(0xDB)
        self._write_cmd(0x40)
        self._write_cmd(0xA4)
        self._write_cmd(0xA6)
        self._write_cmd(0x2E)
        self._write_cmd(0xAF)
        self.fill(0)
        self.show()

    def pixel(self, x, y, color=1):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        page = y // 8
        bit = y % 8
        index = page * self.width + x
        if color:
            self.buffer[index] |= (1 << bit)
        else:
            self.buffer[index] &= ~(1 << bit)

    def fill(self, color=0):
        fill_byte = 0xFF if color else 0x00
        for i in range(len(self.buffer)):
            self.buffer[i] = fill_byte

    def rect(self, x, y, width, height, color=1):
        for i in range(width):
            self.pixel(x + i, y, color)
            self.pixel(x + i, y + height - 1, color)
        for i in range(height):
            self.pixel(x, y + i, color)
            self.pixel(x + width - 1, y + i, color)

    def fill_rect(self, x, y, width, height, color=1):
        for i in range(width):
            for j in range(height):
                self.pixel(x + i, y + j, color)

    def line(self, x1, y1, x2, y2, color=1):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            self.pixel(x1, y1, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def text(self, string, x, y, color=1):
        font = {
            '0': [0x3E, 0x51, 0x49, 0x45, 0x3E],
            '1': [0x00, 0x42, 0x7F, 0x40, 0x00],
            '2': [0x42, 0x61, 0x51, 0x49, 0x46],
            '3': [0x22, 0x41, 0x49, 0x49, 0x36],
            '4': [0x18, 0x14, 0x12, 0x7F, 0x10],
            '5': [0x27, 0x45, 0x45, 0x45, 0x39],
            '6': [0x3E, 0x49, 0x49, 0x49, 0x32],
            '7': [0x01, 0x01, 0x71, 0x09, 0x07],
            '8': [0x36, 0x49, 0x49, 0x49, 0x36],
            '9': [0x26, 0x49, 0x49, 0x49, 0x3E],
            ':': [0x00, 0x24, 0x00, 0x24, 0x00],
            'A': [0x3E, 0x51, 0x49, 0x45, 0x3E],
            'B': [0x7F, 0x49, 0x49, 0x49, 0x36],
            'C': [0x3E, 0x41, 0x41, 0x41, 0x22],
            'D': [0x7F, 0x41, 0x41, 0x41, 0x3E],
            'E': [0x7F, 0x49, 0x49, 0x49, 0x41],
            'F': [0x7F, 0x48, 0x48, 0x48, 0x40],
            'H': [0x7F, 0x08, 0x08, 0x08, 0x7F],
            'I': [0x00, 0x41, 0x7F, 0x41, 0x00],
            'L': [0x7F, 0x01, 0x01, 0x01, 0x01],
            'M': [0x7F, 0x20, 0x10, 0x20, 0x7F],
            'N': [0x7F, 0x10, 0x08, 0x04, 0x7F],
            'O': [0x3E, 0x41, 0x41, 0x41, 0x3E],
            'P': [0x7F, 0x48, 0x48, 0x48, 0x30],
            'R': [0x7F, 0x48, 0x48, 0x4A, 0x34],
            'S': [0x22, 0x49, 0x49, 0x49, 0x36],
            'T': [0x40, 0x40, 0x7F, 0x40, 0x40],
            'U': [0x3E, 0x41, 0x41, 0x41, 0x3E],
            'W': [0x7F, 0x02, 0x0C, 0x02, 0x7F],
            'Y': [0x60, 0x10, 0x0F, 0x10, 0x60],
            ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
        }
        for char in string:
            if char in font:
                for col, byte_val in enumerate(font[char]):
                    for bit in range(5):
                        if byte_val & (1 << bit):
                            self.pixel(x + col, y + bit, color)
            x += 6

    def text_large(self, string, x, y, color=1):
        font_big = {
            '0': [
                [1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1]
            ],
            '1': [
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 1, 1, 1, 1, 1]
            ],
            '2': [
                [1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1]
            ],
            '3': [
                [1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1],
                [0, 0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 0]
            ],
            '4': [
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 1, 1, 0],
                [0, 0, 1, 0, 1, 0],
                [0, 1, 0, 0, 1, 0],
                [1, 0, 0, 0, 1, 0],
                [1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1, 0]
            ],
            '5': [
                [1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 0]
            ],
            '6': [
                [0, 1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [0, 1, 1, 1, 1, 0]
            ],
            '7': [
                [1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0]
            ],
            '8': [
                [0, 1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [0, 1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [0, 1, 1, 1, 1, 0]
            ],
            '9': [
                [0, 1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [0, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1],
                [0, 1, 1, 1, 1, 0]
            ],
            ':': [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0],
                [0, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0],
                [0, 0, 1, 1, 0, 0]
            ],
            ' ': [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]
            ]
        }
        char_width = 6
        char_height = 8
        scale = 2
        for char in string:
            if char in font_big:
                for row in range(char_height):
                    for col in range(char_width):
                        if font_big[char][row][col]:
                            for dy in range(scale):
                                for dx in range(scale):
                                    px = x + col * scale + dx
                                    py = y + row * scale + dy
                                    if px < self.width and py < self.height:
                                        self.pixel(px, py, color)
            x += char_width * scale + 2

    def show(self):
        for page in range(self.PAGES):
            self._write_cmd(0xB0 + page)
            self._write_cmd(0x00)
            self._write_cmd(0x10)
            start = page * self.width
            end = start + self.width
            self._write_data(self.buffer[start:end])

    def clear(self):
        self.fill(0)
        self.show()