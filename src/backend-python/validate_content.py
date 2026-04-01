"""Content-quality validation for story and word seed data.

Run:
    python validate_content.py [--stories-only] [--words-only]
                               [--language CODE] [--json]
Exit codes: 0 = no errors (warnings OK)  ·  1 = errors found
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, ".")

from app.database import SessionLocal, engine, Base
from app.models import Story, Word
from app.utils.dialogue import validate_dialogue_story

Base.metadata.create_all(bind=engine)

# ── Constants ───────────────────────────────────────────────────────────────
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿÆØÅæøå]+(?:'[A-Za-zÀ-ÿÆØÅæøå]+)*")

WORD_COUNT_RANGES: dict[str, tuple[int, int]] = {
    "beginner": (50, 150),
    "intermediate": (150, 300),
    "advanced": (300, 600),
}

EXCEPTIONS_PATH = Path("data/validation-exceptions.json")


def _load_exceptions() -> dict:
    if EXCEPTIONS_PATH.exists():
        return json.loads(EXCEPTIONS_PATH.read_text(encoding="utf-8"))
    return {"ignored_words": [], "ignored_duplicates": []}


# ── Validators ──────────────────────────────────────────────────────────────

class Issue:
    __slots__ = ("level", "category", "target", "message")

    def __init__(self, level: str, category: str, target: str, message: str):
        self.level = level  # ERROR | WARNING | INFO
        self.category = category  # "story" | "word"
        self.target = target
        self.message = message

    def to_dict(self) -> dict:
        return {"level": self.level, "category": self.category,
                "target": self.target, "message": self.message}

    def __str__(self) -> str:
        return f"[{self.level}] {self.target}: {self.message}"


def _word_count(body: str) -> int:
    return len(TOKEN_RE.findall(body))


def validate_stories(db, *, language: str | None = None) -> list[Issue]:
    issues: list[Issue] = []
    query = db.query(Story)
    if language:
        query = query.filter(Story.language == language)
    stories = query.all()

    for s in stories:
        slug = s.slug

        # Empty body
        wc = _word_count(s.body) if s.body else 0
        if wc < 10:
            issues.append(Issue("ERROR", "story", slug, f"body has only {wc} words (min 10)"))

        # Slug format
        if not SLUG_RE.match(slug):
            issues.append(Issue("ERROR", "story", slug, "slug is not lowercase/hyphen URL-safe"))

        # Description completeness
        for field, lang_code in [("description_en", "en"), ("description_da", "da"), ("description_it", "it")]:
            val = getattr(s, field, None)
            if not val or not val.strip():
                issues.append(Issue("ERROR", "story", slug, f"description_{lang_code} is empty"))

        # Length check
        if s.difficulty in WORD_COUNT_RANGES:
            lo, hi = WORD_COUNT_RANGES[s.difficulty]
            margin = 0.2
            if wc < lo:
                if wc < lo * (1 - margin):
                    issues.append(Issue("ERROR", "story", slug,
                                        f"word count {wc} below {s.difficulty} minimum ({lo})"))
                else:
                    issues.append(Issue("WARNING", "story", slug,
                                        f"word count {wc} close to {s.difficulty} minimum ({lo})"))
            elif wc > hi:
                if wc > hi * (1 + margin):
                    issues.append(Issue("ERROR", "story", slug,
                                        f"word count {wc} above {s.difficulty} maximum ({hi})"))
                else:
                    issues.append(Issue("WARNING", "story", slug,
                                        f"word count {wc} close to {s.difficulty} maximum ({hi})"))

        # Dialogue format consistency
        if s.format in ("dialogue", "mixed"):
            errs = validate_dialogue_story(s.body, s.format, s.speakers)
            for e in errs:
                issues.append(Issue("ERROR", "story", slug, e))

    return issues


def validate_words(db, *, language: str | None = None) -> list[Issue]:
    issues: list[Issue] = []
    query = db.query(Word)
    if language:
        query = query.filter(Word.language == language)
    words = query.all()

    exceptions = _load_exceptions()
    ignored_dupes = {tuple(sorted(p)) for p in exceptions.get("ignored_duplicates", [])}

    source_counts: dict[str, int] = {}
    for w in words:
        src = getattr(w, "source", "unknown") or "unknown"
        source_counts[src] = source_counts.get(src, 0) + 1

    for w in words:
        label = f'"{w.word}" ({w.language})'

        # Translation completeness
        for attr, lc in [("translation_en", "en"), ("translation_da", "da"), ("translation_it", "it")]:
            val = getattr(w, attr, None)
            if not val or not val.strip():
                level = "ERROR" if lc == w.language else "WARNING"
                issues.append(Issue(level, "word", label, f"translation_{lc} is empty"))

        # Phonetic hint
        hint = getattr(w, "phonetic_hint", None)
        if not hint or not hint.strip():
            issues.append(Issue("WARNING", "word", label, "no phonetic hint"))

        # Translation plausibility – length ratio
        for attr in ("translation_en", "translation_da", "translation_it"):
            val = getattr(w, attr, None)
            if val and len(val) > 5 * len(w.word):
                issues.append(Issue("WARNING", "word", label,
                                    f"{attr} is >5× longer than source word"))

    # Near-duplicate detection (within same language)
    by_lang: dict[str, list] = {}
    for w in words:
        by_lang.setdefault(w.language, []).append(w)

    for lang, lang_words in by_lang.items():
        for i, a in enumerate(lang_words):
            for b in lang_words[i + 1:]:
                if tuple(sorted([a.word, b.word])) in ignored_dupes:
                    continue
                if _edit_distance(a.word, b.word) <= 2 and a.word != b.word:
                    issues.append(Issue("WARNING", "word",
                                        f'"{a.word}" / "{b.word}" ({lang})',
                                        f"possible duplicates (edit distance ≤ 2)"))

    # Source counts as INFO
    for src, count in sorted(source_counts.items()):
        issues.append(Issue("INFO", "word", "source_counts", f"{src}: {count}"))

    return issues


def _edit_distance(a: str, b: str) -> int:
    """Simple Levenshtein distance."""
    if len(a) < len(b):
        return _edit_distance(b, a)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (ca != cb)))
        prev = curr
    return prev[-1]


# ── Report ──────────────────────────────────────────────────────────────────

def _print_report(story_issues: list[Issue], word_issues: list[Issue]) -> None:
    print("=== Content Validation Report ===\n")

    for label, issues in [("STORIES", story_issues), ("WORDS", word_issues)]:
        errors = [i for i in issues if i.level == "ERROR"]
        warnings = [i for i in issues if i.level == "WARNING"]
        infos = [i for i in issues if i.level == "INFO"]

        print(f"{label} ({len(issues)} issues)")
        if errors:
            print(f"  ERRORS: {len(errors)}")
            for e in errors:
                print(f"    {e}")
        if warnings:
            print(f"  WARNINGS: {len(warnings)}")
            for w in warnings:
                print(f"    {w}")
        if infos:
            print(f"  INFO: {len(infos)}")
            for i in infos:
                print(f"    {i}")
        if not errors and not warnings and not infos:
            print("  No issues found.")
        print()

    total_errors = sum(1 for i in story_issues + word_issues if i.level == "ERROR")
    total_warnings = sum(1 for i in story_issues + word_issues if i.level == "WARNING")
    status = "FAIL (errors found)" if total_errors else "PASS"
    print("SUMMARY")
    print(f"  Stories: {sum(1 for i in story_issues if i.level == 'ERROR')} errors, "
          f"{sum(1 for i in story_issues if i.level == 'WARNING')} warnings")
    print(f"  Words: {sum(1 for i in word_issues if i.level == 'ERROR')} errors, "
          f"{sum(1 for i in word_issues if i.level == 'WARNING')} warnings")
    print(f"  Status: {status}")


def _json_report(story_issues: list[Issue], word_issues: list[Issue]) -> str:
    return json.dumps({
        "stories": [i.to_dict() for i in story_issues],
        "words": [i.to_dict() for i in word_issues],
        "summary": {
            "story_errors": sum(1 for i in story_issues if i.level == "ERROR"),
            "story_warnings": sum(1 for i in story_issues if i.level == "WARNING"),
            "word_errors": sum(1 for i in word_issues if i.level == "ERROR"),
            "word_warnings": sum(1 for i in word_issues if i.level == "WARNING"),
            "status": "FAIL" if any(i.level == "ERROR" for i in story_issues + word_issues) else "PASS",
        },
    }, indent=2, ensure_ascii=False)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Content validation script")
    parser.add_argument("--stories-only", action="store_true")
    parser.add_argument("--words-only", action="store_true")
    parser.add_argument("--language", type=str, default=None, choices=["it", "da", "en"])
    parser.add_argument("--json", dest="json_output", action="store_true")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        story_issues: list[Issue] = []
        word_issues: list[Issue] = []

        if not args.words_only:
            story_issues = validate_stories(db, language=args.language)
        if not args.stories_only:
            word_issues = validate_words(db, language=args.language)

        if args.json_output:
            print(_json_report(story_issues, word_issues))
        else:
            _print_report(story_issues, word_issues)

        has_errors = any(i.level == "ERROR" for i in story_issues + word_issues)
        return 1 if has_errors else 0
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
