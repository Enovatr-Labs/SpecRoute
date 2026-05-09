# `.claude/agents/` - User-Search Implementation Team

The 8 agents that drive the user-search feature implementation. They map to the role assignments in [`agent-roster.md`](../../agent-roster.md) and the per-task assignments in [`tasks.md`](../../tasks.md).

## Roster

| Agent | Role | Model | Color | Tasks |
|---|---|---|---|---|
| [`prd-author`](prd-author.md) | PRD owner + documentation | opus | blue | (PRD revisions), 21 |
| [`backend-engineer`](backend-engineer.md) | Backend implementation | opus | green | 1, 2, 5-12, 18, 19, 20, 22 |
| [`frontend-engineer`](frontend-engineer.md) | Frontend implementation | opus | yellow | 13-17, 19 |
| [`database-engineer`](database-engineer.md) | Schema + migration | sonnet | orange | 4 |
| [`security-auditor`](security-auditor.md) | Security review + privacy | opus | red | 3, reviews 6, 8, 11, 12 |
| [`unit-test-writer`](unit-test-writer.md) | Unit tests | sonnet | yellow | embedded across 5-9, 11, 12, 13-16 |
| [`integration-test-generator`](integration-test-generator.md) | Integration + E2E tests | sonnet | red | 10, 12, 17 |
| [`deployment-validator`](deployment-validator.md) | Load test + rollout + drill | sonnet | pink | 4 (validation), 18, 20, 22 |

## How to invoke

Each agent has trigger phrases in its `description` frontmatter. Claude Code auto-selects when those phrases appear in your prompt. You can also invoke explicitly via the Task tool: `subagent_type: backend-engineer`.

For task-driven work, the typical flow is:

1. Open the relevant numbered task prompt under [`../../prompts/phase{N}_<phase>/`](../../prompts/).
2. The prompt names the **Primary Agent** in its Section 3 (Agent Assignment).
3. Invoke that agent with the task prompt as input.
4. Supporting agents are listed in the same section - delegate sub-tasks to them as the primary agent identifies.

## Customizing for your stack

This roster targets a representative product stack (relational DB, REST API, web frontend). Adapt for your specifics:

- Swap the implementation languages in each agent's operating principles (e.g. "parameterized SQL" -> "parameterized GraphQL" if you're using GraphQL).
- Add agents your stack requires (e.g. `mobile-engineer` if you have a mobile surface).
- Remove agents you don't need (e.g. drop `database-engineer` if your project is purely API-gateway-only).

The frontmatter contract (`name`, `description` with triggers, `model`, `color`) stays the same regardless.

## Mirror to Codex

If you also target Codex, mirror these agents into `.codex/agents/<name>.md` (same shape) and run `tools/sync-skills.py` (which also handles agents) from the SpecForge framework to detect drift.
