# ADR-0018: User-Contributed Words — Community Trust Model Without Moderation

- **Status:** Accepted
- **Date:** 2026-03-29
- **Deciders:** Development team
- **Requirements:** REQ-9 (User-contributed words)

## Context and Problem Statement

Logged-in users can add new words to the shared dictionary (REQ-9). Contributed words are visible to all users immediately — they appear alongside curated seed words in category listings, search results, and progress tracking (F-UGC §3.4). The team needs to decide how to handle content quality and potential abuse: should submissions go through a review process, or should they be published immediately with no moderation?

The PRD explicitly states: "A community-trust model (no moderation) is acceptable for user-contributed words at launch; moderation can be introduced in a later version if needed."

## Decision Drivers

- Immediate availability: users expect their contributed word to be playable right after submission (F-UGC US-UGC2)
- Low operational overhead: no admin UI or moderator role is in scope for v1 (PRD §2 Out of Scope)
- Dictionary integrity: prevent obvious abuse (duplicate entries, empty submissions, overly long text)
- Audio generation cost: every accepted word triggers TTS generation (ADR-0011)
- Future extensibility: moderation could be added later without restructuring the data model

## Considered Options

### Option 1: Community trust model with input validation only — Chosen

Publish user-contributed words immediately with no human review. Prevent abuse through automated validation rules: required fields, duplicate detection (case-insensitive, diacritics-ignored), character limit (100 chars), and rejection of numeric/special-character-only entries.

### Option 2: Admin moderation queue

Submissions enter a "pending" state and are only visible after an admin approves them. Highest content quality guarantee. However, requires an admin UI, moderator accounts, and introduces delay between submission and availability — contradicting the immediate-use expectation.

### Option 3: Community flagging

Users can flag inappropriate words, and flagged words are hidden after a threshold. Lighter than admin moderation but still requires flag tracking, threshold logic, and a review/appeal process. Adds complexity disproportionate to the expected v1 user base.

### Option 4: AI-based content filtering

Run submitted words through a content classification model to auto-reject offensive or nonsensical entries. Adds an external dependency (or model hosting), latency to the submission flow, and false-positive risk for legitimate words in foreign languages.

## Decision Outcome

**Chosen: Option 1 — Community trust with input validation**

### Validation Rules (F-UGC §3.1, §3.5, §4)

| Rule | Implementation |
|---|---|
| Word field required and non-empty | Schema validation (Pydantic) |
| Translation required in user's reference language | Schema validation |
| Duplicate check (same word + same target language, case-insensitive) | Database query before insert |
| Max length: 100 characters for word field | Schema validation |
| Reject words containing only numbers, special characters, or whitespace | Regex validation |
| Optional: category (defaults to "Uncategorised"), difficulty (defaults to Beginner) | Schema defaults |

### Data Model Support

- `Word.source` column distinguishes `"seed"` vs `"user"` entries — enables future filtering or moderation scoping
- `Word.contributed_by` column (FK to `User.id`, `ON DELETE SET NULL`) — tracks contributor but words survive account deletion (GDPR: words remain, attribution removed)
- No `status` or `approved` column in v1 — all words are immediately visible

### Consequences

**Positive:**
- Zero operational overhead — no admin UI, no moderator role, no review queue
- Contributed words are immediately playable, matching user expectation (F-UGC US-UGC2)
- Automated validation prevents the most common abuse vectors (duplicates, empty, long, garbage)
- `source` column provides a future hook for moderation without schema migration

**Negative:**
- Offensive or incorrect words can appear in the dictionary until manually removed via direct database access
- No mechanism for users to report or flag problematic contributions in v1
- TTS audio is generated for every accepted word, including low-quality contributions — wastes cache space but minimal actual cost (Edge TTS is free)

**Neutral:**
- Adding a `status` column and admin review later would be a simple migration — the architecture does not foreclose moderation
- The expected v1 user base is small enough that manual database cleanup (if needed) is feasible
