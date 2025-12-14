## Data Model – Frontend health tracking

| Entity       | Description                     | Key Fields                           |
|--------------|---------------------------------|--------------------------------------|
| HealthStatus | Represents the backend health payload consumed by the frontend UI | `status`: string (e.g., `"ok"` or error text) `timestamp`: ISO datetime from backend (if provided) `message`: optional, carries extra info about failures |

### Validation rules
- `status` must always be a short human-readable string.
- `message` is optional and only used when the backend reports degraded health.

### State transitions
- Frontend simply renders the latest snapshot from the backend; no mutations occur on this structure.
