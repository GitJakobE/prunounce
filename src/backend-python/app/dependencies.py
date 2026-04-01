from fastapi import Depends, Request
from sqlalchemy.orm import Session

from .auth import decode_token, get_request_token
from .database import get_db
from .models import User


def get_current_user_id(request: Request) -> str:
    token = get_request_token(request)
    return decode_token(token)


def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
