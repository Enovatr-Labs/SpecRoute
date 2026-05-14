# Automation Decision Framework: User Search

When this project reaches for which primitive. Concrete from the project's own choices.

## Quick decision matrix

| Approach | Use when | Examples in this project |
|---|---|---|
| **Skill** | Interactive parameterized workflow | (none currently used) |
| **Agent** | Autonomous multi-step task with a clear role | All 8 agents in [`.claude/agents/`](../.claude/agents/) |
| **Command** | Simple non-parameterized check or report | `/sanitize`, `/audit`, `/status`, `/parity` |
| **Hook** | Automatic enforcement on a specific event | SessionStart status, PreToolUse sanitization gate, PostToolUse frontmatter check |

## Why skills aren't used here

Each task in `tasks.md` is well-scoped enough that an agent can execute against it without asking the user mid-stream. The task prompt itself carries the full context. If we found ourselves writing a prompt that asked the user "which file? which environment? which mode?" mid-execution, we'd build a skill. Currently the project's work decomposes neatly into agent-driven task execution.

Likely candidates if scope grew:

- A `scaffold-adr` skill that interactively walks a user through creating a new ADR (number, title, status, sections).
- A `release-readiness` skill that asks the user to confirm each item on the [release-readiness checklist](https://github.com/Enovatr-Labs/SpecRoute/blob/main/workflows/release-readiness.md) before approving the next rollout stage.

## Why agents are the workhorse

The 8 agents map 1:1 to roles in `agent-roster.md`. Each task in `tasks.md` names a primary agent in its Section 3. The mapping makes invocation natural - the user (or another agent) reads the task and invokes the named agent.

The boundaries are crisp:

- `backend-engineer` does not write tests as a primary deliverable - they delegate to `unit-test-writer` / `integration-test-generator`.
- `frontend-engineer` does not implement the API - they consume the API contract from `design.md`.
- `security-auditor` does not implement features - they review the boundary-critical PRs.
- `database-engineer` owns the schema migration only; the application code is `backend-engineer`'s scope.

When boundaries blur, we update each agent's "Don't use for" section.

## Why we have four commands

Each command answers a question the team asks frequently with no parameters:

- `/sanitize` - "is anything forbidden in tracked files?"
- `/audit` - "is this branch ready to commit?"
- `/status` - "where are we across the project?"
- `/parity` - "are runtime mirrors aligned?" (relevant if multi-vendor; currently a no-op in this Claude-only project but kept for symmetry)

If a check needed parameters (e.g. "audit just the files changed in the last 7 days"), it would become a skill.

## Why we have three hooks

Each hook enforces something the team cannot afford to forget:

| Hook | What it enforces | Cost of failure |
|---|---|---|
| `pre-bash-sanitize.sh` | No forbidden strings in commits/pushes | Privacy / compliance leak in tracked files |
| `post-edit-frontmatter.sh` | Frontmatter contracts on agents / skills / commands | Agents fail to register; team debugs why nothing's loading |
| `session-start-status.sh` | Orientation at session start | None (informational); but cheap and helpful |

The PreToolUse hook is the only one that blocks. PostToolUse warns; SessionStart is informational.

## Anti-patterns we avoided

- **Hook overuse**: we have 3, not 30. Each one earns its place.
- **Agent overlap**: every agent has a "Don't use for" section pointing at the right neighbor.
- **Command stuffing**: 4 commands, all parameter-less. If we needed `/audit --since=...` it'd be a skill.
- **Skill sprawl**: zero skills, because zero workflows benefit from interactive prompting in this project.

## See also

- The framework's canonical [`agentic-docs/automation-decision-framework.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/automation-decision-framework.md) for the full theory and anti-patterns.
- [`agentic-coding-model.md`](agentic-coding-model.md) - how the primitives compose in this project.
- [`.claude/agents/README.md`](../.claude/agents/README.md) - the agent roster.
