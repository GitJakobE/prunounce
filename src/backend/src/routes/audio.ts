import { Router, Response } from "express";
import path from "path";
import prisma from "../db.js";
import { authMiddleware, AuthRequest } from "../middleware/auth.js";
import { getAudioPath } from "../services/tts.js";
import { getHost } from "../hosts.js";

const router = Router();

function getTargetExample(w: { language: string; exampleIt: string; exampleEn: string; exampleDa: string }): string {
  switch (w.language) {
    case "da": return w.exampleDa;
    case "en": return w.exampleEn;
    default: return w.exampleIt;
  }
}

async function resolveHostVoice(userId?: string) {
  if (!userId) return { hostId: "marco", voiceName: "it-IT-DiegoNeural" };
  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { hostId: true },
  });
  const hostId = user?.hostId ?? "marco";
  const host = getHost(hostId);
  return { hostId: host.id, voiceName: host.voice.voiceName };
}

// GET /api/audio/:wordId
router.get(
  "/:wordId",
  authMiddleware,
  async (req: AuthRequest, res: Response): Promise<void> => {
    const wordId = req.params.wordId as string;

    const word = await prisma.word.findUnique({ where: { id: wordId } });
    if (!word) {
      res.status(404).json({ error: "Word not found" });
      return;
    }

    const { hostId, voiceName } = await resolveHostVoice(req.userId);
    const host = getHost(hostId);
    if (host.language !== word.language) {
      res.status(400).json({ error: "Word language does not match your host language." });
      return;
    }
    const audioPath = await getAudioPath(word.word, undefined, hostId, voiceName);
    if (!audioPath) {
      res
        .status(503)
        .json({
          error:
            "Pronunciation temporarily unavailable. Please try again shortly.",
        });
      return;
    }

    res.setHeader("Content-Type", "audio/mpeg");
    res.setHeader("Cache-Control", "public, max-age=31536000, immutable");
    res.sendFile(path.resolve(audioPath));
  }
);

// GET /api/audio/:wordId/example — play the example sentence
router.get(
  "/:wordId/example",
  authMiddleware,
  async (req: AuthRequest, res: Response): Promise<void> => {
    const wordId = req.params.wordId as string;

    const word = await prisma.word.findUnique({ where: { id: wordId } });
    if (!word || !getTargetExample(word)) {
      res.status(404).json({ error: "Example not found" });
      return;
    }

    const { hostId, voiceName } = await resolveHostVoice(req.userId);
    const host = getHost(hostId);
    if (host.language !== word.language) {
      res.status(400).json({ error: "Word language does not match your host language." });
      return;
    }
    const targetExample = getTargetExample(word);
    const audioPath = await getAudioPath(`ex_${word.word}_${word.language}`, targetExample, hostId, voiceName);
    if (!audioPath) {
      res.status(503).json({ error: "Audio temporarily unavailable." });
      return;
    }

    res.setHeader("Content-Type", "audio/mpeg");
    res.setHeader("Cache-Control", "public, max-age=31536000, immutable");
    res.sendFile(path.resolve(audioPath));
  }
);

export default router;
