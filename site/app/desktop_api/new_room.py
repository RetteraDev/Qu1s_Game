from flask_socketio import join_room
from models.Games import Rooms
from app import *
from random import randint

@socketio.on('new_room')
def new_room():
    
    code = randint(1000, 9999)
    join_room(str(code))
    
    db.session.add(Rooms(code))
    db.session.commit()
    emit('get_code', code)
