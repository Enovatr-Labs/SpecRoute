# wiki/

Source markdown for the SpecRoute GitHub wiki at https://github.com/Enovatr-Labs/SpecRoute/wiki.

**This directory is intended for the wiki repository, not the main repo.** GitHub exposes wikis as a separate git repository at `<repo>.wiki.git`. Pushing here ships content to the wiki tab.

## Page conventions

- **Filenames map to page titles**: `Spec-Driven-Development.md` → "Spec Driven Development". Hyphens become spaces.
- **Flat directory**: GitHub wiki does not support subdirectories. All pages live at the root of the wiki repo.
- **Home page**: `Home.md` is the landing page shown at `/wiki`.
- **Sidebar**: `_Sidebar.md` renders on every page (right-side nav).
- **Footer**: `_Footer.md` renders on every page (below content).
- **Internal links**: `[[Page Name]]` syntax (gollum-flavored markdown). Spaces in titles map to hyphens in URLs.
- **External / repo file links**: standard markdown `[text](https://github.com/Enovatr-Labs/SpecRoute/blob/main/...)`.

## Pushing to the wiki

The wiki must exist before you can clone it: first **create the Home page once via the wiki UI** at https://github.com/Enovatr-Labs/SpecRoute/wiki, then:

```bash
# Clone the wiki repo (separate from the main repo)
git clone https://github.com/Enovatr-Labs/SpecRoute.wiki.git /tmp/specroute-wiki
cd /tmp/specroute-wiki

# Copy all the files in here (run from your SpecRoute checkout, or adjust the path)
cp "$(git -C /path/to/SpecRoute rev-parse --show-toplevel)"/wiki/*.md .

# Don't copy this README (it's local-only guidance)
rm -f README.md

# Commit and push
git add .
git commit -m "Populate wiki with full SpecRoute documentation"
git push origin master   # the wiki default branch is usually `master`, not `main`
```

After the push, the wiki is live. Subsequent updates: edit files here, copy/diff into the wiki clone, push.

## Updating the wiki

When the source docs in this main repo change, sync into the wiki:

1. Edit the relevant page under `wiki/`.
2. `cp wiki/<page>.md /tmp/specroute-wiki/` and `cd /tmp/specroute-wiki && git commit + push`.

For larger refreshes, it's easier to `cp wiki/*.md /tmp/specroute-wiki/ && git add -A && git commit && git push`.

## Page inventory

**Navigation:** Home, _Sidebar, _Footer

**Getting started:** Quickstart, Repository-Structure

**Concepts:** Philosophy, Spec-Driven-Development, Agentic-Coding-Model, Automation-Decision-Framework, Two-Tier-Docs-Pattern, Multi-Vendor-Context-Files, Documentation-Structure, Agent-Memory

**Artifacts:** Artifact-Taxonomy, PRDs, Specs, Agents, Skills, Commands, Hooks, Prompts, Rules, Frontmatter-Contracts, Sanitization

**Workflows:** Workflows, Workflow-PRD-to-Production, Workflow-Spec-to-Implementation, Workflow-Agent-Review-Loop, Workflow-Testing-and-Validation, Workflow-Release-Readiness

**Vendors:** Vendor-Matrix, Agent-CLI-Integrations, Cross-Vendor-Sync, MCP-Integration, Adding-a-Vendor

**Project:** Worked-Example, Implementation-Team, Contributing, Security, Maintainers, Roadmap, Code-of-Conduct, FAQ, Glossary

Total: 35 wiki pages + 3 navigation files.

## Should this directory be tracked in the main repo?

Your call. Two reasonable choices:

1. **Track it** — `wiki/` lives in the main repo so contributors can edit, review in PRs, and the source-of-truth is colocated. Push to the wiki happens as a separate step (manual `cp` + push, or a small sync script).
2. **Don't track it** — add `wiki/` to `.gitignore`; treat the wiki repo as the only source-of-truth. Edits happen directly in the wiki clone.

If you choose option 1, consider adding a CI check that diffs `wiki/` against the live wiki to catch drift.
