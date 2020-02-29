from models.Games import Rooms, Users
from app import db


db.drop_all()
db.create_all()
