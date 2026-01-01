# Research: Real-Time Agent Tool Calls

## Decision 1: Use OpenAI Agents SDK for tool calling

**Decision**: Use the OpenAI Agents SDK for building the agent and invoking tools.
**Rationale**: SDK provides first-class tool registration and standardized tool call capture.
**Alternatives considered**: Manual Chat Completions tool wiring; rejected due to more boilerplate and less structured tool metadata.

## Decision 2: Register existing task tools without bypass

**Decision**: Wrap existing task tool functions and register them directly with the agent.
**Rationale**: Preserves ownership checks and domain logic already validated in task tools.
**Alternatives considered**: Reimplement tool logic inside agent runtime; rejected due to duplication and risk of bypassing auth checks.

## Decision 3: Return tool call payloads in chat response

**Decision**: Return tool call name, arguments, and result in the `/api/chat` response payload.
**Rationale**: Required for transparency and debugging; matches acceptance criteria.
**Alternatives considered**: Omit tool call payloads or log only; rejected due to functional requirements.
