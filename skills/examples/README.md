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

The four skills under [`.claude/skills/`](../../.claude/skills/) at the repository root are real, tracked implementations of the contract. Read them as worked examples:

- `scaffold-artifact/SKILL.md` - interactive scaffolding for any SpecForge artifact type
- `add-vendor/SKILL.md` - walks a contributor through adding a new agent CLI to the matrix
- `example-walkthrough/SKILL.md` - guided end-to-end build of `examples/sample-feature/`
- `frontmatter-lint/SKILL.md` - interactive frontmatter validation across artifacts

## Adding an example skill

1. Pick a generic, non-domain-specific operation (manifest audit, doc-link checker, naming-convention enforcement, dependency report). Avoid deployment skills tied to specific infrastructure.
2. Create `<slug>/SKILL.md` here using [`../skill-template/SKILL.md`](../skill-template/SKILL.md).
3. Number the steps. Skills feel guided when each step is explicit.
4. Specify `allowed-tools` minimally.
5. Mirror to `runtimes/.claude/skills/<slug>/SKILL.md` and `runtimes/.codex/skills/<slug>/SKILL.md` if it should ship as part of the runtime.
6. Run `/audit` to validate frontmatter and run `/parity` to confirm cross-runtime alignment.

## Skills vs agents vs commands vs hooks

If you're not sure whether your idea is a skill, see [`docs/automation-decision-framework.md`](../../docs/automation-decision-framework.md). Quick test:

- **Will the user invoke it by name AND will it ask them questions?** → Skill.
- **Will the user delegate to it and walk away?** → Agent.
- **Will the user type `/<name>` and expect identical behavior every time?** → Command.
- **Should it run automatically when something happens?** → Hook.
