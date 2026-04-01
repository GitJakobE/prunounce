# Task 008: Frontend Authentication Pages

**Feature:** F-AUTH (User Authentication)
**Priority:** P0
**Dependencies:** 002 (Frontend Scaffolding), 004 (Backend Auth API)
**ADRs:** ADR-0004 (Authentication), ADR-0001 (Frontend Framework)

## Description

Implement the login and registration pages, the AuthProvider context, and the protected route wrapper. Users must be able to register, log in (email/password and Google), and be redirected to the main application. All content routes must be gated behind the ProtectedRoute wrapper.

## Technical Requirements

### AuthProvider

- React context providing: `user`, `token`, `loading`, `setAuth(token, user)`, `logout()`
- Store JWT in localStorage; restore on page load via `GET /api/auth/me`
- Apply the user's language preference to i18next on login
- Clear token and user state on logout

### Login Page (`/login`)

- Email and password input fields with form validation
- "Invalid email or password" error message on failure (non-specific)
- Link to registration page
- On success: store token, redirect to `/`
- Optional: Google social login button

### Registration Page (`/register`)

- Email, password, optional display name, language selector inputs
- Password strength validation (min 8 chars, uppercase, lowercase, digit) with client-side feedback
- Duplicate email error handling
- On success: store token, redirect to `/`
- Link to login page

### ProtectedRoute

- Wrapper component that checks for authentication
- Redirects to `/login` if no valid token/user
- Shows a loading state while restoring session from `GET /api/auth/me`

### Layout

- Shared layout component with header containing: app title, language switcher, profile link, logout button
- Language switcher accessible from every page (header)

## Acceptance Criteria

- [ ] Login page renders with email and password fields
- [ ] Login submits credentials and stores the JWT on success
- [ ] Login shows a non-specific error on failure
- [ ] Registration page renders with all required fields
- [ ] Registration validates password strength
- [ ] Registration shows errors for duplicate emails
- [ ] Registration stores the JWT and redirects on success
- [ ] ProtectedRoute redirects unauthenticated users to `/login`
- [ ] ProtectedRoute shows a loading state while restoring session
- [ ] Layout renders language switcher in the header
- [ ] Switching language updates all UI text without page reload
- [ ] Logout clears the token and redirects to `/login`

## Testing Requirements

- Login page renders all form elements
- Login form calls the API and navigates on success
- Login form shows error message on failure
- Registration page renders all form elements
- ProtectedRoute redirects when unauthenticated
- Language switcher toggles between English and Danish
- Logout clears auth state
