import socket

class http_server():
    # templates
    html = """<!DOCTYPE html><html><head> <title>ESP32</title></head><body><h1>ESP32</h1>{content}</body></html>"""
    done = """<p>Done</p>"""
    sel_net_form = """<form method="POST"><label for="cloud_address">Cloud Address</label><input id="cloud_address" name="cloud_address" type="text"><table><tr><th>#</th><th>SSID</th><th>AUTH</th><th>RSSI</th><th>CH</th></tr>{access_point_from_rols}</table><label for="net_key">SSID KEY : </label><input id="net_key" name="network_key" type="text"><input type="submit"></form>"""
    sel_net_row = """<tr><td><input type="radio" id="{ssid}" name="ssid" value="{ssid}"></td><td><label for="{ssid}">{ssid}</label></td><td>{authname}</td><td>{RSSI}</td><td>{channel}</td></tr>"""

    # configs
    ip = '0.0.0.0'
    port = 80

    # elements
    addr = socket.getaddrinfo(ip, port)[0][-1]
    sock = socket.socket()
    request_data = {}

    def __init__(self, ip='0.0.0.0', port=80):
        self.ip = ip
        self.port = port

    def setup(self):
        self.addr = socket.getaddrinfo(self.ip, self.port)[0][-1]
        self.sock.bind(self.addr)
        self.sock.listen(1)

    def select_network_form(self, ap_list):
        ap_from_rols = ""
        for ap in ap_list:
            ap_from_rols += self.sel_net_row.format(ssid = ap['ssid'],authname = ap['authname'],RSSI = ap['RSSI'],channel = ap['channel'],)
        return self.sel_net_form.format(access_point_from_rols=ap_from_rols)

    def runner(self, apl):
        while True:
            self.request_data = {}
            conn, self.request_data['remote_host'] = self.sock.accept()
            request = conn.makefile('rwb', 0)
            post_data_length = 0
            self.request_data['request'] = request.readline().decode().split("\r\n")[0]
            while True:
                request_line = request.readline()
                if not request_line or request_line == b'\r\n':
                    break
                parts = request_line.decode().split(":")
                part_key = parts[0]
                part_val = ":".join(parts[1:]).split("\r\n")[0]
                self.request_data[part_key] = part_val
                if part_key == "Content-Length":
                    post_data_length = int(self.request_data["Content-Length"])
            if post_data_length:
                post = request.read(post_data_length).decode()
                self.request_data["POST_DATA"] = {}
                for el in post.split("&"):
                    p_key, p_val = el.split("=")
                    self.request_data["POST_DATA"][p_key] = p_val
            if post_data_length:
                response = self.html.format(content=self.done)
            else:
                response = self.html.format(content=self.select_network_form(apl))
            conn.send(response)
            conn.close()
            if post_data_length:
                return self.request_data["POST_DATA"]

ws = http_server()
