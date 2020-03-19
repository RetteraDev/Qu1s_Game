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
        join_room(str(code), sid = current_user.name, namespace='/')
        socketio.emit('new_user', current_user.name, room=str(code))
        return render_template('game.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    
    if current_user.is_anonymous:
        current_user.authenticated = False
        return redirect(url_for('login'))
    else:
        leave_room(str(current_user.code), sid = current_user.name, namespace='/')
        socketio.emit('left_user', current_user.name, room=str(current_user.code))
        db.session.delete(Users.query.filter_by(name=current_user.name).first())
        db.session.commit()
        current_user.authenticated = False
        logout_user()
        
        flash('Вы вышли', 'success')
        return redirect(url_for('login'))

# Игрок заходит в комнату
@socketio.on('join')
def on_join(data):
    name = str(data['name'])
    room = str(data['room'])
    join_room(room)

# Задания приходят в комнату
@socketio.on('new_task_from_game')
def new_task_from_game(a):
    emit("new_task_to_player", a, broadcast=True, room = a['room'])

# Задания приходят в игровой клиент
@socketio.on('new_answer_from_player')
def new_answer_from_player(a):
    emit('new_answer_to_game', a, broadcast = True, room = str(current_user.code))
