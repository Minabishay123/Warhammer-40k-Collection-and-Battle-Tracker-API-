from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from models.user import User

class Collection(db.Model):
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user = relationship('User', back_populates='collections')
    battles = relationship('Battle', back_populates='collection')

class CollectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Collection
        load_instance = True
