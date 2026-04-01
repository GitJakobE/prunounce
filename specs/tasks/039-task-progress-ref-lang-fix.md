# Task 039: Fix Progress Endpoint Reference Language

**Feature:** F-PROGRESS (Progress Tracking), F-LANG (Multi-Language Support)
**Priority:** P0 (Bug fix — review finding CUT-1)
**Dependencies:** 027 (Per-Language Progress Tracking)
**Review reference:** [2026-03-29 review](../reviews/2026-03-29-current-state.md) — CUT-1

## Problem

The `GET /api/progress` endpoint hardcodes the reference language used for category names instead of reading the authenticated user's stored language preference. This causes category names on the progress screen to appear in the wrong language for non-English users.

**Affected code:** `src/backend-python/app/routers/progress.py`, line 35:

```
ref_lang = "da" if target_lang == "en" else "en"
```

This means:

- An Italian-speaking user learning Danish (`target_lang = "da"`) sees category names in **English** instead of Italian.
- A Danish-speaking user learning Italian (`target_lang = "it"`) sees category names in **English** instead of Danish.
- Only English-speaking users learning Danish happen to see the correct language (Danish).

The dictionary categories endpoint (`/api/dictionary/categories`) already handles this correctly via `resolve_ref_lang()` which reads `user.language`. The progress endpoint does not follow the same pattern.

## Expected Behaviour

Category names returned by `GET /api/progress` must be in the user's stored reference language (`user.language`), consistent with how `/api/dictionary/categories` works.

## Acceptance Criteria

- [ ] `GET /api/progress` returns category names in the user's reference language
- [ ] An Italian-speaking user learning Danish sees Italian category names in progress
- [ ] A Danish-speaking user learning Italian sees Danish category names in progress
- [ ] An English-speaking user learning Italian sees English category names in progress
- [ ] The fix uses the same `user.language` lookup pattern as the dictionary router
- [ ] Existing progress endpoint tests are updated or extended to verify reference language
- [ ] No regression in progress counts (totalWords, listenedWords)

## Testing Requirements

- Unit test: user with `language = "it"` learning Danish gets Italian category names in progress response
- Unit test: user with `language = "da"` learning Italian gets Danish category names in progress response  
- Unit test: user with `language = "en"` learning Italian gets English category names in progress response
- Verify that progress totals and listened counts are unaffected by the fix
