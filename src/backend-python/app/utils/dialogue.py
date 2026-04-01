"""Dialogue body parsing and validation for Story content."""
from __future__ import annotations

import json
import re
from typing import TypedDict

# Matches a dialogue line: "Speaker Label: Spoken text"
# Speaker labels: 1-30 chars of letters, spaces, accented chars
_DIALOGUE_RE = re.compile(r"^([A-Za-zÀ-ÖØ-öø-ÿ ]{1,30}):\s(.+)$")


class NarrationSegment(TypedDict):
    type: str  # "narration"
    text: str


class DialogueSegment(TypedDict):
    type: str  # "dialogue"
    speaker: str
    text: str


Segment = NarrationSegment | DialogueSegment


def parse_dialogue_body(body: str, fmt: str) -> list[Segment]:
    """Parse a story body into structured segments.

    For 'narrative' format: returns a single narration segment with the full body.
    For 'dialogue' or 'mixed' format: returns a list of dialogue and narration segments.
    """
    if fmt == "narrative":
        return [{"type": "narration", "text": body}]

    segments: list[Segment] = []
    for line in body.split("\n"):
        line = line.strip()
        if not line:
            continue
        m = _DIALOGUE_RE.match(line)
        if m:
            segments.append({"type": "dialogue", "speaker": m.group(1).strip(), "text": m.group(2).strip()})
        else:
            segments.append({"type": "narration", "text": line})
    return segments


def validate_dialogue_story(body: str, fmt: str, speakers_json: str | None) -> list[str]:
    """Validate a dialogue/mixed story body. Returns a list of error messages (empty = valid)."""
    errors: list[str] = []

    if fmt == "narrative":
        return errors

    # Parse declared speakers
    declared_speakers: list[str] = []
    if speakers_json:
        try:
            declared_speakers = json.loads(speakers_json)
        except (json.JSONDecodeError, TypeError):
            errors.append("speakers field is not valid JSON")
            return errors

    segments = parse_dialogue_body(body, fmt)
    dialogue_segments = [s for s in segments if s["type"] == "dialogue"]
    narration_segments = [s for s in segments if s["type"] == "narration"]

    # Extract unique speakers from body
    found_speakers = list(dict.fromkeys(s["speaker"] for s in dialogue_segments))

    if len(found_speakers) < 2:
        errors.append(f"Dialogue story must have at least 2 speakers, found {len(found_speakers)}")

    if len(found_speakers) > 4:
        errors.append(f"Dialogue story must have at most 4 speakers, found {len(found_speakers)}")

    # Check speaker labels match declared list
    if declared_speakers:
        for speaker in found_speakers:
            if speaker not in declared_speakers:
                errors.append(f"Speaker '{speaker}' not in declared speakers list {declared_speakers}")

    # Mixed format validation
    if fmt == "mixed":
        if not narration_segments:
            errors.append("Mixed-format story must contain at least one narrative paragraph")
        if not dialogue_segments:
            errors.append("Mixed-format story must contain at least one dialogue line")

    return errors
