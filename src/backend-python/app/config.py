from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR.parent
REPO_ROOT = SRC_DIR.parent
DEFAULT_SQLITE_PATH = BASE_DIR / "app.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    port: int = 3001
    jwt_secret: str = "change-me"
    jwt_expires_in_days: int = 30
    audio_cache_dir: str = "./audio-cache"
    frontend_url: str = "http://localhost:5173"
    database_url: str = f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}"


settings = Settings()
LEGACY_BACKEND_DIR = SRC_DIR / "backend"
PUBLIC_DIR = LEGACY_BACKEND_DIR / "public"
