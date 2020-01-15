from desktop_api import new_room, get_stat
from views import login, game
from secret import secret_key
from app import *


if __name__ == "__main__":
    
    app.secret_key = secret_key
    socketio.run(app, debug=True, host='192.168.43.217', port='8080')     
