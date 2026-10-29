---
name: landscape-page-scope
description: spec-driven-landscape.md is a reader's decision aid only - no "what SpecRoute adopted from peers" section, no version column, no numbers in prose; comparison set is selected by three explicit rules (adoption, vendor-native, adjacent-method contrast)
metadata:
  type: project
---

`agentic-docs/spec-driven-landscape.md` (and its wiki mirror `wiki/Spec-Driven-Landscape.md`) is scoped as a **decision aid for a reader choosing a framework**. Deliberate exclusions, confirmed 2026-09-02:

- No "what SpecRoute has taken from peers" / "what we're adopting" section.
- No version column in the comparison table, and no version numbers or star counts anywhere in prose - each is a new rot surface.
- Peer facts are attributed, never adjudicated ("spec-kit's README instructs...", not "spec-kit correctly...").

**Selection rule (updated 2026-09-15, when microsoft/hve-core was added):** the set is chosen by three stated rules, not one - (1) by adoption: the three most-adopted OSS spec-driven projects (spec-kit, OpenSpec, BMAD-METHOD); (2) vendor-native: Kiro; (3) adjacent method for contrast: hve-core, research-first (RPI) rather than spec-first, Copilot-only, explicitly NOT selected by adoption. Star counts justify rule (1) only - the page says not to read hve-core's count against the others.

**Why:** the page earns trust by being useful to someone who might choose a peer over SpecRoute. Self-referential "what we learned" content turns it into advocacy, which is the failure mode the page's own "Scope and method" section is written to avoid. Version/star digits in prose defeat the "raw numbers in the table only" rule that gives the page exactly one place to refresh. Adding a non-SDD project under the old "three most-adopted plus one vendor-native" rule would have made the rule false, so the rule was rewritten rather than stretched.

**Never credit a peer's tooling with refusing out-of-order work (learned 2026-10-05).** The page once said OpenSpec's "three-phase state machine is enforced"; OpenSpec's own workflow docs say the opposite, in bold - "actions, not phases ... do any of them anytime". spec-kit's commands do write each stage's files in sequence, which is a sequencing claim and safe; "the tool refuses out-of-order work" is not, for any peer. Only SpecRoute's own framing - ordering is a convention upheld by review and by hooks you wire yourself - is safe to state flatly. Relatedly, a peer step that is a gate today can become a skippable default without being renamed (hve-core's plan critique did, within three weeks), so re-read the peer's sentence instead of trusting a paraphrase.

**A quoted term is a claim about the peer's current vocabulary (learned 2026-10-05).** The
page quoted BMAD-METHOD's "Agent-as-Code" long after the phrase had been deleted from its
repository; the practice continued, so the sentence never looked wrong. Before quoting a peer's
term, grep the peer's tree for that exact phrase. Prefer describing what the peer ships over
borrowing its branding, which it can retire without notice.

**A superlative is a set-wide claim (learned 2026-10-05).** "The deepest agent-persona library
of the set" was true of BMAD before hve-core joined the set and false after, with no edit to
BMAD or to the sentence. Re-checking count words (all/none/every/three/five) is not enough -
most/deepest/sharpest/clearest must be re-tested against any new member too.

**A peer can ship on two lines at once (learned 2026-10-28).** BMAD-METHOD's README splits a stable line (its own npm installer, `npx bmad-method install`) from a preview line (`npx skills add` or plugin marketplaces). A pass that read only the preview section rewrote the table to drop the stable installer, which made "each ships a CLI" look false when it was half true. Read a peer's whole install section and name both routes by line ("stable"/"preview"), never by version number.

**How to apply:** when asked to expand this page, push additions toward the comparison table or the "when to pick a peer instead" list. Any new entry must name which selection rule admits it; a new rule means rewriting "Scope and method" and re-checking every set-wide count word (all/none/every/three/four/five) in both copies. Convergence claims must say where the contrast project departs (hve-core's `.copilot-tracking/` is gitignored, so it is the exception to "versioned with the code"). SpecRoute does not support GitHub Copilot as a vendor - state it as fact, do not propose adding it. A refresh is re-running the `gh api` command in the page and editing **both** files together - never a timestamp bump in one. See [[landscape-refresh-procedure]].
