from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user_id
from ..hosts import get_host
from ..models import Category, User, UserProgress, Word, WordCategory


router = APIRouter(prefix="/api/search")

SUPPORTED_LANGS = ["en", "da", "it"]


def resolve_ref_lang(query: str | None, target_lang: str) -> str:
    if query and query in SUPPORTED_LANGS and query != target_lang:
        return query
    return "da" if target_lang == "en" else "en"


def get_translation(word: Word, lang: str) -> str:
    if lang == "it":
        return word.translation_it
    if lang == "da":
        return word.translation_da
    return word.translation_en


def get_target_example(word: Word) -> str:
    if word.language == "da":
        return word.example_da
    if word.language == "en":
        return word.example_en
    return word.example_it


def get_ref_example(word: Word, lang: str) -> str:
    if lang == "it":
        return word.example_it
    if lang == "da":
        return word.example_da
    return word.example_en


def get_category_name(category: Category, lang: str) -> str:
    if lang == "it":
        return category.name_it or category.name_en
    if lang == "da":
        return category.name_da
    return category.name_en


def normalize(value: str) -> str:
    base = value.lower()
    mapping = str.maketrans(
        {
            "à": "a",
            "á": "a",
            "â": "a",
            "ã": "a",
            "ä": "a",
            "å": "a",
            "è": "e",
            "é": "e",
            "ê": "e",
            "ë": "e",
            "ì": "i",
            "í": "i",
            "î": "i",
            "ï": "i",
            "ò": "o",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ö": "o",
            "ù": "u",
            "ú": "u",
            "û": "u",
            "ü": "u",
            "ç": "c",
            "ñ": "n",
        }
    )
    return base.translate(mapping)


@router.get("")
def search(
    q: str = Query(default=""),
    lang: str | None = Query(default=None),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    query = (q or "").strip()
    if len(query) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Search term must be at least 2 characters")

    user = db.query(User).filter(User.id == user_id).first()
    target_lang = get_host(user.host_id if user and user.host_id else "marco")["language"]
    ref_lang = resolve_ref_lang(lang, target_lang)
    normalized = normalize(query)

    all_words = db.query(Word).filter(Word.language == target_lang).all()
    listened_word_ids = {
        row.word_id
        for row in db.query(UserProgress.word_id).filter(UserProgress.user_id == user_id).all()
    }

    category_rows = (
        db.query(WordCategory.word_id, Category)
        .join(Category, Category.id == WordCategory.category_id)
        .all()
    )
    categories_by_word: dict[str, list[Category]] = {}
    for word_id, category in category_rows:
        categories_by_word.setdefault(word_id, []).append(category)

    ranked: list[tuple[int, dict]] = []
    for word in all_words:
        word_norm = normalize(word.word)
        translation_norm = normalize(get_translation(word, ref_lang))

        score = 0
        if word_norm == normalized or translation_norm == normalized:
            score = 3
        elif word_norm.startswith(normalized) or translation_norm.startswith(normalized):
            score = 2
        elif normalized in word_norm or normalized in translation_norm:
            score = 1

        if score == 0:
            continue

        ranked.append(
            (
                score,
                {
                    "id": word.id,
                    "word": word.word,
                    "phoneticHint": word.phonetic_hint,
                    "translation": get_translation(word, ref_lang),
                    "exampleTarget": get_target_example(word),
                    "example": get_ref_example(word, ref_lang),
                    "difficulty": word.difficulty,
                    "listened": word.id in listened_word_ids,
                    "categories": [
                        {"id": cat.id, "name": get_category_name(cat, ref_lang)}
                        for cat in categories_by_word.get(word.id, [])
                    ],
                },
            )
        )

    ranked.sort(key=lambda x: x[0], reverse=True)
    results = [entry for _, entry in ranked]

    if not results:
        return {"results": [], "message": f"No results found for '{query}'."}

    return {"results": results}
