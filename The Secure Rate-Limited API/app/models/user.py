from sqlalchemy import String, Boolean, Column, Integer
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True , nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    logs = relationship("Log", back_populates="user", cascade="all, delete-orphan")

    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
