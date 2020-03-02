from socketIO_client import SocketIO
import threading


players = []
room_code = ''
        
class Socket(threading.Thread):
    
    def __call__(self):
        
        socketIO = SocketIO('192.168.43.217', 8080)
        
        socketIO.emit('new_room')
        socketIO.on('get_room_code', self.get_room_code)
        socketIO.on('new_user', self.new_user)
        socketIO.on('left_user', self.left_user)
        socketIO.wait() 

        
    def __init__(self, queue):
        self.queue = queue

    
    def get_room_code(self, code):
        print(code)
        self.queue.put({'code':code}) 


    def new_user(self, name):
        if name not in players:
            players.append(name)
            self.queue.put({'players':players})
            #print(f'[{name} joined room {room_code}]')

    def left_user(self, name):
        if name in players:
            players.remove(name)
            self.queue.put({'players':players})
            #print(f'[{name} exit room {room_code}]')
    
    @staticmethod
    def test(f):
        print("SOCKET:",f)