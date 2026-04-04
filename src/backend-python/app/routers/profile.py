from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..hosts import HOST_IDS, get_host
from ..models import User, UserProgress, Word
from ..schemas import ProfileUpdateInput


router = APIRouter(prefix="/api/profile")


def _to_user_payload(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "displayName": user.display_name,
        "language": user.language,
        "hostId": user.host_id,
    }


@router.get("")
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    target_lang = get_host(current_user.host_id or "marco")["language"]

    total_words = db.query(func.count(Word.id)).filter(Word.language == target_lang).scalar() or 0
    listened_words = (
        db.query(func.count(UserProgress.id))
        .join(Word, Word.id == UserProgress.word_id)
        .filter(UserProgress.user_id == current_user.id, Word.language == target_lang)
        .scalar()
        or 0
    )

    return {
        "user": {
            **_to_user_payload(current_user),
            "createdAt": current_user.created_at,
        },
        "progress": {"totalWords": int(total_words), "listenedWords": int(listened_words)},
    }


@router.patch("")
def update_profile(
    payload: ProfileUpdateInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    updated = False

    if payload.displayName is not None:
        current_user.display_name = payload.displayName
        updated = True

    if payload.language is not None:
        if payload.language not in ["en", "da", "it", "es"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No valid fields to update")
        current_user.language = payload.language
        updated = True

    if payload.hostId is not None:
        if payload.hostId not in HOST_IDS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No valid fields to update")
        current_user.host_id = payload.hostId
        updated = True

    if not updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No valid fields to update")

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"user": _to_user_payload(current_user)}


@router.delete("")
def delete_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    db.delete(current_user)
    db.commit()
    return {"message": "Account and all associated data deleted"}
