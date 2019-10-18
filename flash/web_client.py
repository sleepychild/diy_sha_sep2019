import socket
from time import sleep_ms

class inform_client_class():
    ip = '0.0.0.0'
    port = 9000
    addr = socket.getaddrinfo(ip, port)[0][-1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    terminate = b"TERM"

    def __init__(self, ip='0.0.0.0', port=9000):
        self.ip = ip
        self.port = port
        self.addr = socket.getaddrinfo(self.ip, self.port)[0][-1]
        self.sock.connect(self.addr)

    def setup(self):
        self.sock.connect(self.addr)

    def send(self, data):
        self.sock.send(data)

    def close_connection(self):
        self.sock.send(self.terminate)
        self.sock.close()

class inpipe_client_class():
    ip = '0.0.0.0'
    port = 9001
    uart2_interface = False
    addr = socket.getaddrinfo(ip, port)[0][-1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    terminate = b"TERM"

    def __init__(self, ip='0.0.0.0', port=9001, uart2_interface=False):
        self.ip = ip
        self.port = port
        self.uart2_interface = uart2_interface
        self.addr = socket.getaddrinfo(self.ip, self.port)[0][-1]
        self.sock.connect(self.addr)

    def setup(self):
        self.sock.connect(self.addr)

    def runner(self, delay):
        while True:
            self.uart2_interface.write(self.sock.readline())
            sleep_ms(delay)

    def close_connection(self):
        self.sock.send(self.terminate)
        self.sock.close()

class outpipe_client_class():
    ip = '0.0.0.0'
    port = 9002
    data_line_in = b""
    uart2_interface = False
    addr = socket.getaddrinfo(ip, port)[0][-1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    terminate = b"TERM"

    def __init__(self, ip='0.0.0.0', port=9002, uart2_interface=False):
        self.ip = ip
        self.port = port
        self.uart2_interface = uart2_interface
        self.addr = socket.getaddrinfo(self.ip, self.port)[0][-1]
        self.sock.connect(self.addr)

    def setup(self):
        self.sock.connect(self.addr)

    def runner(self, delay):
        while True:
            if self.uart2_interface.any():
                self.data_line_in += self.uart2_interface.readline()
                if self.data_line_in.endswith(b"\r"):
                    self.sock.send(self.data_line_in)
                    self.data_line_in = b""
            sleep_ms(delay)

    def close_connection(self):
        self.sock.send(self.terminate)
        self.sock.close()
