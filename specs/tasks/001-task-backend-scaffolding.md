# Task 001: Backend Scaffolding

**Feature:** Infrastructure / Scaffolding
**Priority:** P0
**Dependencies:** None (first task)
**ADRs:** ADR-0010 (FastAPI + SQLAlchemy), ADR-0003 (SQLite), ADR-0009 (Repo structure)

> **Note:** The original task referenced Express 5 + Prisma (ADR-0002). The active backend is FastAPI + SQLAlchemy 2.0 (ADR-0010) in `src/backend-python/`. This task has been updated to reflect the current stack.

## Description

Set up the Python/FastAPI backend project structure. Initialize the FastAPI application with middleware (CORS, authentication), configure SQLAlchemy 2.0 with SQLite, create the database schema via SQLAlchemy models, and verify the project builds and runs using Poetry.

## Technical Requirements

- FastAPI application with Python 3.11+, managed via Poetry
- SQLAlchemy 2.0 ORM with SQLite provider (`sqlite:///./pronuncia.db`)
- Middleware: CORS (configurable allowed origins), authentication dependency injection
- Project entrypoint: `uvicorn app.main:app`; separate `app/main.py` from routers for testability
- Health check endpoint: `GET /api/health` → `{ "status": "ok" }`
- Environment configuration via pydantic-settings: `SECRET_KEY`, `DATABASE_URL`, `FRONTEND_URL`, `AUDIO_CACHE_DIR`
- Package manager: Poetry with `pyproject.toml`; dependencies include `fastapi`, `sqlalchemy`, `pydantic-settings`, `python-jose[cryptography]`, `passlib[bcrypt]`, `httpx`, `pytest`, `pytest-asyncio`, `edge-tts`
- `.gitignore` excluding: `__pycache__/`, `*.db`, `audio-cache/`, `.env`

### Database Schema

Models required (see ADR-0003 for data model):
- **User**: id, email, passwordHash, displayName, referenceLanguage (default "en"), hostId (default "marco"), timestamps
- **Category**: id, nameEn, nameDa, nameIt, order
- **Word**: id, word, language, phoneticHint, translationEn, translationDa, translationIt, difficulty, exampleIt, exampleEn, exampleDa, source ("seed"/"user"), contributedBy (FK User → SET NULL); UniqueConstraint on (word, language)
- **WordCategory**: composite key (wordId, categoryId) with cascade delete
- **UserProgress**: id, userId, wordId, listenedAt; UniqueConstraint on (userId, wordId); FK User ondelete CASCADE

## Acceptance Criteria

- [ ] `poetry install` completes without errors in `src/backend-python/`
- [ ] `alembic upgrade head` (or SQLAlchemy `Base.metadata.create_all`) creates the SQLite database and applies the schema
- [ ] `uvicorn app.main:app --reload` starts the FastAPI server on the configured port
- [ ] `GET /api/health` returns `{ "status": "ok" }` with status 200
- [ ] CORS middleware allows requests from the configured `FRONTEND_URL`
- [ ] All SQLAlchemy models are importable without error
- [ ] Pytest can be run without configuration errors

## Testing Requirements

- Health check endpoint returns 200 with correct JSON body (Pytest + HTTPX test client)
- Server starts without errors when environment variables are set
- SQLAlchemy models can be created and queried against an in-memory SQLite test database
