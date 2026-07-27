# `.kiro/skills/` - Kiro Agent Skills

Folder-per-skill workflows Kiro loads on demand. Arrived in **Kiro 0.9** (2026-02-05); unchanged through **Kiro IDE 1.0** (2026-07-23), which reformatted hooks but left skills alone.

## Layout

```
.kiro/skills/<slug>/
├── SKILL.md            required - frontmatter + body
├── scripts/            optional - executable helpers
├── references/         optional - supporting docs
└── assets/             optional - templates
```

Workspace skills live under `.kiro/skills/`; user-global skills live under `~/.kiro/skills/`.

## Frontmatter contract

Kiro follows the Agent Skills open standard (progressive disclosure). Only `name` and `description` are required:

| Field | Required | Notes |
|---|---|---|
| `name` | yes | Must match the folder name. Lowercase, numbers, hyphens only (max 64 chars). |
| `description` | yes | Describes *when* to use the skill. Kiro matches this against the request to decide activation. |
| `license` | no | License name or reference to a bundled license file. |
| `compatibility` | no | Environment requirements (required tools, network access). |
| `metadata` | no | Extra key-value data (author, version). |

> Note: Kiro does NOT use the Claude/Codex skill fields `argument-hint`, `user-invocable`, or `allowed-tools`. When syncing a skill from `.claude/skills/`, strip those fields. Keep the body identical.

## Invocation

There is no separate commands directory. Invoke a skill with `/skill <slug>` in chat, or pull it in automatically by referencing it from a manual-inclusion steering file (`inclusion: manual`).

## See also

- [`audit-artifact/SKILL.md`](audit-artifact/SKILL.md) - canonical sample skill body.
- The same skill in [`../../.claude/skills/audit-artifact/`](../../.claude/skills/audit-artifact/) - source for cross-vendor sync.

## Invoking a skill

Use your runtime's skill prefix. In Claude Code both work once the skill is registered:

```
/all-hands review the changes        # skill/command menu
@all-hands review the changes        # mention picker - lists files AND registered skills
```

A correctly registered skill appears in the `@` picker with type **Skill**. If you see only
directories and no `Skill` row, it did not register - and the cause is almost always
frontmatter:

- **`disable-model-invocation: true` hides it** from the model-facing registry the `@` picker
  completes against. Omit it unless you want the skill reachable *only* from the `/` menu.
- **`allowed-tools` is comma-separated** (`Read, Grep, Glob, Bash, Agent`). Space separation
  and stale tool names (`Task` was superseded by `Agent`) fail silently.
- **The folder name must equal the `name` field.**

Each skill's `SKILL.md` carries a per-runtime invocation table.
