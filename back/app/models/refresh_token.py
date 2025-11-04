from sqlalchemy import ForeignKey, DateTime, func
from models.base import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    revoked: Mapped[bool] = mapped_column(default=False)
    
    user: Mapped["User"] = relationship("User")