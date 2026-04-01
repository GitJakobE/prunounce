# User Review Feedback

This folder holds persona-based review feedback for every major change to Pronuncia.

## Folder Structure

```
reviews/
  README.md              ← you are here
  _template.md           ← copy this to start a new review session
  YYYY-MM-DD-<slug>.md   ← one file per review session
```

## How It Works

1. **Copy** `_template.md` and name it `YYYY-MM-DD-<short-description>.md` (e.g. `2026-04-01-multilang-dictionary.md`).
2. **Fill in** the change summary at the top.
3. **Walk through** the change from each panellist's perspective, answering the three questions from the [User Review Panel](../user-review-panel.md#1-purpose).
4. **Tag** every finding as **blocker**, **significant**, or **minor**.
5. **Commit** the file and link it in the relevant PR or release notes.

## Severity Definitions

| Tag | Meaning | Release gate |
|---|---|---|
| **blocker** | Prevents a panellist from completing their primary goal | Must fix before release |
| **significant** | Degraded experience but a workaround exists | Scheduled for next iteration |
| **minor** | Cosmetic or low-impact issue | Added to backlog |

## Related Documents

- [User Review Panel](../user-review-panel.md) — persona definitions and coverage matrix
- [PRD](../prd.md) — product requirements
