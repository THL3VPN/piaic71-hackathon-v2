# Feature Specification: Secure API requests with JWT verification

**Feature Branch**: `006-jwt-auth`  
**Created**: 2024-10-06  
**Status**: Draft  
**Input**: User description: "Feature: Secure API requests with JWT verification (Better Auth compatible) User journeys 1.1 A signed-in frontend user makes an API request with a JWT token 1.2 Backend accepts valid tokens and rejects invalid/missing tokens 1.3 Developer can test protected endpoints locally with a known JWT Acceptance criteria 2.1 Backend requires Authorization: Bearer <token> for all /api/* endpoints 2.2 Requests without a token return 401 Unauthorized 2.3 Requests with an invalid/expired token return 401 Unauthorized 2.4 Requests with a valid token succeed 2.5 Backend verifies JWT signature using shared secret BETTER_AUTH_SECRET from environment 2.6 Backend extracts user identity from the token (at minimum: user id / subject) and makes it available to route handlers 2.7 A clear error response format exists for auth failures 2.8 No user-specific filtering is required in this step (just verification + extraction) 2.9 pytest covers: missing token, invalid token, valid token Success metrics 3.1 All pytest tests pass for JWT auth behavior 3.2 Manual test: calling a protected endpoint without token returns 401 3.3 Manual test: calling a protected endpoint with a valid token returns 200 3.4 No regressions in existing task API tests (updated to include auth where needed)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Enforce token presence on protected APIs (Priority: P1)

Every request to `/api/*` should include an `Authorization: Bearer <token>` header. Requests that forget to send this header must be rejected before any business logic runs, preventing open access to sensitive data.

**Why this priority**: This is the first line of defense; without enforcement the entire auth effort is meaningless.

**Independent Test**: A pytest hitting `/api/tasks` without `Authorization` can assert on the `401 Unauthorized` and documented error payload.

**Acceptance Scenarios**:

1. **Given** no `Authorization` header, **When** the client calls `/api/tasks`, **Then** the backend returns `401 Unauthorized` with a JSON error stating the token is missing.
2. **Given** an `Authorization` header that does not use the `Bearer` prefix, **When** the request hits `/api/tasks`, **Then** the response is `401` detailing the expected format.

---

### User Story 2 - Verify JWT signature and surface identity (Priority: P2)

Middleware validates the JWT signature using `BETTER_AUTH_SECRET`, rejects expired or tampered tokens, and stores the extracted `user_id`/`sub` claims into the request context.

**Why this priority**: This ensures bad tokens never reach the core handlers and downstream code can rely on a trusted identity.

**Independent Test**: A pytest sending `/api/tasks` with a JWT signed with `BETTER_AUTH_SECRET` should return `200` and the handler should observe the request context populated with the expected subject.

**Acceptance Scenarios**:

1. **Given** a valid JWT signed with the shared secret, **When** the client calls `/api/tasks`, **Then** the endpoint responds `200` and downstream handlers can access the extracted `user_id`.
2. **Given** a JWT signed with a different secret or that is expired, **When** the request arrives, **Then** the response is `401` with an error about invalid or expired identity.

---

### User Story 3 - Share a local test token for manual checks (Priority: P3)

Document a reproducible JWT for local development so developers can manually exercise protected endpoints without integrating an auth provider.

**Why this priority**: Manual verification is practical and ensures the security checks are easy to inspect during reviews.

**Independent Test**: Running curl/HTTPie with the documented token should show `200`, while swapping it for garbage should yield `401`.

**Acceptance Scenarios**:

1. **Given** the documented test JWT, **When** the developer calls `/api/tasks`, **Then** the endpoint returns `200` and the payload looks normal.

---

### Edge Cases

- What happens when `BETTER_AUTH_SECRET` is absent from the environment at startup? The app should fail fast with a clear log message rather than starting insecurely.
- How should the middleware respond when a syntactically valid JWT lacks the `sub` or `user_id` claim expected by downstream code?
- How do we surface token expiry vs. tampering in logs while avoiding leak of sensitive token data?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: All `/api/*` routes MUST require the `Authorization: Bearer <token>` header before invoking business logic.
- **FR-002**: JWT validation MUST use the shared `BETTER_AUTH_SECRET` environment variable; starting without a secret should produce a startup warning and halt the app.
- **FR-003**: Invalid or missing tokens (malformed, expired, wrong secret) MUST return `401 Unauthorized` with a JSON error body like `{ "detail": "..." }` describing the failure.
- **FR-004**: After successful verification, the middleware MUST expose the extracted `user_id` or `sub` claim via a request context object so route handlers see the authenticated identity.
- **FR-005**: Authorization failures MUST include granular, developer-friendly messages (e.g., missing header vs. expired signature) while never logging complete token contents.

### Key Entities *(include if feature involves data)*

- **AuthenticatedContext**: Represents the validated identity from the JWT, carrying `user_id`, optional scopes, and expiry metadata for downstream handlers.
- **JWT Claims**: The payload fields (subject, issued-at, expiry) that the middleware inspects and trusts after verification.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Pytest coverage demonstrates the middleware behavior across missing, invalid, and valid tokens, asserting on HTTP status and JSON error bodies.
- **SC-002**: Manual requests without a token return `401`, while requests with the documented test token return `200` with the usual payload.
- **SC-003**: Existing `/api/tasks` tests continue passing once auth checks wrap them, signaling no regressions.
- **SC-004**: README/quickstart sections document how to set `BETTER_AUTH_SECRET` and provide the test JWT for local development.
