"""Tests for dialogue body parsing and validation."""
import json

from app.utils.dialogue import parse_dialogue_body, validate_dialogue_story


class TestParseDialogueBody:
    """Tests for parse_dialogue_body()."""

    def test_narrative_returns_single_segment(self):
        body = "Once upon a time there was a story. It had no speakers."
        result = parse_dialogue_body(body, "narrative")
        assert len(result) == 1
        assert result[0] == {"type": "narration", "text": body}

    def test_dialogue_parses_speakers(self):
        body = "Marco: Buongiorno!\nBarista: Certo, subito."
        result = parse_dialogue_body(body, "dialogue")
        assert len(result) == 2
        assert result[0] == {"type": "dialogue", "speaker": "Marco", "text": "Buongiorno!"}
        assert result[1] == {"type": "dialogue", "speaker": "Barista", "text": "Certo, subito."}

    def test_mixed_parses_both(self):
        body = "Marco entra nel bar.\n\nMarco: Buongiorno!\nBarista: Certo, subito."
        result = parse_dialogue_body(body, "mixed")
        assert len(result) == 3
        assert result[0] == {"type": "narration", "text": "Marco entra nel bar."}
        assert result[1] == {"type": "dialogue", "speaker": "Marco", "text": "Buongiorno!"}
        assert result[2] == {"type": "dialogue", "speaker": "Barista", "text": "Certo, subito."}

    def test_empty_lines_are_skipped(self):
        body = "Marco: Ciao!\n\n\nBarista: Salve!"
        result = parse_dialogue_body(body, "dialogue")
        assert len(result) == 2

    def test_accented_speaker_labels(self):
        body = "Dottoressa Müller: Buongiorno.\nPaziente José: Mi fa male."
        result = parse_dialogue_body(body, "dialogue")
        assert len(result) == 2
        assert result[0]["speaker"] == "Dottoressa Müller"
        assert result[1]["speaker"] == "Paziente José"

    def test_dialogue_with_colon_in_text(self):
        """Colon inside spoken text should not break parsing."""
        body = "Marco: L'orario è: dalle 9 alle 17."
        result = parse_dialogue_body(body, "dialogue")
        assert len(result) == 1
        assert result[0]["speaker"] == "Marco"
        assert result[0]["text"] == "L'orario è: dalle 9 alle 17."

    def test_narrative_format_preserves_full_body(self):
        body = "Line one.\nLine two.\nLine three."
        result = parse_dialogue_body(body, "narrative")
        assert result[0]["text"] == body


class TestValidateDialogueStory:
    """Tests for validate_dialogue_story()."""

    def test_narrative_always_valid(self):
        errors = validate_dialogue_story("Just text.", "narrative", None)
        assert errors == []

    def test_valid_dialogue_story(self):
        body = "Marco: Ciao!\nBarista: Salve!\nMarco: Un caffè."
        speakers = json.dumps(["Marco", "Barista"])
        errors = validate_dialogue_story(body, "dialogue", speakers)
        assert errors == []

    def test_fewer_than_two_speakers(self):
        body = "Marco: Ciao!\nMarco: Come va?"
        speakers = json.dumps(["Marco"])
        errors = validate_dialogue_story(body, "dialogue", speakers)
        assert any("at least 2 speakers" in e for e in errors)

    def test_more_than_four_speakers(self):
        names = ["Marco", "Sofia", "Barista", "Cliente", "Dottoressa"]
        body = "\n".join(f"{n}: Hello!" for n in names)
        speakers = json.dumps(names)
        errors = validate_dialogue_story(body, "dialogue", speakers)
        assert any("at most 4 speakers" in e for e in errors)

    def test_undeclared_speaker(self):
        body = "Marco: Ciao!\nLuigi: Salve!"
        speakers = json.dumps(["Marco", "Barista"])
        errors = validate_dialogue_story(body, "dialogue", speakers)
        assert any("Luigi" in e for e in errors)

    def test_mixed_must_have_narration(self):
        body = "Marco: Ciao!\nBarista: Salve!"
        speakers = json.dumps(["Marco", "Barista"])
        errors = validate_dialogue_story(body, "mixed", speakers)
        assert any("narrative paragraph" in e for e in errors)

    def test_mixed_must_have_dialogue(self):
        body = "Just a paragraph with no speakers."
        speakers = json.dumps([])
        errors = validate_dialogue_story(body, "mixed", speakers)
        assert any("dialogue line" in e for e in errors)

    def test_valid_mixed_story(self):
        body = "Marco entra nel bar.\n\nMarco: Buongiorno!\nBarista: Certo!"
        speakers = json.dumps(["Marco", "Barista"])
        errors = validate_dialogue_story(body, "mixed", speakers)
        assert errors == []

    def test_invalid_speakers_json(self):
        errors = validate_dialogue_story("Marco: Ciao!", "dialogue", "not json{")
        assert any("not valid JSON" in e for e in errors)
