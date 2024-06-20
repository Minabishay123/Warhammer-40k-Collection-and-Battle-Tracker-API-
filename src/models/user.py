from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from typing import Optional, List
from init import db

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)  # Primary key for the users table
    email: Mapped[str] = mapped_column(String(200), unique=True)  # User's email, must be unique
    name: Mapped[Optional[str]] = mapped_column(String(100))  # User's name, optional
    password: Mapped[str] = mapped_column(String(200))  # User's password
    is_admin: Mapped[bool] = mapped_column(Boolean(), server_default="false")  # Boolean indicating if user is an admin

    miniatures: Mapped[List["Miniature"]] = relationship("Miniature", back_populates="user")  # Relationship to Miniature
    battles: Mapped[List["Battle"]] = relationship("Battle", back_populates="user")  # Relationship to Battle

