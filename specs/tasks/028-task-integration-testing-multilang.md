# Task 028: Integration Testing — Multi-Language & UGC

**Feature:** All features
**Priority:** P0
**Dependencies:** 017–027 (all prior tasks)

## Description

Comprehensive integration testing pass to verify the complete multi-language and user-contributed-words functionality works end-to-end. This includes cross-language host switching, dictionary scoping, audio generation in all languages, word contribution flow, and progress isolation.

## Technical Requirements

### Backend Integration Tests
- **Host switching:** Verify that changing a user's host via the profile API changes the words returned by the dictionary API
- **Multi-language dictionary:** Test that Italian, Danish, and English word sets are independent and correctly filtered
- **Reference language:** Test that `?lang=en|da|it` correctly switches translations and category names
- **Search across languages:** Test that search operates within the target language and doesn't leak results from other languages
- **User word contribution:** Test the full flow: POST a new word → verify it appears in GET dictionary listing → verify audio is generated → verify it appears in search
- **Duplicate detection:** Test that contributing a word that already exists returns 409
- **Progress isolation:** Test that progress recorded for Italian words doesn't appear when the user switches to a Danish host
- **Audio per language:** Test that audio requests for words in different languages use the correct host voice
- **GDPR deletion:** Verify that deleting a user account removes progress and de-attributes contributed words

### Frontend Tests
- **Host selection page:** Test that all 12 hosts render grouped by language
- **Host switcher:** Test that the top-right host indicator is present and navigates to selection
- **Word contribution form:** Test that the form validates, submits, and shows feedback
- **Language switch reactivity:** Test that switching reference language updates displayed translations
- **WordCard multi-language:** Test that WordCard displays `word` field correctly

### Build Verification
- Both backend and frontend compile with zero TypeScript errors
- Frontend production build succeeds
- All backend tests pass
- All frontend tests pass

## Acceptance Criteria

- [ ] All backend tests pass (aim for ≥ 85% coverage on new code)
- [ ] All frontend tests pass
- [ ] Backend compiles with `npx tsc --noEmit` without errors
- [ ] Frontend builds with `npx vite build` without errors
- [ ] No console errors or warnings related to missing translations
- [ ] Audio generation works for at least one word in each of the three target languages
- [ ] End-to-end: register → select host → browse words → play audio → add word → switch host → verify progress isolation

## Testing Requirements

This task IS the testing task. All tests from tasks 017–027 should be verified as passing.
