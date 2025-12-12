# Research: Interactive CLI Todo App

## Decisions

### Interaction stack (Questionary + Rich + Typer wrapper)
- **Decision**: Use Questionary for interactive menu/prompts, Rich for tables/messages, and Typer only as a minimal entry to start the loop.
- **Rationale**: Meets acceptance criteria for interactive selector and formatted views while keeping a single entrypoint; Typer provides simple CLI bootstrapping without per-action commands.
- **Alternatives considered**:
  - Plain `input/print`: simpler but fails the interactive selector requirement and produces poorer UX.
  - `curses` UI: richer control but higher complexity and less portability; unnecessary for scope.

### Task identity (incrementing int IDs per session)
- **Decision**: Assign tasks incremental integer IDs (or list indices) unique for the session.
- **Rationale**: Simple to present, easy for users to select via menu, no persistence needed.
- **Alternatives considered**:
  - UUIDs: unique but cumbersome to read/type in a CLI.
  - Titles-as-keys: conflicts on duplicates and complicates rename.

### Core logic separation
- **Decision**: Keep task operations in a pure in-memory module (functional helpers over a dataclass model) isolated from UI prompts/rendering.
- **Rationale**: Enables 100% unit coverage of core logic, simplifies testing, and aligns with TDD and clean separation.
- **Alternatives considered**:
  - Embedding logic in menu loop: faster to hack, but untestable and harder to maintain.
  - Class-heavy service layer: overkill for current scope; functional helpers suffice.

### Error handling and validation
- **Decision**: Validate non-empty titles; guard ID/index lookup with “task not found” messages; keep the app running and return to main menu after any error.
- **Rationale**: Matches acceptance criteria for graceful handling and resilience; avoids crashing the session.
- **Alternatives considered**:
  - Hard exits on invalid input: conflicts with requirements.
  - Silent failures: poor UX and unclear state.

### Testing strategy
- **Decision**: Unit tests for core task operations (add/view/update/delete/toggle) with pytest; light integration test to exercise menu flow and resilience to invalid inputs; target ≥80% overall and 100% for core logic.
- **Rationale**: Satisfies constitution gates (TDD, coverage) and acceptance criteria; keeps UI testing pragmatic.
- **Alternatives considered**:
  - Skipping integration: risks regressions in menu loop.
  - Heavy end-to-end harness: unnecessary for single-file entry CLI.
