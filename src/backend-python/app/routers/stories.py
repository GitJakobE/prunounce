import json
import math
import re
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user_id
from ..hosts import get_host
from ..models import Story, StoryAudio, User
from ..schemas import CreateStoryInput, StoryDetail, StoryDetailResponse, StoryListItem, StoriesResponse
from ..services.story_audio import STORY_SPEED_TO_RATE, build_story_audio_bytes
from ..utils.dialogue import parse_dialogue_body

router = APIRouter(prefix="/api/stories")

SUPPORTED_LANGS = ["en", "da", "it", "es"]
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
    if ref_lang == "es":
        return story.description_es
    return story.description_en


def _resolve_target_lang(user_id: str, db: Session) -> str:
    user = db.query(User).filter(User.id == user_id).first()
    host_id = (user.host_id if user and user.host_id else "marco")
    return get_host(host_id)["language"]


def _resolve_ref_lang(target_lang: str, user_id: str | None = None, db: Session | None = None) -> str:
    """Reference language from the user's profile, falling back to a sensible default."""
    if user_id and db:
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.language in SUPPORTED_LANGS:
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
    # User stories are only accessible to their owner
    if story.user_id and story.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    story_audio_record = (
        db.query(StoryAudio)
        .filter(StoryAudio.story_id == story.id, StoryAudio.speed == speed)
        .first()
    )

    # For user stories, generate audio on-the-fly if not cached
    if not story_audio_record and story.user_id:
        audio_bytes = build_story_audio_bytes(story, speed)
        if not audio_bytes:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to generate audio for this story.",
            )
        story_audio_record = StoryAudio(
            id=str(uuid.uuid4()),
            story_id=story.id,
            speed=speed,
            mime_type="audio/mpeg",
            content_hash="user-story",
            audio_bytes=audio_bytes,
        )
        db.add(story_audio_record)
        db.commit()

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

    # Global (seeded) stories
    stories = (
        db.query(Story)
        .filter(Story.language == target_lang, Story.user_id.is_(None))
        .order_by(Story.order.asc())
        .all()
    )

    # User's own stories
    user_stories = (
        db.query(Story)
        .filter(Story.language == target_lang, Story.user_id == user_id)
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
            isUserStory=False,
        )
        if story.difficulty in grouped:
            grouped[story.difficulty].append(item)

    # Append user stories at the end of their difficulty group
    for story in user_stories:
        speakers = json.loads(story.speakers) if story.speakers else None
        item = StoryListItem(
            id=story.id,
            slug=story.slug,
            language=story.language,
            difficulty=story.difficulty,
            length=story.length,
            title=story.title,
            description=story.description_en,
            estimatedReadingTime=_reading_time(story.body),
            format=story.format,
            speakers=speakers,
            isUserStory=True,
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
    # User stories are only visible to their owner
    if story.user_id and story.user_id != user_id:
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
            description=_get_description(story, ref_lang) if not story.user_id else story.description_en,
            body=story.body,
            estimatedReadingTime=_reading_time(story.body),
            format=story.format,
            speakers=speakers,
            segments=segments,
            isUserStory=story.user_id is not None,
        )
    }


def _slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:80] or "story"


@router.post("", response_model=StoryDetailResponse, status_code=status.HTTP_201_CREATED)
def create_user_story(
    payload: CreateStoryInput,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    """Create a personal story for the current user."""
    target_lang = _resolve_target_lang(user_id, db)

    if payload.difficulty not in DIFFICULTY_ORDER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid difficulty. Must be one of: {', '.join(DIFFICULTY_ORDER)}",
        )

    # Compute next order value (after all existing stories for this user+lang)
    max_order = (
        db.query(Story.order)
        .filter(Story.language == target_lang, Story.user_id == user_id)
        .order_by(Story.order.desc())
        .first()
    )
    next_order = (max_order[0] + 1) if max_order else 10000  # start above seeded stories

    slug = _slugify(payload.title) + "-" + uuid.uuid4().hex[:8]
    word_count = len(payload.body.split())
    length = "short" if word_count < 150 else ("medium" if word_count < 300 else "long")

    story = Story(
        id=str(uuid.uuid4()),
        slug=slug,
        language=target_lang,
        difficulty=payload.difficulty,
        title=payload.title,
        description_en=payload.description,
        description_da=payload.description,
        description_it=payload.description,
        body=payload.body,
        length=length,
        format="narrative",
        order=next_order,
        user_id=user_id,
    )
    db.add(story)
    db.commit()
    db.refresh(story)

    segments = parse_dialogue_body(story.body, story.format)

    return {
        "story": StoryDetail(
            id=story.id,
            slug=story.slug,
            language=story.language,
            difficulty=story.difficulty,
            length=story.length,
            title=story.title,
            description=story.description_en,
            body=story.body,
            estimatedReadingTime=_reading_time(story.body),
            format=story.format,
            speakers=None,
            segments=segments,
            isUserStory=True,
        )
    }


@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_story(
    story_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:
    """Delete a user's own story."""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    if not story.user_id or story.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete this story")
    db.delete(story)
    db.commit()
