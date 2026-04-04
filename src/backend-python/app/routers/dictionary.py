import re
from datetime import datetime, timezone

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..dependencies import get_current_user_id
from ..hosts import get_host
from ..models import Category, User, UserProgress, Word, WordCategory
from ..database import get_db
from ..schemas import WordLookupResult
from ..services.tts import get_audio_path
from ..services.translation import translate_word


router = APIRouter(prefix="/api/dictionary")

SUPPORTED_LANGS = ["en", "da", "it", "es"]
VALID_DIFFICULTIES = ["beginner", "intermediate", "advanced"]
WORD_MAX_LENGTH = 100
WORD_PATTERN = re.compile(r"[a-zA-ZÀ-ÿæøåÆØÅñÑ]")
WORD_REJECT_DIGITS = re.compile(r"\d")


def resolve_target_language(host_id: str) -> str:
    return get_host(host_id)["language"]


def resolve_ref_lang(query: str | None, target_lang: str, user_id: str | None = None, db: Session | None = None) -> str:
    if query and query in SUPPORTED_LANGS:
        return query
    # Read the user's stored reference language preference
    if user_id and db:
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.language in SUPPORTED_LANGS:
            return user.language
    return "da" if target_lang == "en" else "en"


def get_category_name(category: Category, lang: str) -> str:
    if lang == "it":
        return category.name_it or category.name_en
    if lang == "da":
        return category.name_da or category.name_en
    if lang == "es":
        return category.name_es or category.name_en
    return category.name_en


def get_translation(word: Word, lang: str) -> str:
    if lang == "it":
        return word.translation_it
    if lang == "da":
        return word.translation_da
    if lang == "es":
        return word.translation_es
    return word.translation_en


def get_target_example(word: Word) -> str:
    if word.language == "da":
        return word.example_da
    if word.language == "en":
        return word.example_en
    if word.language == "es":
        return word.example_es
    return word.example_it


def get_ref_example(word: Word, lang: str) -> str:
    if lang == "it":
        return word.example_it
    if lang == "da":
        return word.example_da
    if lang == "es":
        return word.example_es
    return word.example_en


def resolve_user_target(user_id: str, db: Session) -> str:
    user = db.query(User).filter(User.id == user_id).first()
    return resolve_target_language(user.host_id if user and user.host_id else "marco")


def normalize(value: str) -> str:
    base = value.lower()
    mapping = str.maketrans(
        {
            "à": "a", "á": "a", "â": "a", "ã": "a", "ä": "a", "å": "a",
            "è": "e", "é": "e", "ê": "e", "ë": "e",
            "ì": "i", "í": "i", "î": "i", "ï": "i",
            "ò": "o", "ó": "o", "ô": "o", "õ": "o", "ö": "o",
            "ù": "u", "ú": "u", "û": "u", "ü": "u",
            "ç": "c", "ñ": "n",
        }
    )
    return base.translate(mapping)


@router.get("/lookup", response_model=WordLookupResult)
def lookup_word(
    word: str = Query(),
    lang: str | None = Query(default=None),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> WordLookupResult:
    """Look up a single word by exact (normalised) match for use in story translation panel."""
    target_lang = resolve_user_target(user_id, db)
    ref_lang = resolve_ref_lang(lang, target_lang, user_id, db)

    normalised = normalize(word)
    all_words = (
        db.query(Word)
        .filter(Word.language == target_lang)
        .all()
    )
    matched = next(
        (w for w in all_words if normalize(w.word) == normalised),
        None,
    )

    if matched is None:
        # Cascade: try TranslationCache → external translation provider
        translation, source = translate_word(word, target_lang, ref_lang, db)
        return WordLookupResult(
            word=word,
            translation=translation,
            phoneticHint=None,
            wordId=None,
            source=source,
        )

    return WordLookupResult(
        word=matched.word,
        translation=get_translation(matched, ref_lang),
        phoneticHint=matched.phonetic_hint,
        wordId=matched.id,
        source="curated",
    )


@router.get("/categories")
def categories(
    lang: str | None = Query(default=None),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    target_lang = resolve_user_target(user_id, db)
    ref_lang = resolve_ref_lang(lang, target_lang, user_id, db)

    categories_all = db.query(Category).order_by(Category.order.asc()).all()
    listened_word_ids = {
        row.word_id
        for row in db.query(UserProgress.word_id).filter(UserProgress.user_id == user_id).all()
    }

    word_pairs = (
        db.query(WordCategory.category_id, Word)
        .join(Word, Word.id == WordCategory.word_id)
        .filter(Word.language == target_lang)
        .all()
    )

    words_by_category: dict[str, list[Word]] = {}
    for category_id, word in word_pairs:
        words_by_category.setdefault(category_id, []).append(word)

    result = []
    for category in categories_all:
        words = words_by_category.get(category.id, [])
        progress_by_difficulty = []
        for difficulty in VALID_DIFFICULTIES:
            words_at_level = [w for w in words if w.difficulty == difficulty]
            listened = len([w for w in words_at_level if w.id in listened_word_ids])
            progress_by_difficulty.append(
                {"difficulty": difficulty, "total": len(words_at_level), "listened": listened}
            )

        result.append(
            {
                "id": category.id,
                "name": get_category_name(category, ref_lang),
                "totalWords": len(words),
                "listenedWords": len([w for w in words if w.id in listened_word_ids]),
                "progressByDifficulty": progress_by_difficulty,
            }
        )

    return {"categories": result}


@router.get("/categories/{category_id}/words")
def category_words(
    category_id: str,
    lang: str | None = Query(default=None),
    difficulty: str | None = Query(default=None),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    target_lang = resolve_user_target(user_id, db)
    ref_lang = resolve_ref_lang(lang, target_lang, user_id, db)

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    word_query = (
        db.query(Word)
        .join(WordCategory, WordCategory.word_id == Word.id)
        .filter(WordCategory.category_id == category_id, Word.language == target_lang)
    )
    if difficulty and difficulty in VALID_DIFFICULTIES:
        word_query = word_query.filter(Word.difficulty == difficulty)

    words_rows = word_query.all()
    listened_word_ids = {
        row.word_id
        for row in db.query(UserProgress.word_id).filter(UserProgress.user_id == user_id).all()
    }

    words = [
        {
            "id": word.id,
            "word": word.word,
            "phoneticHint": word.phonetic_hint,
            "translation": get_translation(word, ref_lang),
            "exampleTarget": get_target_example(word),
            "example": get_ref_example(word, ref_lang),
            "difficulty": word.difficulty,
            "listened": word.id in listened_word_ids,
        }
        for word in words_rows
    ]

    return {
        "category": {"id": category.id, "name": get_category_name(category, ref_lang)},
        "words": words,
    }


@router.post("/words/{word_id}/listened")
def mark_listened(
    word_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Word not found")

    progress = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == user_id, UserProgress.word_id == word_id)
        .first()
    )
    if progress:
        progress.listened_at = datetime.now(timezone.utc)
    else:
        db.add(UserProgress(user_id=user_id, word_id=word_id))

    db.commit()
    return {"listened": True}


@router.post("/words")
def create_word(
    payload: dict = Body(default={}),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    word = payload.get("word")
    translation = payload.get("translation")
    translation_en_in = payload.get("translationEn")
    translation_da_in = payload.get("translationDa")
    translation_it_in = payload.get("translationIt")
    translation_es_in = payload.get("translationEs")
    phonetic_hint = payload.get("phoneticHint")
    category_id = payload.get("categoryId")
    difficulty = payload.get("difficulty")
    example = payload.get("example")
    example_translation = payload.get("exampleTranslation")

    if not isinstance(word, str) or not word.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Word is required.")

    trimmed_word = word.strip()
    if len(trimmed_word) > WORD_MAX_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Word must be {WORD_MAX_LENGTH} characters or fewer.",
        )
    if not WORD_PATTERN.search(trimmed_word):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Word must contain at least one letter.")
    if WORD_REJECT_DIGITS.search(trimmed_word):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Word must not contain numbers.")

    # Check if any explicit per-language translations were provided
    has_explicit = any(
        isinstance(v, str) and v.strip()
        for v in [translation_en_in, translation_da_in, translation_it_in, translation_es_in]
    )
    has_generic = isinstance(translation, str) and bool(translation.strip())

    if not has_explicit and not has_generic:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one translation is required.")

    diff = difficulty or "beginner"
    if diff not in VALID_DIFFICULTIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Difficulty must be one of: {', '.join(VALID_DIFFICULTIES)}",
        )

    target_lang = resolve_user_target(user_id, db)
    ref_lang = resolve_ref_lang(None, target_lang, user_id, db)

    if category_id:
        cat = db.query(Category).filter(Category.id == category_id).first()
        if not cat:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found.")

    normalized_word = trimmed_word.lower()
    existing = (
        db.query(Word)
        .filter(Word.word == normalized_word, Word.language == target_lang)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "This word already exists.", "existingWordId": existing.id},
        )

    # Per-language translation columns: explicit fields take precedence over generic
    if has_explicit:
        translation_en = translation_en_in.strip() if isinstance(translation_en_in, str) else ""
        translation_da = translation_da_in.strip() if isinstance(translation_da_in, str) else ""
        translation_it = translation_it_in.strip() if isinstance(translation_it_in, str) else ""
        translation_es = translation_es_in.strip() if isinstance(translation_es_in, str) else ""
    else:
        translation_en = translation.strip() if ref_lang == "en" else ""
        translation_da = translation.strip() if ref_lang == "da" else ""
        translation_it = translation.strip() if ref_lang == "it" else ""
        translation_es = translation.strip() if ref_lang == "es" else ""

    ex_target = example.strip() if isinstance(example, str) else ""
    ex_ref = example_translation.strip() if isinstance(example_translation, str) else ""
    example_it = ex_target if target_lang == "it" else ex_ref if ref_lang == "it" else ""
    example_en = ex_target if target_lang == "en" else ex_ref if ref_lang == "en" else ""
    example_da = ex_target if target_lang == "da" else ex_ref if ref_lang == "da" else ""
    example_es = ex_target if target_lang == "es" else ex_ref if ref_lang == "es" else ""

    new_word = Word(
        word=normalized_word,
        language=target_lang,
        source="user",
        contributed_by=user_id,
        phonetic_hint=phonetic_hint.strip() if isinstance(phonetic_hint, str) else "",
        translation_en=translation_en,
        translation_da=translation_da,
        translation_it=translation_it,
        translation_es=translation_es,
        difficulty=diff,
        example_it=example_it,
        example_en=example_en,
        example_da=example_da,
        example_es=example_es,
    )
    db.add(new_word)
    db.flush()

    assign_cat_id = category_id or "uncategorised"
    if not category_id:
        uncategorised = db.query(Category).filter(Category.id == "uncategorised").first()
        if not uncategorised:
            db.add(
                Category(
                    id="uncategorised",
                    name_en="Uncategorised",
                    name_da="Ukategoriseret",
                    name_it="Non categorizzato",
                    name_es="Sin categoría",
                    order=99,
                )
            )
            db.flush()

    db.add(WordCategory(word_id=new_word.id, category_id=assign_cat_id))
    db.commit()

    user = db.query(User).filter(User.id == user_id).first()
    host = get_host(user.host_id if user and user.host_id else "marco")
    try:
        get_audio_path(new_word.word, None, host["id"], host["voice"]["voiceName"])
        if ex_target:
            get_audio_path(
                f"ex_{new_word.word}_{new_word.language}",
                ex_target,
                host["id"],
                host["voice"]["voiceName"],
            )
    except Exception:
        pass

    return {
        "id": new_word.id,
        "word": new_word.word,
        "language": new_word.language,
        "translationEn": new_word.translation_en,
        "translationDa": new_word.translation_da,
        "translationIt": new_word.translation_it,
        "translationEs": new_word.translation_es,
        "source": new_word.source,
        "audioGenerating": True,
    }
