# Research: Frontend Chat UI Integration

## Decision: Use existing Next.js App Router layout

**Rationale**: The repository already uses Next.js and the App Router. The chat UI can be added as a page or panel using existing frontend tooling without introducing new frameworks.

**Alternatives considered**: Build a standalone SPA or separate frontend. Rejected due to unnecessary complexity and loss of shared auth/storage conventions.

## Decision: Persist conversation_id in local storage with optional URL support

**Rationale**: Local storage aligns with existing token storage and is sufficient for continuity. URL query support is optional and can be added later if needed.

**Alternatives considered**: Only in-memory state. Rejected because it loses continuity on refresh.

## Decision: Fetch message history from backend on load

**Rationale**: Backend already stores messages; fetching history provides a complete view and ensures stateless frontend.

**Alternatives considered**: UI-only history. Rejected for less reliable continuity and inconsistent history across reloads.
