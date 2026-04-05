import logging
import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .config import PUBLIC_DIR, settings
from .database import Base, engine, ensure_sqlite_schema
from .routers import audio, auth, dictionary, health, hosts, profile, progress, reports, search, stories

logger = logging.getLogger("pronuncia")


app = FastAPI(title="Pronuncia Italiana API (Python)")


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"error": str(exc.detail)})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = [{"msg": e.get("msg", "Invalid input"), "path": e.get("loc", [""])[-1]} for e in exc.errors()]
    return JSONResponse(status_code=400, content={"errors": errors})


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_sqlite_schema()
    _check_db_writable()
    _check_audio_cache_writable()


def _check_db_writable() -> None:
    """Warn at startup if the SQLite database is not writable."""
    if not settings.database_url.startswith("sqlite"):
        return
    # sqlite:/// or sqlite:////absolute
    db_path = settings.database_url.replace("sqlite:///", "", 1)
    if not db_path:
        return
    db_file = Path(db_path)
    if db_file.exists() and not os.access(db_file, os.W_OK):
        logger.error(
            "DATABASE NOT WRITABLE: %s — user registration and progress tracking will fail. "
            "Fix with: sudo chown www-data:www-data %s",
            db_file,
            db_file,
        )
    db_dir = db_file.parent
    if db_dir.exists() and not os.access(db_dir, os.W_OK):
        logger.error(
            "DATABASE DIRECTORY NOT WRITABLE: %s — SQLite journal creation will fail. "
            "Fix with: sudo chown www-data:www-data %s",
            db_dir,
            db_dir,
        )


def _check_audio_cache_writable() -> None:
    """Warn at startup if the audio cache directory is not writable."""
    cache_dir = Path(settings.audio_cache_dir)
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        logger.error(
            "AUDIO CACHE DIRECTORY CANNOT BE CREATED: %s — %s. "
            "Category word audio will not work.",
            cache_dir.resolve(),
            exc,
        )
        return
    # Verify we can actually write a file
    try:
        with tempfile.NamedTemporaryFile(dir=cache_dir, delete=True):
            pass
    except OSError as exc:
        logger.error(
            "AUDIO CACHE DIRECTORY NOT WRITABLE: %s — %s. "
            "Category word audio will not work. "
            "Fix with: sudo chown www-data:www-data %s",
            cache_dir.resolve(),
            exc,
            cache_dir.resolve(),
        )


hosts_dir = PUBLIC_DIR / "hosts"
if hosts_dir.exists() and hosts_dir.is_dir():
    app.mount("/hosts", StaticFiles(directory=str(hosts_dir)), name="hosts")

# API routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(dictionary.router)
app.include_router(search.router)
app.include_router(audio.router)
app.include_router(hosts.router)
app.include_router(progress.router)
app.include_router(stories.router)
app.include_router(reports.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "backend-python"}
