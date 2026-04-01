# ADR-0011: Story Data Model — New Table with Structured Seed Files

- **Status:** Proposed
- **Date:** 2026-03-29
- **Deciders:** Development team
- **Requirements:** REQ-14 (Story Reading)

## Context and Problem Statement

The Story Reading feature (F-STORY) introduces curated long-form text content alongside the existing word dictionary. Stories are organised by target language and difficulty level, with each story containing a title, description, and full text body. The system needs to store, seed, and serve stories while reusing the existing multi-language and host-persona infrastructure. Key decisions include the database schema design, the relationship between story text and the dictionary (for word lookups), and the seed file format.

## Decision Drivers

- Stories are a new, independent content type — not directly a collection of Word records
- Each story belongs to a single target language and difficulty level
- Story descriptions need translations in all reference languages (same pattern as categories)
- Stories must be seedable idempotently from version-controlled files
- The frontend needs the full story text to render clickable words
- Estimated reading time should be derivable from the text length
- The data model should accommodate future growth (more stories per level, additional metadata)

## Considered Options

### Option 1: Dedicated `Story` table with full text stored as a single column (Chosen)

Add a `Story` table to the SQLAlchemy model with columns for language, difficulty, title, description translations (column-per-language, matching ADR-0006), and the full story text as a single `TEXT` column. Stories are independent of the `Word` table — word lookups happen at query time when a user clicks a word.

### Option 2: Story table with pre-tokenised word references

Store stories with the text broken into tokens, each linked to a `Word` record by foreign key. This pre-computes the word-to-dictionary mapping but is fragile: conjugated forms, punctuation, and words outside the dictionary break the model. It also tightly couples story content to the dictionary, making story authoring harder.

### Option 3: Stories as a special category of words

Reuse the existing `Word` and `Category` tables by creating a "Stories" category type and storing story text across multiple word entries. This overloads the word model for a fundamentally different content type, complicating queries and the frontend rendering.

### Option 4: Stories stored in files only (no database table)

Keep stories as JSON or Markdown files served directly, with no database representation. This simplifies storage but loses the ability to query stories by language/difficulty via the API, track reading progress in the database, or extend with user-generated stories later.

## Decision Outcome

**Chosen: Option 1 — Dedicated `Story` table with full text column**

### Schema Design

```python
class Story(Base):
    __tablename__ = "Story"
    __table_args__ = (
        UniqueConstraint("slug", "language", name="Story_slug_language_key"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    slug: Mapped[str] = mapped_column(String, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False)  # "it", "da", "en"
    difficulty: Mapped[str] = mapped_column(String, nullable=False)  # "beginner", "intermediate", "advanced"
    title: Mapped[str] = mapped_column(String, nullable=False)  # in the target language
    description_en: Mapped[str] = mapped_column("descriptionEn", String, nullable=False, default="")
    description_da: Mapped[str] = mapped_column("descriptionDa", String, nullable=False, default="")
    description_it: Mapped[str] = mapped_column("descriptionIt", String, nullable=False, default="")
    body: Mapped[str] = mapped_column(String, nullable=False)  # full story text in target language
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
```

### Key Design Decisions

| Decision | Rationale |
|---|---|
| Separate `Story` table | Stories are structurally different from words — they have a body, title, and no phonetic hint or category association |
| `slug` + `language` unique constraint | Enables idempotent seeding — the same story concept across languages has the same slug |
| Full text in `body` column | The frontend handles tokenisation for clickable words; storing raw text keeps the schema simple and allows story text to be authored naturally |
| Column-per-language for descriptions | Follows the established pattern from ADR-0006 (same as Category `nameEn`/`nameDa`/`nameIt`) |
| `order` column | Controls display order within a difficulty level, matching the Category model pattern |
| No foreign key to `Word` | Word lookups are performed on-demand when a user clicks a word — this avoids coupling stories to the dictionary and handles conjugated/unknown words gracefully |

### Seed File Format

Stories are seeded from a JSON file (`stories-seed.json`) alongside the existing word seed files:

```json
[
  {
    "slug": "cafe-introduction",
    "language": "it",
    "difficulty": "beginner",
    "title": "Un caffè a Roma",
    "descriptionEn": "Introduce yourself at a Roman café",
    "descriptionDa": "Præsentér dig selv på en romersk café",
    "descriptionIt": "Presentati in un caffè romano",
    "body": "Buongiorno! Mi chiamo Marco. Sono in un caffè a Roma. ...",
    "order": 1
  }
]
```

The seed process uses `slug` + `language` as the upsert key, matching the existing idempotent pattern.

### API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /api/stories?lang={target}` | List all stories for a target language, grouped by difficulty |
| `GET /api/stories/{storyId}` | Get a single story with full body text |
| `GET /api/dictionary/lookup?word={word}&lang={language}` | Look up a single word for the translation panel (reuses existing dictionary data) |

### Consequences

**Positive:**
- Clean separation of concerns — stories don't overload the word model
- Simple schema that follows existing conventions (column-per-language, UUID primary keys, idempotent seeding)
- Story text is authored as plain natural-language text — no special markup required
- No coupling between story content and dictionary entries — stories can contain any words
- The `lookup` endpoint is reusable by other features that need single-word translation

**Negative:**
- Clicking a word in a story may return "Translation not available" if the word isn't in the dictionary (conjugated forms, rare words) — this is an accepted limitation documented in the FRD
- No full-text search on story content — acceptable since stories are browsed by difficulty, not searched
- Adding a fourth reference language requires adding a `description_xx` column — same migration pattern as ADR-0006

**Neutral:**
- Reading time is computed in the API response from `len(body.split())` rather than stored — avoids data staleness if text is edited
- Story reading progress (which stories a user has read/completed) can be added later with a `UserStoryProgress` join table, following the `UserProgress` pattern
