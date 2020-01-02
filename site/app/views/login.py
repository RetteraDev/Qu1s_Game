from models.Games import *
from app import *


@login_manager.user_loader
def load_user(name):
    return Users.query.get(name)


@app.route('/', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('game', code=current_user.code))
    
    if request.method == 'POST':

        name = request.form['name']
        code = request.form['code'] 
        
        if bool(Rooms.query.filter_by(code=code).first()):
            if bool(Users.query.filter_by(name=name).first()):
                flash('Имя уже занято', 'danger') 
                
            else:
                player = Users(code, name)
                db.session.add(player)
                db.session.commit()
                login_user(player, remember=True)
                socketio.emit('new_user', current_user.name)
                return redirect(url_for('game', code=code))
            
        else:
            print(Rooms.query.filter_by(code=code).first())
            flash('Неверный код', 'danger')   

    return render_template('login.html')