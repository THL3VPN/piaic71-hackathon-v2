# Research: MCP Server Extraction

## Decision 1: Use Official MCP SDK server for task tools

**Decision**: Implement a dedicated MCP server using the Official MCP SDK to expose task tools.
**Rationale**: Step 6 explicitly requires MCP extraction and tool exposure through the official SDK.
**Alternatives considered**:
- Keep local tool calls (rejected: violates MCP extraction requirement).
- Proxy tools via HTTP without MCP SDK (rejected: not compliant with official SDK requirement).

## Decision 2: Backend-to-MCP invocation via configured URL

**Decision**: Backend uses `MCP_SERVER_URL` to invoke MCP tools and includes user_id in tool inputs.
**Rationale**: Decouples services and supports deployment flexibility; keeps auth context in backend.
**Alternatives considered**:
- Hardcoded MCP endpoint (rejected: violates env-based configuration requirement).

## Decision 3: Error mapping

**Decision**: MCP server returns not-found style errors for ownership violations; backend keeps friendly responses for tool errors.
**Rationale**: Prevents data leakage and maintains Step 5 behavior.
**Alternatives considered**:
- Distinct error messages for ownership vs missing (rejected: leaks existence).
