# ADR-0019: GDPR Account Deletion — Cascade Delete with Contributed Word Preservation

- **Status:** Accepted
- **Date:** 2026-03-29
- **Deciders:** Development team
- **Requirements:** REQ-4 (User authentication — GDPR account deletion)

## Context and Problem Statement

GDPR requires that users can delete their account and all associated personal data (REQ-4, F-AUTH §3.6). At the same time, the application stores user-contributed words that are part of the shared dictionary (REQ-9). When a user deletes their account, the system must remove all personal data while preserving dictionary integrity — contributed words should remain available to other users but no longer be attributed to the deleted account.

The team needs to decide the cascade deletion strategy: what gets removed, what gets preserved, and how foreign key relationships handle the deletion.

## Decision Drivers

- GDPR compliance: all personal data (profile, preferences, progress) must be permanently removed on request
- Dictionary integrity: contributed words are shared community resources and should survive account deletion (F-AUTH §3.6, F-UGC)
- Single API call: the user must be able to delete their account from the profile/settings page with one confirmation step (F-AUTH §3.6)
- Data consistency: no orphaned records or broken foreign keys after deletion
- Simplicity: leverage database-level cascade rules rather than application-level multi-step cleanup

## Considered Options

### Option 1: Database cascade with SET NULL on contributed words — Chosen

Use SQLAlchemy/SQLite foreign key `ON DELETE` rules to handle all cleanup at the database level. `UserProgress` records are cascade-deleted. `Word.contributed_by` is set to NULL (word preserved, attribution removed). The application issues a single `db.delete(user)` call.

### Option 2: Application-level multi-step deletion

Explicitly delete each related record type in application code before deleting the user. More control over ordering and logging, but duplicates logic that the database can handle, risks partial deletion on error, and requires maintaining deletion logic when new related tables are added.

### Option 3: Soft delete (deactivate account)

Mark the user as deleted without removing the row. Preserves data for audit. However, GDPR requires actual data removal (not just deactivation), and retaining personal data in a "soft deleted" state still constitutes processing under GDPR.

### Option 4: Full cascade including contributed words

Delete everything — including contributed words — when the user is deleted. Simplest cascade rule. However, this damages the shared dictionary, removes words that other users may have listened to or rely on, and contradicts the F-AUTH §3.6 requirement that "the words themselves remain in the dictionary."

## Decision Outcome

**Chosen: Option 1 — Database cascade with SET NULL on contributed words**

### Foreign Key Configuration

| Relationship | FK Column | ON DELETE Rule | Effect |
|---|---|---|---|
| User → UserProgress | `UserProgress.userId` | `CASCADE` | Progress records deleted with user |
| User → Word (contributed) | `Word.contributedBy` | `SET NULL` | Word preserved, attribution cleared |

### Implementation

The deletion is a single endpoint: `DELETE /api/profile`

```python
@router.delete("")
def delete_profile(current_user: User = Depends(get_current_user), db=Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return {"message": "Account and all associated data deleted"}
```

SQLAlchemy model configuration:
- `User.progress` relationship has `cascade="all, delete-orphan"` — ORM-level cascade for `UserProgress`
- `Word.contributed_by` FK: `ForeignKey("User.id", ondelete="SET NULL")` — database-level SET NULL
- `UserProgress` FKs: `ForeignKey("User.id", ondelete="CASCADE")` and `ForeignKey("Word.id", ondelete="CASCADE")`

### What Gets Deleted

| Data | Deleted? | Mechanism |
|---|---|---|
| User row (email, password hash, display name, preferences) | Yes | Direct delete |
| UserProgress rows (listening history) | Yes | CASCADE |
| User's host selection and language preference | Yes | Part of User row |
| Contributed words | **No** — preserved | `SET NULL` on `contributedBy` |
| Cached TTS audio files for contributed words | **No** — preserved | Audio cache is word-keyed, not user-keyed |

### Consequences

**Positive:**
- GDPR-compliant: all personal data is permanently removed in a single transaction
- Dictionary integrity preserved: contributed words and their audio remain available to all users
- Single `db.delete()` call — minimal application code, maximum reliability
- Database-level cascade rules prevent orphaned records even if application logic changes
- No attribution trail: `contributed_by = NULL` provides clean anonymisation

**Negative:**
- If new user-related tables are added, their FK `ON DELETE` rules must be explicitly configured — forgetting to add cascade rules would leave orphaned data
- No audit log of what was deleted — if a deletion needs to be investigated, there is no record of what data existed (acceptable for v1; audit logging can be added)
- `SET NULL` means the `contributed_by` column must be nullable, which slightly reduces data model strictness

**Neutral:**
- Session/token invalidation happens implicitly: the JWT token references a user ID that no longer exists, so subsequent API calls will fail authentication naturally
- Front-end redirects to the login page after receiving the deletion confirmation response
