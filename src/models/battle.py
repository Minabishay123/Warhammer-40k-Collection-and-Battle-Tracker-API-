from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, ForeignKey
from models.user import User
from models.collection import Collection

class Battle(db.Model):
    __tablename__ = "battles"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[Date] = mapped_column()
    opponent: Mapped[str] = mapped_column(String(100))
    outcome: Mapped[str] = mapped_column(String(100))
    collection_id: Mapped[int] = mapped_column(ForeignKey('collections.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    collection = relationship('Collection', back_populates='battles')
    user = relationship('User', back_populates='battles')

class BattleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Battle
        load_instance = True
