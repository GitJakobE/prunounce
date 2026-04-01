# ADR-0020: Host Persona Architecture — In-Code Static Definition with API Exposure

- **Status:** Accepted
- **Date:** 2026-03-29
- **Deciders:** Development team
- **Requirements:** REQ-7 (Host personas), REQ-8 (Host-first landing experience), REQ-3 (Audio pronunciation — per-host voice)

## Context and Problem Statement

The application has 12 host personas (4 per language) that are central to the user experience (REQ-7). Each host has a name, language, personality description (in 3 languages), greeting (in 3 languages), portrait image, colour accent, emoji, and a TTS voice assignment. The host selection is the first screen after login (REQ-8), and the chosen host determines both the target language and the TTS voice used for audio (REQ-3, ADR-0011).

The team needs to decide where and how to define, store, and serve host persona data: in the database, in configuration files, or in application code.

## Decision Drivers

- Host data is static and curated — changes only when a new language or host is added (not user-editable)
- 12 hosts at launch, extensible to more when new languages are added
- Each host defines text in all 3 reference languages (descriptions and greetings) — structured, multilingual data
- Persona data must be served via API (`GET /api/hosts`) for the frontend host selection UI
- TTS voice name must be accessible to the audio service at runtime to resolve per-host voice (ADR-0011)
- No admin UI for host management is in scope for v1

## Considered Options

### Option 1: In-code Python module with static list — Chosen

Define all host personas as a Python list of dictionaries in `app/hosts.py`. Serve directly via the `/api/hosts` endpoint. Provide a helper function `get_host(host_id)` for internal lookups (audio router, profile validation).

### Option 2: Database table seeded from JSON

Store hosts in a `Host` table alongside words and categories. Seed from a JSON file. Provides relational integrity (FK from User.hostId to Host.id) and querying capability. However, adds migration complexity for what is fundamentally static configuration, and requires a seed step before the API can serve hosts.

### Option 3: External JSON/YAML configuration file

Store hosts in a `hosts.json` or `hosts.yml` file loaded at startup. Separates data from code. However, adds file I/O on startup, a parsing dependency (for YAML), and the data is version-controlled alongside code regardless — no operational benefit over in-code definition.

### Option 4: Environment variables or settings

Define hosts via configuration. Completely impractical for 12 hosts × 12+ fields each. Configuration is for operational parameters, not structured domain data.

## Decision Outcome

**Chosen: Option 1 — In-code static definition in `app/hosts.py`**

### Implementation Details

**Module:** `app/hosts.py`

```python
HOSTS = [
    {
        "id": "marco",
        "name": "Marco",
        "language": "it",
        "emoji": "👨‍🍳",
        "imageUrl": "/hosts/marco.jpg",
        "descriptionEn": "A passionate Roman chef...",
        "descriptionDa": "En passioneret romersk kok...",
        "descriptionIt": "Uno chef romano appassionato...",
        "greetingEn": "Ciao! Let's cook up some beautiful Italian words!",
        "greetingDa": "Ciao! Lad os lave nogle smukke italienske ord sammen!",
        "greetingIt": "Ciao! Cuciniamo insieme delle belle parole italiane!",
        "color": "red",
        "voice": {"voiceName": "it-IT-DiegoNeural"},
    },
    # ... 11 more hosts
]

HOST_MAP = {h["id"]: h for h in HOSTS}
HOST_IDS = set(HOST_MAP.keys())

def get_host(host_id: str) -> dict:
    return HOST_MAP.get(host_id, HOST_MAP["marco"])
```

**API:** `GET /api/hosts` returns `{"hosts": HOSTS}` — the full list for the host selection UI.

**Internal usage:**
- Audio router calls `get_host(user.host_id)` to resolve the TTS voice name (ADR-0011)
- Profile router validates `hostId` against `HOST_IDS` before saving user preference
- Default fallback: if a user has no host selected, `get_host()` returns Marco (first Italian host)

### Host Data Schema

| Field | Type | Purpose |
|---|---|---|
| `id` | string | Stable identifier (e.g., `"marco"`, `"freja"`) |
| `name` | string | Display name |
| `language` | string | Target language code (`it`, `da`, `en`) |
| `emoji` | string | Visual identifier for compact UI |
| `imageUrl` | string | Path to AI-generated portrait image |
| `descriptionEn/Da/It` | string | Personality description in each reference language |
| `greetingEn/Da/It` | string | Greeting message in each reference language |
| `color` | string | Colour accent for visual identity |
| `voice.voiceName` | string | Edge TTS neural voice identifier |

### Consequences

**Positive:**
- Zero startup cost: no database query, no file parsing, no seed dependency — hosts are available immediately
- Type-safe lookups: `HOST_MAP` provides O(1) access by ID; `HOST_IDS` set enables fast validation
- Version-controlled: host changes go through the same code review process as any other change
- No migration required: adding a host is a code change, not a database migration
- Frontend receives the complete host list in a single API call — no joins or lookups needed

**Negative:**
- No relational integrity: `User.hostId` is a string column, not a foreign key to a `Host` table — invalid host IDs are caught by application validation, not database constraints
- Adding a new host requires a code deployment — cannot be done at runtime (acceptable for v1 where host additions are infrequent)
- All 12 hosts × all fields are serialised on every `GET /api/hosts` call — acceptable payload size (~5 KB) but not paginated

**Neutral:**
- Migrating to a database table later would be straightforward: create the table, seed from `HOSTS`, add FK constraint, update `User.hostId` references
- Portrait images are served as static files from a `/hosts/` directory — independent of the host data definition
- The `voice` field is a nested object to allow future expansion (e.g., `voice.pitch`, `voice.rate`) without flattening the schema
