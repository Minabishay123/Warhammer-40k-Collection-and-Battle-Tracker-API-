from db.config import db
from app import ma

class Miniature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    faction = db.Column(db.String(80), nullable=False)
    unit_type = db.Column(db.String(80), nullable=False)
    points_cost = db.Column(db.Integer, nullable=False)

class MiniatureSchema(ma.Schema):
    id = ma.Int(dump_only=True)
    user_id = ma.Int(required=True)
    name = ma.Str(required=True)
    faction = ma.Str(required=True)
    unit_type = ma.Str(required=True)
    points_cost = ma.Int(required=True)
