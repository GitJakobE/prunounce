from __future__ import annotations

import hashlib
import uuid
from collections.abc import Iterable

from sqlalchemy.orm import Session

from ..models import Story, StoryAudio
from ..utils.dialogue import parse_dialogue_body
from .tts import DEFAULT_VOICE, PROVIDER


STORY_AUDIO_VERSION = "story-audio-v1"
STORY_SPEED_TO_RATE: dict[str, str] = {
    "very_slow": "-50%",
    "slow": "-25%",
    "normal": "+0%",
    "fast": "+25%",
    "very_fast": "+50%",
}

LANGUAGE_STORY_VOICES: dict[str, list[str]] = {
    "it": ["it-IT-DiegoNeural", "it-IT-IsabellaNeural", "it-IT-GiuseppeMultilingualNeural"],
    "da": ["da-DK-JeppeNeural", "da-DK-ChristelNeural", "da-DK-JeppeNeural"],
    "en": ["en-GB-ThomasNeural", "en-GB-SoniaNeural", "en-AU-WilliamMultilingualNeural"],
}


def _story_voices(language: str) -> list[str]:
    return LANGUAGE_STORY_VOICES.get(language, [DEFAULT_VOICE])


def _content_hash(story: Story, speed: str) -> str:
    raw = "\n".join([
        STORY_AUDIO_VERSION,
        story.id,
        story.language,
        story.length,
        story.format,
        speed,
        story.title,
        story.body,
        story.speakers or "",
        "|".join(_story_voices(story.language)),
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build_story_audio_bytes(story: Story, speed: str) -> bytes | None:
    rate = STORY_SPEED_TO_RATE[speed]
    voices = _story_voices(story.language)
    segments = parse_dialogue_body(story.body, story.format)

    if story.format == "narrative":
        return PROVIDER.generate_bytes(story.body, voices[0], rate=rate)

    speaker_voices: dict[str, str] = {}
    audio_chunks: list[bytes] = []
    for segment in segments:
        if segment["type"] == "dialogue":
            speaker = segment["speaker"]
            voice = speaker_voices.setdefault(speaker, voices[len(speaker_voices) % len(voices)])
            text = segment["text"].strip()
        else:
            voice = voices[0]
            text = segment["text"].strip()

        if not text:
            continue

        audio_bytes = PROVIDER.generate_bytes(text, voice, rate=rate)
        if not audio_bytes:
            return None
        audio_chunks.append(audio_bytes)

    if not audio_chunks:
        return None
    return b"".join(audio_chunks)


def upsert_story_audio(db: Session, story: Story, *, speeds: Iterable[str] | None = None) -> int:
    failures = 0
    for speed in speeds or STORY_SPEED_TO_RATE.keys():
        content_hash = _content_hash(story, speed)
        existing = (
            db.query(StoryAudio)
            .filter(StoryAudio.story_id == story.id, StoryAudio.speed == speed)
            .first()
        )
        if existing and existing.content_hash == content_hash and existing.audio_bytes:
            continue

        audio_bytes = build_story_audio_bytes(story, speed)
        if not audio_bytes:
            failures += 1
            continue

        if existing:
            existing.mime_type = "audio/mpeg"
            existing.content_hash = content_hash
            existing.audio_bytes = audio_bytes
        else:
            db.add(StoryAudio(
                id=str(uuid.uuid4()),
                story_id=story.id,
                speed=speed,
                mime_type="audio/mpeg",
                content_hash=content_hash,
                audio_bytes=audio_bytes,
            ))

    db.commit()
    return failures
