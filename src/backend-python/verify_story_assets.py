"""Verify story dictionary and audio coverage."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, ".")

from app.config import settings
from app.database import SessionLocal
from app.hosts import HOSTS
from app.models import Story, Word
from app.routers.stories import _SPEED_TO_RATE
from app.services.tts import sanitize_filename

TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿÆØÅæøå]+(?:'[A-Za-zÀ-ÿÆØÅæøå]+)*")


def normalize(value: str) -> str:
    base = value.lower()
    mapping = str.maketrans(
        {
            "à": "a", "á": "a", "â": "a", "ã": "a", "ä": "a", "å": "a",
            "è": "e", "é": "e", "ê": "e", "ë": "e",
            "ì": "i", "í": "i", "î": "i", "ï": "i",
            "ò": "o", "ó": "o", "ô": "o", "õ": "o", "ö": "o",
            "ù": "u", "ú": "u", "û": "u", "ü": "u",
            "ç": "c", "ñ": "n",
        }
    )
    return base.translate(mapping)


def host_id_for_lang(lang: str) -> str | None:
    for host in HOSTS:
        if host["language"] == lang:
            return host["id"]
    return None


def main() -> None:
    db = SessionLocal()
    missing_words_total = 0

    for lang in ("it", "da", "en"):
        story_tokens: set[str] = set()
        stories = db.query(Story).filter(Story.language == lang).all()
        for story in stories:
            for token in TOKEN_RE.findall(story.body):
                candidate = token.strip("'")
                if len(candidate) >= 2:
                    story_tokens.add(normalize(candidate))

        dictionary_tokens = {
            normalize(word.word)
            for word in db.query(Word).filter(Word.language == lang).all()
        }

        missing = sorted(story_tokens - dictionary_tokens)
        missing_words_total += len(missing)
        print(f"{lang}: story_tokens={len(story_tokens)} missing={len(missing)}")

    cache_dir = Path(settings.audio_cache_dir)
    audio_missing = 0
    audio_total = 0

    for story in db.query(Story).all():
        host_id = host_id_for_lang(story.language)
        if not host_id:
            continue
        for rate in _SPEED_TO_RATE.values():
            audio_total += 1
            safe_rate = re.sub(
                r"[^a-z0-9]",
                "",
                rate.replace("%", "pct").replace("+", "pos").replace("-", "neg"),
            )
            filename = f"story_{sanitize_filename(story.id)}_{host_id}_{safe_rate}.mp3"
            file_path = cache_dir / filename
            if (not file_path.exists()) or file_path.stat().st_size == 0:
                audio_missing += 1

    print(f"missing_words_total={missing_words_total}")
    print(f"audio_missing={audio_missing} of {audio_total}")

    db.close()


if __name__ == "__main__":
    main()
