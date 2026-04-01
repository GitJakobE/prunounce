# Task 018: Expand Host Personas — Danish & English Hosts

**Feature:** F-HOST (Host Personas & Landing Experience)
**Priority:** P0
**Dependencies:** 017 (Schema Migration)

## Description

Expand the host persona system from 4 Italian-only hosts to 12 hosts across three languages (4 Italian, 4 Danish, 4 English). Each host must have a `language` field linking it to a target language, descriptions and greetings in all three reference languages (English, Danish, Italian), a distinct TTS neural voice in their native language, a colour accent, and a portrait image.

## Technical Requirements

### Host Data Model Changes
- Add a `language` field to the Host interface indicating which target language this host represents (`"it"`, `"da"`, `"en"`)
- Add `descriptionIt` and `greetingIt` fields for Italian-language descriptions/greetings
- Update existing 4 Italian hosts to include the `language: "it"` field and Italian descriptions/greetings

### New Danish Hosts (4)
- **Anders** — Copenhagen barista, hygge culture, male warm voice (da-DK neural voice)
- **Freja** — Aarhus librarian, Nordic literature, female clear voice (da-DK neural voice)
- **Mikkel** — Odense student, Danish design, male younger voice (da-DK neural voice)
- **Ingrid** — Jutland grandmother, traditions, female gentle voice (da-DK neural voice)

### New English Hosts (4)
- **James** — London tour guide, British culture, male warm voice (en-GB neural voice)
- **Emma** — Oxford professor, literature/etymology, female clear voice (en-GB neural voice)
- **Ryan** — Australian surfer, casual English, male younger voice (en-AU neural voice)
- **Margaret** — Scottish grandmother, stories/wisdom, female gentle voice (en-GB neural voice)

### TTS Voice Assignments
- Identify and assign 4 distinct Danish (da-DK) neural voices from the Edge TTS catalogue
- Identify and assign 4 distinct English neural voices (mix of en-GB, en-US, en-AU as appropriate to persona)
- Verify all selected voices are available and functional

### Portrait Images
- Generate or download portrait images for all 8 new hosts (512×512px)
- Place in `src/backend/public/hosts/` alongside existing Italian host images
- Naming convention: `{hostId}.jpg` (e.g., `anders.jpg`, `freja.jpg`)

### API Updates
- Update the `GET /api/hosts` endpoint to return all 12 hosts
- Add a `language` field to the host response so the frontend can group hosts by language
- The `getHost()` utility should work for all 12 host IDs

### Frontend Host Type
- Update the frontend `Host` TypeScript interface to include the `language` field and Italian description/greeting

## Acceptance Criteria

- [ ] 12 hosts total are defined: 4 Italian, 4 Danish, 4 English
- [ ] Each host has a `language` field matching its target language
- [ ] Each host has descriptions and greetings in English, Danish, and Italian
- [ ] Each host has a distinct TTS neural voice in its native language
- [ ] All 12 TTS voices are functional (can generate audio)
- [ ] Portrait images exist for all 12 hosts
- [ ] `GET /api/hosts` returns all 12 hosts with language field
- [ ] Frontend Host type includes the new fields

## Testing Requirements

- All 12 host IDs are valid and resolve via `getHost()`
- Each language group has exactly 4 hosts
- All host portrait images are accessible via HTTP
- TTS voice for each host can generate a test utterance without error
