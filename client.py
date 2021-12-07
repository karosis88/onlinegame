import socket
import asyncio
from time import sleep
import threading
from threading import Lock
from select import select

def client():
    SERVER = (('127.0.0.1', 2060))

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(SERVER)

    while True:
        command = input().encode()

        client_sock.send(command)
        answer = client_sock.recv(6).decode()
        print(answer, type(answer), command)
    
        print(answer)
