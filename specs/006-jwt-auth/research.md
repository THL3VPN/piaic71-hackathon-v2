# Phase 0 Research: JWT auth for API

## Decision 1: Verify tokens on /api/* via middleware
- **Decision**: Introduce auth middleware that inspects Authorization header, verifies JWT signature using `BETTER_AUTH_SECRET`, and enforces header presence before reaching route handlers.
- **Rationale**: Centralizing token enforcement avoids scattering guards across multiple routers and preserves FastAPI dependency flow.
- **Alternatives considered**:
  - Decorators on each endpoint (fragmented and error-prone).
  - Offloading to an API gateway (adds infra weight and slows local iteration).

## Decision 2: Share context via dataclass
- **Decision**: Create `AuthenticatedContext` dataclass carrying `user_id`, claims, and expiry accessible via `request.state.auth`.
- **Rationale**: Dataclasses align with constitution rules, ensure type hints, and keep identity data explicit.
- **Alternatives considered**: Storing raw token string or mutating global state (discarded due to threading concerns).

## Decision 3: Document a static JWT for local tests
- **Decision**: Provide a token signed with `BETTER_AUTH_SECRET` in quickstart so maintainers can manually exercise endpoints.
- **Rationale**: Facilitates manual verification without spinning up a full auth provider.
- **Alternatives considered**: Spinning up dedicated auth service (overkill for this feature).
