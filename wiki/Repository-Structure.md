# Repository Structure

<!-- sources: README.md, AGENTS.md -->

```
specroute/
├── AGENTS.md                  canonical, vendor-neutral root context
├── CLAUDE.md / GEMINI.md      per-vendor delegation shims
├── README.md / ROADMAP.md     project framing
│
├── agentic-docs/              conceptual deep references (philosophy, decision frameworks)
├── prds/                      PRD templates, lifecycle dirs (active / deprecated / archive), examples
├── specs/                     spec triplet templates (requirements, design, tasks), ADR, feature spec
├── agents/                    agent template, 7 archetypes, examples, cross-vendor roster
├── skills/                    skill-template/SKILL.md + examples (folder-per-skill convention)
├── commands/                  per-vendor command templates (Claude markdown, Gemini JSON)
├── hooks/                     per-vendor hook templates covering all six vendors
├── prompts/                   shared/, claude/, codex/ prompt sets + master-prompt trio
├── workflows/                 5 end-to-end execution playbooks
├── rules/                     engineering / code-review / security / docs rules + per-vendor surfacing
├── runtimes/                  copy-pasteable per-vendor runtime layouts + MCP single source
├── tools/                     sync-skills.py and other utility scripts
├── examples/                  sample-project/ canonical worked example
├── assets/                    images and diagrams
│
└── .claude/                   THIS repo's implementation-team runtime — not the consumer template
    ├── agents/                11 implementation agents
    ├── skills/                4 contributor skills (scaffold-artifact, add-vendor, …)
    ├── commands/              4 slash commands (/audit, /parity, /sanitize, /status)
    ├── hooks/                 SessionStart banner, PreToolUse sanitize gate, PostToolUse frontmatter
    └── agent-memory/          per-agent persistent context
```

## Two distinct concerns

**Consumer-facing templates** live under top-level directories (`prds/`, `specs/`, `agents/`, `skills/`, `commands/`, `hooks/`, `prompts/`, `rules/`, `runtimes/`, `examples/`).

**The implementation team that builds SpecRoute itself** lives under `.claude/`. Don't confuse the two. The consumer drops `runtimes/.claude/` into their own repo; they do *not* copy `.claude/`. See [[Implementation Team]].

## Where do new docs go?

| What you're adding | Where |
|---|---|
| A new template or example | The corresponding top-level directory (e.g. `prds/templates/`, `agents/examples/`) |
| Conceptual or framework-level reference | `agentic-docs/` |
| Recurring engineering procedure | `workflows/` |
| Standing engineering standard | `rules/` |
| Directory-specific guidance | That directory's `README.md` |
| Per-vendor configuration / setup | `runtimes/.<vendor>/` |

See [[Documentation Structure]] for the full decision tree.

## Per-directory READMEs

Every directory ships a `README.md`. Treat those as the authoritative answer to "what belongs here and how do I add to it?" The wiki pages summarize and link out:

- [[PRDs]] · [[Specs]] · [[Agents]] · [[Skills]] · [[Commands]] · [[Hooks]] · [[Prompts]] · [[Rules]]
- [[Workflows]] · [[Vendor Matrix]] (for `runtimes/`)
- [[Worked Example]] (for `examples/`)

## File extensions and conventions

- Templates and content: `.md` (Markdown).
- Frontmatter: YAML at the top, fenced by `---`. Required fields vary by artifact — see [[Frontmatter Contracts]].
- Scripts: bash for hooks; Python 3 for tooling. No external runtime dependencies.
- Vendor-specific files keep their native shape (Gemini's `.gemini/commands/*.toml` and `config.toml` stay TOML; Codex's `config.toml` stays TOML; Kiro's `*.kiro.hook` stays JSON).

## What this repo is NOT

- Not a package manager — there's no `package.json` or build step.
- Not a code generator — no runtime emits files.
- Not vendor-specific tooling — patterns work across all six supported CLIs.
- Not a place for proprietary business logic — sanitization is non-negotiable. See [[Sanitization]].

## See also

- [[Quickstart]] · [[Worked Example]]
- [[Documentation Structure]] — the full decision tree for new docs
- [[Implementation Team]] — what `.claude/` contains and how it's wired
