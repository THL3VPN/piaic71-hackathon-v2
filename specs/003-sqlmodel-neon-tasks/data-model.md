# Data Model: Persistent Task Storage (SQLModel + Neon Postgres)

## Entities

### Task
- **Purpose**: Represents a persisted task record in Neon Postgres.
- **Fields**:
  - `id: int` (primary key, auto-increment)
  - `title: str` (required, non-empty)
  - `description: str | None` (optional)
  - `completed: bool` (default: False)
  - `created_at: datetime` (UTC timestamp, default now)
- **Constraints**:
  - Title must be non-empty after trimming whitespace.
  - `created_at` stored in UTC.
- **Relationships**: None in this increment.
- **Indexes**: Primary key on `id`; consider index on `created_at` for ordering (implicit via PK ordering is acceptable for small sets).

## State & Transitions
- Initial state: `completed=False` on creation.
- Allowed transitions: `completed` can toggle true/false; other fields can be updated in future increments (out of scope here).

## Validation Rules
- Title validation performed in service before DB insert.
- Repository returns not-found signal for missing IDs; no exceptions leak to callers.
