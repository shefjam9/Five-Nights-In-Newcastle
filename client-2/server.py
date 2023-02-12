import socket
from _thread import *
import sys


class Server:
    
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._clients = {"Villain": None, "Player": None}
        try:
            self._socket.bind(("127.0.0.1", 5555))
        except socket.error as e:
            str(e)
        self._socket.listen(2)
        print("waiting for connections to server!")
        while(True):
            conn, addr = self._socket.accept()
            start_new_thread(self.server_thread, (conn, ))

    def server_thread(self, connection):
        print("Connection to client successful")
        connection.send(str.encode("Connected"))
        data = connection.recv(2048)
        reply = data.decode("utf-8")
        if reply == "Villain":
            print("Villain Connected!")
            self._clients["Villain"] = connection
        elif reply == "Player":
            print("Player connected!")
            self._clients["Player"] = connection
        while(not self._clients["Villain"] or not self._clients["Player"]):
            pass
        print("Both players connected")
        connection.send(str.encode("Starting"))
        while(True):
            try:
                data = connection.recv(2048)
                msg = data.decode('utf-8')
                print(msg)
            except:
                break
        
        
if __name__ == "__main__":
    s = Server()
