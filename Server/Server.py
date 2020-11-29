import socket
import threading
import pprint
from Message.message import Message
from profile.user import UserProfile
import time


class ChatServer:
    connections = []
    nicknames = []
    message_kit = Message()
    number_users = 0
    encrypt_connection = False

    def __init__(self, ip_address, port_server, number_listen=2):
        self.ip = ip_address
        self.port = port_server
        self.host_data = (self.ip, self.port)
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket_server.bind(self.host_data)
        self.socket_server.listen(number_listen)

    def close_connection(self):
        for user in self.connections:
            user.connection.close()
            self.connections.remove(user)
        print(f"<{user.address}@{user.nickname}> - left chat")
        self.encrypt_connection = False

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

    def broadcast(self, message, current_user='server'):
        for user in self.connections:
            if current_user != user:
                user.connection.send(message)
            elif current_user == 'server':
                user.connection.send(message)

    def encrypting(self):
        """
        100 - pubic key
        101 - partial key
        102 - connected
        :return:
        """
        cods = ['100', '101']
        while True:
            if self.number_users != 2:
                continue
            else:
                for cod in cods:
                    package_msg = self.message_kit.get_package(cod)
                    self.broadcast(package_msg)
                    if cod == '100':
                        for user in self.connections:
                            user.key_pub = self.message_kit.get_message(connection=user.connection)
                        for user in self.connections:
                            package_msg = self.message_kit.get_package(user.key_pub)
                            self.broadcast(package_msg)
                    elif cod == '101':
                        for user in self.connections:
                            user.key_partial = self.message_kit.get_message(connection=user.connection)
                            print(user.key_partial)
                        for user in self.connections:
                            package_msg = self.message_kit.get_package(user.key_partial)
                            self.broadcast(package_msg, user)

                break
        self.send_usernames()
        cod = '102'
        package_msg = self.message_kit.get_package(cod)
        self.broadcast(package_msg)
        self.encrypt_connection = True


    def get_messages(self, user, num):
        # message_new_client = "Welcome to this chatroom!"
        # data_package = self.message_kit.get_package(message_new_client)
        # self.broadcast(data_package)
        # message_broadcast = f"<{user.address}@{user.nickname}>connected to channel"
        # package_message = self.message_kit.get_package(message_broadcast)
        # self.broadcast(package_message, user)

        while True:
            if self.encrypt_connection is False:
                continue
            data = self.message_kit.get_message(connection=user.connection)
            if data:
                if data != 'close':
                    print(f"<{user.address}@{user.nickname}> {data} ")
                    broadcast_message = data
                    data_package = self.message_kit.get_package(broadcast_message)
                    self.broadcast(message=data_package)

                else:
                    data = '103'
                    data_package = self.message_kit.get_package(data)
                    self.close_connection()
                    self.broadcast(data_package)
                    break

    def run(self):
        while True:
            connection, address = self.socket_server.accept()
            user = UserProfile()
            user.connection = connection
            user.nickname = self.message_kit.get_message(connection=connection)
            user.address = address
            self.connections.append(user)
            self.number_users = len(self.connections)
            print(f"<{user.address}@{user.nickname}> - connected to channel")
            print(self.number_users)
            if self.number_users == 2:
                thread_encrypting = threading.Thread(target=self.encrypting)
                thread_encrypting.start()
            thread_messages = threading.Thread(target=self.get_messages,
                                               args=(user, self.number_users), daemon=True)
            thread_messages.start()


if __name__ == '__main__':
    ip = '192.168.0.9'
    port = 9876
    server = ChatServer(ip_address=ip, port_server=port, number_listen=100)
    server.run()
