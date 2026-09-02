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
| `name` | yes | 1-64 chars. Lowercase alphanumerics (`a`-`z`, `0`-`9`) and hyphens only. Must not start or end with a hyphen, and must not contain consecutive hyphens (`pdf--processing` is invalid). Must match the folder name exactly. |
| `description` | yes | 1-1024 chars, non-empty. Describes *when* to use the skill. Kiro matches this against the request to decide activation. |
| `license` | no | License name or reference to a bundled license file. |
| `compatibility` | no | Environment requirements (required tools, network access). Max 500 chars. |
| `metadata` | no | Map of string keys to string values (author, version). |
| `allowed-tools` | no | Standard field, marked **(Experimental)** - a space-separated string of pre-approved tools whose support varies between implementations. Kiro does not consume it. |

> Note: Kiro does NOT use the Claude extensions `argument-hint` or `user-invocable`, and does not consume the standard's experimental `allowed-tools`. When syncing a skill from `.claude/skills/`, strip those fields. Keep the body identical.

### Progressive disclosure budgets

| Stage | What loads | Budget |
|---|---|---|
| Discovery | frontmatter metadata (`name` + `description`) | ~100 tokens, always in context |
| Activation | the full `SKILL.md` body | < 5000 tokens recommended |

Keep the main `SKILL.md` under 500 lines; move detail into `references/`, `scripts/`, or `assets/`.

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
- **`allowed-tools` is a space-separated string** (`Read Grep Glob Bash Agent`), per the standard;
  Claude Code also accepts a YAML list. Comma separation and stale tool names (`Task` was
  superseded by `Agent`) fail silently.
- **The folder name must equal the `name` field.**

Each skill's `SKILL.md` carries a per-runtime invocation table.
