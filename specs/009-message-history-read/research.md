# Research Summary: Message History Read

## Decision 1: Reject non-positive limits with 422

- **Decision**: Treat limit values <= 0 as invalid and return a validation error.
- **Rationale**: Aligns with explicit requirement and prevents silent defaults that could hide client bugs.
- **Alternatives considered**: Default to 50 for non-positive limits; rejected to preserve explicit failure for invalid input.

## Decision 2: Clamp limits above 200

- **Decision**: Clamp any provided limit above 200 to 200.
- **Rationale**: Matches requirement and prevents oversized responses.
- **Alternatives considered**: Return 422 for values above 200; rejected to keep behavior user-friendly without adding extra client handling.

## Decision 3: Stable ordering for equal timestamps

- **Decision**: Order messages by created_at ascending, then id ascending.
- **Rationale**: Ensures deterministic ordering when timestamps are equal.
- **Alternatives considered**: Order only by created_at; rejected due to potential nondeterminism.
