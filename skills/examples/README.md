# Skill Examples

Concrete skills demonstrating the folder-per-skill convention. Each example is a directory containing `SKILL.md`; optional sibling dirs (`scripts/`, `agents/`) hold supporting files.

```
skills/examples/
├── README.md                            (this file)
└── <skill-name>/
    ├── SKILL.md                         required
    ├── scripts/                         optional supporting scripts
    └── agents/                          optional skill-scoped sub-agents
```

## Reference implementations

The skills under [`.claude/skills/`](../../.claude/skills/) at the repository root are real, tracked implementations of the contract. Read them as worked examples:

- `scaffold-artifact/SKILL.md` - interactive scaffolding for any SpecRoute artifact type
- `add-vendor/SKILL.md` - walks a contributor through adding a new agent CLI to the matrix
- `example-walkthrough/SKILL.md` - guided end-to-end build of `examples/sample-project/`
- `frontmatter-lint/SKILL.md` - interactive frontmatter validation across artifacts
- `all-hands/SKILL.md` - multi-agent orchestration over this repo's own agent roster
- `doc-currency-check/SKILL.md` - repeatable version, vendor-fact, count, tense, and mirror audit

## Examples in this directory

- `audit-artifact/SKILL.md` - guided readiness review of a single artifact
- `all-hands/SKILL.md` - the orchestration template, with `<placeholder>` departments to replace. See [`agentic-docs/multi-agent-orchestration.md`](../../agentic-docs/multi-agent-orchestration.md) for the pattern it implements.

## Adding an example skill

1. Pick a generic, non-domain-specific operation (manifest audit, doc-link checker, naming-convention enforcement, dependency report). Avoid deployment skills tied to specific infrastructure.
2. Create `<slug>/SKILL.md` here using [`../skill-template/SKILL.md`](../skill-template/SKILL.md).
3. Number the steps. Skills feel guided when each step is explicit.
4. Specify `allowed-tools` minimally - it pre-approves tools for the invoking turn (fewer prompts), it does not restrict the skill. Use `disallowed-tools` to actually remove tools.
5. Mirror to `runtimes/.<vendor>/skills/<slug>/SKILL.md` for every runtime it should ship in - as of the mid-2026 convergence all supported vendors carry folder-per-skill `SKILL.md`. Use [`tools/sync-skills.py`](../../tools/sync-skills.py) to copy the body across runtimes; it preserves each vendor's own frontmatter.
6. Run `/audit` to validate frontmatter and run `/parity` to confirm cross-runtime alignment.

## Skills vs agents vs commands vs hooks

If you're not sure whether your idea is a skill, see [`agentic-docs/automation-decision-framework.md`](../../agentic-docs/automation-decision-framework.md). Quick test:

- **Will the user invoke it by name AND will it ask them questions?** → Skill.
- **Will the user delegate to it and walk away?** → Agent.
- **Will the user type `/<name>` and expect identical behavior every time?** → Command.
- **Should it run automatically when something happens?** → Hook.
