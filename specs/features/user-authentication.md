# Feature Requirements Document — User Authentication

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-AUTH
**Requirement:** REQ-4
**Priority:** P0 (Must-have for launch)

## 1. Overview

Users must create an account and log in to access the application's content. Authentication enables the system to persist user preferences (host selection, target language, reference language), track progress (words listened to), and deliver personalised experiences. The login gate appears before any dictionary content is accessible.

## 2. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-AU1 | As a new visitor, I want to create an account with my email and password so I can access the site. | Registration form accepts email and password; account is created and user is logged in. |
| US-AU2 | As a registered user, I want to log in with my credentials so I can access my personalised experience. | Login form authenticates user and redirects to the host selection page (or main app if host already chosen). |
| US-AU3 | As a user, I want to stay logged in across visits so I don't have to re-enter credentials every time. | Sessions persist for a reasonable duration (e.g., 30 days) unless the user explicitly logs out. |
| US-AU4 | As a user, I want to log out when I choose to. | A logout option is available; clicking it ends the session and returns to the login page. |

## 3. Functional Requirements

### 3.1 Registration
- Users must provide a valid email address and a password to register.
- Password requirements: minimum 8 characters, at least one uppercase letter, one lowercase letter, and one digit.
- The system must validate that the email is not already registered.
- Upon successful registration, the user is logged in and directed to the host selection page.

### 3.2 Login
- Users log in with email and password.
- After successful login, the user is redirected to the host selection page (if no host chosen) or the main categories page (if host already saved).
- Failed login attempts must show a clear, non-specific error message (e.g., "Invalid email or password") to avoid revealing account existence.

### 3.3 Session Management
- Authenticated sessions must persist so users are not required to log in on every visit.
- Session duration should be configurable (suggested default: 30 days).
- Users must be able to explicitly log out, which ends the session immediately.

### 3.4 Access Control
- All dictionary content, search, contribution, and progress features must be behind the authentication gate.
- Unauthenticated users see only the login/registration page and a brief description of the application.

### 3.5 Profile
- Users must have a profile containing: email, display name (optional), reference language preference, and host selection.
- Users must be able to update their display name and reference language from a settings/profile page.
- Host selection is managed via the host selection UI (see [host-personas.md](host-personas.md)) and stored on the profile.

### 3.6 Account Deletion (GDPR)
- Users must be able to delete their account from the profile/settings page.
- Deleting an account must permanently remove all user data: profile, progress, preferences, contributed words' authorship (the words themselves remain in the dictionary but are no longer attributed), and any associated records.
- The system must ask for confirmation before proceeding with deletion.
- After deletion, the user's session must end and they must be redirected to the login page.

### 3.7 Login Rate Limiting
- The login endpoint must limit the rate of failed authentication attempts to mitigate brute-force attacks.
- After a configurable number of failed attempts (suggested: 5 within 15 minutes) for the same email, subsequent attempts must be temporarily blocked with a clear message (e.g., "Too many login attempts. Please try again in 15 minutes.").
- Rate limiting must not reveal whether the email exists.

### 3.8 Transport Security
- All API communication must occur over HTTPS in production.
- The application must redirect HTTP requests to HTTPS when deployed publicly.
- Cookies and tokens must only be transmitted over secure connections in production.

## 4. Edge Cases

- If a user tries to register with an already-registered email, display: "An account with this email already exists. Try logging in."
- If a user's session token expires while they are using the app, redirect to the login page with a message: "Your session has expired. Please log in again."
- If a user deletes their account, any words they contributed remain in the dictionary but are no longer attributed to them.

## 5. Acceptance Criteria

- [ ] Users can register with email and password.
- [ ] Password validation enforces minimum requirements.
- [ ] Users can log in and are directed to the host selection page (first time) or main app (returning).
- [ ] Sessions persist across browser sessions for at least 30 days.
- [ ] Users can log out, ending their session immediately.
- [ ] All content is gated behind authentication.
- [ ] Users can delete their account and all personal data (GDPR).
- [ ] Rate limiting blocks excessive failed login attempts.
- [ ] Profile stores email, display name, reference language, and host selection.

## 5. Acceptance Criteria

- [ ] Users can register with email and password.
- [ ] Users can log in with email/password or Google social login.
- [ ] Sessions persist across browser restarts (for at least 30 days with "remember me").
- [ ] Password reset flow works end-to-end via email.
- [ ] All content is gated behind authentication.
- [ ] Users can log out and are redirected to the login page.
- [ ] Passwords are never stored in plain text.
- [ ] Failed logins do not reveal whether the email exists.
- [ ] Users can delete their account and all associated data from the settings page.
- [ ] After account deletion, the user is logged out and all their data is removed.
- [ ] Failed login attempts are rate-limited to prevent brute-force attacks.
- [ ] The application uses HTTPS for all communication in production.
