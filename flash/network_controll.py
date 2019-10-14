import network
import ntptime
import webrepl
from settings import cnf

# Connect to network
station_interface = network.WLAN(network.STA_IF)
station_interface.active(True)
station_interface.scan()

wifi_connect_try_count = 5

while not station_interface.isconnected():
    station_interface.connect(cnf.local_wifi_ssid, cnf.local_wifi_password)
    wifi_connect_try_count -= 1
    if not wifi_connect_try_count:
        break

if station_interface.isconnected():
    # Set time
    ntptime.settime()
    
    #Start webrepl
    webrepl.start()

def get_access_points(wifi_interface):
    ap_list = wifi_interface.scan()
    access_points = []
    for ap in ap_list:
        access_point = {
            "ssid":ap[0],
            "bssid":ap[1],
            "channel":ap[2],
            "RSSI":ap[3],
            "authmode":ap[4],
            "hidden":ap[5]
        }
        access_points.append(access_point)
    return access_points