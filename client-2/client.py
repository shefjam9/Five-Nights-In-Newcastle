import socket
from pos import Pos

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.pos = Pos(0, 0)
    
    def send_obstacle(self, id, x, y):
        s_x = 3600*(x-360)/1200
        s_y = 3600*y/1200
        self.send_data = f"{id},{s_x},{s_y}"
        self.socket.send(self.send_data.encode())
        print(f"Sent: {self.send_data}")

    def run(self):
        while True:
            data = self.socket.recv(1024)
            print(data.decode())
            self.pos = Pos(*data.decode().split(','))
            print(f'Received: {self.pos.to_dict()}')
