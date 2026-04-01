---
name: architecture-overview-updater
description: Maintain and update the project architecture overview by reconciling docs with actual code, agents, workflows, and platform setup. Keywords: architecture overview, documentation drift, system design, ADR alignment, docs refresh.
---

# Architecture Overview Updater

Use this skill to keep the project architecture overview accurate, concise, and aligned with the current repository state.

## What This Skill Produces

- Updated architecture overview content grounded in the codebase and docs.
- Explicit drift detection between documented and implemented architecture.
- Clear change summary and confidence notes (verified vs inferred).

## Use This Skill For

- Updating high-level architecture after structural repo changes.
- Refreshing docs after new agents, workflows, services, or runtimes are added.
- Aligning architecture docs with ADR decisions and current implementation.

## Do Not Use This Skill For

- Deep implementation planning or coding tasks.
- Performance tuning or incident root-cause investigations.
- Creating architecture from scratch without repository evidence.

## Primary Source Files (Prunounce)

Prioritize these sources in this order:

1. `docs/architecture.md` (canonical architecture overview).
2. `README.md` and `docs/index.md` (public orientation and topic map).
3. `docs/workflows.md` and `docs/specs-structure.md` (process and artifact structure).
4. `specs/adr/*.md` (architectural decision history).
5. Actual repo structure under `.github/`, `src/`, `scripts/`, `templates/` for verification.

## Workflow

1. Define update intent and scope.
2. Gather architecture facts from docs and codebase.
3. Detect documentation drift.
4. Decide update type and depth.
5. Apply updates to architecture overview.
6. Run quality checks and publish summary.

### 1) Define Intent and Scope

Capture:

- Why the overview is being updated (new component, changed flow, cleanup).
- Audience (new contributors, maintainers, stakeholders).
- Depth target (quick refresh vs full section rewrite).

### 2) Gather Architecture Facts

Collect only verifiable facts:

- Development environment and toolchain.
- Agent topology and responsibilities.
- Workflow stages and key artifacts.
- Runtime components and major source directories.
- External dependencies and integration points explicitly documented.

Mark each fact as:

- Verified in code/docs.
- Unverified if evidence is missing (treat as a gap, not a claim).

### 3) Detect Documentation Drift

Look for mismatches such as:

- Docs mention files/agents/components that no longer exist.
- New repo areas exist but are absent from architecture overview.
- Workflow docs contradict architecture claims.
- ADR decisions are not reflected in architecture narrative.

### 4) Decide Update Type

Branch based on drift size:

- Minor drift: wording updates, file/path references, small bullet changes.
- Moderate drift: update one or two sections (for example Agents or Workflows).
- Major drift: reframe overview structure and add explicit assumptions/unknowns.

If uncertainty remains high, prefer partial update with clearly labeled gaps over speculative edits.

Strictness rule:

- Do not publish inferred architecture statements as facts.
- If a fact cannot be verified from repository sources, record it under "Open Gaps" and request confirmation.
- Prefer omission plus explicit gap notes over guessing.

### 5) Apply Overview Updates

Default target file:

- `docs/architecture.md`

Update principles:

- Keep top-down structure: context -> key building blocks -> workflows -> boundaries.
- Prefer stable responsibilities over transient implementation details.
- Use short sections and concrete repository references.
- Keep terminology consistent with `README.md` and ADR naming.

### 6) Quality Checks

Completion requires all of the following:

- Every major claim traceable to a repository source.
- No stale references to removed files, tools, or agents.
- Architecture overview matches current workflow descriptions.
- New additions include scope boundaries and purpose.
- Summary clearly states what changed and why.

## Reporting Template

Use this structure when delivering results:

- Scope: what was updated.
- Sources consulted: key files used for verification.
- Drift found: concise list of mismatches.
- Changes made: section-by-section summary.
- Confidence: verified vs inferred notes.
- Follow-ups: unresolved ambiguities or recommended ADR/doc updates.

When strict mode is active, replace inferred notes with:

- Verified Facts: claims with source-backed evidence.
- Open Gaps: unknowns that require maintainer confirmation.

## Example Prompts

- "Update docs/architecture.md to reflect the current agent setup and workflow documentation."
- "Reconcile architecture overview with ADR files and list any drift you find."
- "Refresh architecture docs after adding new runtime components under src/."
- "Perform a minor architecture overview cleanup focused on stale references only."

## Quality Bar

- Evidence first, assumptions explicit.
- No speculative or inferred architecture claims presented as fact.
- Reader should understand the system in under 5 minutes.
- Output should reduce onboarding confusion, not add detail noise.
