from socketIO_client import SocketIO
from threading import Thread


class Socket(Thread):
    
    def __init__(self, queue):
        
        Thread.__init__(self)
        self.socketIO = SocketIO('192.168.43.217', 8080)
        
        self.socketIO.emit('new_room')
        self.socketIO.on('get_room_code', self.get_room_code)
        self.socketIO.on('new_user', self.new_user)
        self.socketIO.on('left_user', self.left_user)
        self.socketIO.on('new_answer_to_game', self.new_answer)
        
        self.queue = queue
        self.players = []
        self.stop = False
    
    def run(self):
        while True:
            if self.stop:
                return
            self.socketIO.wait(seconds=1) 

    def get_room_code(self, code):
        print(code)
        self.room_code = str(code)
        self.queue.put({'code':code}) 

    def new_user(self, name):
        if name not in self.players:
            self.players.append(name)
            self.queue.put({'players' : self.players})

    def left_user(self, name):
        if name in self.players:
            self.players.remove(name)
            self.queue.put({'players' : self.players})

    def new_answer(self, answer):
        self.queue.put({'answer' : answer})
    
    def close_room(self):
        self.socketIO.emit('close_room', self.room_code)
        self.stop = True
