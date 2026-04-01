---
name: web-testing
description: End-to-end web testing with MCP Playwright tools for UI flows, regression checks, accessibility snapshots, console/network diagnostics, and reproducible bug reports. Keywords: playwright, e2e, browser automation, smoke test, regression, ui test, mcp_playwright.
---

# Web Testing with MCP Playwright

Use this skill when a task requires browser-based validation, user-flow testing, UI regression checks, or reproduction of frontend bugs with reliable evidence.

## Use This Skill For

- Verifying web app behavior in a real browser context.
- Reproducing frontend bugs with deterministic steps.
- Running smoke tests after UI changes.
- Checking console errors and failed network calls.
- Capturing accessibility snapshots and screenshots for evidence.

## Do Not Use This Skill For

- Pure backend/API testing with no browser interaction.
- Unit-test authoring inside framework test runners unless explicitly requested.
- Performance benchmarking beyond lightweight page-load and request sanity checks.

## Required MCP Tooling

Use MCP Playwright tools for browser automation:

- Navigation and interaction: `mcp_playwright_browser_navigate`, `mcp_playwright_browser_click`, `mcp_playwright_browser_type`, `mcp_playwright_browser_press_key`.
- Inspection and diagnostics: `mcp_playwright_browser_console_messages`, `mcp_playwright_browser_network_requests`, `mcp_playwright_browser_evaluate`.
- Stability helpers: `mcp_playwright_browser_wait_for`, `mcp_playwright_browser_tabs`, `mcp_playwright_browser_navigate_back`.
- Advanced/custom execution: `mcp_playwright_browser_run_code`.
- Visual capture (if needed): activate page capture tools and collect snapshot/screenshot.

If browser actions are unavailable, activate the relevant browser interaction/capture tool categories first.

## Standard Workflow

1. Define test objective and acceptance criteria.
2. Establish deterministic setup.
3. Execute primary user flow.
4. Validate expected outcomes.
5. Collect diagnostics when behavior differs.
6. Report result with reproducible evidence.

### 1) Define Objective

Record:

- URL/environment under test.
- Persona or auth state.
- Critical path (for example: login, search, checkout).
- Assertions that must pass (visible text, URL, element state, API call success).

### 2) Deterministic Setup

- Open the target page directly.
- If login is required, perform login once and confirm landing state.
- Prefer stable selectors and text-based roles over brittle visual anchors.
- Add explicit waits only for known async transitions.

### 3) Execute Flow

- Perform one atomic step at a time.
- After each critical interaction, assert state before moving on.
- For flaky UI transitions, wait for specific text or element visibility/disappearance.

### 4) Validate Outcomes

Minimum checks:

- Correct URL/route reached.
- Required UI text and controls present.
- No blocking console errors.
- No failed critical network requests.

### 5) Diagnostics and Branching

If a step fails:

- Capture console messages at `error` (or `warning`) level.
- Capture network requests and identify failed endpoints.
- Take accessibility snapshot and screenshot for UI-state proof.
- Retry once with targeted waits if failure appears timing-related.

Branching logic:

- If reproducible in two runs: classify as deterministic bug.
- If intermittent: classify as flaky; record suspected timing/source-of-truth issue.
- If environment-dependent: record env details and exact preconditions.

### 6) Completion Criteria

A test run is complete only when all are true:

- Pass/fail status for each acceptance criterion is explicit.
- Reproduction steps are numbered and complete.
- Evidence includes at least one of: snapshot, screenshot, console log, network trace summary.
- Next action is clear: fix required, test passed, or needs environment clarification.

## Reporting Template

Use this structure in responses:

- Objective: what was validated.
- Environment: URL, auth state, browser context.
- Steps executed: numbered sequence.
- Expected vs actual: concise diff.
- Evidence: console/network/snapshot highlights.
- Result: pass, fail, flaky, blocked.
- Next action: concrete recommendation.

## Example Prompts

- "Run a smoke test for login and dashboard navigation using MCP Playwright."
- "Reproduce the bug where search results disappear after filtering, then capture console and network evidence."
- "Validate checkout flow and report deterministic steps plus screenshot evidence if it fails."
- "Check if the profile save button works on mobile viewport and summarize pass/fail criteria."

## Quality Bar

- Reproducible steps over vague descriptions.
- Assertions tied to user-visible outcomes.
- Evidence-first bug reports.
- Minimal, purposeful waits to reduce false positives.
