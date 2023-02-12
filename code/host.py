import socket
import asyncio
from misc.logger import log

class Server:
    def __init__(self, host, port, player):
        self.host = host
        self.port = port
        self.player = player
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.conn = None
        self.addr = None
        self.init = False

    def run(self):
        while True:
            conn, addr = self.socket.accept()
            log("Connected to {addr}")
            self.conn = conn
            self.addr = addr
            self.init = True
            self.listen()
        
    def listen(self):
        while True:
            data = self.conn.recv(1024)
            print(data.decode())

    def send_position(self):
        if self.init:
            message = f"[{self.player.rel.x},{self.player.rel.y}"
            self.conn.send(message.encode())