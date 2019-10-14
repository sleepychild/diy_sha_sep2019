import time
import _thread
import machine
from helper_functions import ls, cat, lscat

def handler(pin):
    print('Enter interupt for: ', pin, 'at ', time.time())
    time.sleep(1)
    print('Exit interupt for: ', pin, 'at ', time.time())

# Pins Out
GPIO2 = machine.Pin(2, machine.Pin.OUT)

# Pins In
GPIO4 = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
GPIO5 = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
GPIO15 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
GPIO18 = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)

# Pin Interupts
GPIO4.irq(trigger=machine.Pin.IRQ_RISING, handler=handler)
GPIO5.irq(trigger=machine.Pin.IRQ_RISING, handler=handler)
GPIO15.irq(trigger=machine.Pin.IRQ_RISING, handler=handler)
GPIO18.irq(trigger=machine.Pin.IRQ_RISING, handler=handler)

# I2C SCL GPIO22 SDA GPIO21
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)

def toggle(pin):
    pin.value(not pin.value())

def toggle_loop(pin, ms):
    while True:
        time.sleep_ms(ms)
        toggle(pin)

_thread.start_new_thread(toggle_loop, (GPIO2, 500))
