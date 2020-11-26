import socket


class ChatServer:
    host_data = tuple()

    def __init__(self, ip_address, port_server):
        self.ip = ip_address
        self.port = port_server
        self.host_data = (self.ip, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(self.host_data)

    def run(self):
        try:

