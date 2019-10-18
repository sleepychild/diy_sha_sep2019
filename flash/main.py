import _thread
from json import dumps
from time import time, sleep_ms, localtime
from gc import collect
from esp32 import raw_temperature, hall_sensor
from machine import Pin, UART, unique_id
from helper_functions import ls, cat, lscat, rm, lsrm, toggle_pin, toggle_pin_loop
from settings import cnf
from lcd import lcd
from wifi import net_if
from web_server import ws
from provision import provision_routine
from web_client import inform_client_class , inpipe_client_class, outpipe_client_class

def main_routine():
    # Gather Data
    dt = {
        "uid": unique_id(),
        "ssid": cnf.ssid,
        "addr": net_if.station_interface.ifconfig()[0],
        "localtime": localtime(),
        "cpu_temp": str(int((raw_temperature() - 32) / 1.8)),
        "hall": hall_sensor()
    }

    # Send Inform
    inform_client.send(dumps(dt))

    # Display On LCD
    lcd.network(dt["ssid"], dt["addr"])
    sleep_ms(1000)
    lcd.time(dt["localtime"])
    sleep_ms(1000)
    lcd.sensor(dt["cpu_temp"], dt["hall"])
    sleep_ms(1000)

def main_thread():
    mt_loop_count = 0
    while True:
        if net_if.station_interface.isconnected():
            main_routine()
        else:
            provision_routine()
        mt_loop_count += 1
        if mt_loop_count > 10:
            collect()

# Pins Out
GPIO2 = Pin(2, Pin.OUT)

# UART
UART2 = UART(2)

# Provision
provision_routine()

# Socket Connections
if net_if.station_interface.isconnected():
    inform_client = inform_client_class(cnf.cloud_address, 9000)
    inpipe_client = inpipe_client_class(cnf.cloud_address, 9001, UART2)
    outpipe_client = outpipe_client_class(cnf.cloud_address, 9002, UART2)

# Start threads
_thread.start_new_thread(main_thread, ())
_thread.start_new_thread(inpipe_client.runner, (250,))
_thread.start_new_thread(outpipe_client.runner, (250,))
_thread.start_new_thread(toggle_pin_loop, (GPIO2, 500))
