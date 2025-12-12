# Data Model: FastAPI Health Service

## Entities

### HealthResponse
- **Fields**:
  - `status: str` — required; indicates service health (e.g., "ok").
- **Validation rules**:
  - Status must be a non-empty string.
- **State transitions**:
  - Static response; no persistence or mutation.
