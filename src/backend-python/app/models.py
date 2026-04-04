from datetime import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey, Integer, LargeBinary, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "User"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column("passwordHash", String, nullable=True)
    display_name: Mapped[str | None] = mapped_column("displayName", String, nullable=True)
    language: Mapped[str] = mapped_column(String, default="en", nullable=False)
    host_id: Mapped[str | None] = mapped_column("hostId", String, nullable=True)
    google_id: Mapped[str | None] = mapped_column("googleId", String, unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column("createdAt", DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column("updatedAt", DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "Category"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name_en: Mapped[str] = mapped_column("nameEn", String, nullable=False)
    name_da: Mapped[str] = mapped_column("nameDa", String, nullable=False)
    name_it: Mapped[str] = mapped_column("nameIt", String, nullable=False, default="")
    name_es: Mapped[str] = mapped_column("nameEs", String, nullable=False, default="")
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class Word(Base):
    __tablename__ = "Word"
    __table_args__ = (UniqueConstraint("word", "language", name="Word_word_language_key"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    word: Mapped[str] = mapped_column(String, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False, default="it")
    phonetic_hint: Mapped[str] = mapped_column("phoneticHint", String, nullable=False)
    translation_en: Mapped[str] = mapped_column("translationEn", String, nullable=False)
    translation_da: Mapped[str] = mapped_column("translationDa", String, nullable=False)
    translation_it: Mapped[str] = mapped_column("translationIt", String, nullable=False, default="")
    translation_es: Mapped[str] = mapped_column("translationEs", String, nullable=False, default="")
    difficulty: Mapped[str] = mapped_column(String, nullable=False)
    example_it: Mapped[str] = mapped_column("exampleIt", String, nullable=False, default="")
    example_en: Mapped[str] = mapped_column("exampleEn", String, nullable=False, default="")
    example_da: Mapped[str] = mapped_column("exampleDa", String, nullable=False, default="")
    example_es: Mapped[str] = mapped_column("exampleEs", String, nullable=False, default="")
    audio_path: Mapped[str | None] = mapped_column("audioPath", String, nullable=True)
    source: Mapped[str] = mapped_column(String, nullable=False, default="seed")
    contributed_by: Mapped[str | None] = mapped_column("contributedBy", String, ForeignKey("User.id", ondelete="SET NULL"), nullable=True)


class WordCategory(Base):
    __tablename__ = "WordCategory"

    word_id: Mapped[str] = mapped_column("wordId", String, ForeignKey("Word.id", ondelete="CASCADE"), primary_key=True)
    category_id: Mapped[str] = mapped_column("categoryId", String, ForeignKey("Category.id", ondelete="CASCADE"), primary_key=True)


class UserProgress(Base):
    __tablename__ = "UserProgress"
    __table_args__ = (UniqueConstraint("userId", "wordId", name="UserProgress_userId_wordId_key"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column("userId", String, ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    word_id: Mapped[str] = mapped_column("wordId", String, ForeignKey("Word.id", ondelete="CASCADE"), nullable=False)
    listened_at: Mapped[datetime] = mapped_column("listenedAt", DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="progress")


class Story(Base):
    __tablename__ = "Story"
    __table_args__ = (UniqueConstraint("slug", "language", name="Story_slug_language_key"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    slug: Mapped[str] = mapped_column(String, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False)
    difficulty: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description_en: Mapped[str] = mapped_column("descriptionEn", String, nullable=False, default="")
    description_da: Mapped[str] = mapped_column("descriptionDa", String, nullable=False, default="")
    description_it: Mapped[str] = mapped_column("descriptionIt", String, nullable=False, default="")
    description_es: Mapped[str] = mapped_column("descriptionEs", String, nullable=False, default="")
    body: Mapped[str] = mapped_column(Text, nullable=False)
    length: Mapped[str] = mapped_column(String, nullable=False, default="short")
    format: Mapped[str] = mapped_column(String, nullable=False, default="narrative")
    speakers: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    setup_type: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    setup_summary: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    user_id: Mapped[str | None] = mapped_column("userId", String, ForeignKey("User.id", ondelete="CASCADE"), nullable=True, default=None)


class StoryAudio(Base):
    __tablename__ = "StoryAudio"
    __table_args__ = (UniqueConstraint("storyId", "speed", name="StoryAudio_storyId_speed_key"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id: Mapped[str] = mapped_column("storyId", String, ForeignKey("Story.id", ondelete="CASCADE"), nullable=False)
    speed: Mapped[str] = mapped_column(String, nullable=False)
    mime_type: Mapped[str] = mapped_column("mimeType", String, nullable=False, default="audio/mpeg")
    content_hash: Mapped[str] = mapped_column("contentHash", String, nullable=False)
    audio_bytes: Mapped[bytes] = mapped_column("audioBytes", LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column("createdAt", DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column("updatedAt", DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class ContentReport(Base):
    __tablename__ = "ContentReport"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str | None] = mapped_column("userId", String, ForeignKey("User.id", ondelete="SET NULL"), nullable=True)
    content_type: Mapped[str] = mapped_column("contentType", String, nullable=False)
    content_id: Mapped[str] = mapped_column("contentId", String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="new")
    resolution_note: Mapped[str | None] = mapped_column("resolutionNote", String, nullable=True)
    created_at: Mapped[datetime] = mapped_column("createdAt", DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column("updatedAt", DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class TranslationCache(Base):
    """Persistent cache for on-the-fly translations produced by an external provider.

    Terminology mapping:
    - sourceLang = the language the word is in (the app's "target language" — what the user is learning)
    - targetLang = the language of the translation (the app's "reference language" — the user's native language)
    """

    __tablename__ = "TranslationCache"
    __table_args__ = (
        UniqueConstraint("word", "sourceLang", "targetLang", name="TranslationCache_word_src_tgt_key"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    word: Mapped[str] = mapped_column(String, nullable=False)
    source_lang: Mapped[str] = mapped_column("sourceLang", String, nullable=False)
    target_lang: Mapped[str] = mapped_column("targetLang", String, nullable=False)
    translation: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column("createdAt", DateTime, nullable=False, server_default=func.now())
