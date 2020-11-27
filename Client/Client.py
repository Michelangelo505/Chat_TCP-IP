import socket
from Message.message import Message
import threading
import time
import sys
import select


class ChatClient:
    message_kit = Message()

    def __init__(self, ip_server, port):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip_server
        self.port = port

    def listen(self):

        try:
            message = self.message_kit.get_message(connection=self.socket_client)
            # message = self.socket_client.recv(1024).decode()
        except Exception as error:
            pass
        return message

    def send(self, data):
        try:
            package_message = self.message_kit.get_package(data=data)
            self.socket_client.send(package_message)
        except Exception as error:
            pass

    def run(self):
        host_data = (self.ip, self.port)
        try:
            self.socket_client.connect(host_data)
        except Exception as error:
            # TODO Переделать
            print('Невозможно подключиться !')
            print(error)
            exit()

    def close_connection(self):
        self.socket_client.close()

        # while True:

    # # Рабочий вариант, но выводит сообщения (если они есть) только после отправки.
    # read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    # for connection in read_sockets:
    #     if connection == self.socket_client:
    #         self.listen()
    #     else:
    #         message = sys.stdin.readline()
    #         package_message = Message.get_package(message)
    #         self.socket_client.send(package_message)
    #         sys.stdout.write("<You>")
    #         sys.stdout.write(message)
    #         sys.stdout.flush()


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9876
    client = ChatClient(ip_server=ip, port=port)
    client.run()
