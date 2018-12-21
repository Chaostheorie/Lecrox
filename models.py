# db_creator.py
from app import db

# Content tables
class snippets(db.Model):
    __tablename__ = "snippets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    content = db.Column(db.String)
    description = db.Column(db.String)

class plans(db.Model):
# here will plans go
    __tablename__ = "plans"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

# create tables
db.create_all()

# Auth is made with flask_sqlalchemy, because flask_user specify that
