---
name: peer-repo-verification-method
description: How to verify third-party peer-framework facts for the landscape page reliably (shallow clone + grep beats gh code search)
metadata:
  type: reference
---

For peer-project facts on the spec-driven landscape page, a `git clone --depth 1` into the scratchpad and `grep -rn` is the reliable method. `gh api search/code?q=AGENTS.md+repo:...` tokenizes the filename and returns noisy matches (e.g. CUSTOM-AGENTS.md), so it cannot prove absence.

Record the commit SHA and date of the clone in findings so the next pass knows the snapshot.

microsoft/hve-core (added as a landscape row 2026-09): consumer guidance says gitignore `.copilot-tracking/` (docs/getting-started/install.md, "Post-Installation: Update Your .gitignore"). Several of its skills are CC-BY-SA-4.0 or other CC licenses despite repo SPDX MIT, so check per-skill `license:` frontmatter, not only the repo SPDX. Related: [[peer-attribution-rule]]
