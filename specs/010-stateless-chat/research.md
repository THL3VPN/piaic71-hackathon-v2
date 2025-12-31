# Research Summary: Stateless Chat Endpoint

## Decision 1: Deterministic dummy response format

- **Decision**: Use "OK (dummy): <message>" for the assistant response.
- **Rationale**: Safe, deterministic echo verifies the full request cycle without tools.
- **Alternatives considered**: Static message; rejected because echoing input confirms data flow.

## Decision 2: Always fetch history (limit 50)

- **Decision**: Fetch prior messages for the conversation on every request.
- **Rationale**: Enforces statelessness and validates DB retrieval path.
- **Alternatives considered**: Skip history when using dummy response; rejected because it weakens the stateless proof.

## Decision 3: Ownership enforcement response

- **Decision**: Return 404 when conversation_id is not owned by the user.
- **Rationale**: Avoids leaking existence and matches existing behavior.
- **Alternatives considered**: Return 403; rejected to avoid confirming resource existence.
