# Task 050: Content Review Dashboard

**Feature:** F-CONTENT-QA (Content Quality Assurance)
**Priority:** P2
**Dependencies:** 048 (ContentReport Data Model & API), 008 (Frontend Auth)

## Description

Build a review dashboard page where content reviewers can triage, investigate, and resolve error reports submitted by learners. The dashboard lists all pending reports with filtering and sorting, and allows reviewers to update report status and add resolution notes.

## Technical Requirements

### Dashboard Page

- Route: `/admin/reports` (or `/review/reports`)
- Accessible to all authenticated users (no separate admin role at this stage — community trust model)
- Page displays a table/list of content reports fetched from `GET /api/reports`

### Report List View

- Table columns:
  - **Content** — The reported item: story title (linked to the story) or word text (linked to the word)
  - **Type** — "Story" or "Word" icon/badge
  - **Category** — Error category (Grammar / Spelling, Wrong Translation, etc.)
  - **Reports** — Number of total reports for the same content item (aggregated)
  - **Description** — Truncated reporter description (expandable)
  - **Status** — Current status badge (New, Reviewed, Resolved, Dismissed)
  - **Date** — When the report was submitted (relative time, e.g., "2 hours ago")
- Default sort: newest first
- Alternative sort options: by report count (most reported items first), by status

### Filtering

- **Status filter** — Tabs or dropdown: All, New, Reviewed, Resolved, Dismissed
- **Content type filter** — Toggle: Stories, Words, All
- **Category filter** — Dropdown: All categories, Grammar / Spelling, Wrong Translation, etc.
- **Language filter** — Dropdown: All, Italian, Danish, English (derived from the reported content's language)
- Filters combine with AND logic
- Default view: status = "New" (show issues that need attention)

### Report Detail / Actions

- Clicking a report row expands it or opens a detail panel showing:
  - Full reporter description
  - The reported content (story excerpt or word details)
  - Report metadata (reporter, date, status history)
- Action buttons:
  - **Mark as Reviewed** — sets status to `"reviewed"` (acknowledging the issue)
  - **Resolve** — sets status to `"resolved"`, prompts for an optional resolution note
  - **Dismiss** — sets status to `"dismissed"`, prompts for an optional reason
- Actions call `PATCH /api/reports/{id}` with the new status and note

### Pagination

- Show 20 reports per page by default
- Pagination controls at the bottom (previous/next or page numbers)
- Total count displayed (e.g., "Showing 1–20 of 45 reports")

### Navigation

- Add a link to the review dashboard in the app's navigation or settings area
- The link should show a badge with the count of "new" reports (if any)

### Responsive Layout

- Desktop: full table with all columns visible
- Mobile: condensed card view with key info (content, category, status, report count)

### i18n

Add translatable strings for:
- Page title ("Content Review")
- Filter labels
- Status labels (New, Reviewed, Resolved, Dismissed)
- Category labels
- Action button labels (Review, Resolve, Dismiss)
- Pagination text
- Empty state message

## Acceptance Criteria

- [ ] Dashboard page accessible at specified route
- [ ] Report list shows all reports with correct columns
- [ ] Filtering by status, content type, category, and language works
- [ ] Sorting by date and report count works
- [ ] Clicking a report shows full details
- [ ] Mark as Reviewed, Resolve, and Dismiss actions update report status
- [ ] Resolution note is captured when resolving or dismissing
- [ ] Report count per content item is displayed
- [ ] Pagination works correctly
- [ ] Navigation link shows badge with new report count
- [ ] Layout is responsive (table on desktop, cards on mobile)
- [ ] All strings are translated via i18next

## Testing Requirements

- Dashboard loads and displays reports from the API
- Status filter shows only reports with selected status
- Content type filter correctly limits to stories or words
- Category filter limits to selected category
- Language filter limits to selected language
- Resolve action sends PATCH with "resolved" status and note
- Dismiss action sends PATCH with "dismissed" status
- Pagination displays correct page and total count
- Empty state shown when no reports match filters
- Navigation badge reflects count of "new" reports
