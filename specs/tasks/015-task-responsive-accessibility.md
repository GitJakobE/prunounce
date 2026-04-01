# Task 015: Responsive Design & Accessibility

**Feature:** Cross-cutting (F-A11Y, F-RESPONSIVE)
**Priority:** P1
**Dependencies:** 008 (Frontend Auth), 009 (Frontend Categories), 010 (Frontend Audio), 011 (Frontend Search), 012 (Frontend Profile)
**ADRs:** ADR-0001 (Frontend Framework), ADR-0021 (Accessibility Testing)

> **Scope note:** This task covers the initial page set (auth, categories, audio, search, profile). Multilang/UGC pages (Tasks 024–027) are covered by Task 037. Story pages are covered by Task 036.

## Description

Ensure the application's initial pages are fully responsive across mobile, tablet, and desktop viewports, and meet WCAG 2.1 Level AA accessibility requirements per F-A11Y and F-RESPONSIVE. Audio play buttons must have appropriate accessible labels, touch targets must meet minimum size, colour contrast must pass AA, and dynamic content must be announced via ARIA live regions.

## Technical Requirements

### Responsive Layout

- **Mobile** (< 768px): single-column layout. Category grid stacks vertically. Word cards full-width. Navigation collapses to hamburger/bottom nav.
- **Tablet** (768px–1023px): two-column category grid. Word cards in compact layout. Top navigation visible.
- **Desktop** (≥ 1024px): multi-column grid (3–4) for categories. Persistent sidebar navigation where appropriate. Max-width ~1200px centred.
- Login/registration pages: full-width form on mobile, split layout (decorative panel + form) on desktop

### Accessibility

- All interactive elements must be keyboard-focusable and operable (Tab / Shift+Tab / Enter / Space)
- Skip-to-main-content link on every page
- Audio play buttons: `aria-label="Play pronunciation of {word}"` and `aria-label="Play example sentence for {word}"`
- Touch targets: minimum 44 × 44 px, minimum 8px gap between targets
- Colour contrast: WCAG AA — 4.5:1 for normal text, 3:1 for large text and UI components
- Language switcher and logout are accessible via keyboard
- Focus management: after login/logout, focus moves to first heading or primary content
- No autoplay audio on page load
- ARIA live regions announce search results, progress updates, and form success/error messages
- Decorative images use `alt=""`; informative images have descriptive alt text
- Layout reflows at 200% zoom without horizontal scrolling on 1280px viewport
- Respect `prefers-reduced-motion`: disable animations when set

### Mobile Audio

- Audio playback must work on iOS Safari (may require user gesture to unlock audio context)
- Audio playback must work on Android Chrome
- Audio button must be easy to tap on mobile (sufficient padding)

## Acceptance Criteria

- [ ] Categories page renders correctly at 375px, 768px, and 1280px widths
- [ ] Login/register pages are usable on a mobile viewport
- [ ] Word cards are readable and tappable on mobile
- [ ] Audio play buttons meet 44px minimum touch target
- [ ] All buttons and links have accessible labels
- [ ] Keyboard navigation works for all interactive elements
- [ ] Audio plays on iOS Safari and Android Chrome
- [ ] No horizontal scroll on any page at mobile widths

## Testing Requirements

- Visual inspection at mobile, tablet, and desktop breakpoints (manual or snapshot)
- Accessibility audit with browser dev tools (Lighthouse or axe)
- Audio button has correct aria-label
- Touch target sizes meet minimum threshold
