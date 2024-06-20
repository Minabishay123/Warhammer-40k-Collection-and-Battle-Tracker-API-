from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import date
from init import db

class Battle(db.Model):
    __tablename__ = "battles"

    id: Mapped[int] = mapped_column(primary_key=True)  # Primary key for the battles table
    date: Mapped[date] = mapped_column()  # Date of the battle
    location: Mapped[str] = mapped_column(String(200))  # Location of the battle
    outcome: Mapped[str] = mapped_column(String(100))  # Outcome of the battle
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # Foreign key linking to users table

    user: Mapped["User"] = relationship("User", back_populates="battles")  # Relationship to User
