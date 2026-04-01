from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Category, Story, StoryAudio, User, UserProgress, Word, WordCategory

# In-memory SQLite with StaticPool so all connections share the same database
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def _override_get_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(scope="session", autouse=True)
def ensure_schema() -> None:
    Base.metadata.create_all(bind=test_engine)


@pytest.fixture(autouse=True)
def clean_db() -> Generator[None, None, None]:
    db = TestSessionLocal()
    db.query(StoryAudio).delete()
    db.query(UserProgress).delete()
    db.query(WordCategory).delete()
    db.query(Word).delete()
    db.query(Category).delete()
    db.query(Story).delete()
    db.query(User).delete()
    db.commit()
    db.close()
    yield


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
