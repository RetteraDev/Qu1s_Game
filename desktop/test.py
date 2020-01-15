from socketIO_client import SocketIO
import requests, time

socketIO = SocketIO('192.168.43.217', 8080) 
    
players = []
submit_code = ''

def new_user(name):
    if name not in players:
        players.append(name)
        print(f'[{name}] connected to the room')

def left_user(name):
    if name in players:
        players.remove(name)
        print(f'[{name}] left')

def get_code(code):
    submit_code = code
    print('code =', code)


socketIO.emit('new_room')
socketIO.on('get_code', get_code)
socketIO.on('new_user', new_user)
socketIO.on('left_user', left_user)

socketIO.wait()
