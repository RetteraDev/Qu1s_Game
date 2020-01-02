from socketIO_client import SocketIO, LoggingNamespace
import requests, time

socketIO = SocketIO('192.168.43.217', 8080)   

players = []
submit_code = ''

def new_user(name,code):
    print(name)
    if name not in players:
        players.append(name)
        print(f'[{name}] connected to the room')

def get_code(code):
    submit_code = code
    print('code =', code)


socketIO.emit('new_room')
socketIO.on('get_code', get_code)
socketIO.on('new_user', new_user)

socketIO.wait()



