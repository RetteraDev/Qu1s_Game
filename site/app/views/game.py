from models.Games import *
from app import *


@app.route('/game/<code>', methods = ['GET', 'POST'])
def game(code):
    
    if current_user.is_anonymous:
        flash('Вы не представились', 'danger')
        return redirect(url_for('login'))
    
    elif current_user.code != code:
        flash('Вас нет в этой комнате', 'danger')
        new_user()
        return redirect(url_for('login'))
    
    elif bool(Rooms.query.filter_by(code=code).first()):
        return render_template('game.html')
    else:
        return redirect(url_for('login'))

