import socket
import time
from misc.logger import log
from objects.obstacles.pigeon import Pigeon
from objects.obstacles.obstacle import ObstacleID

class Server:
    def __init__(self, host, port, player, game_loop):
        self.host = host
        self.port = port
        self.player = player
        self.game_loop = game_loop

        # And you can hear their eyes rolling round in their sockets
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
            split_data = data.decode().split(",")
            id, x, y = int(split_data[0]), float(split_data[1]), float(split_data[2])
            self.game_loop.add_entity(Pigeon(time.perf_counter(), x, y, self.player))

    def send_position(self):
        if self.init:
            message = f"[{self.player.rel.x},{self.player.rel.y}"
            self.conn.send(message.encode())