import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";
import { config } from "../config.js";

export interface AuthRequest extends Request {
  userId?: string;
}

export function authMiddleware(
  req: AuthRequest,
  res: Response,
  next: NextFunction
): void {
  let token: string | undefined;

  const header = req.headers.authorization;
  if (header && header.startsWith("Bearer ")) {
    token = header.slice(7);
  } else if (typeof req.query.token === "string" && req.query.token) {
    // Allow token via query param (needed for <audio> src URLs)
    token = req.query.token;
  }

  if (!token) {
    res.status(401).json({ error: "Authentication required" });
    return;
  }
  try {
    const payload = jwt.verify(token, config.jwtSecret) as { userId: string };
    req.userId = payload.userId;
    next();
  } catch {
    res.status(401).json({ error: "Invalid or expired token" });
  }
}
