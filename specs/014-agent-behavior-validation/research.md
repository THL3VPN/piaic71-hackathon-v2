# Research: Agent Behavior Validation

## Decision 1: Encode behavior rules in system instructions

**Decision**: Implement intent mapping, tool chaining rules, and response style in the agent system instructions (no new infra).
**Rationale**: The scope requires prompt/instructions only and preserving stateless behavior without new configuration layers.
**Alternatives considered**:
- Separate configuration file for behaviors (rejected: adds new infrastructure and storage).
- Model-specific prompt variants (rejected: violates model-independence requirement).

## Decision 2: Deterministic tool chaining rules

**Decision**: Allow only the approved tool chains (list→delete, list→complete, list→update) with deterministic ordering.
**Rationale**: Keeps behavior predictable and avoids guesswork when resolving ambiguous tasks.
**Alternatives considered**:
- Free-form chain selection (rejected: increases nondeterminism across models).

## Decision 3: Validation strategy

**Decision**: Validate behavior using a combination of contract/integration tests with model stubs plus manual curl scenarios from the spec.
**Rationale**: Ensures deterministic CI validation while supporting real-provider verification manually.
**Alternatives considered**:
- Only manual validation (rejected: non-repeatable, not CI-friendly).
