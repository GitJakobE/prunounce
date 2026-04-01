# Task 012: Frontend Profile & Account Management

**Feature:** F-AUTH (Profile, GDPR), F-HOST (Host Persona persistence)
**Priority:** P1
**Dependencies:** 002 (Frontend Scaffolding), 007 (Backend Profile & Hosts API)
**ADRs:** ADR-0004 (Authentication)

## Description

Implement the profile/settings page where users can view their progress, update their display name and language preference, change their host persona, and delete their account (GDPR compliance).

## Technical Requirements

### Profile Page (`/profile`)

- Display user information: email (read-only), display name (editable), language preference (selectable)
- Progress summary: total words listened, overall completion percentage
- Language selector: dropdown or toggle for English/Danish, updates profile via PATCH and changes i18next language
- Display name: editable text field, saves on blur or submit
- Host persona selection (can reuse HostSelector component or provide a simpler selector)

### Account Deletion

- "Delete account" button with red/destructive styling
- Confirmation dialog before deletion: "Are you sure? This will permanently delete your account and all your data."
- On confirmation: call `DELETE /api/profile`
- On success: clear auth state, redirect to `/login`

### Save Behaviour

- Profile updates call `PATCH /api/profile` with changed fields
- Show success/error feedback after save
- Language change updates i18next immediately (no page reload)

## Acceptance Criteria

- [ ] Profile page displays user email and display name
- [ ] Display name can be updated and saved
- [ ] Language can be changed and is persisted
- [ ] Language change updates all UI text immediately
- [ ] Progress summary shows words listened count
- [ ] "Delete account" button is visible
- [ ] Delete requires confirmation before proceeding
- [ ] After deletion, user is logged out and redirected to login
- [ ] Profile changes show success feedback

## Testing Requirements

- Profile page renders user information
- Profile page shows progress stats
- Delete button triggers confirmation dialog
- Profile update calls the API with correct fields
