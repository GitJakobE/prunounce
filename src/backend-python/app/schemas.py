from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class UserOut(BaseModel):
    id: str
    email: EmailStr
    displayName: str | None
    language: str
    hostId: str | None


class AuthResponse(BaseModel):
    token: str
    user: UserOut


class RegisterInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    language: str | None = None
    displayName: str | None = None


class LoginInput(BaseModel):
    email: EmailStr
    password: str


class ProfileUpdateInput(BaseModel):
    displayName: str | None = None
    language: str | None = None
    hostId: str | None = None


class HostVoice(BaseModel):
    voiceName: str


class Host(BaseModel):
    id: str
    name: str
    language: str
    emoji: str
    imageUrl: str
    descriptionEn: str
    descriptionDa: str
    descriptionIt: str
    descriptionEs: str
    greetingEn: str
    greetingDa: str
    greetingIt: str
    greetingEs: str
    color: str
    voice: HostVoice


class StoryListItem(BaseModel):
    id: str
    slug: str
    language: str
    difficulty: str
    length: str = "short"
    title: str
    description: str
    estimatedReadingTime: int  # minutes, rounded up
    format: str = "narrative"
    speakers: list[str] | None = None
    isUserStory: bool = False


class NarrationSegment(BaseModel):
    type: Literal["narration"] = "narration"
    text: str


class DialogueSegment(BaseModel):
    type: Literal["dialogue"] = "dialogue"
    speaker: str
    text: str


StorySegment = NarrationSegment | DialogueSegment


class StoryDetail(BaseModel):
    id: str
    slug: str
    language: str
    difficulty: str
    length: str = "short"
    title: str
    description: str
    body: str
    estimatedReadingTime: int  # minutes, rounded up
    format: str = "narrative"
    speakers: list[str] | None = None
    segments: list[StorySegment] = []
    isUserStory: bool = False


class StoriesResponse(BaseModel):
    stories: dict[str, list[StoryListItem]]  # keyed by difficulty


class CreateStoryInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=10000)
    difficulty: str = "beginner"
    description: str = Field(default="", max_length=500)


class StoryDetailResponse(BaseModel):
    story: StoryDetail


class WordLookupResult(BaseModel):
    word: str
    translation: str | None
    phoneticHint: str | None
    wordId: str | None
    source: str = "curated"  # "curated" | "cached" | "auto-translated" | "none"


# ── Content Reports ────────────────────────────────────────────────────────────

REPORT_CONTENT_TYPES = {"story", "word"}
REPORT_CATEGORIES = {"grammar_spelling", "wrong_translation", "pronunciation", "formatting", "other"}
REPORT_STATUSES = {"new", "reviewed", "resolved", "dismissed"}


class ContentReportCreateRequest(BaseModel):
    contentType: str
    contentId: str
    category: str
    description: str | None = Field(default=None, max_length=500)


class ContentReportUpdateRequest(BaseModel):
    status: str
    resolutionNote: str | None = Field(default=None, max_length=500)


class ContentReportResponse(BaseModel):
    id: str
    userId: str | None
    contentType: str
    contentId: str
    category: str
    description: str | None
    status: str
    resolutionNote: str | None
    createdAt: str
    updatedAt: str


class ContentReportListResponse(BaseModel):
    items: list[ContentReportResponse]
    total: int
