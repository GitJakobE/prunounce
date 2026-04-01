# Task 037: Accessibility & Responsive Audit — Multilang & UGC Pages

**Feature:** Cross-cutting (F-A11Y, F-RESPONSIVE)
**Priority:** P1
**Dependencies:** 015 (Responsive Design & Accessibility — initial pages), 024 (Host-First Landing), 025 (Frontend Multi-Language Dictionary), 026 (Frontend Word Contribution), 027 (Per-Language Progress Tracking)
**ADRs:** ADR-0001 (Frontend Framework), ADR-0021 (Accessibility Testing)

> **Scope:** This task extends the WCAG 2.1 Level AA compliance established in Task 015 to the pages added in the multilang expansion (Tasks 024–027). Story pages have their own accessibility task (036).

## Description

Audit and fix the host-selection landing page, multi-language dictionary views, word contribution form, and per-language progress summary to ensure they meet WCAG 2.1 Level AA accessibility requirements and are fully responsive across all three breakpoints defined in F-RESPONSIVE.

## Technical Requirements

### Pages in Scope

1. **Host Selection Landing** (`/select-host`, Task 024)
2. **Categories & Word Browsing** updated for multilang (`/categories`, `/categories/:id`, Task 025)
3. **Word Search** updated for multilang (`/search`, Task 025)
4. **Word Contribution Form** (`/contribute` or modal, Task 026)
5. **Profile & Progress** updated for per-language progress (Task 027)

---

### Responsive Layout

- **Host selection landing:**
  - Mobile (< 768px): 1-column host grid
  - Tablet (768px–1023px): 2-column host grid
  - Desktop (≥ 1024px): 4-column host grid (one column per language group)
  - Host cards must not overflow or truncate at any breakpoint
- **Category and word browsing:**
  - Dictionary views must reflow at all three breakpoints (same rules as Task 015)
  - Reference language selector must remain accessible and visible on all breakpoints
- **Word contribution form:**
  - All form fields stack vertically on mobile
  - Optional side-by-side layout on tablet/desktop where appropriate
  - Modal or page must not cause horizontal scroll on any viewport
- **Progress summary:**
  - Per-language progress tabs/pills must wrap gracefully on narrow screens
  - Progress bars remain readable at 360px viewport

### Accessibility

#### Host Selection Landing
- Each host card must be keyboard-focusable (Tab) and activatable (Enter / Space)
- Host portrait images must have descriptive `alt` text (e.g., `"Marco, Italian chef host"`)
- Focus moves to the first element of the /categories page after host selection
- Language section headings (`<h2>` or equivalent) must be present and correctly ordered
- ARIA live region announces the selected host name on selection

#### Category & Word Browsing (multilang)
- Reference language switcher must be keyboard-accessible and have a visible label
- Switching reference language must announce the change via an ARIA live region (`aria-live="polite"`)
- Word cards that show multilang translations must have the same `aria-label` pattern as Task 015
- Target language and reference language context must be communicated to screen readers (e.g., `<span class="sr-only">Target language: Italian</span>` in the header)

#### Word Contribution Form
- All form fields have visible `<label>` elements programmatically associated via `for`/`id`
- Required fields are marked `aria-required="true"` and with a visible indicator
- Validation errors communicated via `aria-describedby` linking to error message elements
- Duplicate-detection rejection must announce the error via an ARIA live region
- Success confirmation must be announced via an ARIA live region
- Form can be submitted with keyboard only (Enter on last field or explicit submit button)
- Cancel/dismiss action available via Escape key and a visible button

#### Progress Summary (per-language)
- Language tabs/pills controlling progress view must use `role="tab"` / `role="tabpanel"` pattern
- Active tab must have `aria-selected="true"`
- Progress bars must have `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, and an accessible label (e.g., `"Greetings: 12 of 25 practised"`)

### Colour Contrast
- All new UI elements introduced in Tasks 024–027 must meet WCAG AA:
  - 4.5:1 for normal text
  - 3:1 for large text (≥ 18pt / 14pt bold) and UI components
- Host colour accent banners must be tested against both text and icon colours rendered on them

### Reduced Motion
- Host card entry animations, progress bar fill animations, and form transition animations must respect `prefers-reduced-motion`

### Touch Targets
- All interactive elements in scope: minimum 44 × 44 px touch target with 8px minimum gap

---

## Acceptance Criteria

- [ ] Host selection page renders at 360px, 768px, 1024px, and 1440px widths without horizontal scroll
- [ ] Host cards are keyboard-navigable; Enter/Space triggers selection
- [ ] Host card `alt` text is descriptive for all 12 hosts
- [ ] ARIA live region announces selected host on selection
- [ ] Reference language switcher is keyboard-accessible and labelled
- [ ] Language switch announced to screen readers via live region
- [ ] Word contribution form has associated `<label>` for every field
- [ ] Validation errors are linked to fields via `aria-describedby`
- [ ] Duplicate-detection and success states announced via live regions
- [ ] Progress tabs/pills use `role="tab"` / `role="tabpanel"` pattern with `aria-selected`
- [ ] Progress bars have `role="progressbar"` with numeric value attributes
- [ ] All new UI passes axe-core scan with zero violations
- [ ] All new UI passes WCAG AA colour contrast check
- [ ] `prefers-reduced-motion` disables entry and fill animations
- [ ] All interactive elements meet 44 × 44 px touch target with 8px gap

## Testing Requirements

- **Automated:** Run `@axe-core/react` checks on Host Selection, Category, Search, Contribution Form, and Progress pages; zero violations
- **Keyboard:** Tab through all focusable elements on each page; verify logical order, visible focus indicators, and Escape closes modals/forms
- **Screen reader (NVDA or VoiceOver):** Verify live regions, progress bar labels, tab panel announcements, and host card alt text
- **Visual inspection:** Host grid at 360px / 768px / 1024px / 1440px; contribution form at 360px; progress at 360px
- **Contrast audit:** Lighthouse or axe colour contrast check on host accent banners, word cards, and progress indicators
- Coverage: these pages must be included in the global ≥ 85% test coverage target
