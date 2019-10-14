import _thread
from time import time
from machine import Pin
from helper_functions import ls, cat, lscat, rm, lsrm, toggle_pin, toggle_pin_loop

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
