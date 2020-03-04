from socketIO_client import SocketIO
import threading


players = []
room_code = ''
        
class Socket(threading.Thread):
    
    def __init__(self, queue):
        
        self.socketIO = SocketIO('192.168.43.217', 8080)
        
        self.socketIO.emit('new_room')
        self.socketIO.on('get_room_code', self.get_room_code)
        self.socketIO.on('new_user', self.new_user)
        self.socketIO.on('left_user', self.left_user)
        self.socketIO.on('new_answer_to_game', self.new_answer)
        
        self.queue = queue
        self.running = True
    
    def run(self):
        while self.running:
            self.socketIO.wait() 
    
    def get_room_code(self, code):
        print(code)
        self.queue.put({'code':code}) 


    def new_user(self, name):
        if name not in players:
            players.append(name)
            self.queue.put({'players':players})

    def left_user(self, name):
        if name in players:
            players.remove(name)
            self.queue.put({'players':players})
    
    def new_answer(self, answer):
        self.queue.put({'answer':answer})
    
    def terminate(self):
        self.running = False
    
    @staticmethod
    def test(f):
        print("SOCKET:",f)