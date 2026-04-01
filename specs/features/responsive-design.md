# Feature Requirements Document — Responsive Design & Mobile Usability

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-RESPONSIVE
**Priority:** P0 (Must-have for launch)
**Review Panel Personas:** Patrizia (Android phone), Thomas (one-handed mobile use), Aiden (laptop + phone)

---

## 1. Overview

Pronuncia must provide a complete, comfortable experience across mobile phones, tablets, and desktop screens. The product is web-only (no native apps), so responsive design is the sole mechanism for supporting the diverse devices used by its audience — from Patrizia's hand-me-down Android phone to Nikolaj's ultrawide gaming monitor. This FRD defines the layout expectations, breakpoints, and interaction standards that every page must meet.

## 2. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-R1 | As a mobile user, I want the entire app to be usable on my phone in portrait mode, so that I can learn pronunciation on the go. | All pages render without horizontal scrolling on a 360px-wide viewport. All features are accessible. |
| US-R2 | As a user with large fingers, I want touch targets to be large enough that I don't accidentally tap the wrong button. | All interactive elements (buttons, links, cards, play icons) meet a minimum touch target size of 44 × 44 px. |
| US-R3 | As a tablet user, I want the layout to take advantage of my wider screen without wasting space. | On tablet-size viewports (768px–1023px), cards and grids reflow to use the available width (e.g., 2–3 columns for word cards). |
| US-R4 | As a desktop user with a wide monitor, I want content to be centred and readable, not stretched edge-to-edge. | A maximum content width prevents content from spanning the full width of screens wider than ~1280px. |
| US-R5 | As a user who rotates my phone to landscape, I want the layout to adapt without breaking. | Orientation changes reflow content correctly with no overlapping elements or lost controls. |
| US-R6 | As Thomas, I want to use the app one-handed on my phone, so that I can look up a word while holding a coffee. | Primary actions (play audio, search, navigate categories) are reachable with a thumb in the lower two-thirds of the screen on mobile. |

## 3. Functional Requirements

### 3.1 Breakpoints

The layout must adapt at the following breakpoint thresholds:

| Label | Width range | Typical devices | Layout characteristics |
|---|---|---|---|
| **Mobile** | < 768px | Phones in portrait and landscape | Single-column layout. Stacked navigation. Full-width cards. Bottom-aligned or hamburger navigation. |
| **Tablet** | 768px – 1023px | Tablets, small laptops | Two-column card grids where appropriate. Side-by-side host cards in selection view. Visible top navigation. |
| **Desktop** | ≥ 1024px | Laptops, desktops, wide monitors | Multi-column grids (3–4 columns for word cards). Persistent sidebar or top navigation. Max content width of ~1200px, centred. |

### 3.2 Navigation

- On mobile, the primary navigation must collapse into a hamburger menu or bottom tab bar to save vertical space.
- On tablet and desktop, navigation labels must be visible without requiring a menu toggle.
- The host avatar / switcher control in the top-right corner must remain visible and tappable at all breakpoints.
- The reference-language switcher must be accessible at all breakpoints without excessive scrolling.

### 3.3 Host Selection Page

- On mobile, host cards must stack vertically, one per row, with portrait, name, and a short description visible without truncation.
- On tablet, host cards may display two per row within each language group.
- On desktop, all four hosts for a language may display in a single row.
- Language group headings ("Learn Italian", "Learn Danish", "Learn English") must be clearly visible and act as visual separators at all sizes.

### 3.4 Category & Word Browsing

- Category cards must reflow from a single column on mobile to two or three columns on tablet/desktop.
- Word cards within a category must reflow similarly: single column on mobile, multi-column on wider screens.
- The play button on each word card must be prominently visible and meet the 44 × 44 px minimum at all sizes.
- Progress indicators (e.g., "12 / 25 practised") must remain visible on category cards at all breakpoints, not hidden by truncation.

### 3.5 Search

- The search bar must be full-width on mobile and prominently placed (e.g., top of page or within a sticky header).
- Search results must display comfortably on mobile: word, translation, and play button visible without horizontal scrolling.
- On desktop, search may display inline results in a dropdown or a dedicated results area.

### 3.6 Word Contribution Form

- Form fields must stack vertically on mobile with full-width inputs.
- On tablet/desktop, optional fields may display side-by-side where space allows.
- The submit button must be easily reachable on mobile (not hidden below the fold on a typical phone screen after filling required fields).

### 3.7 Touch & Interaction

- All interactive elements must have a minimum touch target of 44 × 44 px on mobile and tablet.
- Spacing between adjacent touch targets must be sufficient to prevent accidental taps (minimum 8px gap).
- Hover-dependent interactions (tooltips, hover states) must have touch-friendly equivalents (e.g., tap to reveal, long-press).

### 3.8 Typography & Readability

- Base font size must be at least 16px on mobile to prevent iOS Safari forced zoom on input focus.
- Line lengths on desktop must not exceed ~75 characters for comfortable reading.
- Text must remain readable without zooming at all breakpoints.

## 4. Edge Cases

- Extremely long words (e.g., compound Danish words like "speciallægepraksisplanlægningsstabiliseringsperiode") must wrap or truncate gracefully with a tooltip or expandable area, rather than overflowing their container.
- If a user resizes their browser window across breakpoints, the layout must reflow without requiring a page reload.
- The host colour-accent banner must scale its text and image proportionally; it must not clip the host portrait on narrow screens.
- Landscape orientation on mobile must not hide critical controls behind the virtual keyboard when a text input is focused.

## 5. Dependencies

- Accessibility FRD (F-A11Y) — touch target sizes and focus indicators overlap; both must be met simultaneously.
- Host personas FRD (F-HOSTS) — host card layout and banner sizing are defined here but visual identity comes from F-HOSTS.
- Audio pronunciation FRD (F-AUDIO) — play button sizing and placement must conform to both responsive and accessibility requirements.

## 6. Acceptance Criteria

- [ ] All pages render without horizontal scrolling at 360px, 768px, 1024px, and 1440px viewport widths.
- [ ] All interactive elements meet the 44 × 44 px minimum touch target on mobile viewports.
- [ ] Navigation collapses to a mobile-friendly pattern (hamburger or bottom tabs) below 768px and shows full labels at 768px and above.
- [ ] Host selection page displays host cards in a sensible grid at each breakpoint (1 column mobile, 2 tablet, 4 desktop).
- [ ] Word and category cards reflow appropriately across breakpoints with no overlapping or clipped content.
- [ ] Content is centred with a max-width on viewports wider than 1280px.
- [ ] Orientation changes (portrait ↔ landscape) reflow correctly with no broken layout.
- [ ] The Thomas persona walkthrough (mobile, short sessions, one-handed) and Patrizia persona walkthrough (Android phone, first-time user) surface no blocker or significant issues.
