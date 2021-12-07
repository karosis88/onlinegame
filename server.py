import asyncio
import socket
import threading
from select import select
from time import sleep
import roompass

players = {}

class Player:

    def __init__(self, nick, sock) -> None:
        self.sock = sock
        self.nick = nick
        self.room = None

    def posUpdate(self, x, y) -> None:
        for player in self.room.players:
            if not (player is self):
                player.sock.send(f"newpos:{self.nick}:{x}:{y}".encode())

    def newPlayer(self) -> None:
        print('sendind teammates', self.nick, self.room.players)
        for player in self.room.players:
            if not (player is self):
                player.sock.send(f"newpl:{self.nick}".encode())
                print('sended')

class Room:
    all_rooms = {}

    def __init__(self, leader : Player, maxplayers=4) -> None:
        self.leader : Player = leader
        self.players = [leader]
        self.maxplayers = maxplayers
        self.pas = roompass.roompass()
        self.all_rooms[self.pas] = self             

def server():
    
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('', 2075))
    server_sock.listen()
    while True:
        yield ('read', server_sock)
        sock, addr = server_sock.accept()
        yield ('read', sock)
        nick = sock.recv(1024).decode()
        yield ('write', sock)
        if nick not in players:
            sock.send(b'0')
        else:
            sock.send(b'1')
        players[nick] = Player(nick, sock)
        tasks.append(client(sock, players[nick]))

def client(sock, player):

    while True:
        yield ('read', sock)
        msg = sock.recv(1024).decode()
        if msg:
            print(msg)
            if msg == 'createroom':
                print('newroom')
                newRoom = Room(player)
                sock.send(newRoom.pas.encode())
                player.room = newRoom
            elif 'connect' in msg:
                roomCode = msg.split(':')[1]
                if roomCode in Room.all_rooms:
                    if len(Room.all_rooms[roomCode].players) < Room.all_rooms[roomCode].maxplayers:
                        Room.all_rooms[roomCode].players.append(player)
                        player.room = Room.all_rooms[roomCode]
                        sock.send(b'0')
                        sock.send(
                            ';'.join(pl.nick for pl in player.room.players if not (pl is player)).encode()
                        )
                        print('NEWPL')
                        player.newPlayer()
                    else:
                        sock.send(b'1')
            elif 'newpos' in msg:
                _, x, y = msg.split(':')
                player.posUpdate(x, y)
            else:
                sock.send(b'1')
        else:
            yield ('exit', None)

      

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
            try:
                reason, sock = next(task)
            except ConnectionError:
                continue

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


