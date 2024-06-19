from extensions import db
from sqlalchemy.orm import validates    

class Battle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opponent = db.Column(db.String(80), nullable=False)
    result = db.Column(db.String(30), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @validates('opponent', 'result')
    def validate_opponent(self, key, value):
        if not value:
            raise ValueError(f"{key} must not be empty")
        return value