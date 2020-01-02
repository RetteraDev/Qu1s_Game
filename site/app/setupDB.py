from models.Games import *
from app import db


db.drop_all()
db.create_all()
