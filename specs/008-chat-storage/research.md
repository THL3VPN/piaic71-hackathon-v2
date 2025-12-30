# Research Notes: Chat Storage Persistence

## Decision: Ownership enforcement in queries

**Rationale**: Filtering by both `conversation_id` and `user_id` in repository queries prevents cross-user access without additional in-memory checks.

**Alternatives considered**:
- Check ownership after fetching by id (risk of leaking existence; extra query).
- Use row-level security policies (out of scope for this feature).

## Decision: Transaction boundaries for create/append

**Rationale**: Use a single session transaction per request to ensure message creation either fully commits or rolls back with errors.

**Alternatives considered**:
- Autocommit per statement (risk of partial writes).
- Batch multiple operations in a long-lived session (higher coupling and concurrency risk).

## Decision: Message ordering and tie-breaker

**Rationale**: Order by `created_at`, then `id` to guarantee deterministic ordering when timestamps are equal.

**Alternatives considered**:
- Order by `created_at` only (non-deterministic ties).
- Order by `id` only (loses explicit chronological ordering).

## Decision: History limit validation

**Rationale**: Reject non-positive limits with 422 to avoid silent behavior changes and ambiguous client expectations.

**Alternatives considered**:
- Coerce invalid limits to default (hides client errors).
- Return empty list for invalid limits (silent failure).

## Decision: Conversation activity timestamps

**Rationale**: Update `updated_at` on each new message to reflect last activity and support future pagination or sorting.

**Alternatives considered**:
- Update only on explicit conversation updates (misses activity signals).
