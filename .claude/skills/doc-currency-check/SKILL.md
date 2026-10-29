---
name: doc-currency-check
description: Audit SpecRoute's documentation for staleness against reality - vendor facts, version anchors, dates written in the wrong tense, counts that no longer match disk, third-party facts about peer projects on the spec-driven landscape page, and claims mirrored inconsistently across the four vendor-matrix copies. Use before a release, after any vendor ships a breaking change, or on a scheduled currency cycle. Triggers - "check the docs are current", "run a currency pass", "what's gone stale", "audit for dated claims", "are our vendor facts still right", "are the peer comparison numbers still current".
argument-hint: "[area?]  # vendors | versions | counts | mirrors | peers | all (default: all)"
user-invocable: true
allowed-tools: Read Glob Grep Bash WebFetch WebSearch
---

# Doc Currency Check

SpecRoute's value proposition is being *correct about other people's tools*. That makes staleness a correctness bug, not a cosmetic one. This skill finds the classes of rot that have actually bitten this repo before.

## Why these specific checks

Most checks below exist because that exact failure happened here:

- A vendor replaced a config format and 19 files kept describing the dead one.
- A half-applied migration left a contract declared in one file and contradicted in three.
- An EOL date passed and ten files still described it in the future tense.
- A capability table claimed support the runtime layouts didn't ship.
- A fabricated external "standard" was cited as the authority for a real change.

**Step 8**, third-party project facts, was added preventively when the landscape page
first introduced claims about peer projects - and has since earned its place: a peer
added a phase to its published model and renamed nothing, so nothing broke loudly and
no command regenerated the drift. The shipped page carried the old phase model until
this step caught it.

## Step 1: Scope

If given an area, run only that section. Otherwise run all seven checks below.

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

## Step 8: Third-party project facts

`agentic-docs/spec-driven-landscape.md` and its mirror `wiki/Spec-Driven-Landscape.md`
compare SpecRoute against peer frameworks (github/spec-kit, Fission-AI/OpenSpec,
bmad-code-org/BMAD-METHOD, and Kiro's native specs), plus microsoft/hve-core as an
adjacent research-first method included for contrast. This is the only place SpecRoute
asserts facts about *other projects*, and those rot faster than vendor facts: peers
rename commands and restructure directories between minor versions, with no deprecation
window and no migration note.

Two tiers, and the second is the dangerous one.

**Regenerable** - star counts and SPDX license identifiers. They go stale constantly,
but refreshing them is cheap and safe because a command produces them. **Do not write a
second copy of that command here.** The landscape page ships it directly beneath the
table it fills, under "The comparison set"; run the page's own command so there is one
copy to keep right. A duplicate in this skill is just a second thing to drift.

**Not regenerable** - peer slash-command vocabularies (`/speckit.*`, `/opsx:*`,
`RPI Agent` and `/rpi-*`), phase-model names (`propose -> apply -> archive`,
`constitution -> specify -> plan -> tasks -> implement -> converge`, hve-core's
`research when needed -> plan -> implement -> review -> follow-up`), artifact directory
paths (`.specify/`, `openspec/specs/`, `openspec/changes/`, `.kiro/specs/`,
`.copilot-tracking/` and the fact that consumers are told to gitignore it), delivery
channels (hve-core's Copilot CLI plugin and VS Code extension id), target statements
(hve-core's "Copilot-only"), and verdict labels (hve-core's plan-critique and review
outcomes). No command regenerates these.
They change silently, and a wrong one sends the reader to a command or path that no
longer exists - which reads as authoritative and is entirely false. Check each against
the peer's **current** README or docs and record the URL in the finding.

**A borrowed term can vanish while the practice stays.** A phrase the page puts in
quotation marks is a claim about the peer's *current vocabulary*, not about its behavior.
BMAD-METHOD's "Agent-as-Code" was quoted here after the phrase had been removed from its
repository entirely; the practice it named continued unchanged, so nothing read as wrong.
Grep the peer for the phrase itself, not for the idea behind it.

**A superlative is a set-wide claim, so admitting a project can falsify one.** "The
deepest agent-persona library of the set" was true of BMAD-METHOD before hve-core was added
and false afterwards - BMAD ships five named agents, hve-core ships dozens of agent files -
without BMAD changing or the sentence being touched. When the comparison set grows, re-test
every most/deepest/sharpest/clearest against the new member, not just the count words.

**Gate-versus-default framing.** Whether a peer's step is *required* or merely *the
default* is a fact that changes without renaming anything. hve-core's plan critique was
an unconditional gate in September 2026 and a skippable, explicitly advisory default
weeks later, and its review became optional in the same commit. A page that calls such a
step a gate is wrong the moment the peer adds a skip flag, and nothing in the wording
rots visibly. Re-read the peer's own sentence, not your paraphrase of it.

**Claims about a peer's documentation layout rot fastest of all.** "Their README shows
both command forms" is a claim about presentation, not behavior: it broke within a day of
being written here. Where a fact must be cited, cite the peer's reference or
specification page - a reference page is obliged to be exhaustive, a README is obliged to
be short.

The discipline the page already follows, which a currency pass must preserve:

- **Numbers live only in the table, never in prose.** A star count repeated in a
  sentence is a second place to rot that the regeneration command never touches. Finding
  one in prose is itself a finding, whether or not the number is currently right.
- **Every number carries a verified-on date**, and the date moves only when the command
  was actually re-run. A refreshed date over unchanged numbers is a false currency
  signal - worse than an honestly old date.
- **Both copies change.** The wiki mirror deliberately carries the table *and* the
  regeneration command in full, so a real refresh is an edit in **both** files, never a
  timestamp bump in one:

```bash
grep -n "verified 20[0-9][0-9]-\|Last run:" \
  agentic-docs/spec-driven-landscape.md wiki/Spec-Driven-Landscape.md
```

Cells or dates that disagree between the two are drift. Step 6 will **not** catch it -
that check covers the four vendor-matrix mirrors, not this page.

**Attribute, do not adjudicate.** Where a peer claims something about itself that its
repository cannot independently confirm - OpenSpec's "works with 30+ AI coding
assistants" is the live example - the page attributes it ("the project states that...")
instead of asserting it. Re-verifying such a claim means confirming **the peer still
makes it**, not testing whether it is true. Never promote an attributed claim to an
asserted one because it looked plausible, and never "correct" a peer's self-description
against your own count.

A self-description the page **quotes** is re-checked verbatim, not paraphrased back into
agreement. hve-core's "source of patterns and learning rather than a stable platform,
foundation, or production dependency" is the live example; a quote the page has
truncated or reworded is a finding even when its gist still holds.

**Mixed per-artifact licensing.** The SPDX id is regenerable, but it only describes the
repository. hve-core's is MIT, while individual skills declare Creative Commons licenses
in their own `license:` frontmatter - one of them non-commercial. The API's `spdx_id`
cannot see that, so a currency pass re-checks the page's licensing note against the
peer's skill frontmatter, not just the regenerated table cell.

## Step 9: Report

Group by severity:

- **Wrong** - a claim contradicted by current reality. Fix now; it misleads users.
- **Stale** - true when written, overtaken since. Fix or reword to stop rotting.
- **Unsourced** - asserted as external fact with no citation. Source it, soften it, or drop it.
- **Inconsistent** - mirrors disagree. Pick the true one and propagate.

A peer-project finding names the peer's own current documentation as its evidence, and
says plainly whether the claim is one SpecRoute asserts or one it attributes.

For each: `file:line`, the claim, the evidence, and the proposed replacement. Cite a URL or a command whose output proves it. **Never** propose a correction you have not verified - a confident wrong fix is worse than the stale text.

## Don't use for

- Frontmatter validity - that's `frontmatter-lint`.
- Private-content leaks - that's `/sanitize` or `sanitization-auditor`.
- Broken links and TODO health - that's `/audit`.
- Skill body drift across runtimes - that's `/parity`.
