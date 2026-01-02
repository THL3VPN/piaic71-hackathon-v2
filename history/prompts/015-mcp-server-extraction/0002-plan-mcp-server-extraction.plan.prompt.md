---
id: 0002
title: plan-mcp-server-extraction
stage: plan
date: 2026-01-02T02:43:17+05:00
surface: cli
model: gpt-5
feature: 015-mcp-server-extraction
branch: 015-mcp-server-extraction
user: user
command: /sp.plan
labels: [plan, step6, mcp]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/plan.md
  - /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/research.md
  - /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/data-model.md
  - /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/contracts/mcp-tools.openapi.yaml
  - /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/quickstart.md
  - /home/aie/all_data/piaic71-hackathon-v2/AGENTS.md
tests: []
---

## Prompt

## User Input

```text

```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/bash/setup-plan.sh --json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Response snapshot

Created plan, research, data-model, contracts, and quickstart for MCP server extraction; updated agent context.

## Outcome

- ✅ Impact: Phase 0/1 planning artifacts generated for MCP server extraction.
- 🧪 Tests: Not run (plan-only changes).
- 📁 Files: specs/015-mcp-server-extraction/plan.md, specs/015-mcp-server-extraction/research.md, specs/015-mcp-server-extraction/data-model.md, specs/015-mcp-server-extraction/contracts/mcp-tools.openapi.yaml, specs/015-mcp-server-extraction/quickstart.md, AGENTS.md
- 🔁 Next prompts: Proceed to `/sp.tasks` for task breakdown.
- 🧠 Reflection: Keep MCP extraction aligned with Step 5 behavior guarantees.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): N/A
