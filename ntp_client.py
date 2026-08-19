"""
NTP Client - Time synchronization with multiple server fallback
"""

import ntptime
import machine
import time

class NTPClient:
    def __init__(self, timezone_offset=8, servers=None):
        self.timezone_offset = timezone_offset
        self.servers = servers or [
            "time.windows.com",
            "time.nist.gov",
            "pool.ntp.org",
            "time.google.com"
        ]
        self.rtc = machine.RTC()
    
    def sync(self, callback=None):
        """Synchronize time with NTP servers"""
        for i, server in enumerate(self.servers):
            try:
                if callback:
                    callback(20 + (i * 20))
                
                ntptime.host = server
                ntptime.settime()
                
                # Apply timezone offset
                tm = self.rtc.datetime()
                self.rtc.datetime((
                    tm[0], tm[1], tm[2], tm[3],
                    tm[4] + self.timezone_offset,
                    tm[5], tm[6], tm[7]
                ))
                
                return True
            except:
                time.sleep(1)
                continue
        
        return False
    
    def get_datetime(self):
        """Get current date and time as dict"""
        tm = self.rtc.datetime()
        return {
            'year': tm[0],
            'month': tm[1],
            'day': tm[2],
            'weekday': tm[3],
            'hour': tm[4],
            'minute': tm[5],
            'second': tm[6]
        }
