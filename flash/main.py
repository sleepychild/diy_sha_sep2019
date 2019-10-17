import ntptime
import webrepl
import _thread
from time import time, sleep_ms, localtime
from machine import Pin, reset
from helper_functions import ls, cat, lscat, rm, lsrm, url_decode, toggle_pin, toggle_pin_loop
from settings import cnf
from lcd import lcd
from wifi import net_if
from web_server import ws

def display_alternate(delay):
    while True:
        lcd.clear()
        lcd.putstr(cnf.ssid)
        lcd.move_to(0,1)
        lcd.putstr(net_if.station_interface.ifconfig()[0])
        sleep_ms(delay)
        lcd.clear()
        current_time = localtime()
        lcd.putstr("{year}-{month}-{day}".format(year=current_time[0],month=current_time[1],day=current_time[2]))
        lcd.move_to(0,1)
        lcd.putstr("{hour}:{minute}:{second}".format(hour=current_time[3],minute=current_time[4],second=current_time[5]))
        sleep_ms(delay)

def handler(pin):
    print('Interupt for: ', pin, 'at ', time())

# Pins Out
GPIO2 = Pin(2, Pin.OUT)

# Pins In
GPIO4 = Pin(4, Pin.IN, Pin.PULL_UP)
GPIO5 = Pin(5, Pin.IN, Pin.PULL_UP)
GPIO15 = Pin(15, Pin.IN, Pin.PULL_UP)
GPIO18 = Pin(18, Pin.IN, Pin.PULL_UP)

# Pin Interupts
GPIO4.irq(trigger=Pin.IRQ_RISING, handler=handler)
GPIO5.irq(trigger=Pin.IRQ_RISING, handler=handler)
GPIO15.irq(trigger=Pin.IRQ_RISING, handler=handler)
GPIO18.irq(trigger=Pin.IRQ_RISING, handler=handler)

# Start led blink thread
_thread.start_new_thread(toggle_pin_loop, (GPIO2, 500))

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
            lcd.clear()
            lcd.putstr(cnf.ssid)
            lcd.move_to(0,1)
            lcd.putstr(net_if.station_interface.ifconfig()[0])
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

if net_if.station_interface.isconnected():
    # Start webrepl when we get network connectivity
    webrepl.start()
    # Set time via ntp when we get internet connectivity
    ntptime.settime()
    # Alternate the screen
    _thread.start_new_thread(display_alternate, (2000,))
else:
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
