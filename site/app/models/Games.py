from flask_login import UserMixin
from app import *


class Rooms(db.Model):
    
    code = db.Column(db.String(4), nullable = False, primary_key = True, unique = True)
    
    def __init__(self, code):
        self.code = code
    
    
class Users(db.Model, UserMixin):

    id     = db.Column(db.Integer, primary_key = True, autoincrement = True)
    code   = db.Column(db.String(4), nullable = False)
    name   = db.Column(db.String(50), nullable = False, unique = True)
    score  = db.Column(db.Integer)
    answer = db.Column(db.String(100))


    def __init__(self, code, name):
        self.code  = code
        self.name  = name
        self.score = 0
        self.answer = ''