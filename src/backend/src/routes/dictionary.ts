import { Router, Response } from "express";
import prisma from "../db.js";
import { authMiddleware, AuthRequest } from "../middleware/auth.js";
import { getHost } from "../hosts.js";
import { getAudioPath } from "../services/tts.js";

const router = Router();

const SUPPORTED_LANGS = ["en", "da", "it"];

function resolveTargetLanguage(hostId: string): string {
  return getHost(hostId).language;
}

function resolveRefLang(query: string | undefined, targetLang: string): string {
  if (query && SUPPORTED_LANGS.includes(query) && query !== targetLang) return query;
  return targetLang === "en" ? "da" : "en";
}

function getCategoryName(cat: { nameEn: string; nameDa: string; nameIt: string }, lang: string): string {
  if (lang === "it") return cat.nameIt || cat.nameEn;
  if (lang === "da") return cat.nameDa;
  return cat.nameEn;
}

function getTranslation(w: { translationEn: string; translationDa: string; translationIt: string }, lang: string): string {
  if (lang === "it") return w.translationIt;
  if (lang === "da") return w.translationDa;
  return w.translationEn;
}

function getTargetExample(w: { language: string; exampleIt: string; exampleEn: string; exampleDa: string }): string {
  if (w.language === "da") return w.exampleDa;
  if (w.language === "en") return w.exampleEn;
  return w.exampleIt;
}

function getRefExample(w: { exampleIt: string; exampleEn: string; exampleDa: string }, lang: string): string {
  if (lang === "it") return w.exampleIt;
  if (lang === "da") return w.exampleDa;
  return w.exampleEn;
}

async function resolveUserTarget(userId: string): Promise<string> {
  const user = await prisma.user.findUnique({ where: { id: userId }, select: { hostId: true } });
  return resolveTargetLanguage(user?.hostId ?? "marco");
}

// GET /api/dictionary/categories
router.get(
  "/categories",
  authMiddleware,
  async (req: AuthRequest, res: Response): Promise<void> => {
    const userId = req.userId!;
    const targetLang = await resolveUserTarget(userId);
    const lang = resolveRefLang(req.query.lang as string | undefined, targetLang);

    const categories = await prisma.category.findMany({
      orderBy: { order: "asc" },
      include: {
        words: {
          include: { word: true },
          where: { word: { language: targetLang } },
        },
      },
    });

    const listenedWordIds = new Set(
      (
        await prisma.userProgress.findMany({
          where: { userId },
          select: { wordId: true },
        })
      ).map((p) => p.wordId)
    );

    const result = categories.filter((cat) => cat.words.length > 0).map((cat) => {
      const words = cat.words.map((wc) => wc.word);
      const difficulties = ["beginner", "intermediate", "advanced"];
      const progressByDifficulty = difficulties.map((d) => {
        const wordsAtLevel = words.filter((w) => w.difficulty === d);
        const listened = wordsAtLevel.filter((w) =>
          listenedWordIds.has(w.id)
        ).length;
        return { difficulty: d, total: wordsAtLevel.length, listened };
      });

      return {
        id: cat.id,
        name: getCategoryName(cat, lang),
        totalWords: words.length,
        listenedWords: words.filter((w) => listenedWordIds.has(w.id)).length,
        progressByDifficulty,
      };
    });

    res.json({ categories: result });
  }
);

// GET /api/dictionary/categories/:id/words
router.get(
  "/categories/:id/words",
  authMiddleware,
  async (req: AuthRequest, res: Response): Promise<void> => {
    const id = req.params.id as string;
    const userId = req.userId!;
    const targetLang = await resolveUserTarget(userId);
    const lang = resolveRefLang(req.query.lang as string | undefined, targetLang);
    const difficulty = req.query.difficulty as string | undefined;

    const category = await prisma.category.findUnique({ where: { id } });
    if (!category) {
      res.status(404).json({ error: "Category not found" });
      return;
    }

    const wordFilter: Record<string, unknown> = { language: targetLang };
    if (difficulty && ["beginner", "intermediate", "advanced"].includes(difficulty)) {
      wordFilter.difficulty = difficulty;
    }

    const wordCategories = await prisma.wordCategory.findMany({
      where: { categoryId: id, word: wordFilter },
      include: { word: true },
    });

    const listenedWordIds = new Set(
      (
        await prisma.userProgress.findMany({
          where: { userId },
          select: { wordId: true },
        })
      ).map((p) => p.wordId)
    );

    const words = wordCategories.map((wc) => ({
      id: wc.word.id,
      word: wc.word.word,
      phoneticHint: wc.word.phoneticHint,
      translation: getTranslation(wc.word, lang),
      exampleTarget: getTargetExample(wc.word),
      example: getRefExample(wc.word, lang),
      difficulty: wc.word.difficulty,
      listened: listenedWordIds.has(wc.word.id),
    }));

    res.json({
      category: {
        id: category.id,
        name: getCategoryName(category, lang),
      },
      words,
    });
  }
);

// POST /api/dictionary/words/:id/listened
router.post(
  "/words/:id/listened",
  authMiddleware,
  async (req: AuthRequest, res: Response): Promise<void> => {
    const id = req.params.id as string;
    const userId = req.userId!;

    const word = await prisma.word.findUnique({ where: { id } });
    if (!word) {
      res.status(404).json({ error: "Word not found" });
      return;
    }

    await prisma.userProgress.upsert({
      where: { userId_wordId: { userId, wordId: id } },
      update: { listenedAt: new Date() },
      create: { userId, wordId: id },
    });

    res.json({ listened: true });
  }
);

const VALID_DIFFICULTIES = ["beginner", "intermediate", "advanced"];
const WORD_MAX_LENGTH = 100;
const WORD_PATTERN = /[a-zA-ZÀ-ÿæøåÆØÅ]/;

// POST /api/dictionary/words — user-contributed word
router.post(
  "/words",
  authMiddleware,
  async (req: AuthRequest, res: Response): Promise<void> => {
    const userId = req.userId!;
    const { word, translation, phoneticHint, categoryId, difficulty, example, exampleTranslation } = req.body;

    // Validate word
    if (!word || typeof word !== "string" || !word.trim()) {
      res.status(400).json({ error: "Word is required." });
      return;
    }
    const trimmedWord = word.trim();
    if (trimmedWord.length > WORD_MAX_LENGTH) {
      res.status(400).json({ error: `Word must be ${WORD_MAX_LENGTH} characters or fewer.` });
      return;
    }
    if (!WORD_PATTERN.test(trimmedWord)) {
      res.status(400).json({ error: "Word must contain at least one letter." });
      return;
    }

    // Validate translation
    if (!translation || typeof translation !== "string" || !translation.trim()) {
      res.status(400).json({ error: "Translation is required." });
      return;
    }

    // Validate difficulty
    const diff = difficulty || "beginner";
    if (!VALID_DIFFICULTIES.includes(diff)) {
      res.status(400).json({ error: `Difficulty must be one of: ${VALID_DIFFICULTIES.join(", ")}` });
      return;
    }

    // Resolve target language from host
    const targetLang = await resolveUserTarget(userId);
    const refLang = resolveRefLang(undefined, targetLang);

    // Validate category if provided
    if (categoryId) {
      const cat = await prisma.category.findUnique({ where: { id: categoryId } });
      if (!cat) {
        res.status(400).json({ error: "Category not found." });
        return;
      }
    }

    // Duplicate check
    const existing = await prisma.word.findUnique({
      where: { word_language: { word: trimmedWord.toLowerCase(), language: targetLang } },
    });
    if (existing) {
      res.status(409).json({ error: "This word already exists.", existingWordId: existing.id });
      return;
    }

    // Build translation columns
    const translationEn = refLang === "en" ? translation.trim() : "";
    const translationDa = refLang === "da" ? translation.trim() : "";
    const translationIt = refLang === "it" ? translation.trim() : "";

    // Build example columns
    const exTarget = example?.trim() || "";
    const exRef = exampleTranslation?.trim() || "";
    const exampleIt = targetLang === "it" ? exTarget : refLang === "it" ? exRef : "";
    const exampleEn = targetLang === "en" ? exTarget : refLang === "en" ? exRef : "";
    const exampleDa = targetLang === "da" ? exTarget : refLang === "da" ? exRef : "";

    // Create word
    const newWord = await prisma.word.create({
      data: {
        word: trimmedWord.toLowerCase(),
        language: targetLang,
        source: "user",
        contributedBy: userId,
        phoneticHint: phoneticHint?.trim() || "",
        translationEn,
        translationDa,
        translationIt,
        difficulty: diff,
        exampleIt,
        exampleEn,
        exampleDa,
      },
    });

    // Assign category (or "uncategorised")
    const assignCatId = categoryId || "uncategorised";
    if (!categoryId) {
      await prisma.category.upsert({
        where: { id: "uncategorised" },
        update: {},
        create: { id: "uncategorised", nameEn: "Uncategorised", nameDa: "Ukategoriseret", nameIt: "Non categorizzato", order: 99 },
      });
    }
    await prisma.wordCategory.create({
      data: { wordId: newWord.id, categoryId: assignCatId },
    });

    // Async audio generation (fire-and-forget)
    const user = await prisma.user.findUnique({ where: { id: userId }, select: { hostId: true } });
    const host = getHost(user?.hostId ?? "marco");
    getAudioPath(newWord.word, undefined, host.id, host.voice.voiceName).catch(() => {});
    if (exTarget) {
      getAudioPath(`ex_${newWord.word}_${newWord.language}`, exTarget, host.id, host.voice.voiceName).catch(() => {});
    }

    res.status(201).json({
      id: newWord.id,
      word: newWord.word,
      language: newWord.language,
      translationEn: newWord.translationEn,
      translationDa: newWord.translationDa,
      translationIt: newWord.translationIt,
      source: newWord.source,
      audioGenerating: true,
    });
  }
);

export default router;
