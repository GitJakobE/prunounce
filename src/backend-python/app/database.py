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
        if "setup_type" not in story_columns:
            connection.execute(
                text('ALTER TABLE "Story" ADD COLUMN setup_type VARCHAR')
            )
        if "setup_summary" not in story_columns:
            connection.execute(
                text('ALTER TABLE "Story" ADD COLUMN setup_summary VARCHAR')
            )

        if "userId" not in story_columns:
            connection.execute(
                text('ALTER TABLE "Story" ADD COLUMN "userId" VARCHAR REFERENCES "User"("id") ON DELETE CASCADE')
            )
        if "descriptionEs" not in story_columns:
            connection.execute(
                text('ALTER TABLE "Story" ADD COLUMN "descriptionEs" VARCHAR NOT NULL DEFAULT ""')
            )

        # Spanish columns for Word table
        if "Word" in inspector.get_table_names():
            word_columns = {col["name"] for col in inspector.get_columns("Word")}
            if "translationEs" not in word_columns:
                connection.execute(
                    text('ALTER TABLE "Word" ADD COLUMN "translationEs" VARCHAR NOT NULL DEFAULT ""')
                )
            if "exampleEs" not in word_columns:
                connection.execute(
                    text('ALTER TABLE "Word" ADD COLUMN "exampleEs" VARCHAR NOT NULL DEFAULT ""')
                )

        # Spanish column for Category table
        if "Category" in inspector.get_table_names():
            cat_columns = {col["name"] for col in inspector.get_columns("Category")}
            if "nameEs" not in cat_columns:
                connection.execute(
                    text('ALTER TABLE "Category" ADD COLUMN "nameEs" VARCHAR NOT NULL DEFAULT ""')
                )

        # ContentReport table
        if "ContentReport" not in inspector.get_table_names():
            connection.execute(
                text(
                    'CREATE TABLE "ContentReport" ('
                    '"id" VARCHAR NOT NULL PRIMARY KEY, '
                    '"userId" VARCHAR REFERENCES "User"("id") ON DELETE SET NULL, '
                    '"contentType" VARCHAR NOT NULL, '
                    '"contentId" VARCHAR NOT NULL, '
                    '"category" VARCHAR NOT NULL, '
                    '"description" VARCHAR, '
                    '"status" VARCHAR NOT NULL DEFAULT "new", '
                    '"resolutionNote" VARCHAR, '
                    '"createdAt" DATETIME DEFAULT CURRENT_TIMESTAMP, '
                    '"updatedAt" DATETIME DEFAULT CURRENT_TIMESTAMP'
                    ')'
                )
            )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
