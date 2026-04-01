# ADR-0010: Backend Migration — FastAPI + SQLAlchemy (Python)

- **Status:** Accepted
- **Date:** 2026-03-29
- **Deciders:** Development team
- **Supersedes:** [ADR-0002 (Express 5 + TypeScript)](0002-backend-framework.md)
- **Requirements:** REQ-4 (Authentication), REQ-9 (User-contributed words), REQ-11 (Content seeding), REQ-12 (Data persistence), REQ-13 (API surface)

## Context and Problem Statement

The original backend was built with Express 5 + TypeScript + Prisma ORM (ADR-0002). During development, several friction points emerged: Prisma's SQLite driver limitations for multi-language schema evolution, the overhead of maintaining TypeScript type definitions alongside Prisma-generated types, and the desire for a more concise framework with built-in request validation and OpenAPI documentation. The team needed to decide whether to continue investing in the Express backend or migrate to a Python-based stack.

## Decision Drivers

- Developer productivity: faster iteration on API routes and schema changes
- Built-in request validation and automatic OpenAPI/Swagger documentation
- Simpler ORM migration story (Alembic vs Prisma migrate for SQLite)
- Existing team familiarity with Python
- Compatibility with the Edge TTS Python library (`edge-tts`) which has richer async support than the Node equivalent (`msedge-tts`)
- Retain JWT-based stateless authentication (ADR-0004 unchanged)
- Retain SQLite as the database (ADR-0003 unchanged)

## Considered Options

### Option 1: Continue with Express 5 + TypeScript + Prisma (Original)

Stay on the existing stack and work through the friction points. Prisma's ecosystem is maturing and most issues have workarounds.

### Option 2: FastAPI + SQLAlchemy + Pydantic (Chosen)

Migrate to Python with FastAPI for the web framework, SQLAlchemy 2.0 for ORM with mapped columns, Pydantic for request/response validation, and Alembic for schema migrations.

### Option 3: Django REST Framework

Full-featured Python web framework with built-in admin, ORM, and auth. However, Django's opinionated structure adds overhead for an API-only backend, and the admin UI is out of scope for v1.

### Option 4: Hono (TypeScript)

Lightweight TypeScript framework with Web Standards API. Would keep the TypeScript ecosystem but doesn't solve the Prisma friction or provide the same level of built-in validation as FastAPI.

## Decision Outcome

**Chosen: Option 2 — FastAPI + SQLAlchemy + Pydantic**

The Python backend lives in `src/backend-python/` and replaces `src/backend/` as the active runtime. The Node.js backend in `src/backend/` is retained as a reference but is no longer the development target.

### Technology Choices

| Concern | Technology | Rationale |
|---|---|---|
| Web framework | FastAPI 0.116 | Async-first, automatic OpenAPI docs, dependency injection |
| ORM | SQLAlchemy 2.0 | Mapped columns with type hints, mature migration tooling |
| Migrations | Alembic 1.16 | Complements SQLAlchemy; reliable SQLite migration support |
| Validation | Pydantic v2 (via `pydantic-settings`) | Integrated with FastAPI; schema-first request/response models |
| Auth | `python-jose` + `passlib[bcrypt]` | JWT encode/decode and bcrypt password hashing |
| TTS | `edge-tts` + `gTTS` | Native async TTS generation; gTTS as fallback |
| Package manager | Poetry | Lock file, virtual environment isolation, script entry points |
| Testing | Pytest + HTTPX | HTTPX provides async test client for FastAPI; Pytest for fixtures |

### API Compatibility

The Python backend exposes the same REST API surface as the Express backend to maintain frontend compatibility:

- `POST /api/auth/register`, `POST /api/auth/login`
- `GET /api/dictionary/categories`, `GET /api/dictionary/categories/:id/words`
- `GET /api/search?q=...`
- `GET /api/audio/:wordId`, `GET /api/audio/:wordId/example`
- `GET /api/hosts`, `GET /api/profile`, `PUT /api/profile`
- `GET /api/progress`, `POST /api/progress/:wordId`
- `GET /api/health`

### Consequences

**Positive:**
- FastAPI auto-generates OpenAPI/Swagger docs at `/docs` — reduces API documentation burden
- Pydantic models provide runtime request validation with clear error messages
- SQLAlchemy 2.0 mapped columns give type-safe models without a separate code generation step
- `edge-tts` library has native async support, cleaner integration with FastAPI's async handlers
- Poetry lock file ensures reproducible builds

**Negative:**
- Two backend directories exist in the monorepo during migration (`src/backend/` and `src/backend-python/`)
- Team must maintain Python and Node.js toolchains until the Express backend is fully retired
- SQLAlchemy column mappings use `mapped_column("camelCase", ...)` to match the existing Prisma-created database schema — adds verbosity

**Neutral:**
- The frontend requires no changes — API contract is preserved
- ADR-0003 (SQLite) and ADR-0004 (JWT authentication) remain valid and applicable
- ADR-0008 (Testing) is partially superseded: Pytest replaces Vitest for backend tests, but Vitest remains for frontend
