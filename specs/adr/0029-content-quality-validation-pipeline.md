# ADR-0029: Content Quality Validation Pipeline

- **Status:** Proposed
- **Date:** 2026-04-05
- **Deciders:** Development team
- **Requirements:** REQ-16 (Content Quality Assurance), F-CONTENT-QA, F-CONTENT-REVIEW-STORIES
- **Related:** [ADR-0017](0017-content-seeding.md), [ADR-0011](0011-story-data-model.md)

## Context and Problem Statement

REQ-16 requires automated content quality checks (spelling, grammar, translation completeness, word coverage, pronunciation integrity) and a user-facing error reporting mechanism. The Content Quality Assurance FRD (F-CONTENT-QA) and Content Review for Stories FRD describe a validation pipeline that runs before content is published and a feedback loop for learners to report issues.

No architectural decision has been made on:
- Where validation runs (CI, pre-seed script, runtime API, or a combination)
- What tools are used for spelling and grammar checking across four languages
- How user-reported content errors are stored, tracked, and resolved
- Whether validation is a hard gate (blocking publication) or advisory (report with warnings)

The content library is growing with seed data, user-contributed words, and stories in four languages. Without a defined pipeline, quality issues reach learners and erode trust.

## Decision Drivers

- Must support four languages at launch (English, Danish, Italian, Spanish) with different linguistic rules
- Validation must run before seeded content enters the database (pre-publish gate)
- User-contributed words need real-time validation at submission time
- Learners need a way to report errors from the UI
- The team is small — tooling must be automatable, not dependent on manual review for every entry
- Must integrate with the existing Python backend (FastAPI + SQLAlchemy)
- Open-source or free-tier tools preferred to avoid recurring costs

## Considered Options

### Option 1: CLI validation script + LanguageTool + database error reports (Chosen)

A multi-layer approach:

**Layer 1 — Pre-seed validation (CLI script):**
A Python CLI script (`scripts/validate-content.py`) that runs against seed JSON files before seeding. It performs:
- Translation completeness checks (all languages present for every entry)
- Word coverage checks for stories (every token checked against the word dictionary)
- Dialogue format validation (speaker labels, speaker count limits)
- Story length tier validation (word count within difficulty-tier ranges)
- Duplicate detection (fuzzy matching on word entries)
- Phonetic hint presence checks

This script can run locally during authoring and in CI as a pre-merge gate.

**Layer 2 — Runtime input validation (API middleware):**
For user-contributed words, the existing FastAPI endpoint validates:
- Required fields present (word, at least one translation)
- No digits in word field
- No duplicate words (case-insensitive exact match)
- Character validation (letters, spaces, hyphens, apostrophes only)

This already exists per ADR-0018. No change needed.

**Layer 3 — Spelling and grammar checking (LanguageTool):**
Integrate [LanguageTool](https://languagetool.org/) for spelling and grammar validation of story text. LanguageTool is open-source, supports all four launch languages, and can run as a local Java server or via the free public API (rate-limited).

- For CI / pre-seed: call LanguageTool API during the validation script run
- For story authoring: optional preview step to check text before committing to seed files
- Not applied to individual word entries (too short for grammar checking to be meaningful)

**Layer 4 — User error reports (database table):**
A `ContentReport` table allows learners to flag issues:

```
ContentReport
  id              INTEGER PRIMARY KEY
  reporter_id     INTEGER NOT NULL  -- FK to User
  entity_type     TEXT NOT NULL     -- 'word', 'story'
  entity_id       INTEGER NOT NULL
  report_type     TEXT NOT NULL     -- 'wrong_translation', 'grammar', 'pronunciation', 'other'
  description     TEXT              -- free-text details from the user
  status          TEXT NOT NULL DEFAULT 'open'  -- 'open', 'acknowledged', 'resolved', 'dismissed'
  created_at      DATETIME NOT NULL
  resolved_at     DATETIME
```

A simple API endpoint allows authenticated users to submit reports. Reports are stored and can be queried by operators. No admin UI at launch — reports are reviewed via direct database queries or a future admin dashboard.

### Option 2: All-in-one validation service (custom microservice)

Build a dedicated validation microservice that handles all checks: spelling, grammar, completeness, duplicates, and error report management. The main backend calls this service for validation.

**Pros:**
- Clean separation of concerns
- Could be reused by other tools

**Cons:**
- Over-engineered for the current scale — adds deployment complexity, inter-service communication, and a second service to maintain
- The validation logic is tightly coupled to the content schema anyway
- Not justified until the content volume is significantly larger

### Option 3: Client-side validation only

Perform all validation in the frontend (spell-check via browser API, field presence checks in forms).

**Pros:**
- No backend changes needed
- Instant feedback to users

**Cons:**
- Browser spell-check is inconsistent across browsers and languages
- Cannot validate seed data (no browser involved in seeding)
- Cannot enforce quality gates in CI
- No server-side enforcement — bypassing the frontend skips all validation
- Does not address story text validation at all

### Option 4: External SaaS validation (Grammarly API, etc.)

Use a commercial grammar/spelling API for validation.

**Pros:**
- High accuracy, especially for English
- Regularly updated linguistic models

**Cons:**
- Recurring cost per API call
- Multi-language support varies by provider
- Privacy concerns — content sent to third-party servers
- External dependency for a core quality gate

## Decision Outcome

**Chosen: Option 1 — CLI validation script + LanguageTool + database error reports**

### Implementation Details

#### Pre-Seed Validation Script

```
scripts/validate-content.py

Usage:
  python scripts/validate-content.py --words seeds/words.json
  python scripts/validate-content.py --stories seeds/stories.json
  python scripts/validate-content.py --all seeds/

Exit codes:
  0 = all checks pass
  1 = errors found (blocks seeding / CI)
  2 = warnings only (advisory, does not block)
```

**Checks performed:**

| Check | Severity | Applies to |
|---|---|---|
| Missing translation in any language | Error | Words |
| Missing phonetic hint | Warning | Words |
| Missing example sentence | Warning | Words |
| Duplicate word (case-insensitive) | Error | Words |
| Story word count outside tier range | Error | Stories |
| Story word not in dictionary | Warning | Stories |
| Missing speaker label in dialogue story | Error | Stories |
| Speaker count exceeds 4 | Error | Stories |
| Spelling errors (via LanguageTool) | Warning | Stories |
| Grammar errors (via LanguageTool) | Warning | Stories |
| Translation length ratio anomaly | Warning | Words |

#### LanguageTool Integration

- Use the `language-tool-python` package (wraps the LanguageTool Java API)
- For CI: the script starts a local LanguageTool server or uses the public API
- LanguageTool supports: `en`, `da`, `it`, `es` — all four launch languages
- Grammar/spelling results are advisory (warnings), not blocking — human judgment is needed for false positives
- A `.languagetool-ignore` file can list known false positives to suppress

#### User Error Reporting API

```
POST /api/reports
  Body: { entity_type, entity_id, report_type, description }
  Auth: Required (logged-in users only)
  Response: 201 Created

GET /api/reports?status=open
  Auth: Required (future: admin-only)
  Response: List of ContentReport objects
```

- Rate limiting: max 10 reports per user per hour to prevent abuse
- Report types: `wrong_translation`, `grammar`, `pronunciation`, `other`
- Reports include the reporter's user ID for accountability
- No notification system at launch — operators check reports manually

#### Frontend Error Report UI

- A small "Report Error" button (flag icon) on word cards and story views
- Clicking opens a modal with:
  - Pre-filled context (which word/story)
  - Report type dropdown
  - Optional free-text description
  - Submit button
- Submitting shows a brief confirmation ("Thank you — we'll review this")

### CI Integration

The validation script runs as a CI step on any PR that modifies seed data files:

```yaml
- name: Validate content
  run: python scripts/validate-content.py --all seeds/
```

Errors block the merge. Warnings are reported but do not block.

## Consequences

**Positive:**
- Content quality is enforced before it reaches users — errors caught at authoring time
- LanguageTool provides multi-language spelling/grammar checking without recurring costs
- User error reports create a feedback loop — learners become quality contributors
- The validation script is reusable for any future content format
- CI integration prevents regressions in content quality

**Negative:**
- LanguageTool requires Java runtime (for local server) or internet access (for public API) during CI
- False positives from LanguageTool require a manual suppression list
- No admin UI for error reports at launch — review requires database access
- The validation script adds a step to the content authoring workflow

**Neutral:**
- User-contributed word validation remains unchanged (handled by existing API validation per ADR-0018)
- The `ContentReport` table is a simple append-only log — no complex workflow engine
- Pronunciation validation remains manual (human listening) — automated pronunciation accuracy checking is not feasible with current tools
