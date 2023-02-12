import socket
from pos import Pos

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.is_connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.is_connected = True
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
            data_split = data.decode().split('[')
            last_message = data_split[-1].split(",")
            self.pos = Pos(float(last_message[0]), float(last_message[1]))
            print(f'Received: {self.pos.to_dict()}')
