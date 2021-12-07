import socket
from select import select

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(('', 2060))
server_sock.listen()
sock, addr = server_sock.accept()
while True:
    print(sock.recv(100))