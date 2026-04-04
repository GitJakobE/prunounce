from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user_id
from ..hosts import get_host
from ..models import Category, User, UserProgress, Word, WordCategory


router = APIRouter(prefix="/api/progress")

SUPPORTED_LANGS = ["en", "da", "it", "es"]
VALID_DIFFICULTIES = ["beginner", "intermediate", "advanced"]


def get_category_name(category: Category, lang: str) -> str:
    if lang == "it":
        return category.name_it or category.name_en
    if lang == "da":
        return category.name_da or category.name_en
    if lang == "es":
        return category.name_es or category.name_en
    return category.name_en


@router.get("")
def get_progress(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    host_id = user.host_id if user and user.host_id else "marco"
    host = get_host(host_id)
    target_lang = host["language"]

    # Reference language for category names — read from user profile
    ref_lang = "en"
    if user and user.language in SUPPORTED_LANGS:
        ref_lang = user.language
    elif target_lang == "en":
        ref_lang = "da"

    total_words = db.query(func.count(Word.id)).filter(Word.language == target_lang).scalar() or 0
    listened_word_ids = {
        row.word_id
        for row in db.query(UserProgress.word_id).filter(UserProgress.user_id == user_id).all()
    }
    listened_in_lang = (
        db.query(func.count(UserProgress.id))
        .join(Word, Word.id == UserProgress.word_id)
        .filter(UserProgress.user_id == user_id, Word.language == target_lang)
        .scalar()
        or 0
    )

    # Per-category breakdown
    categories_all = db.query(Category).order_by(Category.order.asc()).all()
    word_pairs = (
        db.query(WordCategory.category_id, Word)
        .join(Word, Word.id == WordCategory.word_id)
        .filter(Word.language == target_lang)
        .all()
    )
    words_by_category: dict[str, list[Word]] = {}
    for cat_id, word in word_pairs:
        words_by_category.setdefault(cat_id, []).append(word)

    categories = []
    for cat in categories_all:
        words = words_by_category.get(cat.id, [])
        if not words:
            continue
        listened_count = len([w for w in words if w.id in listened_word_ids])
        categories.append({
            "id": cat.id,
            "name": get_category_name(cat, ref_lang),
            "totalWords": len(words),
            "listenedWords": listened_count,
        })

    return {
        "language": target_lang,
        "totalWords": int(total_words),
        "listenedWords": int(listened_in_lang),
        "categories": categories,
    }
