import { Router, Request, Response } from "express";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import { body, validationResult } from "express-validator";
import prisma from "../db.js";
import { config } from "../config.js";
import { authMiddleware, AuthRequest } from "../middleware/auth.js";
import {
  loginRateLimiter,
  recordFailedAttempt,
  resetAttempts,
} from "../middleware/rate-limit.js";

const router = Router();

function generateToken(userId: string): string {
  return jwt.sign({ userId }, config.jwtSecret, {
    expiresIn: config.jwtExpiresIn,
  } as jwt.SignOptions);
}

// POST /api/auth/register
router.post(
  "/register",
  [
    body("email").isEmail().normalizeEmail(),
    body("password")
      .isLength({ min: 8 })
      .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
      .withMessage(
        "Password must be at least 8 characters with uppercase, lowercase, and a digit"
      ),
    body("language").optional().isIn(["en", "da"]),
  ],
  async (req: Request, res: Response): Promise<void> => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      res.status(400).json({ errors: errors.array() });
      return;
    }

    const { email, password, language, displayName } = req.body;

    const existing = await prisma.user.findUnique({ where: { email } });
    if (existing) {
      res
        .status(409)
        .json({
          error:
            "An account with this email already exists. Try logging in or resetting your password.",
        });
      return;
    }

    const passwordHash = await bcrypt.hash(password, 12);
    const user = await prisma.user.create({
      data: {
        email,
        passwordHash,
        language: language || "en",
        displayName: displayName || null,
      },
    });

    const token = generateToken(user.id);
    res.status(201).json({
      token,
      user: {
        id: user.id,
        email: user.email,
        displayName: user.displayName,
        language: user.language,
        hostId: user.hostId,
      },
    });
  }
);

// POST /api/auth/login
router.post(
  "/login",
  loginRateLimiter(),
  [body("email").isEmail().normalizeEmail(), body("password").notEmpty()],
  async (req: Request, res: Response): Promise<void> => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      res.status(400).json({ errors: errors.array() });
      return;
    }

    const { email, password } = req.body;
    const user = await prisma.user.findUnique({ where: { email } });

    if (!user || !user.passwordHash) {
      recordFailedAttempt(email);
      res.status(401).json({ error: "Invalid email or password" });
      return;
    }

    const valid = await bcrypt.compare(password, user.passwordHash);
    if (!valid) {
      recordFailedAttempt(email);
      res.status(401).json({ error: "Invalid email or password" });
      return;
    }

    resetAttempts(email);
    const token = generateToken(user.id);
    res.json({
      token,
      user: {
        id: user.id,
        email: user.email,
        displayName: user.displayName,
        language: user.language,
        hostId: user.hostId,
      },
    });
  }
);

// POST /api/auth/google
router.post(
  "/google",
  [body("credential").notEmpty()],
  async (req: Request, res: Response): Promise<void> => {
    const { credential } = req.body;

    try {
      // Verify Google ID token
      const { OAuth2Client } = await import("google-auth-library");
      const client = new OAuth2Client(config.googleClientId);
      const ticket = await client.verifyIdToken({
        idToken: credential,
        audience: config.googleClientId,
      });

      const payload = ticket.getPayload();
      if (!payload || !payload.email) {
        res.status(401).json({ error: "Invalid Google token" });
        return;
      }

      // Find or create user
      let user = await prisma.user.findUnique({
        where: { googleId: payload.sub },
      });

      if (!user) {
        user = await prisma.user.findUnique({
          where: { email: payload.email },
        });
        if (user) {
          // Link Google ID to existing account
          user = await prisma.user.update({
            where: { id: user.id },
            data: { googleId: payload.sub },
          });
        } else {
          user = await prisma.user.create({
            data: {
              email: payload.email,
              googleId: payload.sub,
              displayName: payload.name || null,
              language: "en",
            },
          });
        }
      }

      const token = generateToken(user.id);
      res.json({
        token,
        user: {
          id: user.id,
          email: user.email,
          displayName: user.displayName,
          language: user.language,
          hostId: user.hostId,
        },
      });
    } catch {
      res.status(401).json({ error: "Google authentication failed" });
    }
  }
);

// GET /api/auth/me
router.get(
  "/me",
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
      },
    });

    if (!user) {
      res.status(404).json({ error: "User not found" });
      return;
    }

    res.json({ user });
  }
);

export default router;
