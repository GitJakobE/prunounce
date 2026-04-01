# ADR-0017: Content Seeding — JSON Seed Files with Idempotent Python Script

- **Status:** Accepted
- **Date:** 2026-03-29
- **Deciders:** Development team
- **Requirements:** REQ-2 (Curated word dictionary), REQ-10 (Example sentences), REQ-11 (Content seeding)

## Context and Problem Statement

The application launches with a curated dictionary of ~250+ words per language across 10+ categories and 3 difficulty levels (REQ-2). Each word includes translations in all three reference languages, phonetic hints, and example sentences with translations (REQ-10). This initial corpus must be loaded into the database reliably, and re-running the seed process must not create duplicates or lose data (REQ-11: "the seed process is idempotent"). The team needs to decide on the seed data format, storage location, and loading mechanism.

## Decision Drivers

- Idempotent seeding: running the script multiple times must produce the same database state
- Human-editable format: content curators need to review and update words without programming knowledge
- Multi-language support: seed data must cover Italian, Danish, and English words with cross-language translations
- Example sentences: each word needs example sentences in all three languages, linked by word key
- Category assignment: words must be mapped to categories with stable IDs
- Compatibility: the Python backend (ADR-0010) must be able to consume the seed data

## Considered Options

### Option 1: JSON seed files per language with a Python seed script — Chosen

Structured JSON files in `src/backend/data/` (one per language: `seed-words.json`, `seed-words-da.json`, `seed-words-en.json`) plus companion example files (`examples.json`, `examples-da.json`, `examples-en.json`). A standalone Python script reads these files and upserts into the database using SQLAlchemy.

### Option 2: CSV/TSV files

Flat tabular format. Easy to edit in spreadsheets. However, nested structures (categories array, multi-language translations) require awkward encoding (comma-separated category IDs in a single cell). Poor fit for hierarchical data.

### Option 3: YAML seed files

More human-readable than JSON for nested data. However, introduces a YAML parsing dependency, whitespace-sensitive editing can cause subtle bugs, and the existing seed data was already authored in JSON format.

### Option 4: SQL seed scripts

Direct SQL INSERT statements. Most precise database control. However, not human-friendly for content editing, ties seed data to the exact schema DDL, and SQLite-specific syntax would need maintenance if the database changes.

### Option 5: Alembic data migrations

Embed seed data in Alembic migration scripts. Ensures seeds run exactly once as part of schema history. However, conflates schema evolution with content loading, makes content updates require new migrations, and prevents re-seeding without rolling back.

## Decision Outcome

**Chosen: Option 1 — JSON seed files with idempotent Python script**

### Data File Layout

```
src/backend/data/
├── seed-words.json        # Italian words + categories (canonical category list)
├── seed-words-da.json     # Danish words
├── seed-words-en.json     # English words
├── examples.json          # Italian example sentences (keyed by word)
├── examples-da.json       # Danish example sentences
└── examples-en.json       # English example sentences
```

### Seed Script

`src/backend-python/seed_data.py` — run with `py -m poetry run python seed_data.py`

**Idempotency strategy:**
- Categories: upsert by primary key (`db.get(Category, id)`) — updates if exists, inserts if not
- Words: upsert by unique constraint (`word` + `language`) — updates all fields if exists, inserts if not
- WordCategory join records: check existence before inserting to avoid duplicate associations
- The script calls `Base.metadata.create_all()` to ensure tables exist before seeding

**Data flow:**
1. Load Italian seed file (contains the canonical category list used by all languages)
2. Seed categories from the Italian file
3. Transform and seed Italian words with examples
4. Load and seed Danish words with examples
5. Load and seed English words with examples
6. Print summary counts

### JSON Schema (per word entry — Italian example)

```json
{
  "italian": "bruschetta",
  "phoneticHint": "broo-SKET-tah",
  "translationEn": "toasted bread with toppings",
  "translationDa": "ristet brød med topping",
  "difficulty": "beginner",
  "categories": ["cat-food"]
}
```

Danish and English files use a normalised format with `word`, `language`, `phoneticHint`, `translationEn`, `translationDa`, `translationIt`, `difficulty`, and `categories` fields.

### Consequences

**Positive:**
- Fully idempotent: safe to re-run after content updates without data loss or duplication
- Human-readable JSON is reviewable by non-developers and version-controllable
- Separate example files keep word definitions concise while supporting rich example sentences
- Per-language files allow independent content curation per language team
- Script prints row counts for verification

**Negative:**
- Seed data lives in `src/backend/data/` (the original Node backend directory) — a legacy path that works but is counterintuitive for the Python backend
- JSON lacks inline comments — content curators cannot annotate decisions within the data files
- Category IDs must be manually coordinated across files (e.g., `cat-food` must exist in the categories array)
- No automated validation of seed data structure before loading — malformed JSON fails at runtime

**Neutral:**
- Moving seed data to a shared `data/` top-level directory would be a future cleanup but is not blocking
- The script can be extended to validate JSON structure before loading if data quality becomes a concern
