# Contracts: JWT Auth Middleware

## Protected endpoints
- All routes under `/api/*` expect `Authorization: Bearer <token>`.
- Response on failure: `401 Unauthorized` with body `{"detail":"<reason>"}`.
- Success response mirrors existing handlers (`/api/tasks` returns JSON array).

## Token verification steps
1. Ensure header exists and uses `Bearer` prefix.
2. Decode JWT with `BETTER_AUTH_SECRET` via HS256.
3. Reject tokens failing signature or expiry.
4. Populate `request.state.auth` with the extracted `user_id` claim for downstream use.
