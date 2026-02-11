from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class AccessToken(Base):
    __tablename__ = "access_tokens"

    token: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
