import { Router, Response } from "express";
import prisma from "../db.js";
import { authMiddleware, AuthRequest } from "../middleware/auth.js";
import { HOST_IDS, getHost } from "../hosts.js";

const router = Router();

// GET /api/profile
router.get(
  "/",
  authMiddleware,
  async (req: AuthRequest, res: Response): Promise<void> => {
    const user = await prisma.user.findUnique({
      where: { id: req.userId },
      select: {
        id: true,
        email: true,
        displayName: true,
        language: true,
        hostId: true,
        createdAt: true,
      },
    });

    if (!user) {
      res.status(404).json({ error: "User not found" });
      return;
    }

    // Get progress summary scoped to target language
    const targetLang = user.hostId ? getHost(user.hostId).language : "it";
    const totalWords = await prisma.word.count({ where: { language: targetLang } });
    const listenedWords = await prisma.userProgress.count({
      where: { userId: req.userId, word: { language: targetLang } },
    });

    res.json({
      user,
      progress: { totalWords, listenedWords },
    });
  }
);

// PATCH /api/profile
router.patch(
  "/",
  authMiddleware,
  async (req: AuthRequest, res: Response): Promise<void> => {
    const { displayName, language, hostId } = req.body;
    const data: Record<string, string> = {};

    if (displayName !== undefined) data.displayName = displayName;
    if (language && ["en", "da", "it"].includes(language)) data.language = language;
    if (hostId && HOST_IDS.includes(hostId)) data.hostId = hostId;

    if (Object.keys(data).length === 0) {
      res.status(400).json({ error: "No valid fields to update" });
      return;
    }

    const user = await prisma.user.update({
      where: { id: req.userId },
      data,
      select: {
        id: true,
        email: true,
        displayName: true,
        language: true,
        hostId: true,
      },
    });

    res.json({ user });
  }
);

// DELETE /api/profile — GDPR account deletion
router.delete(
  "/",
  authMiddleware,
  async (req: AuthRequest, res: Response): Promise<void> => {
    await prisma.user.delete({ where: { id: req.userId } });
    res.json({ message: "Account and all associated data deleted" });
  }
);

export default router;
