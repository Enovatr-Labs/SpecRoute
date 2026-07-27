# Automation Decision Framework

**The single most cross-referenced doc in SpecRoute.** When you have a new task you want to automate, this framework tells you whether to build it as a skill, agent, command, or hook.

## Quick decision matrix

| Approach | Use when | Example | Location |
|---|---|---|---|
| **Skill** | You need an interactive workflow with parameters and decision points | Bootstrapping a new PRD with a guided template wizard | `skills/<name>/SKILL.md` |
| **Agent** | You need fully autonomous execution that runs to completion | Drafting a 23-section PRD body given a goal | `agents/examples/<name>.md` (consumer) or `.claude/agents/<name>.md` (project-internal) |
| **Command** | You need a simple, non-parameterized operation that always does the same thing | `/run-tests`, `/sanitize`, `/audit` | `commands/<name>.md` (Claude) or `.gemini/commands/<name>.toml` (Gemini) |
| **Hook** | You need automatic enforcement on an event you can't predict | Block `git commit` if sanitization fails; lint frontmatter on every Write | `hooks/<vendor>/...` |

If none feel right, you may not have automated the right unit. Look at it again.

## Detailed breakdown

### Skill (interactive workflows)

A skill is a parameterized, guided multi-step workflow. The user invokes it by name; the skill walks them through decisions, validates inputs at checkpoints, and produces an artifact or completes a task. Skills are **interactive by design** - that's the differentiator.

**When to use:**

- Multiple decision points (which artifact type? which vendor? which feature?).
- Validation checkpoints before destructive actions.
- Educational explanations during the workflow are valuable.
- The workflow varies based on user input.

**Characteristics:**

- ✓ Asks the user questions during execution.
- ✓ Validates inputs before each major step.
- ✓ Explains what it's doing.
- ✓ Safe for learning and exploration.
- ✗ Not appropriate for one-shot deterministic operations.
- ✗ Not appropriate for fully autonomous execution.

**Examples in this repo:**

- `scaffold-artifact` - interactive scaffolding for any artifact type with target-path resolution.
- `add-vendor` - walks a contributor through adding a new agent CLI to the matrix.
- `example-walkthrough` - guided end-to-end build of `examples/sample-project/`.
- `frontmatter-lint` - interactive frontmatter validation with offered fixes.
- `all-hands` - multi-agent orchestration across the implementation roster.
- `doc-currency-check` - audits the docs for claims that have gone stale.

**Usage pattern:**

```
User: "scaffold a new PRD for notification preferences"
Skill: "Which template? (full 23-section / lightweight / SRS)"
User: "lightweight"
Skill: "Slug?"
User: "notification-preferences"
Skill: <copies template, prefills frontmatter, asks about next steps>
```

### Agent (autonomous execution)

An agent is a defined role with a specific brief that runs autonomously to completion. The user delegates a task; the agent produces an output. Agents are **autonomous by design** - that's the differentiator.

**When to use:**

- Task is well-defined enough to run without check-ins.
- The user wants delegation, not collaboration.
- Background or scheduled work where no human is in the loop.
- Domain expertise is required and you've encoded it in an agent's operating principles.

**Characteristics:**

- ✓ Zero user interaction during execution.
- ✓ Operates on predefined logic and the agent's brief.
- ✓ Can make judgment calls within scope.
- ✓ Returns a structured output.
- ✗ Not appropriate when the user wants to drive decisions.
- ✗ Not appropriate for trivial deterministic operations.

**Examples in this repo (the implementation team):**

- `prd-author` - drafts PRD content from a brief.
- `spec-author` - produces the spec triplet for a given PRD.
- `sanitization-auditor` - scans tracked files for forbidden strings, blocks commits.
- `template-quality-reviewer` - reviews templates against the production-grade bar.

**Usage pattern:**

```
User: "have spec-author draft the requirements for the user-search example"
Agent: <reads the PRD, drafts requirements.md with stable IDs, returns artifact>
```

### Command (simple operations)

A command is a slash-invoked operation that does one thing. No parameters (or one well-defined argument). Always behaves the same way. Commands are **deterministic by design** - that's the differentiator.

**When to use:**

- Frequently-used operations.
- No configuration needed.
- Quick status checks or pre-baked validations.
- Operations suitable for muscle memory / keyboard shortcuts.

**Characteristics:**

- ✓ Single slash invocation.
- ✓ No parameters or one well-defined argument.
- ✓ Fast execution.
- ✓ Consistent, repeatable behavior.
- ✓ Easy to remember.
- ✗ Not appropriate for branching workflows.
- ✗ Not appropriate for tasks requiring user judgment mid-flow.

**Examples in this repo:**

- `/sanitize` - string-level scan for forbidden terms.
- `/status` - skeleton state report.
- `/audit` - comprehensive pre-commit check.
- `/parity` - cross-vendor runtime parity check.

**Usage pattern:**

```
User: "/audit"
Command: <runs sanitization, frontmatter checks, matrix consistency, broken-link check, TODO health>
Output: <punch list of findings or PASS>
```

**Vendor note:** Codex has no separate command file in this framework. The equivalent is a skill invoked with `$name` or from `/skills`. Document this equivalence; do not add Claude-only frontmatter to make the analogy work.

### Hook (event-triggered automation)

A hook is automation that runs on an event the user didn't explicitly invoke. Pre-commit checks, file-edit validators, session-start banners. Hooks are **invisible by design** - that's the differentiator.

**When to use:**

- A check or action that *must* run on every relevant event.
- Validation that needs to fail-closed.
- Background information that's useful but not worth interrupting for.
- Cross-cutting enforcement that's tedious to remember manually.

**Characteristics:**

- ✓ Triggered by an event, not user invocation.
- ✓ Sub-second execution target.
- ✓ Idempotent.
- ✓ Fails closed (exit non-zero blocks the action).
- ✗ Not appropriate for slow operations.
- ✗ Not appropriate for actions that need user judgment.
- ✗ Not appropriate for things the user does once and forgets - those are commands.

**Examples in this repo:**

- `SessionStart` - prints a SpecRoute skeleton status banner so Claude orients without re-grepping.
- `PreToolUse` (Bash) - blocks `git commit`/`git push` if sanitization wordlist matches in tracked files.
- `PostToolUse` (Write|Edit) - validates frontmatter on agent/skill/command file writes; reports via `systemMessage` so the warning is actually visible in-session.

**Usage pattern:**

```
User: "git commit -m '...'"
Hook (PreToolUse): <reads .claude/.forbidden-strings.txt, runs git grep, exits 0 or 1>
Bash: <only runs if hook exited 0>
```

**Vendor support:** All six supported vendors ship a hooks system, but the taxonomies are **not** interchangeable. Depth varies (Claude Code 30 events / 5 handler types; Codex 11; Gemini CLI 11; Kiro 10; Cursor 21; Devin Local 8). Claude Code, Codex, Kiro, and Devin Local share several event names, but payloads and decision schemas still differ; Cursor uses camelCase and Gemini uses `BeforeTool` / `AfterModel`. Porting registration between vendors remains a rewrite. See [`hooks/README.md`](../hooks/README.md) for the full matrix.

## Decision-tree shortcut

If you can answer "yes" to any of these, the answer is in the parentheses:

- "Will the user invoke this by name?" + "Will it ask them questions?" → **(Skill)**
- "Will the user delegate this and walk away?" → **(Agent)**
- "Will the user type `/<name>` and expect the same thing every time?" → **(Command)**
- "Should this run automatically when something happens?" → **(Hook)**

If two answers are "yes," the primitive split is wrong. Split the work into two artifacts, each owning its concern.

## Anti-patterns

- **Skill that runs without user input.** That's an agent. Rename it.
- **Agent that asks the user a series of questions.** That's a skill. Rename it.
- **Command with 12 flags.** That's a skill. Refactor.
- **Hook that takes 5 seconds to run.** Move the work into an agent or command; hooks must be fast.
- **Hook that asks the user a question.** Hooks can't ask. Use a skill.
- **Agent with no "Don't use for" section.** It will overlap with neighbors. Define boundaries.

## Composition

The four primitives compose. A typical SpecRoute feature implementation uses all four - see [`agentic-coding-model.md`](agentic-coding-model.md) for the composition pattern.

### Multi-agent orchestration

One composition is common enough to have a name: a **skill whose work product is delegation**. The user invokes one entry point; it triages the work, fans it out across the relevant agents in parallel waves, synthesizes their output, runs the validation commands, and reports.

This is not a fifth primitive - it is skill + agents + commands + hooks wired together:

```
Skill (the coordinator)  →  Agents (the specialists)  →  Commands (the gates)
                                    ↕
                              Hooks (always-on, firing on every edit)
```

It looks like it breaks the decision tree above - the user invokes it by name *and* it runs autonomously. It doesn't: the coordinator asks the user nothing about *how* to do the work, it asks the roster. Reach for it when a change implicates several specialists and the user shouldn't have to know which ones.

Don't reach for it when one agent obviously owns the work - the coordination overhead is real. See [`multi-agent-orchestration.md`](multi-agent-orchestration.md) for the six mechanisms a working orchestrator needs, and [`.claude/skills/all-hands/SKILL.md`](../.claude/skills/all-hands/SKILL.md) for this repo's instance.

## Worked examples in this repo

| Pattern | Where to find an example |
|---|---|
| Skill | `.claude/skills/scaffold-artifact/SKILL.md` |
| Agent | `.claude/agents/prd-author.md` |
| Command | `.claude/commands/audit.md` |
| Hook | `.claude/hooks/pre-bash-sanitize.sh` (script) wired in `.claude/settings.json` (`hooks` key) |
| Multi-agent orchestration | `.claude/skills/all-hands/SKILL.md` |

These are the implementation team's primitives. Consumer-facing templates live under the corresponding top-level dirs (`skills/`, `agents/`, `commands/`, `hooks/`).
