import socket

class Network:

    
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.78.174"
        self.port = 8888
        self.addr = (self.server, self.port)
        self._started = False
        if self.connect() == "Connected":
            print("Connected!")
            self.client.send(str.encode("Villain"))
        if self.client.recv(2048).decode() == "Starting":
            self._started = True

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    
    def send_data(self, id, posx, posy):
        self.client.send(str.encode(f"o{id},{posx},{posy}"))

