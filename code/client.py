import socket
from objects.pos import Pos

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.pos = Pos(0, 0)

    def run(self):
        while True:
            data = self.socket.recv(1024)
            self.pos = Pos(*data.decode().split(','))
            print(f'Received: {self.pos.to_dict()}')

client = Client('127.0.0.1', 6969)
client.run()