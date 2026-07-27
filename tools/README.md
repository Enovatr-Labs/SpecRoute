# Tools

Cross-runtime utility scripts for SpecRoute consumers. These are templates - fork them as your project grows.

```
tools/
├── README.md                            (this file)
├── provenance-audit.py                  local private-source/IP comparison
├── sync-hooks-to-settings.sh            hooks authoring → live settings sync
├── sync-skills.py                       cross-runtime skill body sync
└── wiki-parity.py                       wiki ↔ repo doc parity check
```

## `provenance-audit.py`

Release-only comparison of this public repository against private source
repositories. It detects private identifiers, normalized exact fragments,
near-copy blocks, and 40-token matching runs in the working tree and, with
`--history`, every reachable Git blob. Reports contain only public target
locations and hashes - never private paths or excerpts.

Private inputs are per-installation and gitignored:

```text
.claude/.provenance-sources.txt    one absolute private Git root per line
.claude/.provenance-allowlist.txt  reviewed finding-hash prefixes
.claude/.forbidden-strings.txt     private identifiers and names
```

The publish hook fails closed if the wordlist is not ignored or has been forced
into the index; otherwise the guardrail's own private inputs could be committed.

Run the release gate:

```bash
python3 tools/provenance-audit.py \
  --source-list .claude/.provenance-sources.txt \
  --terms-file .claude/.forbidden-strings.txt \
  --allowlist .claude/.provenance-allowlist.txt \
  --history
```

Any finding requires local human review. Renaming identifiers is not enough:
business rules, unusual schemas, architecture, distinctive prose, prompts, and
workflow structure must be independently authored, publicly sourced, or
demonstrably generalized before release.

## `sync-skills.py`

Body-aware sync of folder-per-skill `SKILL.md` artifacts across every runtime layout under `runtimes/.<vendor>/skills/`: `claude`, `codex`, `gemini`, `kiro`, `cursor`, and `devin`.

It syncs the Markdown **body** below the frontmatter and **preserves each target's own frontmatter**, because the contract differs per vendor (Claude Code carries `argument-hint`/`user-invocable`/`allowed-tools`; the shipped Codex, Gemini, Kiro, and Cursor templates carry `name`/`description`; Devin Desktop uses a YAML-list `allowed-tools` of lowercase tool ids and adds `triggers`). Auxiliary files inside a skill folder (scripts, templates) are copied verbatim.

**Agents are not synced.** Their formats diverge - Claude flat Markdown (`spec-reviewer.md`), Codex standalone TOML (`spec-reviewer.toml`), Devin per-profile directories (`spec-reviewer/AGENT.md`) - so there is no safe file-level copy. Maintain agents per vendor.

Stdlib-only; the PEP 723 block declares `dependencies = []`, so `uv run tools/sync-skills.py` works without installing anything.

### Usage

```bash
# Dry run (default): report drift without writing. Exits 1 when drift exists.
python3 tools/sync-skills.py
python3 tools/sync-skills.py --dry-run

# Apply: overwrite drifted bodies from the source. Missing targets are refused
# until you scaffold their vendor-native frontmatter.
python3 tools/sync-skills.py --apply

# Reverse direction: sync from Codex to every other runtime.
python3 tools/sync-skills.py --source codex --apply

# Single target.
python3 tools/sync-skills.py --target devin
```

### Output

The script reports, per target runtime:

- **MISSING** - skill folder exists in the source but not the target. `--apply`
  refuses to create it because copying source frontmatter can produce an invalid
  target artifact; scaffold the native header first.
- **EXTRA** - skill folder exists in the target but not the source. The script never auto-removes; you decide whether the extra is intentional or stale.
- **DRIFT** - skill exists in both but the `SKILL.md` body or an auxiliary file differs.

### When drift is intentional

Some skills genuinely belong to only one vendor (e.g. a Claude skill that uses the `Task` tool has no Codex equivalent). In that case:

1. Document the asymmetry in `runtimes/README.md` or the skill's own `SKILL.md` body.
2. Accept the EXTRA in the default dry-run output as expected.

If most skills should be in lock-step but a handful are intentional asymmetries, consider extending `sync-skills.py` with an ignore list.

### Extending

The script is intentionally simple (~200 lines). Common extensions:

- **Hooks sync** - render hooks across vendors rather than copying them. Every
  supported runtime now ships its own native hook shape.
- **Selective sync** - only copy skills matching a name pattern.
- **Pre-flight validation** - run frontmatter linting before copying.
- **Git-aware sync** - only sync skills that have changed in the last commit.

Treat this script as a starting point, not a final tool.

## Adding a new tool

When you need a new utility:

1. Make it self-contained - no external dependencies beyond the Python standard library when possible.
2. Default to dry-run; gate destructive operations behind explicit flags.
3. Print findings as a punch list so reviewers can scan results.
4. Document in this README.

## Authoring agent

Cross-vendor sync utilities (and the runtime layouts they sync) are owned by the `runtime-architect` agent.
