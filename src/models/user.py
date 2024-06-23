from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from typing import Optional, List
from marshmallow import fields
from marshmallow.validate import Length

class User(db.Model):
    """
    User model to represent users of the application.

    Attributes:
        id (int): Primary key, unique identifier for the user.
        email (str): Unique email address of the user.
        name (Optional[str]): Optional display name of the user.
        password (str): Hashed password for user authentication.
        is_admin (bool): Flag indicating if the user has administrative privileges.
        collections (List[Collection]): List of collections associated with the user.
        battles (List[Battle]): List of battles associated with the user.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(200))
    is_admin: Mapped[bool] = mapped_column(Boolean(), server_default="false")

    collections: Mapped[List["Collection"]] = relationship(back_populates='user')
    battles: Mapped[List["Battle"]] = relationship(back_populates='user')

class UserSchema(ma.Schema):
    """
    Schema for serializing and validating User data.

    Fields:
        email (Email): Email field for serialization and validation.
        password (String): Password field with validation for minimum length.
    """
    email = fields.Email(required=True)
    password = fields.String(validate=Length(min=8, error='Password must be at least 8 characters long'), required=True)

    class Meta:
        fields = ("id", "email", "name", "password", "is_admin")
