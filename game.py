import socket
import threading
from time import sleep
from multiprocessing import Lock


lk = Lock()
IN_GAME = False

class Player:

    def __init__(self, name, x=1, y=8) -> None:
        self.name = name
        self.x = x
        self.y = y

class MainPlayer(Player):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.teammates = []

def register():
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 2075))

        nick = input()
        print(nick)
        client_socket.send(nick.encode())
        answer = client_socket.recv(1024)
        if answer != b'0':
            print('close')
            client_socket.close()
        else:
            print('yes')
            return (nick, client_socket)



def client(mp, client_socket):
    global IN_GAME
    def servermessage():
        while True:
            print('WAITING')
            msg = client_socket.recv(1024)
            commands = msg.split(';')

            for msg in commands:
                if not msg or msg == b'leaveroom':
                    break
                if 'newpl' in msg.decode():
                    newplayernick = msg.decode().split(':')[1]
                    mp.teammates.append(Player(newplayernick))
                    print('NEW PLAYER')
                elif 'newpos' in msg.decode():
                    assert len(msg.decode().split(':')) == 4, (msg, False)
                    _, newplayernick, x, y = msg.decode().split(':')
                    print('new pos for ', newplayernick, ':', x, y)
                    
                    for teammate in mp.teammates:
                        if teammate.name == newplayernick:
                            teammate.x, teammate.y = x, y

    threadOn = False
    while True:
        command = input()

        if command == 'createroom':
            threadOn = True
            client_socket.send(b'createroom')
            roompass = client_socket.recv(1024)
            print(roompass)
        elif 'connect' in command:
            client_socket.send(command.encode())
            answer = client_socket.recv(1024)
            if answer == b'0':
                threadOn = True
                players = client_socket.recv(1024).decode().split(';')
                mp.teammates.clear()
                for player in players:
                    mp.teammates.append(Player(player))
            
        if threadOn:
            IN_GAME = True
            th3 = threading.Thread(target=servermessage)
            th3.start()
            th3.join()
            IN_GAME = False

if __name__ == '__main__':
    mp, client_socket = register()
    mp = MainPlayer(mp)

    clientThread = threading.Thread(target=client, args=(mp, client_socket))
    clientThread.start()

    h = len(mp.teammates)
    while True:
        if IN_GAME:
            print('changing pos')
            mp.changepos()
        if len(mp.teammates) != h:
            print(mp.teammates, 'NEW TEAMMATE')
        sleep(10) 





