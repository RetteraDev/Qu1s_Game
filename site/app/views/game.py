from flask_socketio import join_room, leave_room
from flask_login import login_required
from random import randint
from models.Games import *
from app import *

@app.route('/game/<code>', methods = ['GET', 'POST'])
def game(code):
    
    if current_user.is_anonymous:
        flash('Вы не представились', 'danger')
        return redirect(url_for('login'))
    
    elif current_user.code != code:
        flash('Вас нет в этой комнате', 'danger')
        return redirect(url_for('login'))
    
    elif bool(Rooms.query.filter_by(code=code).first()):
        join_room(code, sid = current_user.name, namespace='/')
        socketio.emit('new_user', current_user.name, room=str(code))
        return render_template('game.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    leave_room(str(current_user.code), sid = current_user.name, namespace='/')
    socketio.emit('left_user', current_user.name, room=str(current_user.code))
    db.session.delete(Users.query.filter_by(name=current_user.name).first())
    db.session.commit()
    logout_user()
    
    flash('Вы вышли', 'success')
    return redirect(url_for('login'))
 
@socketio.on('join')
def on_join(data):
    name = str(data['name'])
    room = str(data['room'])
    join_room(room)
    print(data)
    send(name + ' has entered the room.', room=room)
    
@socketio.on('task')
def task(a):
    emit("task_browser", a, broadcast=True, room = a['room'])
    
@socketio.on('send message')
def aaa(a):
    emit('message', a, broadcast = True, room = str(current_user.code))
