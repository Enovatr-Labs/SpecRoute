---
name: scaffold-artifact
description: Interactive scaffolding for any SpecRoute artifact (PRD, spec, agent, skill, command, hook, prompt, runtime layout). Asks for artifact type and vendor (where applicable), copies the canonical template, generates the directory structure, and pre-fills the frontmatter. Use when starting a new artifact under prds/, specs/, agents/, skills/, commands/, hooks/, prompts/, or runtimes/.
argument-hint: "[artifact-type] [name] [vendor?]"
user-invocable: true
allowed-tools: Read Write Edit Glob Bash
---

# Scaffold Artifact

Interactive scaffolding for SpecRoute contributors. Reduces "where does this file go and what frontmatter does it need" friction.

## When to use

- Starting a new PRD, spec triplet, ADR, agent, skill, command, hook, or prompt
- Adding a new vendor runtime layout under `runtimes/`
- Bootstrapping the worked example in `examples/sample-project/`

## Step 1: Parse the argument

Argument shape: `[artifact-type] [name] [vendor?]`. Examples:

- `prd notification-preferences`
- `spec-triplet user-search`
- `agent backend-engineer`
- `skill manifest-audit`
- `command claude /run-checks`
- `hook claude pre-commit-sanitize`
- `runtime cursor`

If the argument is missing or unclear, ask the user:

1. Which artifact type? (PRD / lightweight PRD / SRS / spec triplet / feature spec / ADR / agent / skill / command / hook / prompt / runtime)
2. Name (slug, lowercase-hyphenated)?
3. If vendor-specific (command, hook, runtime, prompt): which vendor (claude / codex / gemini / kiro / cursor / windsurf)?

## Step 2: Resolve target path and template

Use the artifact-type → location mapping:

| Type | Target | Template |
|---|---|---|
| `prd` | `prds/active/<name>.md` | `prds/templates/prd-template.md` |
| `lightweight-prd` | `prds/active/<name>.md` | `prds/templates/lightweight-prd-template.md` |
| `srs` | `prds/active/<name>-srs.md` | `prds/templates/platform-srs-template.md` |
| `spec-triplet` | `specs/examples/<name>/{requirements,design,tasks}.md` | `specs/templates/{requirements,design,tasks}-template.md` |
| `feature-spec` | `specs/examples/<name>.md` | `specs/templates/feature-spec-template.md` |
| `adr` | `specs/examples/adr-<NNN>-<name>.md` | `specs/templates/architecture-decision-record.md` |
| `agent` | `agents/examples/<name>.md` | `agents/agent-template.md` |
| `skill` | `skills/examples/<name>/SKILL.md` | `skills/skill-template/SKILL.md` |
| `command` (claude) | `commands/examples/<name>.md` | `commands/command-template.claude.md` |
| `command` (gemini) | (entry in `commands/examples/<name>.gemini.json`) | `commands/command-template.gemini.json` |
| `hook` (claude) | `hooks/claude/<name>.sh` + entry in `hooks/claude/hooks.template.json` | `hooks/claude/hooks.template.json` |
| `hook` (kiro) | `hooks/kiro/examples/<name>.kiro.hook` | (existing example) |
| `prompt` | `prompts/<vendor>/<name>.md` or `prompts/shared/<name>.md` | `prompts/shared/task-prompt-template.md` |
| `runtime` | `runtimes/.<vendor>/` | (mirror nearest existing runtime) |

## Step 3: Create the file(s)

1. Read the template.
2. Replace `<name>` placeholders with the user-provided slug.
3. Pre-fill frontmatter where possible (e.g. `name: <slug>`, today's date).
4. Mark non-derivable fields with `TODO`.
5. Write the file. For spec triplets, write all three.

## Step 4: Report

Report what was created and the next steps:

- Files created (paths)
- Frontmatter fields the user must fill in
- Suggested next agent to invoke (e.g. for a new PRD: "draft Section 1 with `prd-author`")
- Whether the matching example or runtime mirror needs updating

## Step 5: Cross-vendor reminder

If the artifact is vendor-specific (skill, agent, command), remind the user:

- Skills and agents typically need a mirror in `runtimes/.<other-vendor>/` - invoke `runtime-architect` or run the `/parity` command afterward.
- Commands have different shapes per vendor - see `commands/README.md`.

## Don't use for

- Editing existing artifacts (use `Edit` directly).
- Bulk operations (use the dedicated agent - `prd-author`, `spec-author`, etc.).
- Filling in TODO content (that's the artifact author's job, not the scaffolder's).
