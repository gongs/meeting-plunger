from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    current_round: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    participants = relationship("VenueParticipant", back_populates="venue")
    rounds = relationship("VenueRound", back_populates="venue")


class VenueParticipant(Base):
    __tablename__ = "venue_participants"
    __table_args__ = (UniqueConstraint("venue_id", "user_id", name="uq_venue_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    condition: Mapped[int] = mapped_column(Integer, default=6, nullable=False)
    mode: Mapped[str] = mapped_column(String(16), default="normal", nullable=False)
    won: Mapped[bool] = mapped_column(default=False, nullable=False)
    game_over: Mapped[bool] = mapped_column(default=False, nullable=False)
    roll_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    venue = relationship("Venue", back_populates="participants")
    user = relationship("User", back_populates="venue_participations")


class VenueRound(Base):
    __tablename__ = "venue_rounds"
    __table_args__ = (UniqueConstraint("venue_id", "round_number", name="uq_venue_round"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), nullable=False, index=True)
    round_number: Mapped[int] = mapped_column(Integer, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    venue = relationship("Venue", back_populates="rounds")


class VenueRoundResult(Base):
    __tablename__ = "venue_round_results"
    __table_args__ = (UniqueConstraint("venue_id", "round_number", "user_id", name="uq_venue_round_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), nullable=False, index=True)
    round_number: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    won: Mapped[bool] = mapped_column(default=False, nullable=False)
    roll_count: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_seconds: Mapped[float] = mapped_column(nullable=False)

    venue = relationship("Venue")
    user = relationship("User")
