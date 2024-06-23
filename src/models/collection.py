from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from marshmallow import fields

class Collection(db.Model):
    """
    Collection model to represent user's collection of Warhammer miniatures.

    Attributes:
        id (int): Primary key, unique identifier for the collection.
        name (str): Name of the collection.
        count (int): Number of miniatures in the collection.
        user_id (int): Foreign key linking to the user who owns the collection.
        user (User): Reference to the user who owns the collection.
    """
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    count: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    user: Mapped["User"] = relationship(back_populates="collections")

class CollectionSchema(ma.Schema):
    """
    Schema for serializing and validating Collection data.

    Fields:
        name (String): Name field for serialization and validation.
        count (Integer): Count field for serialization and validation.
        user (Nested): Nested User schema for reference.
    """
    name = fields.String(required=True)
    count = fields.Integer(required=True)
    user = fields.Nested("UserSchema", exclude=['password'])

    class Meta:
        fields = ("id", "name", "count", "user")
