import ntptime
import webrepl
from machine import reset
from time import sleep_ms
from helper_functions import url_decode
from settings import cnf
from lcd import lcd
from wifi import net_if
from web_server import ws

def provision_routine():
    #provisioning
    lcd.clear()
    lcd.putstr("Scanning")
    access_points_list = net_if.get_access_points()

    AP_FOUND = False

    for ap in access_points_list:
        if ap['ssid'] == cnf.ssid:
            lcd.move_to(0,1)
            lcd.putstr(cnf.ssid+" found")
            sleep_ms(2000)
            lcd.clear()
            AP_FOUND = True
            break

    if AP_FOUND:
        network_connection_try_count = 5
        lcd.putstr(cnf.ssid)
        lcd.move_to(0,1)
        lcd.putstr("Connecting")
        while network_connection_try_count:
            if net_if.connect_to_ap(cnf.ssid, cnf.key):
                sleep_ms(750)
                lcd.clear()
                lcd.putstr(cnf.ssid)
                lcd.move_to(0,1)
                lcd.putstr(net_if.station_interface.ifconfig()[0])
                if net_if.station_interface.isconnected():
                    # Network services
                    # Start webrepl when we get network connectivity
                    print("Start Web REPL")
                    webrepl.start()
                    # Set time via ntp when we get internet connectivity
                    print("NTP Sync time")
                    ntptime.settime()
                break
            else:
                lcd.clear()
                lcd.putstr(cnf.ssid)
                lcd.move_to(0,1)
                lcd.putstr("Connect Fail")
                sleep_ms(2000)
                lcd.move_to(0,1)
                lcd.putstr("               ")
                lcd.move_to(0,1)
                lcd.putstr("Retrying ")
                network_connection_try_count -= 1
                lcd.putstr(str(network_connection_try_count))
                sleep_ms(2000)

    if not net_if.station_interface.isconnected():
        # Set Access Point
        essid, ip = net_if.start_access_point()
        lcd.clear()
        lcd.putstr(net_if.ap_interface.config('essid'))
        lcd.move_to(0,1)
        lcd.putstr(net_if.ap_interface.ifconfig()[0])    
        # Run Web Server
        ws.ip = net_if.ap_interface.ifconfig()[0]
        ws.setup()
        ws_return_data = ws.runner(access_points_list)
        cnf.ssid = ws_return_data['ssid']
        cnf.key = ws_return_data['network_key']
        cnf.cloud_address = url_decode(ws_return_data['cloud_address'])
        cnf.save_config()
        sleep_ms(750)
        reset()
