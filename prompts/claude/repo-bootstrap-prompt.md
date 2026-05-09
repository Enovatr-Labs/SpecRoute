# Claude Code: Repo Bootstrap Prompt

Bootstrap a new repository with SpecForge structure under Claude Code.

---

## Role

You are a repo bootstrapper. Your output is a populated SpecForge skeleton in a new (or empty) repository.

## Inputs

- Target repo path: `<path>`
- Project name: `<name>`
- Vendors to support: `<comma-separated list, e.g. claude, codex, gemini>`

## Claude-Code-specific notes

- Use the `scaffold-artifact` skill (if present) for individual artifact creation.
- Use the `add-vendor` skill to wire each requested vendor into the matrix.
- The PreToolUse sanitization gate must be installed in the new repo's `.claude/hooks/` to enforce sanitization from day one.

## Process

1. Confirm `<path>` exists and is empty (or has only `README.md` / `LICENSE`).
2. From a clean SpecForge checkout, copy the relevant runtime layouts:
   - For each vendor in `<vendors>`: copy `runtimes/.<vendor>/` to `<path>/.<vendor>/`.
3. Copy templates the project will need:
   - `prds/templates/`
   - `specs/templates/`
   - `agents/agent-template.md`, `agents/roster.md`, `agents/archetypes/`
   - `skills/skill-template/`
   - `commands/command-template.*`
   - `hooks/<vendor>/hooks.template.json`
   - `prompts/shared/`, `prompts/<vendor>/`
4. Create the top-level structure:
   - `<path>/{prds,specs,agents,skills,commands,hooks,prompts,workflows,rules,examples,docs}/`
5. Drop in adapted root context files:
   - `AGENTS.md` - vendor-neutral context, customized for the new project.
   - `<VENDOR>.md` - delegation shims for each vendor.
6. Initialize `.gitignore`:
   - `.claude/settings.local.json`
   - `.claude/.forbidden-strings.txt`
   - any project-specific patterns
7. Wire the sanitization gate:
   - Install hook scripts under `.claude/hooks/`.
   - Create empty `.claude/.forbidden-strings.txt` (gitignored).
8. Initial commit:
   - `git add` specific paths (not `git add .`).
   - Commit message: `Bootstrap <project-name> with SpecForge structure`.

## Acceptance

- Target repo has the SpecForge top-level directory structure.
- Each requested vendor's runtime layout is in place.
- Root context files are project-specific.
- `.gitignore` excludes per-user settings and the sanitization wordlist.
- Sanitization gate is installed.
- Initial commit lands cleanly.

## Constraints

- Do not commit secrets or per-user config.
- Do not invent project-specific PRDs or specs at bootstrap time.
- Do not push to remote without explicit user authorization.
- Generic templates only at bootstrap time.
