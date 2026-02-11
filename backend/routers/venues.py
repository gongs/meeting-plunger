import random

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import get_current_user, get_db
from models.user import User
from models.venue import Venue, VenueParticipant
from racing_engine import roll as engine_roll

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

    class Config:
        from_attributes = True


class VenueDetailResponse(BaseModel):
    id: int
    name: str
    participants: list[ParticipantState]


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


@router.post("/{venue_id}/enter")
def enter_venue(
    venue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Enter a venue; creates participant with initial state if not already in."""
    _get_venue_or_404(venue_id, db)
    _ensure_participant(venue_id, current_user, db)
    return {"status": "ok", "venue_id": venue_id}


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
    return VenueDetailResponse(
        id=venue.id,
        name=venue.name,
        participants=[
            ParticipantState(
                user_id=u.id,
                username=u.username,
                position=p.position,
                condition=p.condition,
                mode=p.mode,
                won=p.won,
                game_over=p.game_over,
            )
            for p, u in participants
        ],
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
    participant.position = result["newPosition"]
    participant.condition = result["newCondition"]
    participant.mode = mode
    participant.won = result["won"]
    participant.game_over = result["gameOver"]
    db.commit()
    return RollResponse(
        dice=dice,
        steps=result["steps"],
        newPosition=result["newPosition"],
        newCondition=result["newCondition"],
        won=result["won"],
        gameOver=result["gameOver"],
    )
