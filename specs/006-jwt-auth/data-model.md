# Phase 1: Data Model for JWT Auth

## AuthenticatedContext
- **Purpose**: Represent the validated identity derived from a JWT after successful verification.
- **Fields**:
  - `user_id: str` – maps to the token subject/`sub` claim.
  - `issued_at: datetime | None` – optional `iat` claim.
  - `expires_at: datetime | None` – optional `exp` claim.
  - `raw_claims: dict[str, Any]` – remaining claims to support future features.
- **Usage**: Attached to `fastapi.Request.state.auth` so route handlers inspect the authenticated identity without reparsing.

## JWT Claims (logical entity)
- **Purpose**: Validate the incoming payload structure.
- **Essential fields**:
  - `sub` (or `user_id`): Unique identifier for the user.
  - `iat`: Issued-at timestamp.
  - `exp`: Expiry timestamp.
  - `aud`/`iss`: Optional fields used for logging or further validation.
- **Validation**: Signed using `BETTER_AUTH_SECRET` and algorithms such as HS256.
