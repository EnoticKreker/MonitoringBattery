from typing import Optional
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Battery(Base):
    __tablename__ = "batteries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    voltage: Mapped[Optional[str]] = mapped_column(Text, nullable=False)
    residual_capacity: Mapped[Optional[str]
                              ] = mapped_column(Text, nullable=False)
    lifetime: Mapped[str] = mapped_column(
        String(300), nullable=False)

    device_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("devices.id", ondelete="SET NULL"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    device: Mapped["Device"] = relationship(
        back_populates="batteries", lazy="selectin")
