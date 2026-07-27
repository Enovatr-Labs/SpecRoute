# Artifact Taxonomy

<!-- sources: AGENTS.md, README.md -->

Every artifact type SpecRoute defines has a template, a contract, an owner agent, and a place it lives. The canonical table lives in [`AGENTS.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/AGENTS.md); this page adds the contracts, relationships, and owners.

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

Those four are the whole set. **Orchestration is not a fifth primitive** — the `all-hands` pattern is a *composition*: a skill (the user-invoked coordinator) that delegates to agents, which trip hooks as they edit, and that runs commands as its validation gates. Nothing new is introduced; what is new is the coordination contract between them. See [[Multi-Agent Orchestration]].

For specification artifacts (PRD / spec / ADR), follow [[Spec-Driven Development]]:

- **PRD** — business intent, before any technical work begins.
- **Spec triplet** (requirements + design + tasks) — the technical contract per feature.
- **Lightweight feature spec** — for single-team, single-owner features.
- **Technical spec** — for non-product-facing work (refactors, migrations).
- **ADR** — for single architectural decisions.

## Frontmatter contracts

Some artifacts have required-field frontmatter. Miss a genuinely required field and the artifact won't register.

| Artifact | Required | Conventional (optional to the runtime) |
|---|---|---|
| Agent | `name`, `description` (with trigger phrases) | `model`, `color`; also `tools`, `memory`, `effort`, `isolation` where useful |
| Skill | `name`, `description` | `argument-hint`, `user-invocable`, `allowed-tools`, `disable-model-invocation` |
| Command (Claude) | nothing strictly | `description` — always set it; it is what `/help` shows |
| PRD | `Version`, `Date`, `Author`, `Status`, `Architecture Reference`, `Scope` | — |
| Spec file | `Version`, `Date`, `Author`, `Status`, `Source PRD` | `Source Requirements` / `Source Design` on downstream files |

For agents and skills only `name` and `description` are load-bearing; the rest is SpecRoute convention. Two corrections that bite:

- **`model` takes a real runtime value** — `opus`, `sonnet`, `haiku`, `fable`, `inherit`, or a full model id. The tier words `flagship` / `balanced` / `fast` are SpecRoute's **vendor-neutral abstractions for roster tables only**; one of them in a real agent file breaks the file. See [[Agents]] for the tier mapping.
- **`allowed-tools` pre-approves tools for the invoking turn — it does not restrict them.** The grant clears when the turn ends. To actually remove tools from the pool, use `disallowed-tools`.

Full per-field guidance: [[Frontmatter Contracts]]. The PostToolUse hook script `.claude/hooks/post-edit-frontmatter.sh` flags violations on save; it is wired from the `hooks` key of `.claude/settings.json`, not from `.claude/hooks/hooks.json` (see [[Hooks]]).

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
| Documentation currency | `docs-currency-auditor` |

`docs-currency-auditor` owns the *currency* of claims rather than the prose: vendor config surfaces, hook taxonomies, version anchors, transition dates, and counts that must still match disk. Its workflow ships as the `doc-currency-check` skill.

See [[Implementation Team]].

## See also

- [[Spec-Driven Development]] — how PRD / spec / impl / validation chain
- [[Automation Decision Framework]] — when to reach for skill vs agent vs command vs hook
- [[Frontmatter Contracts]] — the required-field details
- [[Multi-Agent Orchestration]] — how the four primitives compose into `all-hands`
