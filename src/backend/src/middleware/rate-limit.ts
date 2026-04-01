import { Request, Response, NextFunction } from "express";

interface AttemptRecord {
  attempts: number;
  firstAttemptAt: number;
}

export interface LoginRateLimiterOptions {
  maxAttempts: number;
  windowMs: number;
}

const DEFAULT_OPTIONS: LoginRateLimiterOptions = {
  maxAttempts: 5,
  windowMs: 15 * 60 * 1000, // 15 minutes
};

const store = new Map<string, AttemptRecord>();

// Clean up expired entries every 5 minutes
const CLEANUP_INTERVAL = 5 * 60 * 1000;
let cleanupTimer: ReturnType<typeof setInterval> | null = null;

function startCleanup(windowMs: number) {
  if (cleanupTimer) return;
  cleanupTimer = setInterval(() => {
    const now = Date.now();
    for (const [key, record] of store) {
      if (now - record.firstAttemptAt > windowMs) {
        store.delete(key);
      }
    }
  }, CLEANUP_INTERVAL);
  // Allow the process to exit without waiting for this timer
  if (cleanupTimer.unref) cleanupTimer.unref();
}

export function loginRateLimiter(opts: Partial<LoginRateLimiterOptions> = {}) {
  const { maxAttempts, windowMs } = { ...DEFAULT_OPTIONS, ...opts };
  startCleanup(windowMs);

  return (req: Request, res: Response, next: NextFunction): void => {
    const email = req.body?.email?.toLowerCase?.() ?? "";
    if (!email) {
      next();
      return;
    }

    const now = Date.now();
    const record = store.get(email);

    if (record) {
      // Window expired — reset
      if (now - record.firstAttemptAt > windowMs) {
        store.delete(email);
        next();
        return;
      }

      if (record.attempts >= maxAttempts) {
        res.status(429).json({
          error: "Too many login attempts. Please try again in 15 minutes.",
        });
        return;
      }
    }

    next();
  };
}

export function recordFailedAttempt(email: string): void {
  const key = email.toLowerCase();
  const now = Date.now();
  const record = store.get(key);

  if (!record || now - record.firstAttemptAt > DEFAULT_OPTIONS.windowMs) {
    store.set(key, { attempts: 1, firstAttemptAt: now });
  } else {
    record.attempts += 1;
  }
}

export function resetAttempts(email: string): void {
  store.delete(email.toLowerCase());
}

/** Exposed for testing only */
export function _clearStore(): void {
  store.clear();
}
