# ADR 006: JWT verification middleware for `/api/*`

## Context
The task API must be guarded by JWT authentication before downstream handlers examine requests. We already have FastAPI + SQLModel services.

## Decision
Introduce a shared middleware layer (`AuthMiddleware`) that parses the `Authorization: Bearer <token>` header, verifies the token against `BETTER_AUTH_SECRET`, checks expiry, and builds an `AuthenticatedContext` accessible via `request.state`. FastAPI route handlers then depend on `auth.get_authenticated_context` to access the validated `user_id` without re-parsing the token.

## Consequences
- Keeps token validation centralized so new endpoints automatically receive the guard.
- Allows manual testing via the documented token without spinning up an external auth provider.
