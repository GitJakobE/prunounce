# ADR-0008: Testing Strategy — Vitest with Supertest and Testing Library

- **Status:** Partially superseded (backend: Pytest + HTTPX per [ADR-0010](0010-backend-python-migration.md); frontend Vitest remains)
- **Date:** 2026-03-16
- **Deciders:** Development team
- **Requirements:** All (cross-cutting quality concern)

## Context and Problem Statement

The application needs automated testing to verify correctness of the API routes, React components, and user interactions. The testing framework must integrate with the TypeScript + Vite toolchain used by both frontend and backend, support fast execution for developer feedback, and enable both unit and integration testing patterns.

## Decision Drivers

- Consistent test runner across frontend and backend
- Native TypeScript and ESM support without additional transpilation config
- Fast execution (sub-10-second full suite)
- Integration with Vite's module resolution and transforms
- Component testing with DOM assertions for React
- HTTP-level integration testing for Express routes
- Jest-compatible API to leverage existing knowledge

## Considered Options

### Option 1: Vitest + supertest + @testing-library/react (Chosen)

Vitest is a Vite-native test runner with a Jest-compatible API. It reuses Vite's transform pipeline, providing instant TypeScript support. Paired with supertest for backend HTTP testing and @testing-library/react for frontend component testing, it covers all testing needs with a single runner.

### Option 2: Jest

The most widely used JavaScript test runner. However, Jest requires additional configuration for TypeScript (ts-jest or SWC transform) and ESM support. With Vite already in the toolchain, Vitest leverages the same configuration without duplication.

### Option 3: Playwright / Cypress (E2E only)

Browser-based end-to-end testing tools. Ideal for testing the full user journey. However, they're complementary to (not a replacement for) unit and integration tests, and add significant execution time. E2E tests can be added later without changing the unit/integration setup.

## Decision Outcome

**Chosen: Option 1 — Vitest + supertest + @testing-library/react**

### Test Architecture

**Backend (35 tests across 5 files):**

| Test file | Scope | Pattern |
|---|---|---|
| `health.test.ts` | Health check endpoint | supertest GET |
| `auth.test.ts` | Registration, login, token validation | supertest POST + GET with auth |
| `dictionary.test.ts` | Categories, words, filtering | supertest GET with auth |
| `profile.test.ts` | Profile CRUD, account deletion | supertest PATCH/DELETE with auth |
| `search.test.ts` | Word search by Italian and reference language | supertest GET with query params |

- Tests use `app.ts` (extracted from `index.ts`) to avoid starting the HTTP server
- A global setup script runs `prisma db push` to create a test database
- Each test file registers a user and authenticates to get a token

**Frontend (13 tests across 4 files):**

| Test file | Scope | Pattern |
|---|---|---|
| `WordCard.test.tsx` | Word display, difficulty badge, listened state | render + assertions |
| `LanguageSwitcher.test.tsx` | Language toggle behaviour | render + user event |
| `LoginPage.test.tsx` | Form rendering, submission, navigation | render + form interaction |
| `CategoriesPage.test.tsx` | Category loading, host components | render + async assertions |

- Tests use jsdom environment for DOM simulation
- API calls are mocked with `vi.mock()` to avoid backend dependency
- Auth context is mocked to provide test tokens and user objects

### Consequences

**Positive:**
- Single `vitest` command runs all tests in each project — no configuration divergence
- Sub-4-second frontend suite, sub-45-second backend suite (includes DB setup)
- Vitest reuses Vite's TypeScript transform — zero additional config for TS support
- @testing-library's "test as the user sees it" philosophy catches real rendering bugs
- supertest validates the full Express middleware chain (auth, validation, error handling)
- `vi.mock()` provides Jest-compatible module mocking with hoisting

**Negative:**
- No E2E tests yet — user flows across pages (register → browse → play) are untested end-to-end
- Backend tests hit a real SQLite database — slower than in-memory mocks but more realistic
- Frontend mocks must be updated when API response shapes change (e.g., adding `hostId`, `exampleIt`)

**Neutral:**
- Test files live alongside source in `src/test/` directories
- Global setup and test config are defined in `vitest.config.ts` per project
