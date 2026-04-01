from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    pass


connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def ensure_sqlite_schema() -> None:
    """Apply lightweight SQLite schema upgrades for local/dev databases."""
    if not settings.database_url.startswith("sqlite"):
        return

    with engine.begin() as connection:
        inspector = inspect(connection)
        if "Story" not in inspector.get_table_names():
            return

        story_columns = {column["name"] for column in inspector.get_columns("Story")}
        if "length" not in story_columns:
            connection.execute(
                text('ALTER TABLE "Story" ADD COLUMN length VARCHAR NOT NULL DEFAULT "short"')
            )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
