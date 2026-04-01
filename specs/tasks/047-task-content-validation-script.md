# Task 047: Content Validation Script

**Feature:** F-CONTENT-QA (Content Quality Assurance)
**Priority:** P1
**Dependencies:** 042 (Story Dialogue Body Format), 030 (Story Seed Data), 003 (Content Seeding)

## Description

Build a standalone validation script that checks all story and word seed content for quality issues before publication. The script produces a structured report of errors (must-fix) and warnings (should-review), acting as a quality gate for content deployments. This extends the existing `verify_story_assets.py` approach with comprehensive language and content checks.

## Technical Requirements

### Script Interface

- Script: `src/backend-python/validate_content.py`
- Runnable via: `python validate_content.py` (from the backend-python directory)
- Accepts optional flags:
  - `--stories-only` — validate only story content
  - `--words-only` — validate only word dictionary content
  - `--language <code>` — filter to a single language (it, da, en)
  - `--json` — output results as JSON (for CI integration)
- Default: validate all content, output human-readable report to stdout
- Exit code: `0` if no errors (warnings are OK), `1` if any errors found

### Story Validation Checks

1. **Length check** — Verify word count of each story body falls within difficulty guidelines:
   - Beginner: 50–150 words
   - Intermediate: 150–300 words
   - Advanced: 300–600 words
   - Severity: ERROR if outside range by >20%, WARNING if within 20% of boundary

2. **Dialogue format consistency** — For `format: "dialogue"` stories:
   - Every line that starts with `LABEL:` must use a label from the `speakers` list
   - Story must have 2–4 speakers (ERROR if violated)
   - Every dialogue line must have non-empty text after the colon
   - No blank speaker labels
   - Severity: ERROR

3. **Speaker label validation** — For dialogue stories:
   - Labels are no longer than 30 characters
   - Labels contain only letters, spaces, and accented characters
   - Severity: ERROR

4. **Word coverage check** — For each unique word token in story body:
   - Check if a matching Word entry exists in the database (or seed data)
   - Report uncovered words (these will show "Translation not available" in the app)
   - Severity: WARNING (not an error — some words may intentionally lack entries)

5. **Empty body check** — Story body must be non-empty and contain at least 10 words
   - Severity: ERROR

6. **Slug format check** — Slug must be lowercase, hyphens only, URL-safe
   - Severity: ERROR

7. **Description completeness** — All three description fields (en, da, it) must be non-empty
   - Severity: ERROR

### Word Dictionary Validation Checks

1. **Translation completeness** — Every word entry must have non-empty values in `translationEn`, `translationDa`, and `translationIt`
   - Severity: ERROR for the word's own language being empty; WARNING for other languages

2. **Phonetic hint presence** — Every word entry must have a non-empty `phoneticHint`
   - Severity: WARNING

3. **Translation plausibility** — Flag when a translation is more than 5× longer (by character count) than the source word, or when a translation is identical to the source word in a different language
   - Severity: WARNING

4. **Example sentence completeness** — Flag words missing example sentences in all three languages
   - Severity: WARNING

5. **Near-duplicate detection** — Flag word pairs within the same language where the edit distance (Levenshtein) is ≤ 2 and they are not already the same entry
   - Severity: WARNING

6. **Source tracking** — Report counts of words by source: `"seed"`, `"story_auto"`, `"user"` — for visibility into content composition
   - Severity: INFO (no action required)

### Report Format

Human-readable output:
```
=== Content Validation Report ===

STORIES (27 total)
  ERRORS: 3
    [ERROR] it-beginner-cafe: word count 45 below beginner minimum (50)
    [ERROR] da-advanced-interview: speaker "Interviewer" not in speakers list
    [ERROR] en-intermediate-meeting: descriptionDa is empty
  WARNINGS: 8
    [WARNING] it-beginner-mercato: 5 words not found in dictionary: zucchine, centesimi, ...
    [WARNING] da-beginner-kaffe: word count 52 close to minimum boundary (50)
    ...

WORDS (850 total)
  ERRORS: 2
    [ERROR] "buongiorno" (it): translationIt is empty
    [ERROR] "grazie" (it): translationDa is empty
  WARNINGS: 15
    [WARNING] "ciao" (it) and "ciào" (it): possible duplicates (edit distance 1)
    [WARNING] "appartamento" (it): no example sentences
    ...

SUMMARY
  Stories: 3 errors, 8 warnings
  Words: 2 errors, 15 warnings
  Status: FAIL (errors found)
```

### Known Exceptions List

- Maintain a file `src/backend-python/data/validation-exceptions.json` containing:
  - `ignored_words` — words that should not trigger "word not in dictionary" warnings (e.g., proper nouns, intentionally untranslated terms)
  - `ignored_duplicates` — word pairs that are known non-duplicates despite low edit distance
- The validation script reads this file and suppresses matching warnings

## Acceptance Criteria

- [ ] Script validates all 27 stories and all word entries
- [ ] Story checks: length, dialogue format, speakers, word coverage, slug, descriptions
- [ ] Word checks: translation completeness, phonetic hint, plausibility, examples, duplicates
- [ ] Report clearly distinguishes ERRORS from WARNINGS
- [ ] Exit code 0 when no errors, 1 when errors found
- [ ] `--json` flag produces machine-readable output
- [ ] `--stories-only`, `--words-only`, `--language` flags filter correctly
- [ ] Known exceptions list suppresses flagged items
- [ ] Script can run without a running application server (reads from DB or seed files directly)

## Testing Requirements

- Script detects a story with word count outside difficulty range
- Script detects a dialogue story with inconsistent speaker labels
- Script detects a word with missing translation
- Script detects near-duplicate words
- Script reports uncovered story words as warnings
- Known exceptions are correctly suppressed
- `--json` output is valid JSON matching the expected schema
- Exit code is correct for pass and fail scenarios
- Script handles empty database gracefully (no crashes)
