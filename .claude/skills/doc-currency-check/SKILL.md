---
name: doc-currency-check
description: Audit SpecRoute's documentation for staleness against reality - vendor facts, version anchors, dates written in the wrong tense, counts that no longer match disk, and claims mirrored inconsistently across the four vendor-matrix copies. Use before a release, after any vendor ships a breaking change, or on a scheduled currency cycle. Triggers - "check the docs are current", "run a currency pass", "what's gone stale", "audit for dated claims", "are our vendor facts still right".
argument-hint: "[area?]  # vendors | versions | counts | mirrors | all (default: all)"
user-invocable: true
allowed-tools: Read Glob Grep Bash WebFetch WebSearch
---

# Doc Currency Check

SpecRoute's value proposition is being *correct about other people's tools*. That makes staleness a correctness bug, not a cosmetic one. This skill finds the classes of rot that have actually bitten this repo before.

## Why these specific checks

Every check below exists because that exact failure happened here:

- A vendor replaced a config format and 19 files kept describing the dead one.
- A half-applied migration left a contract declared in one file and contradicted in three.
- An EOL date passed and ten files still described it in the future tense.
- A capability table claimed support the runtime layouts didn't ship.
- A fabricated external "standard" was cited as the authority for a real change.

## Step 1: Scope

If given an area, run only that section. Otherwise run all six checks below.

## Step 2: Vendor facts (needs internet)

For each vendor in the matrix, check the **official docs** - not blog posts, which are frequently wrong about this ecosystem:

1. Does the config path still exist? Has the file format changed?
2. Have hook event names, counts, or handler types changed?
3. Have frontmatter contracts gained or lost fields?
4. Is the product still called what we call it?

**Prefer an installed binary over documentation** when one is available. Docs lag and third-party sources contradict each other. Grepping a vendor's shipped binary for its own path and event-name constants has settled several questions here that docs could not:

```bash
command -v codex gemini cursor
# then grep the resolved binary for the constants you care about
```

Record the *evidence* for each answer, not just the answer.

## Step 3: Version anchors

```bash
rg -n "v?[0-9]+\.[0-9]+(\.[0-9]+)?" --glob '*.md' --glob '!.git/**' | grep -iE "as of|current|stable|version|since"
```

Any anchor naming a specific vendor release is a rot candidate. Two failure shapes:

- **Overtaken** - "current stable vX" where X is now several releases behind.
- **Load-bearing** - "requires vX+" where the feature is now unconditional.

Prefer statements that don't rot. "Supported since vX" ages well; "current stable is vX" does not.

## Step 4: Dates and tense

```bash
rg -n "20[0-9]{2}-[0-9]{2}-[0-9]{2}" --glob '*.md' --glob '!.git/**'
```

For every date in the past, confirm the surrounding prose uses the past tense. The specific bug to hunt: a future-dated EOL or migration written as "reaches end of life on <date>" or "is being superseded", where the date has since passed. Grep for the giveaways:

```bash
rg -ni "will (be|become|reach)|is being (superseded|replaced)|during the transition|reaches end of life" --glob '*.md' --glob '!.git/**'
```

## Step 5: Counts that must match disk

Any number describing this repository must be regenerable. Check each against reality:

```bash
ls .claude/agents/*.md | grep -cv README        # agent count
ls -d .claude/skills/*/ | wc -l                 # skill count
ls -d runtimes/.*/ | wc -l                      # runtime layouts
ls runtimes/mcp/render/render_*.py | wc -l      # MCP renderers
```

Then grep the docs for hard-coded versions of those numbers and compare.

**The deeper check:** does the doc distinguish *"the vendor supports X"* from *"SpecRoute ships a runtime layout for X"*? Conflating those is what produced this repo's over-claiming capability table. Verify support claims against the layouts:

```bash
for v in claude codex gemini kiro cursor devin; do
  printf "%-9s hooks:%s agents:%s skills:%s commands:%s\n" "$v" \
    "$([ -d runtimes/.$v/hooks ] && echo Y || echo N)" \
    "$([ -d runtimes/.$v/agents ] && echo Y || echo N)" \
    "$([ -d runtimes/.$v/skills ] && echo Y || echo N)" \
    "$([ -d runtimes/.$v/commands ] || [ -d runtimes/.$v/workflows ] && echo Y || echo N)"
done
```

## Step 6: Mirror consistency

The vendor matrix appears in **four** files and must agree:

- `README.md` · `AGENTS.md` · `wiki/Vendor-Matrix.md` · `agentic-docs/agent-cli-integrations.md`

Extract the matrix rows from each and diff them. A change to one that didn't reach the other three is the single most common drift in this repo. Also check the *secondary* tables inside `wiki/Vendor-Matrix.md` - the capability-convergence and MCP-shapes tables have drifted from the main table before.

Then run the structural checks:

```bash
python3 tools/wiki-parity.py     # wiki sources exist, [[links]] resolve
python3 tools/sync-skills.py     # skill bodies in sync across runtimes
```

## Step 7: Unverifiable claims

Grep for anything asserting an external standard or requirement:

```bash
rg -ni "standard|specification|must (stay|be|not)|budget|required by|mandates" --glob '*.md' --glob '!.git/**'
```

For each, ask: **can I produce a source?** If not, it either goes or gets restated as SpecRoute's own convention. Citing a standard that doesn't say what you claim is worse than citing nothing - it is the failure mode this framework exists to prevent, applied to itself.

## Step 8: Report

Group by severity:

- **Wrong** - a claim contradicted by current reality. Fix now; it misleads users.
- **Stale** - true when written, overtaken since. Fix or reword to stop rotting.
- **Unsourced** - asserted as external fact with no citation. Source it, soften it, or drop it.
- **Inconsistent** - mirrors disagree. Pick the true one and propagate.

For each: `file:line`, the claim, the evidence, and the proposed replacement. Cite a URL or a command whose output proves it. **Never** propose a correction you have not verified - a confident wrong fix is worse than the stale text.

## Don't use for

- Frontmatter validity - that's `frontmatter-lint`.
- Private-content leaks - that's `/sanitize` or `sanitization-auditor`.
- Broken links and TODO health - that's `/audit`.
- Skill body drift across runtimes - that's `/parity`.
