import socket

class inform_server_class():
    ip = '0.0.0.0'
    port = 9001
    addr = socket.getaddrinfo(ip, port)[0][-1]
    sock = socket.socket()
    terminate = b"TERM"

    def __init__(self, ip='0.0.0.0', port=9001):
        self.ip = ip
        self.port = port

    def setup(self):
        self.addr = socket.getaddrinfo(self.ip, self.port)[0][-1]
        self.sock.bind(self.addr)
        self.sock.listen(1)

    def runner(self):
        while True:
            conn, remote_host = self.sock.accept()
            print(remote_host)
            while conn.fileno():
                in_data = input("SEND: ")
                conn.send(in_data.encode()+b"\r\n")
            conn.close()

inform_server = inform_server_class()
inform_server.setup()
inform_server.runner()
