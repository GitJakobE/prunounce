# 0024 seeded-audio-generation-strategy

**Date**: 2026-03-30
**Status**: Accepted

## Context

The product requires dictionary pronunciation audio to feel instant for learners and to remain replayable without repeated TTS work. The current architecture already caches generated audio files per host voice, but the runtime path still allows first-click generation for curated dictionary content. In practice, this pushes TTS latency into the core learning interaction for categories and word cards.

This is at odds with the product requirements and feature specifications:
- F-AUDIO requires playback to start within 1 second and states that repeated playback should not trigger new TTS generation.
- F-EXAMPLES states that both the word clip and example-sentence clip are pre-generated and cached.
- ADR-0007 already assumes static audio files are served from a file cache.
- ADR-0017 established an idempotent seeding model for curated dictionary content, which makes build-time or post-seed audio generation feasible.

At the same time, REQ-9 and the user-contributed words feature require new words to become playable shortly after submission, which means the system still needs a runtime generation path for dynamic content.

## Decision Drivers

- Sub-1-second perceived latency for the core dictionary playback flow
- Curated dictionary data is seeded, stable, and changes infrequently
- Example sentence audio is part of the normal playback chain and should not add first-use latency
- User-contributed words require runtime generation after submission
- Operational simplicity for v1 should be preserved; no new mandatory cloud infrastructure should be required
- Re-running seed and backfill jobs must remain safe and idempotent
- Existing per-host voice cache keys and file-serving model should remain valid

## Considered Options

### Option 1: Fully lazy generation on first request
**Description**: Keep the current cache-aside approach for all word and example audio. Generate a clip the first time a user requests it, then cache it for later requests.

**Pros**:
- Minimal up-front processing time during seed or deploy
- No storage spent on clips that are never played
- Simple to reason about for newly added words

**Cons**:
- First-click latency remains user-visible for curated content
- Example playback chains inherit generation delays and can feel broken
- Core learning flow depends on live TTS availability at click time

### Option 2: Fully pre-generate all audio and remove runtime generation
**Description**: Generate all word and example audio ahead of time for all hosts and require the cache to be complete before any word becomes playable.

**Pros**:
- Best and most predictable playback latency for curated content
- No TTS dependency in the runtime request path for dictionary playback
- Easier to measure cache coverage operationally

**Cons**:
- Incompatible with user-contributed words and other dynamic additions unless a separate workflow is built first
- Missing or invalidated assets would become hard failures rather than recoverable misses
- Makes the system less resilient during migrations, reseeds, or voice changes

### Option 3: Hybrid strategy - pre-generate seeded audio, keep lazy fallback for dynamic content and repairs
**Description**: Pre-generate all curated dictionary word and example audio for every supported host after content seeding or during deployment. Retain runtime generation only for user-contributed words, cache misses, and repair scenarios.

**Pros**:
- Removes first-click latency from the main dictionary experience
- Preserves flexibility for user-contributed words and future dynamic content
- Fits the existing seeded-data workflow and file-cache delivery model
- Allows gradual operational hardening without blocking launch on new infrastructure

**Cons**:
- Requires a backfill job or script and deploy-time operational discipline
- Increases total storage used by the audio cache
- Still leaves a smaller runtime generation path to maintain

### Option 4: Queue-backed asynchronous generation for every miss
**Description**: When a requested clip is missing, enqueue generation work and return a pending response. Playback becomes available only after a background worker completes the job.

**Pros**:
- Removes expensive TTS work from the request thread
- Scales better than synchronous request-time generation if misses spike
- Aligns well with background-job and queue-based processing patterns

**Cons**:
- Adds queueing, worker, status-tracking, and retry infrastructure
- More operational complexity than the project currently needs
- Still provides a degraded first-use experience unless curated content is pre-generated anyway

## Decision Outcome

**Chosen Option**: Option 3 - Hybrid strategy - pre-generate seeded audio, keep lazy fallback for dynamic content and repairs

**Rationale**:
- Curated dictionary audio is a mostly static, expensive-to-construct asset. Microsoft caching guidance recommends prepopulating caches for static or infrequently changing data when it reduces demand on expensive runtime paths.
- Background-job guidance recommends moving batch-style, I/O-intensive work off the interactive request path when the UI should not wait for completion.
- This hybrid model best matches the product split between seeded dictionary content and user-contributed content.
- It preserves the existing local file-cache architecture from ADR-0007 and provider model from ADR-0016 while eliminating the most visible runtime latency problem.
- It avoids introducing queues or new cloud services as a prerequisite for launch.

## Consequences

### Positive
- Curated category and dictionary playback no longer depends on first-click TTS generation
- Word-plus-example playback becomes more predictable because both assets are expected to exist before the user presses play
- The runtime TTS path becomes an exception path instead of the normal user path
- Cache coverage can be verified after seeding or deploy by running a backfill job and checking for misses

### Negative
- Seed or deploy workflows take longer because audio backfill becomes part of environment preparation
- Audio cache size grows because clips are generated for all curated words and hosts, not only the ones users happen to play
- Voice or provider changes require a deliberate regeneration workflow
- Local file caches remain instance-local; in multi-instance deployments, every instance needs the same pre-generated assets or a shared storage layer

### Neutral
- This decision changes generation timing, not the storage medium or authentication model described in ADR-0007
- Runtime generation remains necessary for user-contributed words and repair scenarios, but it is no longer the primary delivery strategy for curated content

## Implementation Notes (Optional)

- Add an idempotent backend script or job that iterates all seeded words and all hosts, generating both pronunciation and example-sentence audio into the existing cache directory.
- Run this backfill after dictionary seeding and as part of deployment or environment bootstrap.
- Keep runtime generation available for:
  - user-contributed words after submission
  - cache misses caused by deployment drift or manual file deletion
  - future regeneration events during provider or voice changes
- Treat cache-miss generation as a fallback path; operational monitoring should focus on driving misses toward zero for curated content.
- If the application later runs across multiple instances, consider promoting the audio cache from local disk to shared object storage or another shared cache layer.

## References (Optional)

- PRD: [specs/prd.md](../prd.md)
- Feature requirements: [audio-pronunciation.md](../features/audio-pronunciation.md), [example-sentences.md](../features/example-sentences.md), [user-contributed-words.md](../features/user-contributed-words.md)
- Related ADRs: [0007-audio-delivery.md](0007-audio-delivery.md), [0016-tts-provider-edge-tts.md](0016-tts-provider-edge-tts.md), [0017-content-seeding.md](0017-content-seeding.md)
- Microsoft Learn: Azure Architecture Center guidance on caching and background jobs