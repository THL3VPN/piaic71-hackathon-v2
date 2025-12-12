# Implementation Plan: Interactive CLI Todo App

**Branch**: `001-interactive-todo-cli` | **Date**: 2025-12-12 | **Spec**: specs/001-interactive-todo-cli/spec.md
**Input**: Feature specification from `/specs/001-interactive-todo-cli/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deliver a single-entry (`python main.py`) interactive CLI todo app that keeps tasks in memory for the session. Present a persistent main menu with options to view, add, update, delete, toggle completion, and exit. Core task logic is separated from the UI to enable full unit coverage; UI uses Questionary for prompts and Rich for rendering, with Typer as the minimal entry wrapper.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.12+ (required)  
**Primary Dependencies**: UV-managed Python packages: typer (entry wrapper), questionary (interactive menus), rich (tables/messages), pytest (tests)  
**Storage**: In-memory only (no filesystem, no DB)  
**Testing**: pytest (required), target ≥80% overall coverage and 100% for core task logic  
**Target Platform**: Interactive CLI on Linux/macOS terminals (assumed)  
**Project Type**: Single CLI application  
**Performance Goals**: Sub-100ms response per menu action; instant menu return after each action  
**Constraints**: Coverage ≥80%, type hints everywhere using `|` unions, dataclasses for data structures, TDD red-green-refactor, simple functional approach where sensible, ADRs for material decisions  
**Scale/Scope**: Single-user, single-session task list; modest task counts (<1k items) in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests defined first (pytest), executed to red, then implemented to green; plan commits to red-green-refactor.
- Python 3.12+ with type hints everywhere; dataclasses for task data structures.
- UV as package/environment manager; dependencies: typer, questionary, rich, pytest.
- Quality bars: maintain ≥80% coverage overall and 100% for core task logic; ADRs if architecture/process decisions change materially. No violations identified.

## Project Structure

### Documentation (this feature)

```text
specs/001-interactive-todo-cli/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
├── models/
│   └── task.py           # Task dataclass
├── services/
│   └── task_store.py     # In-memory task operations (functional helpers)
├── cli/
│   ├── menu.py           # Menu definitions, questionary prompts
│   ├── render.py         # Rich-based render helpers
│   └── app.py            # Loop orchestrator using task_store + menu
└── main.py               # Typer entrypoint to launch app loop

tests/
├── unit/
│   └── test_task_store.py
├── integration/
│   └── test_cli_flow.py  # Light UI flow checks (can stub input)
└── contract/
    └── test_menu_contract.py (optional: menu options/labels)
```

**Structure Decision**: Single CLI project under `src/` with core logic separated from UI; tests mirror `src` with unit and integration coverage.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (none) | - | - |
