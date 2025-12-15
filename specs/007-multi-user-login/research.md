# Research: Username/Password Auth with User-Scoped Tasks

## Decisions

- **Password hashing**: Use passlib[bcrypt] with reasonable rounds (passlib defaults) to avoid introducing argon2 dependency now; revisit via ADR if stronger hashing required. Never store plaintext; logins compare hash safely.
- **JWT**: HS256 with shared `BETTER_AUTH_SECRET`; claims: `sub` (user id), `username`, `exp` (default 24h). No refresh/rotation in scope; short-lived tokens acceptable for MVP.
- **Authorization failures**: Return 401 for missing/invalid tokens; return 403 for cross-user access to tasks (consistent and clear). Validation errors remain 422.
- **Data model**: Add `User` table (id, username unique, password_hash, created_at). Add `owner_id` FK to `Task`.
- **Token storage (frontend)**: Use localStorage (current pattern) for JWT. Logout clears localStorage token. CSRF considered low risk because token is in header, not cookie.
- **DB**: Neon PostgreSQL via `DATABASE_URL`; reuse existing async engine/session helpers; ensure create_all applies to new User table.

## Alternatives considered

- Argon2 instead of bcrypt: more secure but adds dependency/packaging overhead; deferred for now.
- 404 vs 403 on cross-user: 403 chosen for clarity to clients; document consistently in API responses.
- Cookie-based auth: would need CSRF protections; out of scope for current JWT-based API.

## Open items

- Token expiry duration can be tuned later; default 24h unless product requires shorter window.
- Scale assumptions not provided; if high concurrency required, revisit hashing cost and DB pooling.
