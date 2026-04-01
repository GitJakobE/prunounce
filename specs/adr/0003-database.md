# ADR-0003: Database — SQLite with Prisma ORM

- **Status:** Partially superseded — SQLite remains the database, but the ORM has changed from Prisma to SQLAlchemy 2.0 (see [ADR-0010](0010-backend-python-migration.md)) (ORM superseded: Prisma replaced by SQLAlchemy per [ADR-0010](0010-backend-python-migration.md))
- **Date:** 2026-03-16
- **Deciders:** Development team
- **Requirements:** REQ-2 (Word dictionary), REQ-6 (Progress tracking), REQ-9 (Content seeding), REQ-10 (Data persistence)

## Context and Problem Statement

The application needs persistent storage for user accounts, the word dictionary (~250+ words across 10 categories), user progress (words listened to), and preferences (language, host persona). The data model includes relational associations (words ↔ categories, users ↔ progress). The solution must be simple to develop against, easy to deploy, and appropriate for the expected data volume and concurrency.

## Decision Drivers

- Relational data model (many-to-many: words ↔ categories; one-to-many: users ↔ progress)
- Small data volume: hundreds of words, low thousands of users at most
- Low concurrency: single-digit simultaneous writes expected
- Simple deployment: no external database server to provision or maintain
- Type-safe database access from TypeScript
- Idempotent seeding support (upsert operations)

## Considered Options

### Option 1: SQLite + Prisma 6 (Chosen)

SQLite is a serverless, file-based relational database. Prisma provides a type-safe ORM with schema-driven migrations, auto-generated TypeScript client, and built-in upsert operations for idempotent seeding.

### Option 2: PostgreSQL + Prisma

Full-featured relational database with excellent concurrency, full-text search, and JSON support. Ideal for production systems with multiple concurrent writers. However, requires a separate database server (or managed service), adding deployment complexity and cost for an application that will comfortably run on SQLite's concurrency model.

### Option 3: MongoDB + Mongoose

Document database that maps naturally to JSON. Good for flexible schemas. However, the application's data model is inherently relational (word ↔ category associations, user ↔ progress tracking). MongoDB would require denormalisation or manual reference management that a relational database handles natively.

### Option 4: JSON file storage

The simplest option — store everything in JSON files. Adequate for the word dictionary (read-heavy, seed-once). However, concurrent writes for user progress and account management would require manual locking, making this fragile and error-prone.

## Decision Outcome

**Chosen: Option 1 — SQLite + Prisma 6**

### Consequences

**Positive:**
- Zero-config database: a single `.db` file, no server process to manage
- Prisma generates a fully typed TypeScript client from the schema, catching query errors at compile time
- Prisma Migrate manages schema changes with versioned migration files
- `createMany`, `upsert`, and transaction support enable clean idempotent seeding (REQ-9)
- The `@@unique` constraint on `[userId, wordId]` in UserProgress enforces data integrity for progress tracking
- SQLite's read performance is excellent for the dictionary browsing and search use cases

**Negative:**
- SQLite supports only one concurrent writer — acceptable at current scale but would require migration to PostgreSQL if write contention becomes an issue
- No built-in full-text search — word search uses `LIKE`/`contains` queries, which is adequate for ~250 words but wouldn't scale to tens of thousands
- Prisma's generated client binary (~4 MB) adds to deployment size
- SQLite file must be on a persistent volume in containerised deployments

**Neutral:**
- Migration path to PostgreSQL is straightforward: change `provider` in schema.prisma and adjust the connection URL — Prisma abstracts the SQL dialect differences
- The database file lives at `prisma/dev.db` in development and is excluded from version control

### Data Model Summary

| Model | Purpose | Key Relationships |
|---|---|---|
| User | Account, preferences, host selection | → UserProgress[] |
| Category | Thematic word grouping | → WordCategory[] |
| Word | Italian word with translations and examples | → WordCategory[], UserProgress[] |
| WordCategory | Many-to-many join (word ↔ category) | — |
| UserProgress | Tracks which words a user has listened to | — |
