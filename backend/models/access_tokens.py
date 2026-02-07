from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class AccessToken(Base):
    __tablename__ = "access_tokens"

    token: Mapped[str] = mapped_column(String, primary_key=True)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
