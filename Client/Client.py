import socket
import random
from Message.message import Message
import threading
import time
import sys
import select
from profile.user import UserProfile


class ChatClient:
    message_kit = Message()

    def __init__(self, ip_server, port, name):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip_server
        self.port = port
        self.user = UserProfile()
        self.user.nickname = name
        self.user.key_pub = str(random.randint(100, 400))
        self.user.key_private = str(random.randint(100, 400))

    def listen(self):
        message = self.message_kit.get_message(connection=self.socket_client)
        # message = self.socket_client.recv(1024).decode()
        return message

    def send(self, data):
        package_message = self.message_kit.get_package(data=data)
        self.socket_client.send(package_message)

    def run(self):
        host_data = (self.ip, self.port)
        try:
            self.socket_client.connect(host_data)
            self.send(self.user.nickname)
        except Exception as error:
            print('Невозможно подключиться !')
            print(error)
            exit()

    def close_connection(self):
        data = 'close'
        package_message = self.message_kit.get_package(data=data)
        self.socket_client.send(package_message)
        self.socket_client.close()


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9879
    client = ChatClient(ip_server=ip, port=port)
    client.run()
