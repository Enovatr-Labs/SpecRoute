# Adding a Vendor

Process for adding a new agent CLI to the SpecForge supported matrix. **Adding a vendor is a new column, not a fork.** The framework's content (PRDs, specs, prompts, rules) stays unchanged; the runtime shell adapts.

The `add-vendor` skill walks through this interactively — see [`.claude/skills/add-vendor/SKILL.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/.claude/skills/add-vendor/SKILL.md).

## Steps

### 1. Create the runtime layout

```
runtimes/.<vendor>/
├── README.md                   per-runtime setup steps (model on existing READMEs)
├── settings.template.json      or .toml — whatever the vendor consumes
├── (agents/)                   only if the vendor has an agent primitive
├── (skills/)                   only if the vendor has a skill primitive
├── (commands/ or commands.json) only if the vendor has commands
└── (hooks/)                    if the vendor has hooks
```

Pattern: only ship the directories the vendor actually consumes. Don't add empty `agents/` if the vendor has no agent concept.

### 2. Add the row to the matrix

The matrix appears in three files. Update **all three** in lock-step:

- `README.md` — supported vendor matrix section.
- `AGENTS.md` — supported vendor matrix section.
- `agentic-docs/agent-cli-integrations.md` — supported vendor matrix section.

Each row: `Vendor | Runtime dir | Root context file | Skills | Agents | Commands | Hooks | MCP config`.

Use `–` for what the vendor doesn't support. If hooks are supported, also update the per-vendor hook depth table in `agentic-docs/agent-cli-integrations.md` and the event matrix in `hooks/README.md`.

### 3. Add the per-vendor rule file

```
rules/<vendor>-rules.md
```

Document:

- How the vendor surfaces rules (always-on file, glob-matched, etc.).
- How the shared rules (`engineering`, `code-review`, `security`, `documentation`) map onto the vendor's format.
- Vendor-specific frontmatter conventions.
- Known limitations vs Claude / Codex.

### 4. Wire MCP rendering (if supported)

If the vendor consumes MCP servers:

1. Document the vendor's MCP config shape and path.
2. Add `runtimes/mcp/render/render_<vendor>.py`.
3. Update `runtimes/mcp/servers.yaml` per-server `enabled_for` lists to include the new vendor.

See [[MCP Integration]].

### 5. Update cross-vendor sync (if applicable)

If the vendor shares artifact shapes with Claude or Codex:

- **For agents** — extend `tools/sync-skills.py` to include the new vendor's agents directory.
- **For skills** — same.

If the shapes are genuinely different (Kiro's `.kiro.hook` vs Claude's `hooks.json`), no sync target; document the asymmetry.

### 6. Add hook templates

For each vendor that supports hooks:

```
hooks/<vendor>/
├── hooks.template.json (or .toml or per-hook files)
└── scripts/             optional supporting shell scripts
```

Use the existing per-vendor templates under `hooks/` as the model. Document the event list and blocking semantics in `hooks/README.md`.

### 7. Add the delegation shim (if the vendor auto-loads a root file)

If the vendor reads a specific filename at session start (like Claude's `CLAUDE.md`), add a short delegation shim at the repo root:

```markdown
# <VENDOR>.md

<Vendor> shim for this repository. Read `AGENTS.md` first; it is the canonical
vendor-neutral source of truth.

## <Vendor>-Specific Context

- (Vendor-specific runtime location, frontmatter quirks, hook config path…)

## Before Publishing

(Vendor-specific sanitization or pre-commit notes.)
```

Length: 30–50 lines. See [[Multi-Vendor Context Files]].

### 8. Run `/audit`

After the changes, run `/audit` — it checks vendor-matrix consistency across the three files and flags broken cross-references.

## Acceptance criteria for "vendor support is complete"

- [ ] `runtimes/.<vendor>/` exists with a README and the appropriate template files.
- [ ] Matrix row is identical across `README.md`, `AGENTS.md`, `agentic-docs/agent-cli-integrations.md`.
- [ ] `rules/<vendor>-rules.md` documents how rules surface.
- [ ] If the vendor consumes MCP: renderer exists, `servers.yaml` per-server `enabled_for` updated.
- [ ] If the vendor has hooks: `hooks/<vendor>/` templates exist, event list documented in `hooks/README.md`.
- [ ] If the vendor auto-loads a root file: delegation shim exists at repo root (30–50 lines).
- [ ] Per-runtime README walks through setup (rename templates, .gitignore additions, etc.).
- [ ] `/audit` passes.

## Owner agent

Vendor onboarding is owned by the `runtime-architect` agent.

## See also

- [[Vendor Matrix]] — the contract
- [[Agent CLI Integrations]] — how each existing vendor is wired
- [[Cross-Vendor Sync]] — keeping things aligned
- [[Multi-Vendor Context Files]] — the delegation-shim pattern
