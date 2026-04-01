# ADR-0014: GDPR Data Lifecycle — Hard Delete with Orphaned Content Retention

- **Status:** Accepted
- **Date:** 2026-03-29
- **Deciders:** Development team, Product owner
- **Requirements:** F-AUTH (User Authentication §3.6), REQ-4 (GDPR), PRD Constraint (GDPR compliance for EU users)

## Context and Problem Statement

The Authentication FRD (F-AUTH §3.6) requires that users can delete their accounts and all associated personal data. The PRD lists GDPR compliance as a constraint. When a user who has contributed words to the shared dictionary deletes their account, the team must decide what happens to their contributions — and more broadly, how to implement the "right to erasure" across all data types while preserving dictionary integrity.

## Decision Drivers

- GDPR Article 17 (Right to Erasure) requires deletion of personal data upon request
- User-contributed words are part of a shared dictionary used by all users — removing them would damage the learning experience for others
- The F-AUTH FRD states: "contributed words remain in the dictionary but are no longer attributed" after account deletion
- The system stores: user profile, authentication credentials, host/language preferences, progress records, and contribution authorship
- SQLite (ADR-0003) does not natively support cascading soft deletes — simplicity favours hard deletes
- The team does not want to build a complex audit/anonymization system for v1

## Considered Options

### Option 1: Hard Delete User + Orphan Contributions (Chosen)

Permanently delete the user record, credentials, preferences, and progress from the database. For contributed words, set `contributed_by` to `NULL` (orphan the content). The words themselves remain in the dictionary, playable and searchable, but no longer linked to any user.

### Option 2: Soft Delete with Anonymization

Mark the user as deleted (soft delete flag) but retain the record with anonymized fields (email → hash, display name → "Deleted User"). Contributed words retain the anonymized user reference. This preserves referential integrity but retains a data record, which may not satisfy strict GDPR interpretations.

### Option 3: Hard Delete Everything Including Contributions

Delete the user and all their contributed words. Fully satisfies erasure but degrades the dictionary for all other users and undermines the contribution incentive (goal G-5).

### Option 4: Data Export + Hard Delete

Provide a "Download my data" export (JSON) before deletion, then hard-delete everything. The export satisfies GDPR Article 20 (Right to Portability). This adds implementation cost for the export feature.

## Decision Outcome

**Chosen: Option 1 — Hard Delete User + Orphan Contributions**

This satisfies the right to erasure for all personal data while preserving the shared dictionary. Contributed words contain no personal data (they are language content), so retaining them with a `NULL` author does not violate GDPR.

### Deletion Scope

| Data type | Action on account deletion |
|---|---|
| **User record** (email, password hash, display name) | Hard delete |
| **Authentication tokens** | Invalidated (JWT becomes unverifiable after user record is deleted) |
| **Preferences** (host, target language, reference language) | Hard delete (stored on user record) |
| **Progress records** (words listened to) | Hard delete (cascade from user) |
| **Contributed words** | Retained; `contributed_by` set to `NULL` |
| **Contributed word audio cache** | Retained (shared asset, not personal data) |

### Implementation

1. User clicks "Delete my account" on the settings page
2. A confirmation dialog warns that the action is irreversible and explains that contributed words will remain anonymously
3. On confirmation, the backend:
   a. Sets `contributed_by = NULL` on all words where `contributed_by = user_id`
   b. Deletes all `UserProgress` rows for this user
   c. Deletes the `User` row (which includes profile, preferences, credentials)
4. The user's JWT is invalidated (the user record it references no longer exists)
5. The user is redirected to the login page

### Data Export (Deferred)

GDPR Article 20 (Data Portability) is not addressed at launch. If users request an export, it can be handled manually. A self-service export feature may be added in a future iteration.

### Consequences

**Positive:**
- Complete removal of personal data — satisfies right to erasure
- Dictionary content is preserved — no degradation for other users
- Simple implementation — no soft-delete flags, no anonymization logic
- JWT invalidation is automatic (no user record → token verification fails)

**Negative:**
- No self-service data export at launch (GDPR Article 20 deferred)
- Contributed words with `NULL` author cannot be retroactively attributed if the user changes their mind (deletion is irreversible)
- If contributed words contain personal data in the word itself (e.g., someone adds their own name), the word would not be deleted — mitigated by character validation (ADR-0013)

**Neutral:**
- The confirmation dialog and F-AUTH acceptance criteria already require clear communication about irreversibility
- The deletion operation is a single transaction — no partial states
