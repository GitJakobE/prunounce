from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user_id
from ..hosts import get_host
from ..models import User, Word
from ..services.tts import get_audio_path


router = APIRouter(prefix="/api/audio")


def get_target_example(word: Word) -> str:
    if word.language == "da":
        return word.example_da
    if word.language == "en":
        return word.example_en
    return word.example_it


def resolve_host_voice(user_id: str, db: Session) -> tuple[str, str]:
    user = db.query(User).filter(User.id == user_id).first()
    host_id = user.host_id if user and user.host_id else "marco"
    host = get_host(host_id)
    return host["id"], host["voice"]["voiceName"]


@router.get("/{word_id}")
def word_audio(
    word_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> FileResponse:
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Word not found")

    host_id, voice_name = resolve_host_voice(user_id, db)
    host = get_host(host_id)
    if host["language"] != word.language:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Word language does not match your host language.")

    audio_path = get_audio_path(word.word, None, host_id, voice_name)
    if not audio_path:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pronunciation temporarily unavailable. Please try again shortly.",
        )

    return FileResponse(
        path=str(audio_path),
        media_type="audio/mpeg",
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )


@router.get("/{word_id}/example")
def example_audio(
    word_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> FileResponse:
    word = db.query(Word).filter(Word.id == word_id).first()
    target_example = get_target_example(word) if word else ""
    if not word or not target_example:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Example not found")

    host_id, voice_name = resolve_host_voice(user_id, db)
    host = get_host(host_id)
    if host["language"] != word.language:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Word language does not match your host language.")

    audio_path = get_audio_path(f"ex_{word.word}_{word.language}", target_example, host_id, voice_name)
    if not audio_path:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Audio temporarily unavailable.")

    return FileResponse(
        path=str(audio_path),
        media_type="audio/mpeg",
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )
