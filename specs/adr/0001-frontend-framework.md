# ADR-0001: Frontend Framework — React + Vite + Tailwind CSS

- **Status:** Accepted
- **Date:** 2026-03-16
- **Deciders:** Development team
- **Requirements:** REQ-1 (Multi-language support), REQ-2 (Dictionary browsing), REQ-5 (Word search), REQ-7 (Host personas)

## Context and Problem Statement

Pronuncia Italiana needs a responsive, single-page frontend that supports internationalisation, audio playback, real-time search, and component-based UI with host persona selection. The framework must enable fast development for a small team and produce a lightweight bundle for public deployment.

## Decision Drivers

- Component-based architecture for reusable UI elements (word cards, audio buttons, host selectors)
- First-class TypeScript support for type safety across the stack
- Rich ecosystem for i18n, routing, and testing
- Fast development feedback loop (hot module replacement)
- Small production bundle size for fast initial load
- Team familiarity and hiring availability

## Considered Options

### Option 1: React 19 + Vite 6 + Tailwind CSS 4 (Chosen)

React is the most widely adopted component framework. Vite provides near-instant HMR and fast builds via esbuild/Rollup. Tailwind CSS offers utility-first styling that eliminates CSS file proliferation and produces small, purged production bundles.

### Option 2: Next.js (App Router)

Full-featured React meta-framework with SSR, file-based routing, and API routes. Would consolidate frontend and backend into one project. However, the application is fully authenticated (no public SEO-critical pages), making SSR unnecessary overhead. The separate Express backend is already established.

### Option 3: Vue 3 + Vite

Vue offers a gentler learning curve and similar Vite integration. However, the React ecosystem has broader library support for i18n (react-i18next) and testing (@testing-library/react), and the team has stronger React experience.

### Option 4: Svelte / SvelteKit

Excellent performance and minimal bundle size. However, the ecosystem is smaller, particularly for i18n and component testing libraries. Higher risk for a project that needs established solutions.

## Decision Outcome

**Chosen: Option 1 — React 19 + Vite 6 + Tailwind CSS 4**

### Consequences

**Positive:**
- Vite delivers sub-second HMR and 7-second production builds (measured: 316 KB JS gzipped to 99 KB)
- react-i18next provides mature i18n with namespace support, fitting REQ-1
- React Router 7 handles client-side routing with protected routes for auth gating
- @testing-library/react enables component testing (13 tests passing)
- Tailwind CSS 4 produces a 23 KB CSS bundle with no unused styles
- Lucide React provides consistent, tree-shakeable icons

**Negative:**
- React 19's RSC features are unused since we're running client-only (no SSR)
- Tailwind's utility classes require familiarity; can produce verbose markup
- No SSR means the initial HTML is empty — acceptable since all content is behind authentication

**Neutral:**
- Vite's dev server proxies API requests to the Express backend on port 3001
- TypeScript 5.9 is shared across frontend and backend for consistency
