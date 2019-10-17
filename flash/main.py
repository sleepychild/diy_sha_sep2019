import ntptime
import webrepl
import _thread
from time import time
from machine import Pin
from helper_functions import ls, cat, lscat, rm, lsrm, toggle_pin, toggle_pin_loop
from settings import cnf
from lcd import lcd
from wifi import net_if

'''
# Start webrepl when we get network connectivity
webrepl.start()
# Set time via ntp when we get internet connectivity
ntptime.settime()    
'''

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

access_points_list = net_if.get_access_points()

for ap in access_points_list:
    if ap['ssid'] == cnf.ssid:
        net_if.connect_to_ap(cnf.ssid, cnf.key)
        break

if not net_if.station_interface.isconnected():
    essid, ip = net_if.start_access_point()
    lcd.clear()
    lcd.putstr(net_if.ap_interface.config('essid'))
    lcd.move_to(0,1)
    lcd.putstr(net_if.ap_interface.ifconfig()[0])
