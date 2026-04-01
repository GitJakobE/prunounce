# ADR-0002: Backend Framework — Express 5 + TypeScript

- **Status:** Superseded by [ADR-0010](0010-backend-python-migration.md)
- **Date:** 2026-03-16
- **Deciders:** Development team
- **Requirements:** REQ-4 (Authentication), REQ-9 (Content seeding), REQ-10 (Data persistence), REQ-11 (API surface)

## Context and Problem Statement

The application needs a backend that serves a REST API for authentication, dictionary browsing, search, audio delivery, and profile management. It must support middleware (auth, validation, CORS, security headers) and integrate with Prisma ORM and file-based audio caching.

## Decision Drivers

- Lightweight framework suitable for a focused REST API
- Native async/await support for clean request handlers
- Strong middleware ecosystem (security, validation, CORS)
- TypeScript-first development for shared type safety with the frontend
- Mature testing support with supertest
- Low ceremony — minimal boilerplate for route definitions

## Considered Options

### Option 1: Express 5 + TypeScript (Chosen)

Express is the most established Node.js web framework. Version 5 adds native Promise support in route handlers (rejected promises automatically result in error responses). Combined with TypeScript, it provides a well-understood, minimal API layer.

### Option 2: Fastify

Higher performance than Express with schema-based validation and built-in TypeScript support. However, the performance advantage is irrelevant at this application's scale (~250 words, single-digit concurrent users at launch). Express's larger ecosystem and broader team familiarity outweigh Fastify's throughput gains.

### Option 3: NestJS

Opinionated, Angular-inspired framework with dependency injection, decorators, and modules. Provides excellent structure for large teams and complex domains. However, for a focused pronunciation tool with ~6 route files, NestJS's ceremony (modules, controllers, services, DTOs) adds unnecessary complexity.

### Option 4: Hono

Ultra-lightweight, edge-ready framework with Web Standard APIs. Excellent for serverless deployment. However, its ecosystem for middleware (helmet, express-validator equivalents) is less mature, and the application targets a traditional Node.js deployment.

## Decision Outcome

**Chosen: Option 1 — Express 5 + TypeScript**

### Consequences

**Positive:**
- Express 5's async error handling eliminates the need for try/catch wrappers in every route
- helmet middleware adds security headers with one line of configuration
- express-validator provides declarative input validation for auth and profile endpoints
- supertest integrates natively for API testing (35 tests passing)
- Extracting `app.ts` from `index.ts` enables clean test setup without starting the server
- cors middleware handles cross-origin requests from the Vite dev server

**Negative:**
- Express lacks built-in request/response typing — `req.params` requires manual casting
- No built-in schema validation — express-validator adds this but with verbose syntax
- Express 5 was in beta for years; some ecosystem packages still target v4 APIs

**Neutral:**
- tsx provides TypeScript execution in development without a compile step
- The `type: "commonjs"` module format is used for compatibility with Prisma's generated client
