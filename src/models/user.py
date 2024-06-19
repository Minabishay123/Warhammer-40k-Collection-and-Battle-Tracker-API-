from extensions import db, bcrypt
from sqlalchemy.orm import validates 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    collections = db.relationship('Collection', backref='user', lazy=True)
    battles = db.relationship('Battle', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username must not be empty')
        return username