"""Ensure complete story assets.

What this script does:
1. Ensures every word token used in stories exists in Word with non-empty translations.
2. Pre-generates narration audio for every story at every supported speed.

Run with:
  poetry run python ensure_story_assets.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, ".")

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.hosts import HOSTS
from app.models import Story, Word
from app.routers.stories import _SPEED_TO_RATE
from app.services.tts import PROVIDER, sanitize_filename

try:
    from deep_translator import GoogleTranslator
except Exception:  # pragma: no cover - optional dependency for tooling script
    GoogleTranslator = None


LANGS = ("it", "da", "en")
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


def extract_tokens(text: str) -> list[str]:
    tokens: list[str] = []
    for raw in TOKEN_RE.findall(text):
        token = raw.strip("'").lower()
        if len(token) < 2:
            continue
        tokens.append(token)
    return tokens


def preferred_host_for_language(language: str) -> tuple[str, str]:
    for host in HOSTS:
        if host["language"] == language:
            return host["id"], host["voice"]["voiceName"]
    raise RuntimeError(f"No host found for language: {language}")


class AutoTranslator:
    def __init__(self) -> None:
        self.available = GoogleTranslator is not None
        self._cache: dict[tuple[str, str, str], str] = {}

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if target_lang == source_lang:
            return text

        key = (source_lang, target_lang, text)
        if key in self._cache:
            return self._cache[key]

        if not self.available:
            self._cache[key] = text
            return text

        try:
            translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
            value = (translated or text).strip()
        except Exception:
            value = text

        self._cache[key] = value
        return value


def ensure_story_words(db) -> tuple[int, int]:
    stories = db.query(Story).all()

    existing_by_lang: dict[str, dict[str, Word]] = {lang: {} for lang in LANGS}
    for word in db.query(Word).all():
        existing_by_lang[word.language][normalize(word.word)] = word

    by_lang_tokens: dict[str, dict[str, str]] = {lang: {} for lang in LANGS}
    token_difficulty: dict[tuple[str, str], str] = {}

    for story in stories:
        if story.language not in LANGS:
            continue
        for token in extract_tokens(story.body):
            key = normalize(token)
            by_lang_tokens[story.language].setdefault(key, token)
            token_difficulty.setdefault((story.language, key), story.difficulty)

    translator = AutoTranslator()
    added = 0

    for language in LANGS:
        for norm, source_word in by_lang_tokens[language].items():
            if norm in existing_by_lang[language]:
                continue

            translation_en = translator.translate(source_word, language, "en")
            translation_da = translator.translate(source_word, language, "da")
            translation_it = translator.translate(source_word, language, "it")

            new_word = Word(
                word=source_word,
                language=language,
                phonetic_hint=source_word,
                translation_en=translation_en or source_word,
                translation_da=translation_da or source_word,
                translation_it=translation_it or source_word,
                difficulty=token_difficulty.get((language, norm), "intermediate"),
                example_it="",
                example_en="",
                example_da="",
                audio_path=None,
                source="story_auto",
                contributed_by=None,
            )
            db.add(new_word)
            existing_by_lang[language][norm] = new_word
            added += 1

    db.commit()
    total_story_tokens = sum(len(tokens) for tokens in by_lang_tokens.values())
    return added, total_story_tokens


def ensure_story_audio(db) -> tuple[int, int]:
    stories = db.query(Story).all()
    cache_dir = Path(settings.audio_cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    created = 0
    total_expected = 0

    for story in stories:
        if story.language not in LANGS:
            continue
        host_id, voice_name = preferred_host_for_language(story.language)
        for rate in _SPEED_TO_RATE.values():
            total_expected += 1
            safe_rate = re.sub(r"[^a-z0-9]", "", rate.replace("%", "pct").replace("+", "pos").replace("-", "neg"))
            filename = f"story_{sanitize_filename(story.id)}_{host_id}_{safe_rate}.mp3"
            file_path = cache_dir / filename
            if file_path.exists() and file_path.stat().st_size > 0:
                continue
            ok = PROVIDER.generate(story.body, voice_name, file_path, rate=rate)
            if ok:
                created += 1

    return created, total_expected


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        print("Ensuring story word coverage...")
        added_words, total_story_tokens = ensure_story_words(db)
        print(f"  Added dictionary words: {added_words}")
        print(f"  Unique story tokens tracked: {total_story_tokens}")

        print("Ensuring story narration audio...")
        created_audio, total_audio = ensure_story_audio(db)
        print(f"  Audio files created now: {created_audio}")
        print(f"  Total audio variants expected: {total_audio}")
        print("Done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
