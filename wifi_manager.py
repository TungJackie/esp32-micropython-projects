"""
WiFi Manager - Handles WiFi connection with retry logic
"""

import network
import time

class WiFiManager:
    def __init__(self, ssid, password, timeout=15):
        self.ssid = ssid
        self.password = password
        self.timeout = timeout
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
    
    def connect(self, callback=None):
        """Connect to WiFi with progress callback"""
        if self.wlan.isconnected():
            return True
        
        self.wlan.connect(self.ssid, self.password)
        t = self.timeout
        
        while not self.wlan.isconnected() and t > 0:
            time.sleep(1)
            t -= 1
            if callback:
                callback((self.timeout - t) * 100 // self.timeout)
        
        return self.wlan.isconnected()
    
    def disconnect(self):
        """Disconnect from WiFi"""
        self.wlan.disconnect()
        self.wlan.active(False)
    
    def get_status(self):
        """Get connection status"""
        if self.wlan.isconnected():
            return {
                'connected': True,
                'ip': self.wlan.ifconfig()[0],
                'ssid': self.ssid
            }
        return {'connected': False}
