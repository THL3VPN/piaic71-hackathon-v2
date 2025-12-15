# API Contracts: Auth + User-Scoped Tasks (High Level)

All responses are JSON; errors include `detail` message. Auth required for `/api/tasks*` unless noted.

## Auth

- **POST /api/register**
  - Request: `{ "username": string, "password": string }`
  - Responses:
    - 201 `{ "id": int, "username": string }`
    - 400/409 duplicate username `{ "detail": "username already exists" }`

- **POST /api/login**
  - Request: `{ "username": string, "password": string }`
  - Responses:
    - 200 `{ "token": string, "token_type": "bearer", "expires_in": int }`
    - 401 invalid credentials `{ "detail": "invalid credentials" }`

## Tasks (all require `Authorization: Bearer <token>`)

- **GET /api/tasks**
  - Response 200: list of tasks owned by caller.

- **POST /api/tasks**
  - Request: `{ "title": string, "description": string? }`
  - Response 201: created task (owner_id = caller).
  - Errors: 422 validation; 401 missing/invalid token.

- **GET /api/tasks/{id}**
  - 200: task if owned by caller.
  - 403 if not owned; 404 if not found.

- **PUT /api/tasks/{id}**
  - Request: `{ "title": string, "description": string? }`
  - 200: updated task if owned.
  - 403/404 as above; 422 validation.

- **DELETE /api/tasks/{id}**
  - 204 on success if owned; 403/404 otherwise.

- **PATCH /api/tasks/{id}/complete**
  - Request: `{ "completed": boolean }`
  - 200: updated task if owned; 403/404 otherwise; 422 validation.
