---
name: browser-bug-triage
description: Triage frontend bugs with MCP Playwright using console logs, network analysis, DOM state checks, reproducibility testing, and root-cause classification. Keywords: bug triage, playwright, console errors, network failures, frontend diagnostics, flaky test, regression.
---

# Browser Bug Triage with MCP Playwright

Use this skill to investigate, classify, and report browser-visible issues with reproducible evidence and a likely root-cause category.

## Outcomes

- Reproduce or disprove a reported browser bug.
- Collect objective evidence from console, network, and UI state.
- Classify the issue into a root-cause bucket.
- Produce a concise, developer-ready triage report.

## Use This Skill For

- "It is broken in the browser" reports with unclear cause.
- UI regressions after frontend or API changes.
- Intermittent failures that may be flaky or timing-related.
- Issues where screenshots alone are insufficient.

## Do Not Use This Skill For

- Non-browser backend failures already reproducible via API tests only.
- Deep performance profiling (use dedicated performance tooling).
- Security penetration testing.

## Core MCP Playwright Tools

Primary tools:

- `mcp_playwright_browser_navigate`
- `mcp_playwright_browser_snapshot`
- `mcp_playwright_browser_click`
- `mcp_playwright_browser_type`
- `mcp_playwright_browser_wait_for`
- `mcp_playwright_browser_console_messages`
- `mcp_playwright_browser_network_requests`
- `mcp_playwright_browser_evaluate`

Optional tools:

- `mcp_playwright_browser_screenshot`
- `mcp_playwright_browser_tabs`
- `mcp_playwright_browser_navigate_back`
- `mcp_playwright_browser_run_code`

If tools are unavailable, activate browser interaction and page capture tool groups before triage.

## Triage Workflow

1. Normalize the bug report.
2. Reproduce with minimal steps.
3. Capture first-pass diagnostics.
4. Isolate likely failure layer.
5. Re-run for confidence and flake check.
6. Classify root cause and recommend next action.

## Repository-Specific Triage Profiles (Prunounce)

Use these flow profiles first when the report is ambiguous.

### Auth and Profile Flow

- Start logged out and navigate to authentication.
- Verify login success state (user-facing profile/account context appears).
- Reproduce issue in profile update path (for example, saving user info or preferences).
- Capture console and API evidence for auth tokens/session/cookie-related failures.

### Dictionary and Search Flow

- Select language context first (for example Danish, English, Italian) before search assertions.
- Reproduce via category browse and direct search.
- Validate that results list, word detail, and example sentences agree with selected language.
- If empty results appear, compare request parameters against UI language and query state.

### Pronunciation Audio Flow

- Reproduce from word detail where audio playback is triggered.
- Capture behavior for first play, repeated play, and rapid repeated clicks.
- If playback fails silently, check console errors and audio request failures.
- Record whether issue affects one language only or all languages.

### Host Persona and Landing Flow

- Reproduce issue from host-first landing path before navigating deeper.
- Confirm selected host/persona persists through navigation where expected.
- Capture mismatches between displayed host UI and fetched content/audio source.

### 1) Normalize the Bug Report

Extract and restate:

- Exact page/URL.
- User state (logged in/out, role, locale).
- Trigger action.
- Expected result.
- Actual result.
- Frequency (always/sometimes/unknown).

If required data is missing, state assumptions explicitly in the report.

### 2) Reproduce with Minimal Steps

- Start from a stable entry point (direct URL when possible).
- Execute shortest path to failure.
- Keep a numbered sequence of steps.
- Stop adding new variables until baseline behavior is confirmed.

### 3) Capture First-Pass Diagnostics

Immediately after failure (or unexpected behavior), collect:

- Console messages at `error` level, then `warning` if needed.
- Network requests with failed status or obvious payload issues.
- Accessibility snapshot of current UI state.
- Screenshot only when visual state is relevant.

### 4) Isolate Failure Layer

Use evidence to map the issue:

- UI-only layer: incorrect rendering/state despite healthy API responses.
- Data/API layer: failed requests, invalid payloads, auth/permission failures.
- Timing/race layer: state updates out-of-order, intermittent visibility, async lag.
- Environment/config layer: locale, feature flags, base URL, cookie/session differences.

Quick checks:

- Compare failing request to expected endpoint and status.
- Inspect key DOM values via evaluate when text/UI is ambiguous.
- Retry once with precise wait condition to test timing suspicion.

### 5) Confidence and Flakiness Check

Run the same repro flow twice more:

- 3 out of 3 fails: deterministic defect.
- Mixed pass/fail with same steps: flaky/intermittent.
- Fails only with a specific precondition: environment-dependent.

### 6) Classify and Recommend

Classify into one primary bucket:

- `frontend-state-bug`
- `api-contract-or-backend-error`
- `auth-or-permission-issue`
- `race-condition-or-flake`
- `environment-or-config-mismatch`
- `cannot-reproduce`

Attach one immediate recommendation:

- Owning team suggestion.
- Most likely fix location (UI component, API route, auth middleware, config).
- Additional data needed if blocked.

## Completion Criteria

Triage is complete only when all are true:

- Reproduction status is explicit (reproduced/cannot reproduce/flaky).
- Numbered repro steps are present.
- Evidence includes console or network details, plus UI state artifact when needed.
- Root-cause category is assigned.
- Next action is actionable and specific.

## Report Template

Use this output format:

- Summary: one-line issue statement.
- Repro Status: reproduced, flaky, cannot reproduce.
- Environment: URL, auth state, locale, relevant flags.
- Steps: numbered exact sequence.
- Expected vs Actual: concise behavior delta.
- Evidence:
- Console: key errors/warnings.
- Network: failed/suspicious requests and statuses.
- UI State: snapshot/screenshot notes.
- Root-Cause Category: one bucket from taxonomy.
- Recommendation: owner plus immediate next fix step.

## Example Prompts

- "Triage why profile save fails after login and classify whether it is auth, API, or frontend state."
- "Investigate dictionary search returning no words in Italian and report UI vs API evidence."
- "Reproduce pronunciation audio not playing on a word detail page and determine if it is deterministic or flaky."
- "Analyze host-first landing showing the wrong persona after navigation and classify the root cause."

## Quality Bar

- No vague conclusions without evidence.
- Clear separation between facts, assumptions, and hypotheses.
- Single primary root-cause category to reduce ambiguity.
- Actionable recommendation that a dev can pick up immediately.
