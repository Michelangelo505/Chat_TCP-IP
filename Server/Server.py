import socket
import threading
import pprint
from Message.message import Message


class ChatServer:
    connections = []

    def __init__(self, ip_address, port_server, number_listen):
        self.ip = ip_address
        self.port = port_server
        self.host_data = (self.ip, self.port)
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket_server.bind(self.host_data)
        self.socket_server.listen(number_listen)

    def get_messages(self, connection, ip_address):
        message_kit = Message()
        message_new_client = "Welcome to this chatroom!"
        data_package = message_kit.get_package(message_new_client)
        connection.send(data_package)
        while True:
            data = message_kit.get_message(connection=connection)
            if data:
                print(f"<{ip_address}> {data} ")
                data_package = message_kit.get_package(data)
                self.broadcast(message=data_package, sender=connection)

    def broadcast(self, message, sender):
        for connection in self.connections:
            connection.send(message)

    def remove_connection(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)

    def run(self):
        while True:
            connection, address = self.socket_server.accept()
            self.connections.append(connection)
            ip_address = address[0]
            print(f"{ip_address} - connected")
            print(self.connections)
            thread_messages = threading.Thread(target=self.get_messages, args=(connection, ip_address), daemon=True)
            thread_messages.start()


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9876
    server = ChatServer(ip_address=ip, port_server=port, number_listen=100)
    server.run()
