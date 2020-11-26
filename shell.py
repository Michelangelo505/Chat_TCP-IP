from Client.Client import ChatClient
from Server.Server import ChatServer
import sys

ip = '127.0.0.1'
port = 9876
if sys.argv[1] == '-c':
    client = ChatClient(ip_server=ip, port=port)
    client.run()
if sys.argv[1] == '-s':
    server = ChatServer(ip_address=ip, port_server=port, number_listen=100)
    server.run()
