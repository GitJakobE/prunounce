import logging
import re

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from ..auth import create_access_token, hash_password, verify_password
from ..database import get_db
from ..dependencies import get_current_user
from ..models import User
from ..rate_limit import check_login_allowed, record_failed_attempt, reset_attempts
from ..schemas import AuthResponse, LoginInput, RegisterInput


router = APIRouter(prefix="/api/auth")
logger = logging.getLogger("pronuncia.auth")


def _to_user_payload(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "displayName": user.display_name,
        "language": user.language,
        "hostId": user.host_id,
    }


def _validate_password_strength(password: str) -> bool:
    return bool(re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", password))


@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterInput, db: Session = Depends(get_db)) -> dict:
    if not _validate_password_strength(payload.password):
        return_error = {
            "errors": [
                {
                    "msg": "Password must be at least 8 characters with uppercase, lowercase, and a digit",
                    "path": "password",
                }
            ]
        }
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=return_error)

    language = payload.language or "en"
    if language not in ["en", "da", "it", "es"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"errors": [{"msg": "Invalid value", "path": "language"}]})

    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists. Try logging in or resetting your password.",
        )

    display_name = payload.displayName
    if not display_name or not display_name.strip():
        display_name = payload.email.split("@")[0]

    user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        language=language,
        display_name=display_name,
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except OperationalError as exc:
        db.rollback()
        logger.error("Registration failed — database write error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Registration is temporarily unavailable. Please try again later.",
        ) from exc

    return {"token": create_access_token(user.id), "user": _to_user_payload(user)}


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginInput, db: Session = Depends(get_db)) -> dict:
    check_login_allowed(payload.email)

    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not user.password_hash:
        record_failed_attempt(payload.email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not verify_password(payload.password, user.password_hash):
        record_failed_attempt(payload.email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    reset_attempts(payload.email)
    return {"token": create_access_token(user.id), "user": _to_user_payload(user)}


@router.get("/me")
def me(current_user: User = Depends(get_current_user)) -> dict:
    return {"user": _to_user_payload(current_user)}


@router.post("/google")
def google_login() -> dict:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Google login not implemented in Python backend yet")
