from Client.Client import ChatClient
from Server.Server import ChatServer
import sys

# ip = '192.168.0.9'
# port = 9876
if sys.argv[1] == '-c':
    client = ChatClient(ip_server=sys.argv[2], port=int(sys.argv[3]))
    client.run()
if sys.argv[1] == '-s':
    server = ChatServer(ip_address=sys.argv[2], port_server=int(sys.argv[3]), number_listen=2)
    server.run()
