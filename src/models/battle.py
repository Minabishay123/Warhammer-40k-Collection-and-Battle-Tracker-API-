from sqlalchemy import Column, Integer, String, ForeignKey
from ..extensions import db

class Battle(db.Model):
    __tablename__ = 'battles'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    result = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    collection_id = Column(Integer, ForeignKey('collections.id'), nullable=False)
