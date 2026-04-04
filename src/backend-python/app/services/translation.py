"""On-the-fly translation service with provider abstraction and persistent caching.

Mirrors the TTSProvider ABC pattern from app.services.tts.
"""

from __future__ import annotations

import logging
import uuid
from abc import ABC, abstractmethod

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models import TranslationCache

logger = logging.getLogger(__name__)

SUPPORTED_LANGS = {"en", "da", "it", "es"}


class TranslationProvider(ABC):
    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str | None:
        """Translate *text* from *source_lang* to *target_lang*.

        Returns the translated string on success, ``None`` on failure.
        Language codes use ISO 639-1 (``it``, ``en``, ``da``).
        """
        raise NotImplementedError


class GoogleFreeTranslationProvider(TranslationProvider):
    """Translation via the ``deep-translator`` library (Google Translate free endpoint)."""

    def translate(self, text: str, source_lang: str, target_lang: str) -> str | None:
        try:
            from deep_translator import GoogleTranslator

            result = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
            return result if result else None
        except Exception:
            logger.exception("Translation failed for %r (%s → %s)", text, source_lang, target_lang)
            return None


PROVIDER: TranslationProvider = GoogleFreeTranslationProvider()


def translate_word(
    word: str,
    source_lang: str,
    target_lang: str,
    db: Session,
) -> tuple[str | None, str]:
    """High-level lookup: cache check → external call → cache write.

    Returns ``(translation, source)`` where *source* is one of
    ``"cached"``, ``"auto-translated"``, or ``"none"``.
    """
    if source_lang not in SUPPORTED_LANGS or target_lang not in SUPPORTED_LANGS:
        return None, "none"

    # Step 1 — cache hit?
    normalised = word.lower()
    cached = (
        db.query(TranslationCache)
        .filter(
            TranslationCache.word == normalised,
            TranslationCache.source_lang == source_lang,
            TranslationCache.target_lang == target_lang,
        )
        .first()
    )
    if cached is not None:
        return cached.translation, "cached"

    # Step 2 — external provider
    translation = PROVIDER.translate(normalised, source_lang, target_lang)
    if translation is None:
        return None, "none"

    # Step 3 — persist to cache (handle concurrent inserts gracefully)
    entry = TranslationCache(
        id=str(uuid.uuid4()),
        word=normalised,
        source_lang=source_lang,
        target_lang=target_lang,
        translation=translation,
    )
    try:
        db.add(entry)
        db.commit()
    except IntegrityError:
        db.rollback()
        # Another request cached the same word concurrently — treat as success.

    return translation, "auto-translated"
