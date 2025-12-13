# Contracts: Task Persistence API (outline)

These routes assume FastAPI wiring that delegates to the service layer. Service logic must be testable independently of HTTP.

## POST /tasks
- **Purpose**: Create a task.
- **Request Body**:
  - `title: string` (required, non-empty)
  - `description: string|null` (optional)
- **Responses**:
  - `201 Created` with body `{ id, title, description, completed, created_at }`
  - `400 Bad Request` if title is empty/whitespace
  - `500` on DB failure (error logged, message sanitized)

## GET /tasks/{id}
- **Purpose**: Fetch a task by ID.
- **Responses**:
  - `200 OK` with body `{ id, title, description, completed, created_at }`
  - `404 Not Found` if ID missing

## GET /tasks
- **Purpose**: List tasks.
- **Query Params**: none (default order by created_at asc)
- **Responses**:
  - `200 OK` with body `[ { id, title, description, completed, created_at }, ... ]`

## Error Handling
- Input validation errors → 400 with clear message.
- Missing resources → 404.
- DB/connection errors → 500; log details, do not leak secrets (no connection strings in responses).

## Notes
- Routes are thin: they call service methods `create_task`, `get_task`, `list_tasks`.
- Integration tests may exercise service directly; API layer can be tested separately when endpoints are wired.
