# This file is executed on every boot (including wake-boot from deepsleep)
import esp
import network
import ntptime
import webrepl

# Set debuging
esp.osdebug(0)

# Connect to network
station_interface = network.WLAN(network.STA_IF)
station_interface.active(True)
station_interface.scan()

wifi_connect_try_count = 5

while not station_interface.isconnected():
    station_interface.connect('M-Tel_06A9', '48575443C706A97B')
    wifi_connect_try_count -= 1
    if not wifi_connect_try_count:
        break

if station_interface.isconnected():
    # Set time
    ntptime.settime()
    
    #Start webrepl
    webrepl.start()