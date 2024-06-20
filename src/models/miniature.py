from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from init import db

class Miniature(db.Model):
    __tablename__ = "miniatures"

    id: Mapped[int] = mapped_column(primary_key=True)  # Primary key for the miniatures table
    name: Mapped[str] = mapped_column(String(100))  # Miniature's name
    faction: Mapped[str] = mapped_column(String(100))  # Miniature's faction
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # Foreign key linking to users table

    user: Mapped["User"] = relationship("User", back_populates="miniatures")  # Relationship to User

