import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import create_token, get_current_user, get_db, hash_password, verify_password
from models.access_tokens import AccessToken
from models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


class MeResponse(BaseModel):
    id: int
    username: str


class RegisterBody(BaseModel):
    username: str
    password: str


class LoginBody(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str


@router.get("/me", response_model=MeResponse)
def me(current_user: User = Depends(get_current_user)):
    """Return current user id and username."""
    return MeResponse(id=current_user.id, username=current_user.username)


@router.post("/register", response_model=TokenResponse)
def register(body: RegisterBody, db: Session = Depends(get_db)):
    """Register a new user. Returns 409 if username already exists."""
    try:
        existing = db.query(User).filter(User.username == body.username).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="用户名已存在",
            )
        user = User(
            username=body.username,
            password_hash=hash_password(body.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_token()
        db.add(AccessToken(token=token, user_id=user.id))
        db.commit()
        return TokenResponse(token=token)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Registration failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册失败，请查看后端日志或确认已安装依赖 (pip install -r requirements.txt)",
        ) from e


@router.post("/login", response_model=TokenResponse)
def login(body: LoginBody, db: Session = Depends(get_db)):
    """Login with username and password."""
    user = db.query(User).filter(User.username == body.username).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_token()
    db.add(AccessToken(token=token, user_id=user.id))
    db.commit()
    return TokenResponse(token=token)
