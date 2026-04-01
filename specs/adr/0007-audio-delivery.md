# ADR-0007: Audio Delivery — Server-Side File Cache with Token-Authenticated Streaming

- **Status:** Accepted
- **Date:** 2026-03-16
- **Deciders:** Development team
- **Requirements:** REQ-3 (Audio pronunciation), REQ-4 (Authentication), REQ-8 (Example sentences)

## Context and Problem Statement

Audio pronunciation is the core feature of the application. Every word and example sentence has a pre-generated MP3 file that must be served to authenticated users via `<audio>` HTML elements. The challenge is that `<audio>` elements set their source via the `src` attribute — a URL that the browser fetches with a standard GET request. Unlike `fetch()` calls, `<audio src="...">` cannot set custom HTTP headers (such as `Authorization: Bearer`). The delivery mechanism must authenticate requests while remaining compatible with the browser audio API.

## Decision Drivers

- `<audio>` elements cannot set HTTP headers — standard Bearer token auth doesn't work
- All content is behind authentication — unauthenticated audio access must be prevented
- Sub-1-second latency from click to playback
- Sequential playback: word → pause → example sentence
- Audio files are static once generated — aggressive caching is appropriate
- Simple implementation without additional infrastructure (CDN, signed URLs)

## Considered Options

### Option 1: Server-side file serving with query parameter token (Chosen)

Serve audio files through Express routes (`/api/audio/:wordId` and `/api/audio/:wordId/example`). Accept the JWT as a `?token=` query parameter in addition to the standard `Authorization` header. The auth middleware checks both sources. Audio files are read from the local `audio-cache/` directory and streamed to the client.

### Option 2: Fetch + Object URL

Use `fetch()` with the Authorization header to download the audio as a blob, then create a `URL.createObjectURL()` and set it as the `<audio>` src. This keeps the token out of URLs entirely. However, it adds complexity (blob management, memory cleanup), prevents the browser from caching audio natively, and doubles memory usage (blob in memory + audio element buffer).

### Option 3: Signed URLs (pre-signed, time-limited)

Generate a short-lived signed URL for each audio request. The URL contains a cryptographic signature that the server validates. No token in the URL — the signature proves authorisation. However, this adds complexity (signature generation, expiry logic) without meaningful security benefit over the simpler query parameter approach for this application's threat model.

### Option 4: Cookie-based auth for audio routes

If authentication used HTTP-only cookies (see ADR-0004), `<audio>` elements would automatically send the cookie. However, the application uses JWT in localStorage, making this incompatible without a broader auth architecture change.

## Decision Outcome

**Chosen: Option 1 — Server-side file serving with query parameter token**

### Implementation Details

- **Auth middleware**: checks `Authorization: Bearer <token>` first; if absent, checks `req.query.token` — same JWT validation either way
- **Word audio**: `GET /api/audio/:wordId?token=<jwt>` → reads `audio-cache/{italian}.mp3`
- **Example audio**: `GET /api/audio/:wordId/example?token=<jwt>` → reads `audio-cache/ex_{italian}.mp3`
- **Frontend playback**: `new Audio(\`/api/audio/${wordId}?token=${token}\`)` — avoids `<audio>` elements in the DOM; uses the Audio API directly
- **Sequential playback**: AudioButton chains word audio → 600ms pause → example audio via `onended` event
- **Single-instance management**: a module-level `currentAudio` variable ensures only one audio plays at a time — starting a new word stops the previous one

### Consequences

**Positive:**
- Works with the standard browser Audio API without blob workarounds
- Sub-100ms serving latency (local file read, no external API calls at runtime)
- Simple implementation — the auth middleware change is ~5 lines of code
- Audio files are small (~10-30 KB each) — negligible bandwidth impact
- The `Audio()` constructor approach avoids DOM element management

**Negative:**
- JWT appears in the URL query string — visible in server access logs and browser history
- Mitigation: HTTPS encrypts the URL in transit; access logs should be configured to exclude query parameters in production
- No browser-level audio caching (each play creates a new `Audio()` object) — acceptable since files are small and the server is local

**Neutral:**
- The sequential playback (word → example) is managed entirely in the frontend AudioButton component
- `markListened()` is called after the full playback chain completes, accurately tracking progress
