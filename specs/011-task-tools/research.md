# Research: Task Tools Layer

## Decisions

### Decision 1: Use domain errors for tool failures

**Decision**: Tool functions raise TaskNotFound, InvalidInput, or UnauthorizedAccess instead of HTTP exceptions.

**Rationale**: Keeps tools transport-agnostic and reusable across chat/API/MCP layers.

**Alternatives considered**: Raise HTTPException directly; rejected due to coupling to FastAPI.

---

### Decision 2: Status filter mapping and validation

**Decision**: list_tasks accepts status = all | pending | completed; unknown values raise InvalidInput.

**Rationale**: Deterministic behavior and explicit validation.

**Alternatives considered**: Treat unknown status as "all"; rejected to avoid silent misuse.

---

### Decision 3: Reject empty update_task payloads

**Decision**: update_task raises InvalidInput when no fields are provided.

**Rationale**: Avoids ambiguous no-op updates and aligns with spec requirement.

**Alternatives considered**: Return existing task without update; rejected to avoid ambiguous outcomes.
