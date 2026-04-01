# ADR-0021: Accessibility Testing Toolchain — axe-core + Manual Screen Reader Audit

- **Status:** Accepted
- **Date:** 2026-03-29
- **Deciders:** Development team
- **Requirements:** F-A11Y (Accessibility & Inclusive Design), PRD Scope (Responsive web design)

## Context and Problem Statement

The Accessibility FRD (F-A11Y) mandates WCAG 2.1 Level AA conformance across all pages and flows. The User Review Panel includes Farah, a low-vision user who relies on NVDA and VoiceOver, and whose persona walkthrough must pass with no blocker issues. The team needs to decide how to verify accessibility — balancing automated coverage (fast, repeatable, CI-friendly) with manual testing (catches dynamic, contextual, and assistive-technology issues that automation misses).

## Decision Drivers

- F-A11Y acceptance criteria require both automated checks (axe-core with zero violations) and manual screen-reader walkthroughs
- The frontend uses React + Tailwind (ADR-0001), which generates semantic HTML when done correctly but can easily produce inaccessible markup if components lack ARIA attributes
- Must integrate into the existing CI pipeline without adding significant build time
- Team has limited accessibility expertise — tooling should surface clear, actionable errors
- Farah's persona requires NVDA (Windows) and VoiceOver (macOS/iOS) compatibility

## Considered Options

### Option 1: axe-core (automated) + Manual Screen Reader Audit (Chosen)

Use `@axe-core/react` for development-time warnings, `axe-core` via Playwright in CI for automated regression checks, and a manual screen-reader walkthrough checklist for each major release.

### Option 2: pa11y CI Only

Run pa11y against rendered pages in CI. Simpler setup but less granular — pa11y runs against full pages, not individual component states, and does not catch issues in dynamic content (modals, live search results, language switching).

### Option 3: Lighthouse Accessibility Audit Only

Use Lighthouse CI's accessibility score with a threshold (e.g., ≥ 95). Lighthouse uses axe-core internally but provides less control over which rules are enforced and does not support component-level testing.

### Option 4: Full Manual Testing Only

Rely entirely on screen-reader walkthroughs. Thorough but not repeatable, not scalable, and regressions slip through between audits.

## Decision Outcome

**Chosen: Option 1 — axe-core (automated) + Manual Screen Reader Audit**

This combines the strengths of automation (fast, repeatable, catches regressions) with manual testing (catches real-world assistive technology issues).

### Implementation

| Layer | Tool | When | Purpose |
|---|---|---|---|
| Development | `@axe-core/react` | On every render in dev mode | Logs a11y violations to the browser console so developers catch issues as they build |
| CI — Component | `vitest-axe` (jest-axe for Vitest) | On every PR | Runs axe-core against rendered React components in unit/integration tests |
| CI — E2E | `@axe-core/playwright` | On every PR | Runs axe-core against full pages rendered by Playwright, including after dynamic interactions (search, language switch, modal open) |
| Pre-release | Manual NVDA + VoiceOver walkthrough | Before each major release | Farah persona walkthrough: login → host selection → browse → play word → search → contribute → progress |

### axe-core Configuration

- **Standard:** WCAG 2.1 Level AA (`wcag21aa` tag)
- **Threshold:** Zero violations in CI (any violation fails the build)
- **Excluded rules:** None at launch; if a rule produces false positives, it must be explicitly documented and tracked for resolution

### Manual Audit Checklist (per Farah Walkthrough)

1. Keyboard-only navigation through all core flows — no traps, logical focus order
2. Screen reader announces all interactive elements with meaningful labels
3. Dynamic content changes (search results, language switch, progress update) announced via live regions
4. Colour contrast verified on host accent banners and all button states
5. 200% zoom with no horizontal scrolling on 1280px viewport

### Consequences

**Positive:**
- Automated checks prevent accessibility regressions from merging
- Developer-time warnings reduce the cost of fixing issues (caught early)
- Manual walkthroughs catch real-world AT issues that automation cannot
- Zero-violation threshold creates a culture of accessibility by default

**Negative:**
- `@axe-core/react` adds a dev dependency and minor console noise in development
- Manual screen-reader testing requires time and some training
- axe-core catches ~57% of WCAG issues (per Deque's own data); manual testing is essential to cover the rest

**Neutral:**
- axe-core is already a transitive dependency of Playwright's accessibility testing utilities
- The manual checklist maps directly to the Farah persona walkthrough, so it doubles as a release gate
