from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from datetime import date
from marshmallow import fields
from typing import Optional

class Battle(db.Model):
    """
    Battle model to represent battles recorded by the user.

    Attributes:
        id (int): Primary key, unique identifier for the battle.
        opponent (str): Name of the opponent.
        description (Optional[str]): Optional description of the battle.
        date (date): Date of the battle.
        result (str): Result of the battle.
        user_id (int): Foreign key linking to the user who recorded the battle.
        user (User): Reference to the user who recorded the battle.
    """
    __tablename__ = "battles"

    id: Mapped[int] = mapped_column(primary_key=True)
    opponent: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    date: Mapped[date] 
    result: Mapped[str] = mapped_column(String(50))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="battles")

class BattleSchema(ma.Schema):
    """
    Schema for serializing and validating Battle data.

    Fields:
        opponent (String): Opponent field for serialization and validation.
        description (String): Description field for serialization.
        date (Date): Date field for serialization and validation.
        result (String): Result field for serialization and validation.
        user (Nested): Nested User schema for reference.
    """
    opponent = fields.String(required=True)
    description = fields.String()
    date = fields.Date(required=True)
    result = fields.String(required=True)
    user = fields.Nested("UserSchema", exclude=['password'])

    class Meta:
        fields = ("id", "opponent", "description", "date", "result", "user")
