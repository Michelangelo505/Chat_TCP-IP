import socket
import threading
import pprint
from Message.message import Message
from profile.user import UserProfile


class ChatServer:
    connections = []
    nicknames = []
    message_kit = Message()

    def __init__(self, ip_address, port_server, number_listen=2):
        self.ip = ip_address
        self.port = port_server
        self.host_data = (self.ip, self.port)
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket_server.bind(self.host_data)
        self.socket_server.listen(number_listen)

    def get_messages(self, user, num):
        message_new_client = "Welcome to this chatroom!"
        data_package = self.message_kit.get_package(message_new_client)
        user.connection.send(data_package)
        message_broadcast = f"<{user.address}@{user.nickname}>connected to channel"
        package_message = self.message_kit.get_package(message_broadcast)
        self.broadcast(package_message)
        self.send_usernames()
        while True:
            data = self.message_kit.get_message(connection=user.connection)
            if data:
                if data != 'close':
                    print(f"<{user.address}@{user.nickname}> {data} ")
                    broadcast_message = f"<{user.address}@{user.nickname}>" + data
                    data_package = self.message_kit.get_package(broadcast_message)
                    self.broadcast(message=data_package)
                else:
                    data = f"<{user.address}@{user.nickname}>left chat"
                    print(data)
                    data_package = self.message_kit.get_package(data)
                    self.close_connection(user)
                    self.broadcast(message=data_package)

    def close_connection(self, user):
        if user in self.connections:
            user.connection.close()
            self.connections.remove(user)
        # print(self.nicknames)
        self.send_usernames()

    def send_usernames(self):
        cod = "users"
        package_message = self.message_kit.get_package(cod)
        names = self.get_usernames()
        self.broadcast(package_message)
        users = ",".join(names)
        package_message = self.message_kit.get_package(users)
        self.broadcast(package_message)

    def get_usernames(self):
        names = []
        for user in self.connections:
            names.append(user.nickname)
        return names

    def broadcast(self, message):
        for user in self.connections:
            user.connection.send(message)

    def run(self):
        while True:
            connection, address = self.socket_server.accept()
            user = UserProfile()
            user.connection = connection
            user.nickname = self.message_kit.get_message(connection=connection)
            user.address = address
            self.connections.append(user)
            print(f"<{user.address}@{user.nickname}> - connected to channel")
            thread_messages = threading.Thread(target=self.get_messages,
                                               args=(user, 1), daemon=True)
            thread_messages.start()


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9871
    server = ChatServer(ip_address=ip, port_server=port, number_listen=100)
    server.run()
