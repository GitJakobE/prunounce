# ADR-0023: Host Persona Image Pipeline — AI-Generated Static Assets with Local Serving

- **Status:** Accepted
- **Date:** 2026-03-29
- **Deciders:** Development team
- **Requirements:** F-HOSTS (Host Personas & Landing Experience), REQ-7

## Context and Problem Statement

The Host Personas FRD (F-HOSTS) defines 12 host personas (4 per language), each requiring a unique AI-generated portrait image (512×512 px). These images are the visual centrepiece of the host selection page and the per-page host banner. The team needs to decide how to generate, store, and serve these images, balancing quality, cost, and operational simplicity.

## Decision Drivers

- 12 images at launch, growing by ~4 per new language (infrequent additions)
- Images are static — they don't change per user or per session
- The project already contains `scripts/generate-host-images.mjs`, indicating a script-based generation approach
- The frontend is a React SPA served as static files (ADR-0001)
- The backend serves the API only; static assets should not route through the API server
- The site will be deployed to Azure (public internet deployment per PRD scope)
- F-A11Y requires meaningful `alt` text for all host portraits

## Considered Options

### Option 1: AI-Generated at Build Time, Committed to Repo, Served as Static Assets (Chosen)

Generate portraits using an AI image service (e.g., DALL-E, Stable Diffusion) via the existing generation script. Commit the output images to the repository under `src/frontend/public/` (or a shared `public/` directory). The frontend references them by path. Images are served as static files by the web server or CDN.

### Option 2: AI-Generated, Stored in Azure Blob Storage, Served via CDN

Generate images and upload them to Azure Blob Storage with a CDN front. The frontend references them by CDN URL. Provides edge caching and separates binary assets from the code repository.

### Option 3: AI-Generated On Demand via API

Generate images dynamically when a host is first requested, cache the result. This is unnecessary complexity for 12 static images and introduces latency on first load.

### Option 4: Stock Photos or Hand-Drawn Illustrations

Use stock photography or commission illustrations instead of AI generation. Higher quality control but introduces licensing costs and longer iteration cycles for new hosts.

## Decision Outcome

**Chosen: Option 1 — AI-Generated at Build Time, Served as Static Assets**

For 12 images that rarely change, committing them to the repository and serving them as static files is the simplest approach. The generation script enables reproducible image creation when new hosts are added.

### Image Pipeline

1. **Generation:** Run `scripts/generate-host-images.mjs` which calls one or more AI image providers with per-host prompts (personality, appearance, style consistency). The current priority order is Google Gemini when `GOOGLE_API_KEY` is configured, then Pollinations, then AI Horde.
2. **Output:** 512×512 px JPEG files, named by host slug and variant (e.g., `marco-1.jpg`, `freja-2.jpg`)
3. **Storage:** Committed to `src/backend/public/hosts/` and served as static assets by the application
4. **Serving:** The web server (or Azure Static Web Apps / CDN in production) serves images as static files with long cache headers (`Cache-Control: public, max-age=31536000, immutable`)
5. **Optimization:** Images are compressed at generation time. WebP variants may be added for browsers that support them.

### Accessibility (per F-A11Y)

- Each host portrait `<img>` must have an `alt` attribute describing the host: e.g., `alt="Marco — a cheerful Roman chef who teaches through Italian food culture"`
- If the image fails to load, the alt text provides the host's identity to screen readers and visual users

### Adding New Hosts

When a new language is added (per PRD extensibility scope):
1. Define the new host personas in the hosts configuration
2. Add generation prompts to the script
3. Run the script to generate new portraits
4. Commit the images and update the host data

### Consequences

**Positive:**
- Zero runtime dependencies — images are static files, no external service needed at serving time
- Long cache headers mean images are effectively free after first load
- Version-controlled images make changes auditable and rollback trivial
- The generation script is repeatable for new hosts

**Negative:**
- Binary files in the repository increase clone size (~12 × 100KB ≈ 1.2 MB — negligible)
- Changing a host's appearance requires re-running the script and committing new files
- AI-generated images may require iteration to achieve consistent visual style across all hosts

**Neutral:**
- If the project later moves to Azure Blob Storage + CDN (Option 2) for performance at scale, the migration is straightforward — update image URLs from local paths to CDN URLs
- The generation script is a development-time tool, not a runtime dependency
