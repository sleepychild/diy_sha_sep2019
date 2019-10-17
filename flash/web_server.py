import machine

html = """<!DOCTYPE html>
<html><head> <title>ESP32</title></head><body><h1>ESP32</h1>
{content}
</body></html>"""

def select_network_form(ap_list):
    sel_net_form = """<form>
        <table>
            <tr>
                <th>#</th><th>SSID</th><th>AUTH</th><th>RSSI</th><th>CH</th>
            </tr>
            {access_point_from_rols}
        </table>
        <input name="text_value" type="text">
        <input type="submit">
    </form>"""
    ap_from_rols = """"""
    for ap in ap_list:
        ap_from_rols += """<tr><td><input type="radio" id="{ssid}" name="ssid" value="{ssid}"></td><label for="{ssid}"><td>{ssid}</td><td>{authname}</td><td>{RSSI}</td><td>{channel}</td></label></tr>""".format(ssid = ap['ssid'],authname = ap['authname'],RSSI = ap['RSSI'],channel = ap['channel'],)
    return sel_net_form.format(access_point_from_rols=ap_from_rols)

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        print(line)
        if not line or line == b'\r\n':
            break
    response = html.format(content=select_network_form(access_points_list))
    cl.send(response)
    cl.close()