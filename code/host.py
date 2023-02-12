import socket

class Server:
    def __init__(self, host, port, player):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.connections = []
        self.run()
        self.player = player

    def run(self):
        while True:
            conn, addr = self.socket.accept()
            self.connections.append(conn)
            print(f"Connected by {addr}")
            self.send_message(conn, "Hello, world")

    def send_message(self, conn, message):
        conn.sendall(message.encode())