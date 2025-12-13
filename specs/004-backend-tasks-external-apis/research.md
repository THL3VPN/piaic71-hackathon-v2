## Research & Decisions: Task REST API

### Decision: Keep a single FastAPI backend with dedicated `/api/tasks` router
- **Rationale**: The feature builds directly on the existing CLI/Neon backend, so adding a FastAPI router that delegates to the current `task_repo` avoids a separate microservice and keeps deployment simple.
- **Alternatives considered**:
  1. **Split into a new service** (adds inter-process comms, more infra); rejected because the value is primarily testable CRUD within the same codebase.
  2. **Attach routes to the CLI app** (mixes concerns); rejected because separating API handlers into `src/api/tasks.py` keeps the CLI and HTTP layers decoupled.

### Decision: Service layer handles business validation, routes remain thin
- **Rationale**: Existing constitution emphasizes clean separation; the service functions already validate titles and default fields, so routes should simply parse requests, call services, and translate results to HTTP responses.
- **Alternatives considered**:
  1. **Validate directly in routers** (faster to write but duplicates logic); rejected to avoid drifting from existing service tests and to keep tests focused on business rules.
  2. **Use middleware for validation** (adds indirection); rejected because SQLModel Pydantic models already enforce `title` constraints easily.

### Decision: Consistent error responses (`{"detail":"Task not found"}` with 404)
- **Rationale**: Acceptance criteria demand uniform 404 messaging; the router/service pair will raise `HTTPException(404, detail=...)` for missing tasks so all endpoints share the same JSON body.
- **Alternatives considered**:
  1. **Return 204 for missing deletes** (not acceptable; client expects failure).  
  2. **Use custom error codes** (adds extra handling without clear benefit).

### Decision: API contracts defined with OpenAPI subset in `contracts/openapi.yaml`
- **Rationale**: Provides a clear, machine-readable specification for the new endpoints and supports testing via schema-driven clients.
- **Alternatives considered**:
  1. **Skip formal contract** (less clarity); rejected because the feature touches new HTTP routes and a contract aids testing and documentation.
  2. **Use GraphQL schema** (misaligned with REST requirement); rejected as it contradicts the user input.
