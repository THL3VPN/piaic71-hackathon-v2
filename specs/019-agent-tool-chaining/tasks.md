---

description: "Task list for agent tool chaining fix"
---

# Tasks: Agent Tool Chaining Fix

**Input**: Design documents from `/specs/019-agent-tool-chaining/`
**Prerequisites**: plan.md, spec.md

## Phase 1: User Story 1 - Multi-step tool calls succeed (Priority: P1) 🎯 MVP

**Goal**: The agent can perform a second tool call and return a final response without fallback.

**Independent Test**: A chain request (list then complete/update) returns a successful assistant response and two tool_calls.

### Tests (write first)

- [x] T001 [P] [US1] Add unit test for multi-step tool chaining in `tests/unit/test_agent_runtime_tools.py`
- [x] T002 [P] [US1] Add contract test for chained tool_calls payload in `tests/contract/test_agent_behavior_chain_contract.py`

### Implementation

- [x] T003 [US1] Implement bounded two-step tool execution in `src/services/agent_runtime.py`

### Verification

- [x] T004 [US1] Run unit + contract tests for tool chaining (`tests/unit/test_agent_runtime_tools.py`, `tests/contract/test_agent_behavior_chain_contract.py`)
