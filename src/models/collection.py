from extensions import db
from sqlalchemy.orm import validates

class collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name must not be empty')
        return name