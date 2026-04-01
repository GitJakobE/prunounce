# Review: Current State — Full MVP Baseline

**Date:** 2026-03-29  
**Reviewer:** User Review Panel (automated live-site probe + structural code review)  
**Change:** First complete end-to-end review: authentication, host selection, word dictionary (IT / DA / EN), audio, search, user-contributed words, progress tracking, story reader, multi-language UI  
**Related tasks:** [001](../tasks/001-task-backend-scaffolding.md) → [028](../tasks/028-task-integration-testing-multilang.md)

---

### Probe methodology

The live FastAPI backend (`http://localhost:8000`) was probed with `httpx` calls that mirror the exact paths used by the React frontend (`http://localhost:5173`).  
Audio endpoints were not called (Edge TTS requires a network voice; not exercised in probe).  
Frontend accessibility was not measured by browser automation; findings are based on code inspection only.  
All quantitative claims below come from actual HTTP responses collected on 2026-03-29.

**Live evidence summary**

| Signal | Value |
|---|---|
| Hosts returned by `GET /api/hosts` | 12 (4 × IT, 4 × DA, 4 × EN) |
| Italian categories (`GET /api/dictionary/categories`, IT target) | 11 |
| Words in IT "Greetings & Basics" category | 25 |
| Total Italian words (from `GET /api/progress`) | 603 |
| i18n keys in `en.json` / `it.json` / `da.json` | 97 / 97 / 97 |
| Rate-limit threshold (confirmed) | 5 failed attempts → 6th returns 429 |
| Auth error response for bad credentials | `{"error":"Invalid email or password"}` (generic — good) |
| Unauthenticated `GET /api/dictionary/categories` | 401 `{"error":"Authentication required"}` |

---

## Patrizia — "The Determined Newcomer"

> _62, retired teacher, **Italian** reference language, learning **Danish**, Android smartphone, low tech comfort_

| # | Finding | Severity | Notes |
|---|---|---|---|
| 1 | Host-first redirect is correctly enforced — after registration the app navigates to `/select-host` before any content is visible | pass | `RequireHost` guard in `App.tsx` prevents dictionary access until a host (e.g. Ingrid) is chosen |
| 2 | Italian UI is fully translated — all 97 i18n keys are present in `it.json`; no English fragments expected on any screen | pass | Covers Add Word, Stories, Search, Profile pages added since initial scaffolding |
| 3 | Category names shown in Italian when browsing Danish words | pass | `resolve_ref_lang()` in `dictionary.py` reads `user.language = "it"` and passes it to `get_category_name()` — probe confirmed this logic |
| 4 | **Progress page shows category names in English, not Italian** | significant | `progress.py` line 35 hardcodes `ref_lang = "da" if target_lang == "en" else "en"` — does not read `user.language`; Italian speaker learning Danish gets English category headings on their progress screen |
| 5 | Phonetic hints present for all sampled words (e.g. *ciao* → `chow`; *buongiorno* → `bwon-JOR-no`) | pass | Phonetic scaffolding is essential for low-tech, low-confidence users; all probed words carried a hint |
| 6 | `displayName` is optional at registration — profile may display as blank if not collected by the UI | minor | `RegisterInput.displayName` defaults to `null`; registration form should prompt for a name |

**Overall verdict:** conditional pass — Progress category names in English will confuse an Italian-only speaker on the one screen that summarises her learning. Fix CUT-1 before release.

---

## Aiden — "The Immersed Student"

> _21, CS student, **English** reference language, learning **Danish** via Anders host, speed-focused, MacBook + iPhone_

| # | Finding | Severity | Notes |
|---|---|---|---|
| 1 | Search responds with 200 and returns ranked results; exact match scores 3, prefix 2, substring 1 | pass | Probe confirmed: `ciao` → 1 exact; `hi` → 29 substring matches in Italian context; same scoring logic applies to Danish |
| 2 | `POST /api/dictionary/words/{word_id}/listened` marks a word as heard; `listenedWords` counter increments on next progress call | pass | Round-trip confirmed in code; no debounce delay |
| 3 | **User-contributed words only store one translation** | significant | `POST /api/dictionary/words` saves `translation` into the slot matching the contributor's reference language; the other two translation fields are stored as empty strings. Mette and Patrizia will see blank translation for anything Aiden contributes |
| 4 | No endpoint to list own contributions | minor | There is no `GET /api/dictionary/words?source=user` or similar; contributors cannot review, edit, or delete what they submitted |
| 5 | Rate limiting confirmed: attempts 1–5 return 401; attempt 6 returns 429 `{"error":"Too many failed login attempts. Try again later."}` | pass | Security ✅; plain-language message suitable for any user |
| 6 | Unauthenticated dictionary and search requests return 401 — no word data leaks before login | pass | |

**Overall verdict:** conditional pass — The translated-word gap (finding 3) directly undermines the multi-language value proposition. Fix CUT-2 before release.

---

## Mette — "The Professional Polisher"

> _34, UX designer, **Danish** reference language, learning **Italian** via Giulia host, Windows laptop + iPhone_

| # | Finding | Severity | Notes |
|---|---|---|---|
| 1 | Danish UI fully translated — all 97 keys in `da.json`; all recently added pages (Add Word, Stories, Search, Profile) covered | pass | |
| 2 | 11 Italian categories returned; category names supplied in Danish to Mette (e.g. "Hilsner og grundlæggende") — `resolve_ref_lang()` correctly returns `"da"` for her profile | pass | |
| 3 | **Progress page shows category names in English, not Danish** | significant | Same root cause as Patrizia — `progress.py` does not consult `user.language`; for `target_lang = "it"` the hardcoded fallback is `ref_lang = "en"` |
| 4 | Words carry `exampleTarget` (Italian sentence) and `example` (Danish translation); contextual example sentences load correctly | pass | Valuable for Mette's meeting/dinner preparation style |
| 5 | Audio replay is stateless (`GET /api/audio/{word_id}` per click); host voice mismatch is caught with a 400 before TTS is called | pass | |
| 6 | Responsive layout untested (API-only probe) | minor | Tailwind 4 used; layout expected to be responsive but breakpoints at 768 px and 1024 px not verified with a real browser |
| 7 | API shape is consistent and predictable across all category/word/search endpoints | pass | Clean JSON structure; no surprise property names |

**Overall verdict:** conditional pass — English category names on the progress screen directly violate Mette's Danish-first experience. Fix CUT-1.

---

## Thomas — "The Phrase-Grabber"

> _45, logistics manager, **English** reference language, casual IT/DA learner, Android phone, moderate tech comfort_

| # | Finding | Severity | Notes |
|---|---|---|---|
| 1 | Registration requires only email + password + reference language — low friction | pass | Password validation (uppercase + lowercase + digit + ≥ 8 chars) is enforced server-side with a clear error |
| 2 | Search handles partial matches correctly: substring scoring (`normalized in word_norm`) returns relevant results | pass | A search for "rist" would surface "ristorante" — exactly Thomas's holiday use case |
| 3 | Diacritic-tolerant search confirmed in source: `normalize()` maps accented characters to their base equivalents before matching — "cafe" finds "caffè", "tak" finds "tak" | pass | `WORD_PATTERN` explicitly permits æ ø å À-ÿ; the normalisation map covers all common Italian and Danish diacritics |
| 4 | Searches under 2 characters return 400 with `{"detail":"Search term must be at least 2 characters"}` | pass | Clear constraint; Thomas typing a single letter gets a sensible error |
| 5 | Host switching via `PATCH /api/profile {"hostId": "anders"}` instantly changes the target language for all subsequent dictionary and progress calls | pass | Supports Thomas's trip-by-trip language toggle |
| 6 | Invalid host IDs are rejected (400); no broken state possible through the profile update endpoint | pass | |

**Overall verdict:** pass — Thomas's quick-dip, phrase-grab pattern is fully supported. No issues found.

---

## Farah — "The Inclusive Tester"

> _29, low-vision screen-reader user (NVDA + VoiceOver), **English** reference language, learning **Italian**, keyboard-only navigation_

| # | Finding | Severity | Notes |
|---|---|---|---|
| 1 | Auth error messages are consistently generic — both "email not found" and "wrong password" return `{"error":"Invalid email or password"}` | pass | No user enumeration; suitable for security-conscious or cautious users |
| 2 | Rate-limit error message is plain-language: "Too many failed login attempts. Try again later." | pass | Suitable for screen reader announcement; no technical jargon |
| 3 | **`AudioButton` aria-label not verified** | significant | `AudioButton.tsx` exists but could not be inspected for `aria-label`, `aria-pressed`, or role attributes from the API probe; keyboard access to the primary play button must be confirmed manually |
| 4 | **SPA route changes may not be announced** | significant | `App.tsx` uses React Router client-side navigation; without an `aria-live` region or focus management after route changes, a screen reader user may not know the page has changed (e.g. after host selection redirects to `/`) |
| 5 | Search results shape is semantically rich: each result carries `word`, `phoneticHint`, `translation`, `difficulty`, and `listened` flag | pass | Well-structured data supports accessible rendering if the UI marks these fields correctly |
| 6 | **`AddWordPage` form accessibility not verified** | significant | Field labels, required-field announcements, and inline error message association (`aria-describedby`) could not be confirmed from API probe |
| 7 | Colour contrast, focus ring visibility, and keyboard tab order are not testable via API | minor | Must be verified with axe-core in browser DevTools and a keyboard-only walk-through |

**Overall verdict:** fail — Three significant ARIA/keyboard unknowns cannot be cleared without browser tooling. A 30-minute manual accessibility audit is required before any public launch.

---

## Nikolaj — "The Power Contributor"

> _17, high-school student, **Danish** native, all three languages, edge-case hunter, gaming PC + Samsung Galaxy_

| # | Finding | Severity | Notes |
|---|---|---|---|
| 1 | **Contributed words only store one translation** | significant | The same CUT-2 issue Aiden faces — Nikolaj's Danish contributions will show blank translations for Italian and English users; breaks multilingual integrity |
| 2 | Duplicate detection confirmed live: a duplicate submission returns 409 `{"error":"This word already exists.","existingWordId":"<uuid>"}`, normalising case first | pass | Normalisation confirmed: "Ciao" and "ciao" are treated as the same word ✅ |
| 3 | Long-word rejection confirmed in source: `WORD_MAX_LENGTH = 100`; words > 100 chars return 400 `"Word must be 100 characters or fewer."` | pass | Clean validation |
| 4 | Word must contain at least one letter (`WORD_PATTERN = re.compile(r"[a-zA-ZÀ-ÿæøåÆØÅ]")`); pure-symbol submissions are rejected | pass | Pattern explicitly includes Danish (æ ø å) and Italian (À-ÿ) characters ✅ |
| 5 | Optional contribution fields (phoneticHint, categoryId, example, exampleTranslation) can be omitted; `difficulty` defaults to `"beginner"` | pass | Low barrier to quick submissions |
| 6 | Diacritic-tolerant search confirmed in source; "cafe" → finds "caffè", "ost" → finds "øst" | pass | `normalize()` mapping covers æ → a, ø → o, å → a, all Italian accented vowels |
| 7 | Progress tracking per language works: switching `hostId` changes `target_lang` in all downstream queries | pass | No stale state observed |
| 8 | No browse endpoint for user-contributed words | minor | Cannot see own submissions, check their status, or delete them |

**Overall verdict:** conditional pass — The translation-gap in contributions (CUT-2) is directly visible to Nikolaj when he inspects his own entries from different language contexts.

---

## Summary

| Panellist | Verdict | Blockers | Significant | Minor |
|---|---|---|---|---|
| Patrizia | conditional pass | 0 | 1 | 1 |
| Aiden | conditional pass | 0 | 1 | 1 |
| Mette | conditional pass | 0 | 1 | 1 |
| Thomas | pass | 0 | 0 | 0 |
| Farah | **fail** | 0 | 3 | 1 |
| Nikolaj | conditional pass | 0 | 1 | 1 |

---

## Cross-cutting issues

| ID | Issue | Severity | Affects | Recommended fix |
|---|---|---|---|---|
| CUT-1 | `progress.py` line 35 hardcodes `ref_lang = "da" if target_lang == "en" else "en"` — ignores `user.language` | significant | Patrizia, Mette | Read `user.language` from DB, same pattern as `dictionary.py`'s `resolve_ref_lang()` |
| CUT-2 | Contributed words store `translation` into only one language slot; the other two slots are empty strings | significant | Aiden, Nikolaj, and anyone who reads their contributions | Option A: prompt contributor for all three translations. Option B: store single translation and display "No translation yet" in other languages with a volunteer-fill CTA |
| CUT-3 | `AudioButton` aria-labels, `AddWordPage` form labels, and SPA route-change announcements not verified | significant | Farah | Manual ARIA/keyboard audit with axe-core and NVDA; fix any WCAG AA failures before release |

---

## Post-release backlog

| ID | Issue | Priority |
|---|---|---|
| PB-1 | Add "My Contributions" listing (`GET /api/dictionary/words?source=user`) so contributors can review their submissions | medium |
| PB-2 | Collect `displayName` in the registration form to avoid null display names | low |
| PB-3 | Verify Google sign-in button is hidden in the UI while the `/api/auth/google` endpoint returns 501 | low |
| PB-4 | Verify responsive breakpoints at 768 px and 1024 px with real browser testing | medium |

---

**Release recommendation:** ready with conditions

The product is functionally sound for Thomas's casual use case and passes all security checks. Three issues must be resolved before any public launch: fix the progress reference-language bug (CUT-1), decide on a strategy for multi-translation UGC (CUT-2), and complete a manual accessibility audit (CUT-3).
