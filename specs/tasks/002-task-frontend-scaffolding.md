# Task 002: Frontend Scaffolding

**Feature:** Infrastructure / Scaffolding
**Priority:** P0
**Dependencies:** None (can be done in parallel with 001)
**ADRs:** ADR-0001 (React + Vite + Tailwind), ADR-0009 (Repo structure)

## Description

Set up the React/TypeScript frontend project with Vite, Tailwind CSS, routing, and internationalisation. Configure the Vite dev server to proxy API requests to the backend. Establish the component architecture and shared type definitions.

## Technical Requirements

- React 19 with TypeScript and Vite 6
- Tailwind CSS 4 with the `@tailwindcss/vite` plugin
- React Router 7 with route definitions for: `/login`, `/register`, `/` (categories), `/categories/:id`, `/search`, `/profile`
- i18next + react-i18next with translation files for English (`en.json`), Danish (`da.json`), and Italian (`it.json`) — all three languages required at scaffolding time
- Vite dev server proxy: `/api` → `http://localhost:8000` (FastAPI default port)
- Lucide React for icons
- Shared type definitions: `User`, `Host`, `WordEntry`, `Category`; `WordEntry` uses `word` field (not `italian`)
- API service module with `fetch`-based request helper including JWT-based Authorization header
- `.gitignore` excluding: `node_modules/`, `dist/`

### Component Architecture

- `AuthProvider` — React context for auth state (user, token, setAuth, logout)
- `ProtectedRoute` — Wrapper that redirects unauthenticated users to `/login`
- `Layout` — Shared layout with header, language switcher, navigation

## Acceptance Criteria

- [ ] `npm install` completes without errors in `src/frontend/`
- [ ] `npm run dev` starts the Vite dev server on port 5173
- [ ] API requests to `/api/*` are proxied to `http://localhost:3001`
- [ ] `npm run build` produces a production bundle without TypeScript errors
- [ ] i18next loads English and Danish translation files
- [ ] React Router renders the correct component for each route
- [ ] Tailwind CSS utility classes are applied and purged in production builds

## Testing Requirements

- Vitest configured with jsdom environment and `@testing-library/react`
- At least one smoke test: app renders without crashing
- i18n loads both language files successfully
