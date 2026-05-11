# Artifact Taxonomy

<!-- sources: AGENTS.md, README.md -->

SpecForge defines nine artifact types. Each has a template, a contract, an owner agent, and a place it lives.

| Artifact | What it is | Lives in | Wiki page |
|---|---|---|---|
| **PRD** | Business intent, goals, scope, success metrics | `prds/` | [[PRDs]] |
| **Spec** | Requirements + design + tasks (or single feature spec) | `specs/` | [[Specs]] |
| **Agent** | Defined role + model + tools, invokable by a runtime | `agents/` | [[Agents]] |
| **Skill** | Interactive parameterized workflow (`SKILL.md` per skill) | `skills/` | [[Skills]] |
| **Command** | Simple slash-invoked operation, vendor-specific shape | `commands/` | [[Commands]] |
| **Hook** | Event-triggered automation (file-edit, pre-commit, session-start) | `hooks/` | [[Hooks]] |
| **Prompt** | Reusable prompt — global master, phase master, or task | `prompts/` | [[Prompts]] |
| **Workflow** | End-to-end execution model | `workflows/` | [[Workflows]] |
| **Rule** | Engineering standard, vendor-specific or shared | `rules/` | [[Rules]] |
| **Runtime** | Copy-pasteable per-vendor layout consumers drop into their own repos | `runtimes/` | [[Vendor Matrix]] / [[Agent CLI Integrations]] |

## When to reach for which

For automation primitives (skill / agent / command / hook), apply [[Automation Decision Framework]]:

- "Will the user invoke this by name?" + "Will it ask questions?" → **Skill**
- "Will the user delegate this and walk away?" → **Agent**
- "Will the user type `/<name>` and expect the same result every time?" → **Command**
- "Should this run automatically when something happens?" → **Hook**

For specification artifacts (PRD / spec / ADR), follow [[Spec-Driven Development]]:

- **PRD** — business intent, before any technical work begins.
- **Spec triplet** (requirements + design + tasks) — the technical contract per feature.
- **Lightweight feature spec** — for single-team, single-owner features.
- **Technical spec** — for non-product-facing work (refactors, migrations).
- **ADR** — for single architectural decisions.

## Frontmatter contracts (load-bearing)

Several artifacts have required-field frontmatter that the runtime validates. Missing fields = the artifact won't register.

| Artifact | Required fields |
|---|---|
| Agent | `name`, `description` (with trigger phrases), `model`, `color` |
| Skill | `name`, `description`, `argument-hint`, `user-invocable`, `allowed-tools` |
| Command (Claude) | `description` |
| PRD | `Version`, `Date`, `Author`, `Status`, `Architecture Reference`, `Scope` |
| Spec file | `Version`, `Date`, `Author`, `Status`, `Source PRD` (+ `Source Requirements` / `Source Design` for downstream files) |

Full per-field guidance: [[Frontmatter Contracts]]. The PostToolUse hook (`.claude/hooks/post-edit-frontmatter.sh`) flags violations on save.

## Cross-artifact relationships

```
PRD ──drives──> requirements.md ──drives──> design.md ──drives──> tasks.md
                       ↑                          ↑                    ↑
                       └──────── back-refs ───────┴────────────────────┘
                                                                       │
                                                                       ▼
                                                              code + tests
                                                                       │
                                                                       ▼
                                                              validation report
                                                                       │
                                                                       ▼
                                                              PR + review + merge
```

- **Stable IDs are load-bearing.** Once `R1.1` is published, the ID never gets reused. Tasks, PRs, commits, tests all cross-reference requirements without fear of drift.
- **Tasks back-reference requirements.** `_Requirements: R1.1, R1.2_` at the end of every task. Tasks without back-refs are unscoped.
- **Tests back-reference requirements.** One or more tests per requirement, asserting the acceptance criteria.

## Owner agents

Each artifact type has a primary author agent:

| Artifact | Owner agent (in `.claude/agents/`) |
|---|---|
| PRD | `prd-author` |
| Spec | `spec-author` |
| Agent definition / roster | `agent-roster-architect` |
| Skill | `skill-author` |
| Command | `command-author` |
| Hook | `hooks-author` |
| Prompt | `prompt-engineer` |
| Workflow / docs / rule | `framework-docs-author` |
| Runtime layout | `runtime-architect` |
| Sanitization | `sanitization-auditor` |
| Template quality | `template-quality-reviewer` |

See [[Implementation Team]].

## See also

- [[Spec-Driven Development]] — how PRD / spec / impl / validation chain
- [[Automation Decision Framework]] — when to reach for skill vs agent vs command vs hook
- [[Frontmatter Contracts]] — the required-field details
