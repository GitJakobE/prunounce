import json
import math

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user_id
from ..hosts import get_host
from ..models import Story, StoryAudio, User
from ..schemas import StoryDetail, StoryDetailResponse, StoryListItem, StoriesResponse
from ..services.story_audio import STORY_SPEED_TO_RATE
from ..utils.dialogue import parse_dialogue_body

router = APIRouter(prefix="/api/stories")

SUPPORTED_LANGS = ["en", "da", "it"]
DIFFICULTY_ORDER = ["beginner", "intermediate", "advanced"]
# Average words per minute for language learners
_WPM = 150

def _reading_time(body: str) -> int:
    """Return estimated reading time in whole minutes (minimum 1)."""
    word_count = len(body.split())
    return max(1, math.ceil(word_count / _WPM))


def _get_description(story: Story, ref_lang: str) -> str:
    if ref_lang == "it":
        return story.description_it
    if ref_lang == "da":
        return story.description_da
    return story.description_en


def _resolve_target_lang(user_id: str, db: Session) -> str:
    user = db.query(User).filter(User.id == user_id).first()
    host_id = (user.host_id if user and user.host_id else "marco")
    return get_host(host_id)["language"]


def _resolve_ref_lang(target_lang: str, user_id: str | None = None, db: Session | None = None) -> str:
    """Reference language from the user's profile, falling back to a sensible default."""
    if user_id and db:
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.language in SUPPORTED_LANGS and user.language != target_lang:
            return user.language
    return "da" if target_lang == "en" else "en"


@router.get("/{story_id}/audio")
def story_audio(
    story_id: str,
    speed: str = Query(default="normal"),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> Response:
    """Stream story narration audio at a given speed. Speed must be one of: very_slow, slow, normal, fast, very_fast."""
    if speed not in STORY_SPEED_TO_RATE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid speed '{speed}'. Must be one of: {', '.join(STORY_SPEED_TO_RATE)}",
        )

    target_lang = _resolve_target_lang(user_id, db)

    story = db.query(Story).filter(Story.id == story_id).first()
    if not story or story.language != target_lang:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    story_audio_record = (
        db.query(StoryAudio)
        .filter(StoryAudio.story_id == story.id, StoryAudio.speed == speed)
        .first()
    )
    if not story_audio_record:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Story audio has not been pre-generated yet.",
        )

    return Response(
        content=story_audio_record.audio_bytes,
        media_type=story_audio_record.mime_type,
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )


@router.get("", response_model=StoriesResponse)
def list_stories(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    target_lang = _resolve_target_lang(user_id, db)
    ref_lang = _resolve_ref_lang(target_lang, user_id, db)

    stories = (
        db.query(Story)
        .filter(Story.language == target_lang)
        .order_by(Story.order.asc())
        .all()
    )

    grouped: dict[str, list[StoryListItem]] = {d: [] for d in DIFFICULTY_ORDER}
    for story in stories:
        speakers = json.loads(story.speakers) if story.speakers else None
        item = StoryListItem(
            id=story.id,
            slug=story.slug,
            language=story.language,
            difficulty=story.difficulty,
            length=story.length,
            title=story.title,
            description=_get_description(story, ref_lang),
            estimatedReadingTime=_reading_time(story.body),
            format=story.format,
            speakers=speakers,
        )
        if story.difficulty in grouped:
            grouped[story.difficulty].append(item)

    return {"stories": grouped}


@router.get("/{story_id}", response_model=StoryDetailResponse)
def get_story(
    story_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    target_lang = _resolve_target_lang(user_id, db)
    ref_lang = _resolve_ref_lang(target_lang, user_id, db)

    story = db.query(Story).filter(Story.id == story_id).first()
    if not story or story.language != target_lang:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    speakers = json.loads(story.speakers) if story.speakers else None
    segments = parse_dialogue_body(story.body, story.format)

    return {
        "story": StoryDetail(
            id=story.id,
            slug=story.slug,
            language=story.language,
            difficulty=story.difficulty,
            length=story.length,
            title=story.title,
            description=_get_description(story, ref_lang),
            body=story.body,
            estimatedReadingTime=_reading_time(story.body),
            format=story.format,
            speakers=speakers,
            segments=segments,
        )
    }
