from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..extensions import db

class Collection(db.Model):
    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    battles = relationship('Battle', backref='collection', lazy=True)
