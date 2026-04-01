# Task 051: Dialogue & Content QA Integration Testing

**Feature:** F-DIALOGUE, F-CONTENT-QA
**Priority:** P1
**Dependencies:** 043 (Seed Data Rewrite), 044 (Backend Dialogue API), 045 (Frontend Dialogue Rendering), 046 (Dialogue TTS Narration), 047 (Content Validation Script), 048 (ContentReport API), 049 (Frontend Error Reporting), 050 (Content Review Dashboard)

## Description

End-to-end integration testing covering the dialogue story pipeline (data → API → frontend → narration) and the content quality assurance workflow (validation script → error reporting → review dashboard). This task ensures all components work together correctly and that the overall user experience is cohesive.

## Technical Requirements

### Dialogue Story E2E Tests

1. **Data → API → Frontend pipeline**
   - Seed a dialogue story with known speakers and body content
   - Fetch via story list API → verify `format`, `speakers` fields present
   - Fetch via story detail API → verify `segments` array has correct structure
   - Render the story reading page → verify speaker labels and dialogue layout
   - Click a word in a dialogue line → verify translation panel opens with correct lookup

2. **Narration pipeline**
   - Request narration audio for a dialogue story at each speed
   - Verify audio is generated and returned as MP3
   - Play audio and verify karaoke highlighting moves through dialogue turns
   - Verify pauses are present between speaker turns in the audio

3. **Mixed content handling**
   - Seed a mixed story (narrative paragraphs + dialogue sections)
   - Verify API returns correct segment types in order
   - Verify frontend renders narrative paragraphs and dialogue differently
   - Verify narration handles transitions between narration and dialogue

4. **Backward compatibility**
   - Verify that a narrative-format story (no dialogue) still renders correctly
   - Verify existing story list and detail API contracts are not broken
   - Verify existing narration functionality works for narrative stories

### Content QA E2E Tests

5. **Validation script integration**
   - Run the validation script against the full seed data set
   - Verify the script completes without unhandled errors
   - If errors are found, verify they match known issues in the seed data
   - Verify `--json` output is valid JSON and matches the expected schema
   - Verify `--stories-only` and `--words-only` flags filter correctly

6. **Error reporting flow**
   - Log in as a user, navigate to a story, click the report button
   - Submit a report with category "grammar_spelling" and a description
   - Verify the report is created (check via GET /api/reports)
   - Attempt to submit a duplicate report for the same item → verify rejection
   - Navigate to a word, click the report button on the translation panel
   - Submit a word report → verify creation

7. **Review workflow**
   - Open the review dashboard → verify submitted reports appear
   - Filter by status "new" → verify correct reports shown
   - Click a report → verify details are displayed
   - Resolve the report with a note → verify status update
   - Verify the report count decreases in the "new" filter

8. **Cross-feature interaction**
   - Submit a report on a dialogue story → verify the report captures the story ID correctly
   - Run the validation script on a story that has reports → verify the script operates independently of reports (validation and reporting are separate concerns)

### Accessibility Tests

9. **Dialogue accessibility**
   - Verify screen reader announces speaker names with their dialogue text
   - Verify keyboard navigation through dialogue turns follows reading order
   - Verify colour coding meets WCAG AA contrast requirements

10. **Reporting accessibility**
    - Verify report form is fully keyboard-navigable
    - Verify toast notifications are announced to screen readers
    - Verify review dashboard is navigable with keyboard and screen reader

### Performance Tests

11. **Validation script performance**
    - Verify the script completes validation of all 27 stories and full word dictionary within a reasonable time (< 30 seconds)

12. **Dialogue rendering performance**
    - Verify advanced-difficulty dialogue stories (300–600 words) render without perceptible lag
    - Verify word click response time is < 200ms on dialogue stories

## Acceptance Criteria

- [ ] All dialogue E2E tests pass: data → API → frontend → narration
- [ ] Mixed content stories render correctly end-to-end
- [ ] Narrative stories remain fully functional (backward compatibility)
- [ ] Validation script runs successfully against full seed data
- [ ] Error reporting flow works: report → list → resolve
- [ ] Review dashboard correctly reflects report lifecycle
- [ ] Duplicate report prevention works
- [ ] Accessibility tests pass for dialogue and reporting features
- [ ] Performance is acceptable for dialogue rendering and validation script

## Testing Requirements

- At least 3 E2E test scenarios for the dialogue pipeline
- At least 3 E2E test scenarios for the reporting workflow
- Backward compatibility regression tests for existing story functionality
- Accessibility audit using axe-core or equivalent
- All tests documented with clear steps and expected outcomes
