import socket
import asyncio
from time import sleep
import threading
from threading import Lock
from select import select

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.connect(('127.0.0.1', 2060))
j =0
while True:

    server_sock.send(str(j).encode())
    j+=1
    print(server_sock.recv(1024).decode())
    sleep(5)