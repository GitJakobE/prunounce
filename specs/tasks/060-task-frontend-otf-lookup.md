# Task 060: Frontend On-the-Fly Lookup & Audio

**Feature:** F-OTFLOOKUP (On-the-Fly Word Lookup & Audio)
**Priority:** P1
**Dependencies:** 058 (Lookup Cascade Endpoint), 059 (Pronounce Audio Endpoint)

## Description

Update the frontend to consume the extended lookup cascade (the `source` field on `WordLookupResult`) and the new `/api/audio/pronounce` endpoint. The translation panel must show an "auto-translated" indicator for non-curated translations, and the play button must work for any word regardless of whether it has a `wordId`.

## Technical Requirements

### TypeScript Type Update

- Add `source` field to `WordLookupResult` in `src/frontend/src/types/index.ts`:
  ```ts
  export interface WordLookupResult {
    word: string;
    translation: string | null;
    phoneticHint: string | null;
    wordId: string | null;
    source: "curated" | "cached" | "auto-translated" | "none";
  }
  ```

### New API Helper

- Add `pronounceAudioUrl(word: string, lang: string): string` to `src/frontend/src/services/api.ts`:
  ```ts
  export function pronounceAudioUrl(word: string, lang: string): string {
    const token = getToken();
    return `${API_BASE}/audio/pronounce?word=${encodeURIComponent(word)}&lang=${encodeURIComponent(lang)}&token=${token}`;
  }
  ```

### TranslationPanel Changes (`StoryReadingPage.tsx`)

1. **Auto-translated indicator:** When `selected.source` is `"cached"` or `"auto-translated"`, display a small label below the translation text (e.g., "Auto-translated" in muted/italic style). Use existing i18n key pattern: `stories.autoTranslated`.

2. **Play button for all words with translations:**
   - Currently the play button only renders when `selected.wordId` is truthy
   - Change the condition: render the play button when `selected.translation` is truthy (any word with a translation can be pronounced)
   - Audio source logic:
     - If `selected.wordId` exists (curated word) → use existing `audioUrl(selected.wordId)`
     - If `selected.wordId` is null (auto-translated word) → use `pronounceAudioUrl(selected.word, storyLanguage)` where `storyLanguage` is the story's target language
   - The `playWordAudio` callback in the parent must be updated to accept the appropriate URL

3. **Pass story language to TranslationPanel** so it can construct the pronounce URL for non-curated words.

### i18n

- Add `stories.autoTranslated` key to all locale files (e.g., `"Auto-translated"` / `"Auto-tradotto"` / `"Auto-oversat"`)

### No Session Cache Changes

- The existing `lookupWord()` call and any in-component word lookup caching remain unchanged — the backend now handles caching via `TranslationCache`

## Acceptance Criteria

- [ ] `WordLookupResult` TypeScript interface includes `source` field
- [ ] `pronounceAudioUrl()` helper exists and constructs correct URL
- [ ] Curated words show no extra indicator; play button uses `audioUrl(wordId)` as before
- [ ] Auto-translated words show "Auto-translated" label below the translation
- [ ] Auto-translated words have a working play button using `/api/audio/pronounce`
- [ ] Words with `source="none"` (failed translation) still show "Translation unavailable" with no play button
- [ ] i18n keys added for all supported locales
- [ ] No regressions in curated word lookup flow

## Testing Requirements

- Curated word renders without auto-translated label and play button uses `audioUrl`
- Auto-translated word renders with label and play button uses `pronounceAudioUrl`
- Word with `source="none"` shows "Translation unavailable" and no play button
- Play button disabled state works for both curated and auto-translated audio
- `pronounceAudioUrl` correctly encodes word and lang parameters
