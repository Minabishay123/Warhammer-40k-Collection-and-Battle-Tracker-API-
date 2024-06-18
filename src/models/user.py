from db.config import db
from sqlalchemy.orm import relationship
from app import ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    miniatures = relationship('Miniature', backref='user', lazy=True)
    battles = relationship('Battle', backref='user', lazy=True)
    
class UserSchema(ma.Schema):
    id = ma.Int(dump_only=True)
    username = ma.Str(required=True)
    email = ma.Email(required=True)
    password = ma.Str(load_only=True)
