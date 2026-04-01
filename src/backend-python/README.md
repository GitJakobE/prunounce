# Backend Python (Migration In Progress)

This service is the Python migration target for the existing backend.

## Stack

- FastAPI
- SQLAlchemy
- Alembic (to be wired next)
- JWT auth + bcrypt password hashing

## Current Status

Implemented:
- `GET /api/health`
- `GET /api/hosts`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/profile`
- `PATCH /api/profile`
- `DELETE /api/profile`
- `GET /api/dictionary/categories`
- `GET /api/dictionary/categories/:id/words`
- `POST /api/dictionary/words/:id/listened`
- `POST /api/dictionary/words`
- `GET /api/search`
- `GET /api/audio/:wordId`
- `GET /api/audio/:wordId/example`
- Base schema models and DB bootstrap
- Error-shape compatibility handler (`error`/`errors` payloads)

Pending migration:
- Auth Google flow
- TTS provider integration
- Alembic migration scripts
- Full parity test suite

## Run

```bash
py -m poetry install
py -m poetry run backend-python
```

## Test

```bash
py -m poetry run pytest
```

## Poetry Environment

To keep the virtual environment inside this project folder:

```bash
py -m poetry config virtualenvs.in-project true
```

If you add Poetry to PATH, you can use `poetry` instead of `py -m poetry`.
