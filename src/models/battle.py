from db.config import db
from app import ma

class Battle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    opponent_name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    outcome = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120))
    notes = db.Column(db.Text)
    
class BattleSchema(ma.Schema):
    id = ma.Int(dump_only=True)
    user_id = ma.Int(required=True)
    opponent_name = ma.Str(required=True)
    date = ma.Date(required=True)
    outcome = ma.Str(required=True)
    location = ma.Str()
    notes = ma.Str()
