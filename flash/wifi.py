import network

class network_interface():
    station_interface = network.WLAN(network.STA_IF)
    ap_interface = network.WLAN(network.AP_IF)

    def interface_mode(self, mode=None):
        if mode == None:
            if self.station_interface.active():
                self.ap_interface.active(False)
                return network.STA_IF
            if self.ap_interface.active():
                self.station_interface.active(False)
                return network.AP_IF
        if mode == network.STA_IF:
            self.ap_interface.active(False)
            self.station_interface.active(True)
            return network.STA_IF
        if mode == network.AP_IF:
            self.station_interface.active(False)
            self.ap_interface.active(True)
            return network.AP_IF
        return None

    def connect_to_ap(self, ssid, wifi_key):
        self.interface_mode(network.STA_IF)
        self.station_interface.connect(ssid, wifi_key)
        return self.station_interface.isconnected()

    def start_access_point(self):
        self.interface_mode(network.AP_IF)
        return net_if.ap_interface.config('essid'), net_if.ap_interface.ifconfig()[0]

    def get_authmode_name(self, authmode):
        if authmode == network.AUTH_MAX:
            return "MAX"
        if authmode == network.AUTH_OPEN:
            return "OPEN"
        if authmode == network.AUTH_WEP:
            return "WEP"
        if authmode == network.AUTH_WPA2_PSK:
            return "WPA2_PSK"
        if authmode == network.AUTH_WPA_PSK:
            return "WPA_PSK"
        if authmode == network.AUTH_WPA_WPA2_PSK:
            return "WPA_WPA2_PSK"
        return None

    def get_access_points(self):
        IF_MODE = self.interface_mode()
        IS_CONNECTED = self.station_interface.isconnected()
        if IF_MODE == network.STA_IF and IS_CONNECTED:
            self.station_interface.disconnect()
        else:
            self.interface_mode(network.STA_IF)
        ap_list = self.station_interface.scan()
        self.interface_mode(IF_MODE)
        access_points = []
        for ap in ap_list:
            access_point = {
                "ssid":ap[0].decode(),
                "bssid":ap[1],
                "channel":ap[2],
                "RSSI":ap[3],
                "authmode":ap[4],
                "authname":self.get_authmode_name(ap[4]),
                "hidden":ap[5]
            }
            access_points.append(access_point)
        return access_points

net_if = network_interface()
