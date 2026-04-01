import time

from fastapi import HTTPException, status


MAX_ATTEMPTS = 5
WINDOW_SECONDS = 15 * 60

_store: dict[str, tuple[int, float]] = {}


def _is_expired(first_attempt_at: float) -> bool:
    return (time.time() - first_attempt_at) > WINDOW_SECONDS


def check_login_allowed(email: str) -> None:
    key = email.lower()
    record = _store.get(key)
    if not record:
        return

    attempts, first_attempt_at = record
    if _is_expired(first_attempt_at):
        _store.pop(key, None)
        return

    if attempts >= MAX_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts. Try again later.",
        )


def record_failed_attempt(email: str) -> None:
    key = email.lower()
    now = time.time()
    attempts, first_attempt_at = _store.get(key, (0, now))
    if _is_expired(first_attempt_at):
        _store[key] = (1, now)
        return
    _store[key] = (attempts + 1, first_attempt_at)


def reset_attempts(email: str) -> None:
    _store.pop(email.lower(), None)
