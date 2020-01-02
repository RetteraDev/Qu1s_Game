from models.Games import *
from app import *
import time

@app.route('/get_stat/<code>', methods = ['GET','POST'])
def get_stat(code):

    time.sleep(1)
    response = {}
    users = Users.query.filter_by(code=code).all()

    for i in range(len(users)):
        user = users[i]
        response[i] = {'name'  : user.name,
                       'score' : user.score,
                       'answer': user.answer}
    return response
