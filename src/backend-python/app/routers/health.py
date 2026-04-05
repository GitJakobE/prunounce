import os
import tempfile
from pathlib import Path

from fastapi import APIRouter

from ..config import settings

router = APIRouter(prefix="/api")


def _check_db_writable() -> bool:
    """Return True if the SQLite database file and its directory are writable."""
    if not settings.database_url.startswith("sqlite"):
        return True
    db_path = settings.database_url.replace("sqlite:///", "", 1)
    if not db_path:
        return True
    db_file = Path(db_path)
    if db_file.exists() and not os.access(db_file, os.W_OK):
        return False
    db_dir = db_file.parent
    if db_dir.exists() and not os.access(db_dir, os.W_OK):
        return False
    return True


def _check_audio_cache_writable() -> bool:
    """Return True if the audio cache directory exists and is writable."""
    cache_dir = Path(settings.audio_cache_dir)
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=cache_dir, delete=True):
            pass
        return True
    except OSError:
        return False


@router.get("/health")
def health() -> dict:
    db_ok = _check_db_writable()
    audio_ok = _check_audio_cache_writable()
    checks = {
        "database_writable": db_ok,
        "audio_cache_writable": audio_ok,
    }
    status_value = "ok" if all(checks.values()) else "degraded"
    return {"status": status_value, **checks}
