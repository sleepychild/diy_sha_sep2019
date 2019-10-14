import network

station_interface = network.WLAN(network.STA_IF)
station_interface.active(True)
station_interface.scan()
station_interface.connect('M-Tel_06A9', '48575443C706A97B')