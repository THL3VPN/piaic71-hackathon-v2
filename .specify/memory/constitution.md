<!--
Sync Impact Report
- Version change: n/a -> 1.0.0
- Modified principles: initialized (Test-First Delivery; Typed Python 3.12+; Clean & Simple Code; SOLID OOP with Dataclasses; Decision Traceability via ADRs; Tooling & Quality Gates)
- Added sections: Technical Stack & Constraints; Workflow & Quality Gates
- Removed sections: none
- Templates requiring updates: .specify/templates/plan-template.md ✅; .specify/templates/spec-template.md ✅; .specify/templates/tasks-template.md ✅
- Follow-up TODOs: none
-->
# Piaic71 Hackathon v2 Constitution

## Core Principles

### I. Test-First Delivery (TDD)
Tests are written first, approved, and run to red before implementation; the team follows a strict red-green-refactor cycle with pytest. All tests must pass before merge, and coverage must remain at or above 80% for every change set. New code without failing tests is not allowed.

### II. Typed Python 3.12+ Standard
All runtime code targets Python 3.12+ and uses type hints everywhere (functions, methods, data structures, external interfaces). Type checks and runtime behavior must agree; signatures are part of the public contract and must be maintained.

### III. Clean & Simple Code (KISS/DRY)
Favor readability and minimal complexity: small, single-purpose functions; eliminate duplication; prefer clear control flow over cleverness. Refactor routinely during the green phase to keep the design small and easy to change.

### IV. SOLID OOP with Dataclasses
When modeling domain state, use dataclasses as the default structure. Apply SOLID principles for objects with behavior, keeping responsibilities narrow and dependencies explicit. Composition is favored over inheritance except where a stable abstraction is clear.

### V. Decision Traceability via ADRs
Material architectural or process decisions require an ADR before implementation. ADRs capture context, options, and consequences, and are stored under version control to keep reasoning auditable.

### VI. Tooling & Quality Gates
Use the UV package manager for Python dependency and environment management, pytest for all testing, and git to track all project files. CI/local gates include: tests pass, coverage ≥80%, type hints present, and changes linked to relevant ADRs when decisions are involved.

## Technical Stack & Constraints

- Language: Python 3.12+ with type hints across all code paths.
- Dependency & environment management: UV; lockfiles committed.
- Testing: pytest is mandatory; red-green-refactor enforced; coverage ≥80%.
- Data modeling: dataclasses preferred for structured data.
- Repository hygiene: all project files tracked in git; no untracked runtime artifacts.

## Workflow & Quality Gates

1. Write ADRs for significant decisions before coding; reference them in related work.
2. Define tests with pytest first; run to red; implement to green; refactor while keeping tests green.
3. Enforce type hints and keep signatures current with behavior.
4. Reject changes that drop coverage below 80% or bypass tests/linters.
5. Code review verifies TDD evidence, typing, ADR links, and adherence to SOLID/KISS/DRY.

## Governance

- This constitution supersedes other guidance for engineering practice.
- Amendments require a documented change proposal (referencing affected principles), review, and recorded approval; accompany with ADRs when altering process or architecture.
- Versioning follows semantic rules: MAJOR for breaking/removing principles, MINOR for new principles or substantive guidance additions, PATCH for clarifications.
- Compliance is checked in every review: TDD trace (red/green), type hints, ADR references, coverage threshold, and stack/tooling adherence.

**Version**: 1.0.0 | **Ratified**: 2025-12-12 | **Last Amended**: 2025-12-12
