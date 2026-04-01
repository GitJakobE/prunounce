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
    greetingEn: str
    greetingDa: str
    greetingIt: str
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


class StoriesResponse(BaseModel):
    stories: dict[str, list[StoryListItem]]  # keyed by difficulty


class StoryDetailResponse(BaseModel):
    story: StoryDetail


class WordLookupResult(BaseModel):
    word: str
    translation: str | None
    phoneticHint: str | None
    wordId: str | None
