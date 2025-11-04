from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base
from sqlalchemy import Enum
import enum


class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String(250), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
