import { Router, Response } from "express";
import prisma from "../db.js";
import { authMiddleware, AuthRequest } from "../middleware/auth.js";
import { getHost } from "../hosts.js";

const router = Router();

const SUPPORTED_LANGS = ["en", "da", "it"];

function resolveRefLang(query: string | undefined, targetLang: string): string {
  if (query && SUPPORTED_LANGS.includes(query) && query !== targetLang) return query;
  return targetLang === "en" ? "da" : "en";
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

function getCategoryName(cat: { nameEn: string; nameDa: string; nameIt: string }, lang: string): string {
  if (lang === "it") return cat.nameIt || cat.nameEn;
  if (lang === "da") return cat.nameDa;
  return cat.nameEn;
}

// GET /api/search?q=term&lang=en
router.get(
  "/",
  authMiddleware,
  async (req: AuthRequest, res: Response): Promise<void> => {
    const q = (req.query.q as string || "").trim();
    const userId = req.userId!;

    // Resolve target language from user's host
    const user = await prisma.user.findUnique({ where: { id: userId }, select: { hostId: true } });
    const targetLang = getHost(user?.hostId ?? "marco").language;
    const lang = resolveRefLang(req.query.lang as string | undefined, targetLang);

    if (q.length < 2) {
      res.status(400).json({ error: "Search term must be at least 2 characters" });
      return;
    }

    // Normalize: lowercase, strip common diacritics for matching
    const normalized = q
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");

    // Search within target language word set
    const allWords = await prisma.word.findMany({
      where: { language: targetLang },
      include: {
        categories: {
          include: { category: true },
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

    const results = allWords
      .map((w) => {
        const wordNorm = w.word
          .toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "");
        const translationNorm = getTranslation(w, lang)
          .toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "");

        // Rank: exact match > prefix > contains
        let score = 0;
        if (wordNorm === normalized || translationNorm === normalized) {
          score = 3;
        } else if (
          wordNorm.startsWith(normalized) ||
          translationNorm.startsWith(normalized)
        ) {
          score = 2;
        } else if (
          wordNorm.includes(normalized) ||
          translationNorm.includes(normalized)
        ) {
          score = 1;
        }

        if (score === 0) return null;

        return {
          score,
          word: {
            id: w.id,
            word: w.word,
            phoneticHint: w.phoneticHint,
            translation: getTranslation(w, lang),
            exampleTarget: getTargetExample(w),
            example: getRefExample(w, lang),
            difficulty: w.difficulty,
            listened: listenedWordIds.has(w.id),
            categories: w.categories.map((wc) => ({
              id: wc.category.id,
              name: getCategoryName(wc.category, lang),
            })),
          },
        };
      })
      .filter((r) => r !== null)
      .sort((a, b) => b.score - a.score)
      .map((r) => r.word);

    if (results.length === 0) {
      res.json({ results: [], message: `No results found for '${q}'.` });
      return;
    }

    res.json({ results });
  }
);

export default router;
