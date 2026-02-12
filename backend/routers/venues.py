import random
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import get_current_user, get_db
from models.user import User
from models.venue import Venue, VenueParticipant, VenueRound, VenueRoundResult
from racing_engine import roll as engine_roll


def _now() -> datetime:
    return datetime.now(timezone.utc)

router = APIRouter(prefix="/venues", tags=["venues"])


class CreateVenueBody(BaseModel):
    name: str


class VenueItem(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ParticipantState(BaseModel):
    user_id: int
    username: str
    position: int
    condition: int
    mode: str
    won: bool
    game_over: bool
    roll_count: int = 0

    class Config:
        from_attributes = True


class RankingItem(BaseModel):
    rank: int
    user_id: int
    username: str
    won: bool
    game_over: bool
    roll_count: int
    duration_seconds: float


class VenueDetailResponse(BaseModel):
    id: int
    name: str
    current_round: int
    round_complete: bool
    participants: list[ParticipantState]
    ranking: list[RankingItem] = []


@router.get("", response_model=list[VenueItem])
def list_venues(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all venues."""
    venues = db.query(Venue).order_by(Venue.id).all()
    return [VenueItem.model_validate(v) for v in venues]


@router.post("", response_model=VenueItem, status_code=status.HTTP_201_CREATED)
def create_venue(
    body: CreateVenueBody,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new venue."""
    venue = Venue(name=body.name)
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return VenueItem.model_validate(venue)


def _get_venue_or_404(venue_id: int, db: Session) -> Venue:
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")
    return venue


def _ensure_venue_round(venue_id: int, db: Session) -> None:
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        return
    existing = (
        db.query(VenueRound)
        .filter(VenueRound.venue_id == venue_id, VenueRound.round_number == venue.current_round)
        .first()
    )
    if not existing:
        db.add(VenueRound(venue_id=venue_id, round_number=venue.current_round, started_at=_now()))
        db.commit()


def _ensure_participant(venue_id: int, user: User, db: Session) -> VenueParticipant:
    participant = (
        db.query(VenueParticipant)
        .filter(VenueParticipant.venue_id == venue_id, VenueParticipant.user_id == user.id)
        .first()
    )
    if not participant:
        participant = VenueParticipant(
            venue_id=venue_id,
            user_id=user.id,
            position=0,
            condition=6,
            mode="normal",
            won=False,
            game_over=False,
        )
        db.add(participant)
        db.commit()
        db.refresh(participant)
    return participant


def _maybe_snapshot_round(venue_id: int, db: Session) -> None:
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        return
    participants = (
        db.query(VenueParticipant, User)
        .join(User, VenueParticipant.user_id == User.id)
        .filter(VenueParticipant.venue_id == venue_id)
        .all()
    )
    if not participants:
        return
    if not all(p.finished_at is not None for p, _ in participants):
        return
    existing = (
        db.query(VenueRoundResult)
        .filter(
            VenueRoundResult.venue_id == venue_id,
            VenueRoundResult.round_number == venue.current_round,
        )
        .first()
    )
    if existing:
        return
    round_row = (
        db.query(VenueRound)
        .filter(
            VenueRound.venue_id == venue_id,
            VenueRound.round_number == venue.current_round,
        )
        .first()
    )
    if not round_row:
        return
    started = round_row.started_at
    if started.tzinfo is None:
        started = started.replace(tzinfo=timezone.utc)
    for p, u in participants:
        fin = p.finished_at
        if fin and fin.tzinfo is None:
            fin = fin.replace(tzinfo=timezone.utc)
        duration = (fin - started).total_seconds() if fin else 0.0
        db.add(
            VenueRoundResult(
                venue_id=venue_id,
                round_number=venue.current_round,
                user_id=u.id,
                username=u.username,
                won=p.won,
                roll_count=p.roll_count,
                duration_seconds=duration,
            )
        )
    db.commit()


@router.post("/{venue_id}/enter")
def enter_venue(
    venue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Enter a venue; creates participant with initial state if not already in."""
    _get_venue_or_404(venue_id, db)
    _ensure_participant(venue_id, current_user, db)
    _ensure_venue_round(venue_id, db)
    return {"status": "ok", "venue_id": venue_id}


def _ranking_for_venue_round(venue_id: int, round_number: int, db: Session) -> list[RankingItem]:
    rows = (
        db.query(VenueRoundResult)
        .filter(
            VenueRoundResult.venue_id == venue_id,
            VenueRoundResult.round_number == round_number,
        )
        .order_by(VenueRoundResult.roll_count.asc(), VenueRoundResult.duration_seconds.asc())
        .all()
    )
    return [
        RankingItem(
            rank=i + 1,
            user_id=r.user_id,
            username=r.username,
            won=r.won,
            game_over=not r.won,
            roll_count=r.roll_count,
            duration_seconds=r.duration_seconds,
        )
        for i, r in enumerate(rows)
    ]


@router.get("/{venue_id}", response_model=VenueDetailResponse)
def get_venue(
    venue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get venue and all participants (user must be in venue)."""
    venue = _get_venue_or_404(venue_id, db)
    participant = (
        db.query(VenueParticipant)
        .filter(VenueParticipant.venue_id == venue_id, VenueParticipant.user_id == current_user.id)
        .first()
    )
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not in this venue; enter first",
        )
    participants = (
        db.query(VenueParticipant, User)
        .join(User, VenueParticipant.user_id == User.id)
        .filter(VenueParticipant.venue_id == venue_id)
        .all()
    )
    round_complete = False
    ranking: list[RankingItem] = []
    if participants and all(p.finished_at is not None for p, _ in participants):
        has_results = (
            db.query(VenueRoundResult)
            .filter(
                VenueRoundResult.venue_id == venue_id,
                VenueRoundResult.round_number == venue.current_round,
            )
            .first()
        )
        if has_results:
            round_complete = True
            ranking = _ranking_for_venue_round(venue_id, venue.current_round, db)
    return VenueDetailResponse(
        id=venue.id,
        name=venue.name,
        current_round=venue.current_round,
        round_complete=round_complete,
        participants=[
            ParticipantState(
                user_id=u.id,
                username=u.username,
                position=p.position,
                condition=p.condition,
                mode=p.mode,
                won=p.won,
                game_over=p.game_over,
                roll_count=p.roll_count,
            )
            for p, u in participants
        ],
        ranking=ranking,
    )


class RollBody(BaseModel):
    mode: str = "normal"


class RollResponse(BaseModel):
    dice: int
    steps: int
    newPosition: int
    newCondition: int
    won: bool
    gameOver: bool


@router.post("/{venue_id}/roll", response_model=RollResponse)
def roll_dice(
    venue_id: int,
    body: RollBody,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Roll dice (1-6 from server), apply rules, update participant state. Requires being in venue and not won/game_over."""
    _get_venue_or_404(venue_id, db)
    participant = (
        db.query(VenueParticipant)
        .filter(VenueParticipant.venue_id == venue_id, VenueParticipant.user_id == current_user.id)
        .first()
    )
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not in this venue; enter first",
        )
    if participant.won:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already won")
    if participant.game_over:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game over")
    mode = body.mode if body.mode in ("normal", "super") else "normal"
    dice = random.randint(1, 6)
    result = engine_roll(
        position=participant.position,
        condition=participant.condition,
        mode=mode,
        dice=dice,
    )
    participant.roll_count += 1
    participant.position = result["newPosition"]
    participant.condition = result["newCondition"]
    participant.mode = mode
    participant.won = result["won"]
    participant.game_over = result["gameOver"]
    if result["won"] or result["gameOver"]:
        if participant.finished_at is None:
            participant.finished_at = _now()
    db.commit()
    _maybe_snapshot_round(venue_id, db)
    return RollResponse(
        dice=dice,
        steps=result["steps"],
        newPosition=result["newPosition"],
        newCondition=result["newCondition"],
        won=result["won"],
        gameOver=result["gameOver"],
    )


class RoundItem(BaseModel):
    round_number: int
    started_at: str


@router.post("/{venue_id}/start_new_race")
def start_new_race(
    venue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Start a new race (only when current round is complete). Resets all participants."""
    venue = _get_venue_or_404(venue_id, db)
    participant = (
        db.query(VenueParticipant)
        .filter(VenueParticipant.venue_id == venue_id, VenueParticipant.user_id == current_user.id)
        .first()
    )
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not in this venue; enter first",
        )
    participants = (
        db.query(VenueParticipant).filter(VenueParticipant.venue_id == venue_id).all()
    )
    if not participants or not all(p.finished_at is not None for p in participants):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Round not complete; all participants must finish first",
        )
    has_results = (
        db.query(VenueRoundResult)
        .filter(
            VenueRoundResult.venue_id == venue_id,
            VenueRoundResult.round_number == venue.current_round,
        )
        .first()
    )
    if not has_results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Round not complete",
        )
    new_round = venue.current_round + 1
    db.add(VenueRound(venue_id=venue_id, round_number=new_round, started_at=_now()))
    venue.current_round = new_round
    for p in participants:
        p.position = 0
        p.condition = 6
        p.mode = "normal"
        p.won = False
        p.game_over = False
        p.roll_count = 0
        p.finished_at = None
    db.commit()
    return {"current_round": new_round}


@router.get("/{venue_id}/rounds")
def list_rounds(
    venue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List past rounds for this venue."""
    venue = _get_venue_or_404(venue_id, db)
    _ = (
        db.query(VenueParticipant)
        .filter(VenueParticipant.venue_id == venue_id, VenueParticipant.user_id == current_user.id)
        .first()
    )
    if not _:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not in this venue; enter first",
        )
    rounds = (
        db.query(VenueRound)
        .filter(VenueRound.venue_id == venue_id)
        .order_by(VenueRound.round_number.asc())
        .all()
    )
    return [
        RoundItem(
            round_number=r.round_number,
            started_at=r.started_at.isoformat() if r.started_at else "",
        )
        for r in rounds
    ]


@router.get("/{venue_id}/rounds/{round_number}/results")
def get_round_results(
    venue_id: int,
    round_number: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get ranking results for a specific round."""
    venue = _get_venue_or_404(venue_id, db)
    _ = (
        db.query(VenueParticipant)
        .filter(VenueParticipant.venue_id == venue_id, VenueParticipant.user_id == current_user.id)
        .first()
    )
    if not _:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not in this venue; enter first",
        )
    return _ranking_for_venue_round(venue_id, round_number, db)
