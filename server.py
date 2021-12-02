import socket
import asyncio
from time import sleep
import threading
from select import select


def server():
    
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('', 2060))
    server_sock.listen()
    while True:
        yield ('read', server_sock)
        sock, addr = server_sock.accept()
        tasks.append(client(sock))

def client(sock):
    
    while True:
        yield ('read', sock)
        msg = sock.recv(1024)
        if msg:
            print('NEW MSG:', msg.decode())

        yield ('write', sock)
        sock.send(msg)

def event_loop():

    while True:
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
            
        try:
            task = tasks.pop(0)
            reason, sock = next(task)

            if reason == 'read':
                to_read[sock] = task
            elif reason == 'write':
                to_write[sock] = task
        except StopIteration:
            pass

if __name__ == '__main__':

    tasks = [server()]
    to_read = {}
    to_write = {}

    threading.Thread(target = event_loop).start()


