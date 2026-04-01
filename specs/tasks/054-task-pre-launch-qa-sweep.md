# Task 054: Pre-Launch QA — Responsive & axe-core Sweep

**Feature:** F-A11Y (Accessibility), F-RESPONSIVE (Responsive Design)
**Priority:** P1
**Dependencies:** 052 (Accessibility ARIA Polish — fixes should land before sweep)
**Review reference:** [2026-03-30 post-fix review](../reviews/2026-03-30-post-fix-review.md) — REM-4, REM-6
**ADRs:** ADR-0021 (Accessibility Testing)

## Problem

The 2026-03-30 review's accessibility and responsive verdicts are based on source-level code inspection and API probing only. Two verification steps remain:

1. **REM-4 — Responsive breakpoints:** The responsive layout has not been verified in a real browser at the three target breakpoints (375px mobile, 768px tablet, ≥1280px desktop). Horizontal scrolling, touch-target sizing, and layout integrity are unconfirmed.

2. **REM-6 — axe-core automated sweep:** axe-core has not been run against any page. While the source audit found no critical issues, an automated scan may catch colour-contrast problems, missing landmarks, or ordering issues that are invisible in code review.

## Requirements

### 1. axe-core automated scan (REM-6)

- Run `@axe-core/cli` or browser DevTools axe extension on every major page while authenticated:
  - `/login`
  - `/register`
  - `/select-host`
  - `/` (categories landing)
  - `/categories/:id` (word list with AudioButton)
  - `/search`
  - `/add-word`
  - `/profile`
  - `/stories`
  - `/stories/:id` (story reading view)
- Capture results per page
- **Pass threshold:** zero critical or serious violations
- Document any moderate/minor violations as known issues with a remediation plan

### 2. Responsive breakpoint verification (REM-4)

- Open every page listed above at three viewport widths:
  - **Mobile:** 375 × 812 (iPhone SE / small Android)
  - **Tablet:** 768 × 1024 (iPad portrait)
  - **Desktop:** 1280 × 800 (standard laptop)
- For each page × breakpoint, verify:
  - No horizontal scrollbar appears
  - All touch targets are ≥ 44 × 44px
  - Text is readable without zooming (≥ 16px body font)
  - Navigation is usable (hamburger menu on mobile if applicable)
  - Content does not overlap or get clipped
  - Images (host portraits) scale appropriately
- Document any failures with page name, breakpoint, and description

### 3. Keyboard navigation smoke test

- Tab through the full flow: login → select host → browse categories → open category → play audio → search → add word → profile → stories → read story
- Confirm every interactive element is reachable and activatable via keyboard
- Confirm visible focus indicator on all focusable elements
- Document any elements that are unreachable or lack focus indicators

## Acceptance Criteria

- [ ] axe-core scan completed on all 10 pages — zero critical or serious violations
- [ ] Responsive check completed at 3 breakpoints × 10 pages — no horizontal scroll, no clipped content
- [ ] All touch targets ≥ 44 × 44px at mobile breakpoint
- [ ] Keyboard-only walkthrough completes the full learning flow without mouse
- [ ] All findings documented with page, breakpoint/tool, severity, and description
- [ ] Any moderate axe-core violations documented with remediation plan
- [ ] QA report created at `specs/reviews/pre-launch-qa-report.md`

## Testing Requirements

- **axe-core:** Automated scan on 10 pages; capture JSON or screenshot results
- **Responsive:** Manual verification at 3 breakpoints; screenshots optional but recommended
- **Keyboard:** Full-flow walkthrough documented step-by-step
- **Regression:** No code changes expected from this task (QA only), but if fixes are needed, all existing tests must continue passing
- **Output:** `specs/reviews/pre-launch-qa-report.md` with pass/fail per page × check
