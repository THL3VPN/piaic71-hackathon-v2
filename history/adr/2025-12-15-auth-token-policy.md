# ADR: JWT auth strategy for multi-user tasks

Date: 2025-12-15

## Status
Accepted

## Context
- We must secure all `/api/*` endpoints with a shared-secret JWT that works with Better Auth on the frontend.
- Users and tasks live in Postgres via SQLModel; task ownership must be enforced server-side.
- CORS must permit the Next.js frontend at `http://localhost:3000` (and `127.0.0.1`).
- Errors need to be predictable for missing/invalid tokens and cross-user access.

## Decision
- JWT: HS256 signed with `BETTER_AUTH_SECRET`; `sub` carries the user id, plus optional username/email. Tokens are required on every `/api/*` route.
- Passwords: hashed with bcrypt via `passlib`; no plaintext storage.
- Middleware: `AuthMiddleware` extracts `Authorization: Bearer <token>`, validates signature/expiry, and attaches `AuthContext` (`user_id`, `claims`) to the request state. Missing/invalid tokens return `401`.
- Ownership: task queries filter by `owner_id`; cross-user access raises `403`. Missing records return `404`.
- CORS: allow localhost origins, send proper preflight responses.
- Error format: JSON `{"detail": "<message>"}` for auth failures and forbidden access.

## Consequences
- Backend and frontend must share `BETTER_AUTH_SECRET`; tests set this via env.
- Any new `/api/*` route must depend on the auth context and avoid trusting client-supplied user ids.
- Adding new resources should mirror this pattern: validate token, derive user from context, filter by owner, return 403/404 consistently.
