# ADR-0009: Monorepo Structure — Single Repository with Independent Frontend and Backend Projects

- **Status:** Accepted
- **Date:** 2026-03-16
- **Deciders:** Development team
- **Requirements:** All (cross-cutting structural concern)

## Context and Problem Statement

The application consists of a React frontend and an Express backend that communicate via REST APIs. The two projects have different runtimes, build tools, and dependencies. The repository structure must support independent development, testing, and deployment of each project while keeping them co-located for ease of development.

## Decision Drivers

- Single developer / small team — co-location reduces context switching
- Shared TypeScript language across both projects
- Independent build and test commands per project
- Ability to deploy frontend and backend independently in the future
- Simple CI/CD configuration
- Specs, docs, and scripts shared across both projects

## Considered Options

### Option 1: Single repo with `src/frontend/` and `src/backend/` directories (Chosen)

Both projects live under `src/` in the same repository, each with their own `package.json`, `tsconfig.json`, and build scripts. Shared specifications live at the repository root in `specs/`. No monorepo tooling (no Turborepo, no Nx, no workspaces).

### Option 2: npm/pnpm workspaces monorepo

Use package manager workspaces to link the projects and share dependencies. Adds `node_modules` hoisting and cross-project dependency resolution. However, the two projects share no runtime code — they're connected only by HTTP API contracts. Workspace overhead adds complexity without benefit.

### Option 3: Separate repositories

Each project in its own repository. Clean separation but requires coordinating changes across repos (e.g., adding `hostId` to API responses requires changes in both). For a single developer, the coordination overhead outweighs the isolation benefit.

## Decision Outcome

**Chosen: Option 1 — Single repo, independent projects, no monorepo tooling**

### Repository Layout

```
spec2cloud/
├── specs/              # PRD, FRDs, ADRs, task specs
│   ├── prd.md
│   ├── features/       # Feature requirement documents
│   ├── adr/            # Architecture decision records
│   └── tasks/          # Task specifications
├── src/
│   ├── backend/        # Express + Prisma + TypeScript
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   ├── prisma/
│   │   ├── src/
│   │   └── audio-cache/
│   └── frontend/       # React + Vite + Tailwind
│       ├── package.json
│       ├── tsconfig.json
│       └── src/
├── docs/               # Documentation site content
├── scripts/            # Installation and setup scripts
└── templates/          # Project templates
```

### Consequences

**Positive:**
- One `git clone` gets everything — specs, frontend, backend, scripts
- PRD/FRD changes are committed alongside the code changes they drive
- Simple CI: run `cd src/backend && npm test` and `cd src/frontend && npm test` in parallel
- No monorepo tooling to learn, configure, or maintain
- Each project has fully independent `node_modules` — no hoisting surprises

**Negative:**
- No shared TypeScript types between frontend and backend — API contracts are duplicated (e.g., `User` type defined in both projects)
- No unified `npm install` or `npm test` at the root — developers must know to work in subdirectories
- `package.json` at the root level doesn't exist — tooling that expects it (e.g., some CI templates) needs adjustment

**Neutral:**
- The Vite dev server proxies `/api` requests to `localhost:3001` during development, making the two servers transparent to the browser
- Deployment can serve the frontend's `dist/` as static files from the Express server, or deploy them separately to a CDN
