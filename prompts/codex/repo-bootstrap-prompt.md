# Codex: Repo Bootstrap Prompt

Bootstrap a new repository with SpecRoute structure under Codex.

---

## Role

You are a repo bootstrapper. Your output is a populated SpecRoute skeleton in a new (or empty) repository.

## Inputs

- Target repo path: `<path>`
- Project name: `<name>`
- Vendors to support: `<comma-separated list, e.g. claude, codex, gemini>`

## Process

1. Confirm `<path>` exists and is empty (or has only `README.md` / `LICENSE`).
2. From a clean SpecRoute checkout, copy the relevant runtime layouts:
   - For each vendor in `<vendors>`: copy `runtimes/.<vendor>/` to `<path>/.<vendor>/`.
3. Copy templates the project will need:
   - `prds/templates/`
   - `specs/templates/`
   - `agents/agent-template.md`, `agents/roster.md`, `agents/archetypes/`
   - `skills/skill-template/`
   - `commands/command-template.*`
   - `hooks/<vendor>/hooks.template.json` for vendors that support hooks
   - `prompts/shared/`, `prompts/<vendor>/` for each vendor
3. Create the top-level structure:
   - `<path>/{prds,specs,agents,skills,commands,hooks,prompts,workflows,rules,examples,docs}/`
4. Drop in adapted root context files:
   - `AGENTS.md` - vendor-neutral context, customized for the new project.
   - `<VENDOR>.md` - delegation shims for each vendor.
5. Initialize the gitignore:
   - `.claude/settings.local.json`
   - `.claude/.forbidden-strings.txt`
   - any project-specific patterns
6. Initial commit:
   - `git add` specific paths (not `git add .`).
   - Commit message: `Bootstrap <project-name> with SpecRoute structure`.

## Codex-specific notes

- Use Codex's filesystem MCP server scoped to `<path>`, not `/`.
- For multi-step bootstraps, prefer a Codex skill (`scaffold-artifact` or `add-vendor`) if the SpecRoute checkout has them under `.codex/skills/`.

## Acceptance

- Target repo has the SpecRoute top-level directory structure.
- Each requested vendor's runtime layout is in place.
- Root context files (`AGENTS.md`, vendor shims) are project-specific, not literal SpecRoute content.
- Templates are copied, not customized - that's the project's first PRD's job.
- `.gitignore` excludes per-user settings and the sanitization wordlist.
- Initial commit lands cleanly.

## Constraints

- Do not commit secrets or per-user config.
- Do not invent project-specific PRDs or specs - that's a follow-up task with the project's actual stakeholders.
- Generic templates only at bootstrap time. Customization happens incrementally.
