# 📝 Product Requirements Document (PRD)

## 1. Purpose

**Pronuncia** is a public-facing web application that helps users learn how to pronounce words in multiple languages. The platform supports learning Italian, Danish, and English pronunciation, with each language guided by its own set of native host personas who speak in their language. Users choose which language they want to learn and which reference language they want translations displayed in. Beyond fixed vocabulary, users can contribute their own words to the shared dictionary, with audio automatically generated for new entries.

Existing dictionaries and translation tools are not optimised for quick, audio-first pronunciation practice. Users need a focused, simple tool that lets them hear correct pronunciation across languages, organised by category and difficulty to support progressive learning, and that grows with community contributions.

### Target Users

| Persona | Description |
|---|---|
| **Beginner Learner** | An adult starting to learn a new language who needs to hear correct pronunciation of common words (e.g., Patrizia — Italian retiree learning Danish to connect with her grandchildren's community). |
| **Intermediate Learner** | Someone with basic knowledge of the target language who wants to improve pronunciation of more complex or commonly mispronounced words (e.g., Mette — Danish professional refining her Italian for client work). |
| **Traveller** | A person preparing for a trip who wants quick access to key phrases and words sorted by practical category (e.g., Thomas — British logistics manager grabbing phrases before weekend trips). |
| **Exchange / Immersion Student** | A young adult living abroad who already speaks English well and wants to learn the local language to integrate socially (e.g., Aiden — Canadian student at DTU learning Danish). |
| **Accessibility-Dependent User** | A user who relies on assistive technology (screen readers, keyboard navigation, high contrast) and needs the product to be fully accessible (e.g., Farah — low-vision translator learning Italian). |
| **Contributor / Power User** | A tech-savvy user who exhausts the curated word list quickly and contributes new words, tests edge cases, and pushes the system (e.g., Nikolaj — Danish teen adding slang and switching languages). |

> **Full persona backgrounds** — see [User Review Panel](user-review-panel.md) for the six standing review personas that map to these groups.

## 2. Scope

### In Scope

- **Multi-language learning** — Users can learn pronunciation in Italian, Danish, or English, with reference translations in any of the other supported languages
- **Language-specific host personas** — Four host personas per target language (12 total at launch), each speaking in their native language with a distinct TTS voice
- **Host-first landing experience** — Host selection is the first interaction after login; the chosen host defines the target language and persists across sessions
- **Curated word dictionary** organised by 10+ thematic categories and 3 difficulty levels (~25 words per category–difficulty group)
- **User-contributed words** — Any logged-in user can add new words to the shared dictionary; TTS audio is auto-generated for new entries
- **Audio pronunciation** powered by Microsoft Edge TTS with per-host distinct neural voices and caching
- User authentication (email/password) with session persistence
- Word search and lookup (by target-language word or reference-language word)
- Progress tracking (words listened to, per-category completion)
- Contextual example sentences with audio
- **Story Reading mode** — A top-level learning section alongside Categories, offering curated stories in the target language at three difficulty levels (Beginner, Intermediate, Advanced), with host narration at five speed settings and an inline word translation panel
- **Story dialogue formatting** — Conversational stories are displayed in play/script format with speaker attribution so learners know who is saying what; narration includes vocal differentiation between speakers
- **Content quality assurance** — Automated validation checks for spelling, grammar, translation completeness, and pronunciation accuracy across stories and words, plus a user-facing error reporting mechanism for learners to flag issues
- Content seeding from a structured data file (words and stories)
- GDPR-compliant account deletion
- Responsive web design (mobile, tablet, desktop)
- Public internet deployment

### Out of Scope

- Practice mode / quiz functionality
- Pronunciation recording and comparison (speech recognition)
- Target languages beyond Italian, Danish, and English
- Mobile native apps (web-responsive only)
- Offline mode
- Admin UI for content moderation (community trust model for v2)

## 3. Goals & Success Criteria

| # | Goal | Success Metric |
|---|---|---|
| G-1 | Provide a useful, publicly accessible multi-language pronunciation tool | ≥ 500 unique visitors/month within 6 months of launch |
| G-2 | Build a growing word library across all supported languages | ≥ 10 categories with ≥ 25 words each per language at launch |
| G-3 | Support multi-language audiences and learning directions from day one | Full UI, word translations, and host personas for Italian, Danish, and English at launch |
| G-4 | Encourage repeat usage through personalisation and contribution | ≥ 30% of registered users return within 7 days |
| G-5 | Grow the dictionary through user contributions | ≥ 50 user-contributed words within 3 months of launch |

## 4. High-Level Requirements

- [REQ-1] **Multi-language learning** — Users choose a target language (the language they want to learn to pronounce) and a reference language (the language they understand). The platform supports Italian, Danish, and English as both target and reference languages. The target language determines which words/audio are shown; the reference language determines which translations and UI text are displayed. Both preferences persist across sessions.
- [REQ-2] **Curated word dictionary** — Words are organised into at least 10 thematic categories (e.g., Greetings, Food & Drink, Travel, Numbers) with three difficulty levels (Beginner, Intermediate, Advanced). Each category–difficulty group targets ~25 words. Each word entry shows the target-language word, a phonetic hint, and the reference-language translation.
- [REQ-3] **Audio pronunciation** — Every word has a pronunciation audio clip in the target language, generated via Microsoft Edge TTS with language-appropriate neural voices. Clicking a word plays its pronunciation immediately (< 1 s latency). Audio is cached after first generation. After the word pronunciation, an example sentence using that word in context is played automatically.
- [REQ-4] **User authentication** — Users register with email/password. All content is gated behind login. Sessions persist across visits. Users can delete their account and all associated data (GDPR).
- [REQ-5] **Word search & lookup** — A global search bar lets users type a word in the target language or their reference language. Matching results display inline with translation and a play button. Search is case-insensitive and tolerant of missing diacritical marks.
- [REQ-6] **Progress tracking** — The system records which words a user has listened to. Words already played show a visual indicator. A summary view shows per-category completion (e.g., “12 / 25 practised”). Category names in the progress view must be displayed in the user’s reference language.
- [REQ-7] **Host personas** — Each supported language has four host personas, each with a distinct name, portrait image, personality, TTS voice, and greeting. The user's chosen host determines both their guide and their target language. Hosts are the central identity of the experience.
- [REQ-8] **Host-first landing experience** — After login, the first screen the user sees is a host selection page showcasing all available hosts grouped by language. Selecting a host sets both the target language and the persona. The chosen host can be switched at any time via a control in the top-right corner of every page.
- [REQ-9] **User-contributed words** — Logged-in users can add new words to the shared dictionary. Each submission includes the word in the target language and a translation in at least one supported language (the contributor’s reference language is required; the other two languages are optional but encouraged). Words must contain only letters, spaces, hyphens, and apostrophes — digits are rejected. TTS audio is auto-generated for new words that don’t already have cached audio. User-contributed words are visible to all users.
- [REQ-10] **Contextual example sentences** — Every word entry includes an example sentence in the target language that uses the word in natural context, along with translations into each reference language. The example is displayed on the word card and its audio plays automatically after the word pronunciation.
- [REQ-11] **Content seeding** — The initial word dictionary is loaded from structured seed files containing words, phonetic hints, categories, difficulties, example sentences, and translations for each supported language. The seed process is idempotent.
- [REQ-12] **Data persistence** — User accounts, preferences (including host selection and language choices), progress, contributed words, and the word dictionary are stored persistently, surviving server restarts and accessible across devices.
- [REQ-13] **API surface** — The frontend communicates with the backend through APIs covering: authentication, user profile, dictionary browsing, word contribution, search, audio retrieval, story listing/retrieval, and host persona listing. All responses include appropriate error information.
- [REQ-14] **Story Reading** — Users can browse and read curated stories in the target language, organised by difficulty level (Beginner, Intermediate, Advanced), with at least 3 stories per level per language at launch. The host reads stories aloud at five selectable speeds with karaoke-style text highlighting. Clicking any word in the story opens a translation panel showing the reference-language translation, phonetic hint, and a play button for that word's pronunciation. Story length tiers must produce materially different reading experiences rather than scaled versions of the same template, and the story library must span varied setups, settings, and narrative patterns so stories do not all begin from the same premise.
- [REQ-15] **Story Dialogue Formatting** — Conversational stories must be formatted in a play/script style with named speaker labels for each line of dialogue, so learners can follow who is saying what. The system supports both narrative and dialogue story types, with vocal differentiation during host narration.
- [REQ-16] **Content Quality Assurance** — All seeded and contributed content must pass automated quality checks (spelling, grammar, translation completeness, word coverage, pronunciation integrity) before publication. Users can report content errors (wrong translation, grammar mistake, pronunciation issue) from the learning interface, and reported issues are tracked through a review workflow.
- [REQ-17] **Security Hardening** — The system must enforce secure defaults for secret management, token handling, and request processing. Required secrets must be validated at startup. Authentication tokens must not be exposed in logs or browser history beyond what is technically unavoidable. Request payloads must be size-limited. Security-relevant HTTP headers must be present in all responses.
- [REQ-18] **On-the-Fly Word Lookup & Audio** — When a user clicks a word in a story that is not in the curated dictionary, the system must attempt to translate it on-the-fly using an external translation source and generate pronunciation audio via TTS if no cached audio exists. Results must be cached for subsequent use. Auto-translated results must be visually distinguished from curated dictionary entries. First-click latency for uncached words must not exceed 3 seconds; cached results must respond within 1 second.

## 5. User Stories

### Language & Host Selection

```gherkin
As a first-time user, I want to see all available hosts grouped by language after login,
so that I can choose both my guide and the language I want to learn.
```

```gherkin
As a user, I want to switch my host at any time from the top-right corner,
so that I can change my target language or persona without navigating away.
```

```gherkin
As a returning user, I want my chosen host to greet me when I open the app,
so that the experience feels familiar and my preference is remembered.
```

```gherkin
As a user, I want to choose my reference language independently of my target language,
so that I see translations in the language I understand best.
```

### Learning & Browsing

```gherkin
As a learner, I want to choose between Categories and Stories from the main page,
so that I can pick the learning mode that suits me.
```

```gherkin
As a learner, I want to browse words by category and difficulty,
so that I can focus on topics and levels relevant to me.
```

```gherkin
As a learner, I want to click a word and hear it pronounced in the target language,
so that I can learn the correct pronunciation.
```

```gherkin
As a learner, I want to replay a pronunciation as many times as I want,
so that I can practise until I feel confident.
```

```gherkin
As a user, I want to search for a specific word,
so that I can quickly find and hear any word in the dictionary.
```

```gherkin
As a learner, I want to hear each word used in an example sentence after the pronunciation,
so that I understand how the word is used in context.
```

```gherkin
As a learner, I want to see the example sentence written out with a translation,
so that I can read along and reinforce my understanding.
```

### Story Reading

```gherkin
As a learner, I want to read curated stories in my target language at my level,
so that I can practise reading comprehension with connected text.
```

```gherkin
As a learner, I want short stories to feel genuinely shorter and simpler than long stories,
so that choosing a level changes the scope and effort of the reading task.
```

```gherkin
As a learner, I want stories to begin from different kinds of situations,
so that the library feels varied instead of repetitive.
```

```gherkin
As a learner, I want my host to read a story aloud at a speed I choose,
so that I can listen and follow along at a comfortable pace.
```

```gherkin
As a learner, I want to click any word in a story and see its translation, phonetic hint, and a play button,
so that I can understand unfamiliar words without leaving the page.
```

```gherkin
As a learner, I want the text to highlight along with the narration,
so that I can follow where the host is reading.
```

```gherkin
As a learner, I want to see who is speaking each line in a dialogue story,
so that I can follow the conversation naturally like reading a play.
```

```gherkin
As a learner, I want to hear distinct vocal characteristics for each character during narration,
so that I can tell who is speaking even with my eyes closed.
```

### Content Quality

```gherkin
As a learner, I want to report an error I notice in a story or word entry,
so that it gets reviewed and fixed.
```

```gherkin
As a content author, I want automated checks to catch grammar and spelling errors before publishing,
so that learners never encounter broken content.
```

```gherkin
As a content author, I want a validation report showing which story words have no dictionary match,
so that I can fill gaps before the story goes live.
```

### User-Contributed Words

```gherkin
As a user, I want to add a new word to the dictionary,
so that I and other learners can practise its pronunciation.
```

```gherkin
As a user who added a new word, I want audio to be generated automatically,
so that the word is immediately usable for pronunciation practice.
```

```gherkin
As a contributor, I want to provide translations in all three languages when adding a word,
so that learners in every language group benefit from my contribution.
```

```gherkin
As a learner, I want to see user-contributed words mixed into the dictionary,
so that the word library continually grows.
```

### Account & Progress

```gherkin
As a new visitor, I want to create an account and log in,
so that my progress and preferences are saved.
```

```gherkin
As a returning user, I want to see which words I've already listened to,
so that I can track my progress.
```

```gherkin
As a user, I want to delete my account and all my data,
so that my personal information is removed in compliance with GDPR.
```

## 6. Assumptions & Constraints

### Assumptions

- Microsoft Edge TTS (msedge-tts) is available and reliable for Italian, Danish, and English neural voice generation.
- The initial word list (~250+ words per language) will be curated manually and maintained in seed files.
- Users have a modern browser with audio playback support (no plugins required).
- Each supported language has at least four suitable neural TTS voices available in the Edge TTS voice catalogue.
- English is an acceptable fallback when a translation is missing in another reference language.
- A community-trust model (no moderation) is acceptable for user-contributed words at launch; moderation can be introduced in a later version if needed.

### Constraints

- Edge TTS introduces a dependency on Microsoft's neural voice service; mitigated by caching all generated audio.
- Adding a new target language requires: new host personas, new TTS voice assignments, seed data for that language, and translations for all existing reference languages.
- The site must comply with GDPR for EU users.
- User-contributed words without example sentences will have reduced learning value compared to curated entries.

---

### Feature Requirements Documents

| Feature | FRD | Req |
|---|---|---|
| Multi-language learning | [multi-language-support.md](features/multi-language-support.md) | REQ-1 |
| Word dictionary & categories | [word-dictionary.md](features/word-dictionary.md) | REQ-2, REQ-11 |
| Audio pronunciation | [audio-pronunciation.md](features/audio-pronunciation.md) | REQ-3 |
| User authentication | [user-authentication.md](features/user-authentication.md) | REQ-4 |
| Word search & lookup | [word-search.md](features/word-search.md) | REQ-5 |
| Progress tracking | [progress-tracking.md](features/progress-tracking.md) | REQ-6 |
| Host personas & landing experience | [host-personas.md](features/host-personas.md) | REQ-7, REQ-8 |
| User-contributed words | [user-contributed-words.md](features/user-contributed-words.md) | REQ-9 |
| Contextual example sentences | [example-sentences.md](features/example-sentences.md) | REQ-10 |
| Story Reading | [story-reading.md](features/story-reading.md) | REQ-14 |
| Story Dialogue Formatting | [story-dialogue-formatting.md](features/story-dialogue-formatting.md) | REQ-15 |
| Content Quality Assurance | [content-quality-review.md](features/content-quality-review.md) | REQ-16 |
| Security hardening | [security-hardening.md](features/security-hardening.md) | REQ-17 |
| On-the-fly word lookup & audio | [on-the-fly-word-lookup.md](features/on-the-fly-word-lookup.md) | REQ-18 |
| Accessibility & inclusive design | [accessibility.md](features/accessibility.md) | Cross-cutting |
| Responsive design & mobile usability | [responsive-design.md](features/responsive-design.md) | Cross-cutting |

### Architecture Decision Records

| ADR | Decision | Status | Related Req / FRD |
|---|---|---|---|
| [ADR-0001](adr/0001-frontend-framework.md) | Frontend: React 19 + Vite 6 + Tailwind CSS 4 | Accepted | REQ-1, REQ-2, REQ-5, REQ-7 |
| [ADR-0002](adr/0002-backend-framework.md) | Backend: Express 5 + TypeScript | **Superseded** by ADR-0010 | — |
| [ADR-0003](adr/0003-database.md) | Database: SQLite (ORM updated to SQLAlchemy per ADR-0010) | Partially superseded | REQ-12 |
| [ADR-0004](adr/0004-authentication.md) | Authentication: Stateless JWT | Accepted | REQ-4, F-AUTH |
| [ADR-0005](adr/0005-tts-provider.md) | TTS: Google Translate Free Endpoint | **Superseded** by ADR-0016 | REQ-3 |
| [ADR-0006](adr/0006-internationalisation.md) | i18n: i18next + Column-per-Language (3 languages) | Accepted | REQ-1, F-LANG |
| [ADR-0007](adr/0007-audio-delivery.md) | Audio Delivery: Server-Side Cache with Token Auth | Accepted | REQ-3, F-AUDIO |
| [ADR-0008](adr/0008-testing-strategy.md) | Testing: Vitest + Testing Library | Partially superseded (backend → Pytest) | — |
| [ADR-0009](adr/0009-repo-structure.md) | Repo: Monorepo with Independent Projects | Accepted | — |
| [ADR-0010](adr/0010-backend-python-migration.md) | Backend Migration: FastAPI + SQLAlchemy 2.0 | Accepted | REQ-12, REQ-13 |
| [ADR-0011](adr/0011-story-data-model.md) | Story Data Model (future feature) | Proposed | REQ-14 |
| [ADR-0012](adr/0012-story-narration-tts.md) | Story Narration TTS (future feature) | Proposed | REQ-14 |
| [ADR-0013](adr/0013-story-word-lookup.md) | Story Word Lookup (future feature) | Accepted, extended by ADR-0027 | REQ-14 |
| [ADR-0016](adr/0016-tts-provider-edge-tts.md) | TTS: Microsoft Edge TTS with Per-Host Voices | Accepted | REQ-3, REQ-7, F-AUDIO |
| [ADR-0017](adr/0017-content-seeding.md) | Content Seeding: JSON Files + Idempotent Script | Accepted | REQ-2, REQ-10, REQ-11 |
| [ADR-0018](adr/0018-user-content-trust-model.md) | UGC: Community Trust Model with Input Validation | Accepted | REQ-9, F-UGC |
| [ADR-0019](adr/0019-gdpr-account-deletion.md) | GDPR: Cascade Delete + Contributed Word Preservation | Accepted | REQ-4, F-AUTH |
| [ADR-0020](adr/0020-host-persona-architecture.md) | Host Personas: In-Code Static Definition | Accepted | REQ-7, REQ-8, F-HOSTS |
| [ADR-0021](adr/0021-accessibility-testing.md) | Accessibility Testing: axe-core + Manual Audit | Accepted | F-A11Y |
| [ADR-0022](adr/0022-search-implementation.md) | Search: In-Memory Normalize-and-Rank | Accepted | REQ-5, F-SEARCH |
| [ADR-0023](adr/0023-host-image-pipeline.md) | Host Images: AI-Generated Static Assets | Accepted | REQ-7, F-HOSTS |
| [ADR-0024](adr/0024-seeded-audio-generation-strategy.md) | Audio: Hybrid Pre-Generate + Lazy Fallback | Accepted | REQ-3, F-AUDIO |
| [ADR-0025](adr/0025-on-the-fly-translation-provider.md) | Translation: deep-translator with Google Free | Proposed | REQ-18, F-OTFLOOKUP |
| [ADR-0026](adr/0026-on-the-fly-translation-caching.md) | Caching: TranslationCache Table + Existing Audio Cache | Proposed | REQ-18, F-OTFLOOKUP |
| [ADR-0027](adr/0027-story-lookup-cascade-and-otf-audio.md) | Lookup Cascade & Text-Based Audio Endpoint | Proposed | REQ-18, REQ-14, F-OTFLOOKUP |

### Quality Assurance

| Document | Purpose |
|---|---|
| [User Review Panel](user-review-panel.md) | Six representative personas used to evaluate every major change before release |
| [Review Feedback](reviews/) | Per-session feedback files logged by the review panel (one file per major change) |

### Post-Launch Backlog

Items identified during technical review that do not block launch but should be addressed in a follow-up sprint.

| ID | Item | Severity | Related |
|---|---|---|---|
| PB-1 | "My Contributions" listing — endpoint and UI for users to browse their own contributed words | Minor | F-UGC, REQ-9 |
| PB-2 | `displayName` optional at registration — profile may display as blank; consider requiring or defaulting | Minor | REQ-4 |
| PB-3 | Login / Register error messages lack `role="alert"` — screen readers may not announce auth failures promptly | Minor | F-A11Y, REQ-4 |
| PB-4 | Search input lacks `aria-label` — screen readers may not identify the search field | Minor | F-A11Y, F-SEARCH, REQ-5 |
| PB-5 | Responsive breakpoints not verified with real browser — recommend Playwright visual regression check | Minor | F-RESPONSIVE |
| PB-6 | axe-core automated accessibility sweep not performed — recommended before or shortly after launch | Minor | F-A11Y |
