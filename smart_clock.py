from machine import Pin, I2C
import time
import network
import ntptime
from ssd1306 import SSD1306_I2C

# ===== WiFi =====
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

# ===== OLED =====
i2c = I2C(scl=Pin(2), sda=Pin(22), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# ===== 时间函数 =====
def get_date_string():
    import machine
    rtc = machine.RTC()
    tm = rtc.datetime()
    return "{:04d}-{:02d}-{:02d}".format(tm[0], tm[1], tm[2])

def get_weekday_string():
    import machine
    rtc = machine.RTC()
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return weekdays[rtc.datetime()[3]]

def get_time_string_short():
    import machine
    rtc = machine.RTC()
    tm = rtc.datetime()
    return "{:02d}:{:02d}:{:02d}".format(tm[4], tm[5], tm[6])

# ===== 进度条（靠下，无文字） =====
def show_loading(progress):
    oled.fill(0)
    
    # 进度条放在偏下位置 (y=38)
    bar_x = 10
    bar_y = 38
    bar_w = 108
    bar_h = 12
    oled.rect(bar_x, bar_y, bar_w, bar_h, 1)
    fill = int(bar_w * progress / 100)
    if fill > 0:
        oled.fill_rect(bar_x+1, bar_y+1, fill-1, bar_h-2, 1)
    
    oled.show()

# ===== WiFi =====
def connect_wifi():
    show_loading(10)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        t = 15
        while not wlan.isconnected() and t > 0:
            time.sleep(1)
            t -= 1
            show_loading(10 + (15-t) * 3)
    if wlan.isconnected():
        show_loading(50)
        time.sleep(0.5)
        return True
    else:
        show_loading(50)
        time.sleep(0.5)
        return False

# ===== NTP =====
def sync_time():
    show_loading(60)
    
    servers = [
        "time.windows.com",
        "time.nist.gov", 
        "pool.ntp.org",
        "time.google.com"
    ]
    
    for server in servers:
        try:
            print("Trying NTP:", server)
            ntptime.host = server
            ntptime.settime()
            
            import machine
            rtc = machine.RTC()
            tm = rtc.datetime()
            rtc.datetime((tm[0], tm[1], tm[2], tm[3], tm[4]+8, tm[5], tm[6], tm[7]))
            
            print("Time synced from:", server)
            show_loading(90)
            time.sleep(0.5)
            return True
        except Exception as e:
            print("NTP failed:", server, e)
            time.sleep(1)
    
    print("All NTP servers failed")
    show_loading(90)
    time.sleep(0.5)
    return False

# ===== 大号时钟 =====
def display_clock():
    oled.fill(0)
    
    date_str = get_date_string()
    date_x = (128 - len(date_str) * 6) // 2
    oled.text(date_str, date_x, 0, 1)
    
    weekday = get_weekday_string()
    oled.text(weekday, 88, 0, 1)
    
    for x in range(5, 123):
        oled.pixel(x, 10, 1)
    
    time_str = get_time_string_short()
    total_width = len(time_str) * 14
    time_x = (128 - total_width) // 2
    if time_x < 0:
        time_x = 0
    
    oled.text_large(time_str, time_x, 16, 1)
    
    for x in range(10, 118, 10):
        oled.pixel(x, 62, 1)
    
    oled.show()

# ===== 主程序 =====
def main():
    print("=" * 40)
    print("ESP32 OLED Clock")
    print("=" * 40)
    
    import machine
    rtc = machine.RTC()
    rtc.datetime((2026, 1, 1, 3, 0, 0, 0, 0))
    
    show_loading(5)
    time.sleep(0.5)
    
    print("Connecting WiFi...")
    wifi_ok = connect_wifi()
    
    if wifi_ok:
        print("WiFi OK")
        time_ok = sync_time()
        if time_ok:
            print("Time synced OK")
        else:
            print("Time sync failed")
    else:
        print("WiFi failed, using default time")
        show_loading(90)
        time.sleep(1)
    
    show_loading(100)
    time.sleep(0.5)
    
    # 不显示任何小字，直接进入时钟
    print("=" * 40)
    print("Clock Running...")
    print("Current Time:", get_time_string_short())
    print("=" * 40)
    
    while True:
        try:
            display_clock()
            time.sleep(1)
        except KeyboardInterrupt:
            print("Stopped")
            break
        except Exception as e:
            print("Error:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()