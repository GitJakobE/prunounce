# Task 016: End-to-End Integration Testing

**Feature:** Cross-cutting (quality assurance)
**Priority:** P1
**Dependencies:** All feature tasks (008–012)
**ADRs:** ADR-0008 (Testing Strategy)

## Description

Verify that all features work together end-to-end by running the full backend test suite, the full frontend test suite, and performing structured manual testing of key user flows. Ensure test coverage meets the target threshold and all tests pass.

## Technical Requirements

### Backend Test Suite

- Run `npm test` in `src/backend/`
- All existing tests must pass (health, auth, dictionary, profile, search)
- Test coverage target: ≥ 85% for route handlers and middleware
- Tests should cover the new fields added during host persona and example sentence features (hostId, exampleIt, exampleEn, exampleDa)

### Frontend Test Suite

- Run `npm test` in `src/frontend/`
- All existing tests must pass (WordCard, LanguageSwitcher, LoginPage, CategoriesPage)
- Mock data must include all current fields (hostId in User, example/exampleIt in WordEntry)

### Manual Integration Test Plan

Execute the following user flows and verify correct behaviour:

1. **Registration flow**: Register new account → select language → redirected to categories
2. **Login flow**: Log out → log in with credentials → return to categories
3. **Host selection**: Select each of the four hosts → verify banner updates → reload page → verify persistence
4. **Category browsing**: Click a category → see word list → filter by difficulty → verify progress indicators
5. **Audio playback**: Click play on a word → hear pronunciation → hear example sentence → verify listened checkmark appears
6. **Search**: Navigate to search → search by Italian word → search by English word → verify results
7. **Profile management**: Update display name → change language → verify all text updates
8. **Account deletion**: Delete account → verify redirect to login → verify cannot login with old credentials

### Build Verification

- `npm run build` succeeds in both frontend and backend
- No TypeScript errors in either project
- Frontend production build size is reasonable (< 500 KB JS)

## Acceptance Criteria

- [ ] All backend tests pass (35+ tests)
- [ ] All frontend tests pass (13+ tests)
- [ ] Both projects build without TypeScript errors
- [ ] All 8 manual integration test flows pass
- [ ] Frontend production build is under 500 KB JS
- [ ] No console errors during normal usage

## Testing Requirements

- This is itself a testing task — the acceptance criteria define the tests
- Document any bugs found during integration testing and file them for resolution
