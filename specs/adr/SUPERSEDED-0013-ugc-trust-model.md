# ADR-0013: User-Generated Content Trust Model — Immediate Publish, No Moderation at Launch

- **Status:** Accepted
- **Date:** 2026-03-29
- **Deciders:** Development team, Product owner
- **Requirements:** F-UGC (User-Contributed Words), REQ-9

## Context and Problem Statement

The User-Contributed Words FRD (F-UGC) allows any logged-in user to add words to the shared dictionary. Contributed words are immediately visible to all users and integrated into category listings, search, and progress tracking. The PRD explicitly states that an "Admin UI for content moderation" is out of scope for v1, relying on a "community trust model." The team needs to decide how to handle content quality and abuse prevention at launch without a moderation system.

## Decision Drivers

- The PRD scopes moderation to v2 — any moderation system would delay launch
- The expected user base at launch is small (target: 500 unique visitors/month within 6 months)
- Contributed words require authentication — anonymous submissions are not possible
- Each contribution is associated with a user account, providing accountability
- The word contribution form has built-in validation (duplicate detection, non-empty fields)
- TTS audio is auto-generated for contributed words, which could be exploited to generate audio for offensive content

## Considered Options

### Option 1: Immediate Publish with Lightweight Safeguards (Chosen)

All contributions are published immediately. Protection relies on authentication (accountability), duplicate detection, rate limiting on the contribution endpoint, and a basic word-length/character-set validation. No human review before publication.

### Option 2: Moderation Queue (Pre-Publish Review)

Contributions enter a queue and are not visible until approved by a moderator. This prevents abuse but requires building a moderation UI and assigning moderator roles — directly contradicting the PRD's scope decision.

### Option 3: Post-Publish Flagging

Contributions are published immediately, but other users can flag content for review. Flagged items are hidden until reviewed. This is lighter than a full queue but still requires a flag UI, a review UI, and moderator roles.

### Option 4: AI Content Filter

Run contributed words through a content-filtering API (e.g., Azure Content Safety) before publishing. Catches obviously offensive content but adds an external dependency, latency, and cost, and may produce false positives for legitimate words in foreign languages.

## Decision Outcome

**Chosen: Option 1 — Immediate Publish with Lightweight Safeguards**

At the expected scale, the risk of abuse is low and the cost of building moderation outweighs the benefit. Lightweight safeguards provide a reasonable baseline.

### Safeguards at Launch

| Safeguard | Implementation | Purpose |
|---|---|---|
| **Authentication required** | All contributions require a valid JWT | Links every contribution to an identifiable user |
| **Rate limiting** | Max 10 word contributions per user per hour | Prevents bulk spam submissions |
| **Duplicate detection** | Case-insensitive, diacritical-normalized check against existing words | Prevents flooding with variants of existing words |
| **Character validation** | Word must contain only letters, hyphens, apostrophes, and spaces; max 100 characters | Blocks injection of URLs, code, or excessively long strings |
| **Attribution tracking** | `contributed_by` field stored on each word (de-attributed but not deleted on account deletion) | Enables retroactive cleanup if a user is identified as abusive |
| **Seed-word protection** | Seeded words cannot be overwritten or duplicated by contributions | Protects the curated dictionary baseline |

### Preparation for v2 Moderation

The data model should support a future transition to moderated contributions:
- A `status` field on contributed words (default: `published`) can later support `pending` and `rejected` states without schema changes
- The `contributed_by` foreign key enables per-user contribution auditing

### Consequences

**Positive:**
- No launch delay — no moderation UI to build
- Contributors see their words immediately, encouraging participation (goal G-5: ≥ 50 contributions in 3 months)
- Simple implementation aligned with current scope

**Negative:**
- Risk of inappropriate or low-quality content appearing in the dictionary
- If abuse occurs before v2 moderation is built, cleanup is manual (direct database intervention)
- Auto-generated TTS audio for offensive words could be embarrassing

**Neutral:**
- The small expected user base (authenticated only) makes widespread abuse unlikely
- The `status` field prepares for a smooth transition to moderation in v2
- Rate limiting also protects the TTS service from excessive audio generation requests
