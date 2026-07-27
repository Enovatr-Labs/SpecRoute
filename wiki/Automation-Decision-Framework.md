# Automation Decision Framework

<!-- sources: agentic-docs/automation-decision-framework.md -->

**The single most cross-referenced doc in SpecRoute.** When you have a new task to automate, this framework tells you whether to build it as a skill, agent, command, or hook.

For the canonical version, see [`agentic-docs/automation-decision-framework.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/automation-decision-framework.md).

## Quick decision matrix

| Approach | Use when | Example | Location |
|---|---|---|---|
| **Skill** | You need an interactive workflow with parameters and decision points | Bootstrapping a new PRD with a guided template wizard | `skills/<name>/SKILL.md` |
| **Agent** | You need fully autonomous execution that runs to completion | Drafting a 23-section PRD body given a goal | `agents/examples/<name>.md` |
| **Command** | You need a simple, non-parameterized operation that always does the same thing | `/run-tests`, `/sanitize`, `/audit` | `commands/<name>.md` (Claude) |
| **Hook** | You need automatic enforcement on an event you can't predict | Block `git commit` if sanitization fails | `hooks/<vendor>/...` |

If none feel right, you may not have automated the right unit. Look at it again.

## Decision-tree shortcut

If you can answer "yes" to any of these, the answer is in parentheses:

- "Will the user invoke this by name?" + "Will it ask questions?" → **(Skill)**
- "Will the user delegate this and walk away?" → **(Agent)**
- "Will the user type `/<name>` and expect the same thing every time?" → **(Command)**
- "Should this run automatically when something happens?" → **(Hook)**

If two answers are "yes," the primitive split is wrong. Split into two artifacts.

## Detailed differentiators

### Skill — *interactive by design*
- ✓ Asks the user questions during execution.
- ✓ Validates inputs before each major step.
- ✓ Explains what it's doing.
- ✗ Not for one-shot deterministic operations.
- ✗ Not for fully autonomous execution.

### Agent — *autonomous by design*
- ✓ Zero user interaction during execution.
- ✓ Operates on the agent's brief.
- ✓ Can make judgment calls within scope.
- ✗ Not when the user wants to drive decisions.
- ✗ Not for trivial deterministic operations.

### Command — *deterministic by design*
- ✓ Single slash invocation.
- ✓ No parameters or one well-defined argument.
- ✓ Fast, consistent, easy to remember.
- ✗ Not for branching workflows.
- ✗ Not for tasks requiring user judgment mid-flow.

### Hook — *invisible by design*
- ✓ Triggered by an event, not user invocation.
- ✓ Sub-second execution target.
- ✓ Idempotent; fails closed.
- ✗ Not for slow operations.
- ✗ Not for actions needing user judgment.
- ✗ Not for things the user does once — those are commands.

## Anti-patterns

- **Skill that runs without user input** → that's an agent. Rename.
- **Agent that asks the user a series of questions** → that's a skill. Rename.
- **Command with 12 flags** → that's a skill. Refactor.
- **Hook that takes 5 seconds** → move work into an agent or command.
- **Hook that asks the user a question** → hooks can't ask. Use a skill.
- **Agent with no "Don't use for" section** → it will overlap with neighbors. Define boundaries.

## Composition

The four primitives compose — see [[Agentic Coding Model]] for the canonical composition pattern. A typical SpecRoute feature implementation uses all four.

## Worked examples (in this repo)

| Primitive | Where to find an example |
|---|---|
| Skill | [`.claude/skills/scaffold-artifact/SKILL.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/skills/scaffold-artifact/SKILL.md) |
| Agent | [`.claude/agents/prd-author.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/agents/prd-author.md) |
| Command | [`.claude/commands/audit.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/commands/audit.md) |
| Hook | [`.claude/hooks/pre-bash-sanitize.sh`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/hooks/pre-bash-sanitize.sh) |

Consumer-facing templates live under the corresponding top-level dirs.

## Vendor notes

- **Codex** has no separate command file in this framework. Equivalent: a skill invoked with `$name` or from `/skills`. Document this; do not add Claude-only frontmatter to make the analogy work.
- **All six vendors** ship hooks; per-vendor depth varies — Claude Code 30 events / Codex 11 / Gemini 11 / Kiro 10 / Cursor 21 / Devin Local 8. Cascade retains a separate 12-event compatibility surface. See [[Hooks]].

## See also

- [[Skills]] · [[Agents]] · [[Commands]] · [[Hooks]] — the per-primitive references
- [[Agentic Coding Model]] — how the four compose
- [[Implementation Team]] — 12 worked agents + 6 skills + 4 commands + 3 hooks
