import socket
import threading
import pprint
from Message.message import Message
from profile.user import UserProfile


class ChatServer:
    connections = []
    message_kit = Message()

    def __init__(self, ip_address, port_server, number_listen):
        self.ip = ip_address
        self.port = port_server
        self.host_data = (self.ip, self.port)
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket_server.bind(self.host_data)
        self.socket_server.listen(number_listen)

    def get_messages(self, connection, ip_address, name):
        message_new_client = "Welcome to this chatroom!"
        data_package = self.message_kit.get_package(message_new_client)
        connection.send(data_package)
        while True:
            data = self.message_kit.get_message(connection=connection)
            if data:
                if data != 'close':
                    print(f"<{ip_address}> {data} ")
                    broadcast_message = f"<{ip_address}@{name}>" + data
                    data_package = self.message_kit.get_package(broadcast_message)
                    self.broadcast(message=data_package)
                else:
                    data = f"{connection.nickname} - покинул чат"
                    data_package = self.message_kit.get_package(data)
                    self.close_connection(connection)
                    self.broadcast(message=data_package)

    def close_connection(self, user):
        if user in self.connections:
            user.connection.close()
            self.connections.remove(user)
        length = len(self.connections)
        if length == 0:
            exit()

    def broadcast(self, message):
        for user in self.connections:
            user.connection.send(message)

    def run(self):
        while True:
            connection, address = self.socket_server.accept()
            user = UserProfile()
            user.connection = connection
            user.nickname = self.message_kit.get_message(connection=connection)
            user.address = address[0]
            message_broadcast = f"<{user.address}@{user.nickname}> - подключился к чату"
            self.connections.append(user)
            self.broadcast(message_broadcast)
            print(f"<{user.address}@{user.nickname}> - connected")
            thread_messages = threading.Thread(target=self.get_messages,
                                               args=(user.connection, user.address, user.nickname), daemon=True)
            thread_messages.start()


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9876
    server = ChatServer(ip_address=ip, port_server=port, number_listen=100)
    server.run()
