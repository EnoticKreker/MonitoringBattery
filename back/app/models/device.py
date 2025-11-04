from sqlalchemy import String, DateTime, func
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from datetime import datetime


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(150), nullable=False, unique=True, index=True)
    version: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[bool] = mapped_column(nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    batteries: Mapped[list["Battery"]] = relationship(
        back_populates="device",
        cascade="save-update",
        lazy="selectin"
    )
