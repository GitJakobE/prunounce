"""
Seed database from the existing JSON data files in src/backend/data/.
Run with: py -m poetry run python seed_data.py
"""
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, ".")

from app.database import SessionLocal, engine, Base, ensure_sqlite_schema
from app.models import Category, Story, Word, WordCategory

DATA_DIR = Path(__file__).parent.parent / "backend" / "data"


def load(filename: str) -> dict | list:
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def seed_categories(db, categories: list) -> None:
    print(f"  Seeding {len(categories)} categories...")
    for cat in categories:
        existing = db.get(Category, cat["id"])
        if existing:
            existing.name_en = cat["nameEn"]
            existing.name_da = cat["nameDa"]
            existing.name_it = cat.get("nameIt", "")
            existing.name_es = cat.get("nameEs", "")
            existing.order = cat["order"]
        else:
            db.add(Category(
                id=cat["id"],
                name_en=cat["nameEn"],
                name_da=cat["nameDa"],
                name_it=cat.get("nameIt", ""),
                name_es=cat.get("nameEs", ""),
                order=cat["order"],
            ))
    db.commit()


def seed_words(db, words: list, examples: dict, label: str) -> None:
    print(f"  Seeding {len(words)} {label} words...")
    for w in words:
        ex = examples.get(w["word"], {})
        existing = (
            db.query(Word)
            .filter(Word.word == w["word"], Word.language == w["language"])
            .first()
        )
        if existing:
            word_obj = existing
            existing.phonetic_hint = w["phoneticHint"]
            existing.translation_en = w["translationEn"]
            existing.translation_da = w["translationDa"]
            existing.translation_it = w.get("translationIt", "")
            existing.translation_es = w.get("translationEs", "")
            existing.difficulty = w["difficulty"]
            existing.example_it = ex.get("it", "")
            existing.example_en = ex.get("en", "")
            existing.example_da = ex.get("da", "")
            existing.example_es = ex.get("es", "")
        else:
            word_obj = Word(
                id=str(uuid.uuid4()),
                word=w["word"],
                language=w["language"],
                phonetic_hint=w["phoneticHint"],
                translation_en=w["translationEn"],
                translation_da=w["translationDa"],
                translation_it=w.get("translationIt", ""),
                translation_es=w.get("translationEs", ""),
                difficulty=w["difficulty"],
                example_it=ex.get("it", ""),
                example_en=ex.get("en", ""),
                example_da=ex.get("da", ""),
                example_es=ex.get("es", ""),
                source="seed",
            )
            db.add(word_obj)
            db.flush()  # get the id

        for cat_id in w.get("categories", []):
            exists = (
                db.query(WordCategory)
                .filter(WordCategory.word_id == word_obj.id, WordCategory.category_id == cat_id)
                .first()
            )
            if not exists:
                db.add(WordCategory(word_id=word_obj.id, category_id=cat_id))

    db.commit()


def seed_stories(db, stories: list) -> None:
    print(f"  Seeding {len(stories)} stories...")
    for s in stories:
        existing = (
            db.query(Story)
            .filter(Story.slug == s["slug"], Story.language == s["language"])
            .first()
        )
        if existing:
            existing.difficulty = s["difficulty"]
            existing.title = s["title"]
            existing.description_en = s.get("descriptionEn", "")
            existing.description_da = s.get("descriptionDa", "")
            existing.description_it = s.get("descriptionIt", "")
            existing.description_es = s.get("descriptionEs", "")
            existing.body = s["body"]
            existing.order = s.get("order", 0)
        else:
            db.add(Story(
                id=s.get("id", str(uuid.uuid4())),
                slug=s["slug"],
                language=s["language"],
                difficulty=s["difficulty"],
                title=s["title"],
                description_en=s.get("descriptionEn", ""),
                description_da=s.get("descriptionDa", ""),
                description_it=s.get("descriptionIt", ""),
                description_es=s.get("descriptionEs", ""),
                body=s["body"],
                order=s.get("order", 0),
            ))
    db.commit()


def main() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_sqlite_schema()
    db = SessionLocal()
    try:
        # --- Categories (from Italian seed file which has the full list) ---
        it_data = load("seed-words.json")
        seed_categories(db, it_data["categories"])

        # --- Italian words ---
        it_examples = load("examples.json")
        it_words = [
            {
                "word": w["italian"],
                "language": "it",
                "phoneticHint": w["phoneticHint"],
                "translationEn": w["translationEn"],
                "translationDa": w["translationDa"],
                "translationIt": w["italian"],
                "difficulty": w["difficulty"],
                "categories": w["categories"],
            }
            for w in it_data["words"]
        ]
        seed_words(db, it_words, it_examples, "Italian")

        # --- Danish words ---
        da_data = load("seed-words-da.json")
        da_examples = load("examples-da.json")
        da_words = [{**w, "language": "da"} for w in da_data["words"]]
        seed_words(db, da_words, da_examples, "Danish")

        # --- English words ---
        en_data = load("seed-words-en.json")
        en_examples = load("examples-en.json")
        en_words = [{**w, "language": "en"} for w in en_data["words"]]
        seed_words(db, en_words, en_examples, "English")

        # --- Spanish words ---
        es_data = load("seed-words-es.json")
        es_examples = load("examples-es.json")
        es_words = [{**w, "language": "es"} for w in es_data["words"]]
        seed_words(db, es_words, es_examples, "Spanish")

        # --- Top-100 per-language words ---
        for lang, label in [("it", "Italian"), ("da", "Danish"), ("en", "English"), ("es", "Spanish")]:
            top_data = load(f"seed-top100-{lang}.json")
            top_words = [{**w, "language": lang} for w in top_data["words"]]
            seed_words(db, top_words, {}, f"Top-100 {label}")

        # --- Stories (seeded after words so vocabulary is available) ---
        stories_data = load("stories.json")
        seed_stories(db, stories_data)

        # Summary
        print("\nDone!")
        for table, model in [("Category", Category), ("Word", Word), ("WordCategory", WordCategory), ("Story", Story)]:
            count = db.query(model).count()
            print(f"  {table}: {count} rows")
    finally:
        db.close()


if __name__ == "__main__":
    main()
