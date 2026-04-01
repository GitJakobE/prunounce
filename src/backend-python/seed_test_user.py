"""
Create a test user for local development.
Run with: py -m poetry run python seed_test_user.py
"""
import sys
import uuid
from datetime import datetime

# Ensure the app package is importable from this directory
sys.path.insert(0, ".")

from app.auth import hash_password
from app.database import SessionLocal, engine, Base
from app.models import User

EMAIL = "test@example.com"
PASSWORD = "Test1234!"

def main():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == EMAIL).first()
        if existing:
            print(f"User '{EMAIL}' already exists (id={existing.id}). Nothing to do.")
            return

        user = User(
            id=str(uuid.uuid4()),
            email=EMAIL,
            password_hash=hash_password(PASSWORD),
            display_name="Test User",
            language="en",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created test user:")
        print(f"  email:    {EMAIL}")
        print(f"  password: {PASSWORD}")
        print(f"  id:       {user.id}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
