#!/usr/bin/env python3
"""Check parity between wiki/*.md and the source docs they summarize.

This script complements the lychee URL link-check (`.github/workflows/links.yml`).
Lychee verifies external/repo URLs; this script handles two things lychee cannot:

1. **Source-manifest validation.** Each wiki page MAY declare which source files
   it summarizes via a HTML comment immediately under the H1:

       <!-- sources: agentic-docs/philosophy.md -->
       <!-- sources: workflows/prd-to-production.md, README.md -->

   The script checks:
     a. Every declared source path exists on disk.
     b. The wiki page's last-modified git timestamp is >= the source's.
        If a source is newer, the wiki summary is potentially stale (warning).

2. **Wiki-internal link resolution.** GitHub-wiki gollum-style `[[Page Name]]`
   links are not URLs and aren't checked by lychee. This script verifies each
   target resolves to an existing `wiki/<Page-Name>.md`.

Exit codes:
  0  — no findings
  1  — hard breaks (missing source file, unresolved [[wiki link]])
  2  — only staleness warnings (no hard breaks)

Run locally:
  python3 tools/wiki-parity.py

Or via the wiki-parity workflow on every PR.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"

# <!-- sources: a.md, b/c.md -->  (case-insensitive, multiline-safe)
SOURCES_RE = re.compile(r"<!--\s*sources:\s*(.+?)\s*-->", re.IGNORECASE)

# [[Page Name]]  or  [[Display|Page-Name]]
WIKI_LINK_RE = re.compile(r"\[\[([^\]\n]+?)\]\]")

# Files in wiki/ that are not wiki pages (don't load into GitHub wiki).
WIKI_NON_PAGES = {"README.md"}


def run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO_ROOT, text=True).strip()


def dirty_paths() -> set[str]:
    """Return modified, deleted, renamed, and untracked paths in the worktree."""
    raw = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "-z"],
        cwd=REPO_ROOT,
    )
    paths: set[str] = set()
    rows = raw.split(b"\0")
    index = 0
    while index < len(rows):
        row = rows[index]
        index += 1
        if not row:
            continue
        text = row.decode("utf-8", errors="surrogateescape")
        status = text[:2]
        path = text[3:]
        if status[0] in {"R", "C"} and index < len(rows):
            path = rows[index].decode("utf-8", errors="surrogateescape")
            index += 1
        paths.add(path)
    return paths


def git_last_modified_ts(path: Path) -> int | None:
    """Return last-commit Unix timestamp for `path`, or None if untracked."""
    try:
        rel = path.relative_to(REPO_ROOT)
    except ValueError:
        return None
    try:
        out = run_git(["log", "-1", "--format=%ct", "--", str(rel)])
        return int(out) if out else None
    except subprocess.CalledProcessError:
        return None


def collect_wiki_page_stems() -> set[str]:
    """Return the set of stems (filenames without .md) for all wiki pages.

    Excludes non-page files (README.md). Includes navigation files (_Sidebar, _Footer)
    and Home so [[Home]] resolves.
    """
    stems: set[str] = set()
    for p in WIKI_DIR.glob("*.md"):
        if p.name in WIKI_NON_PAGES:
            continue
        stems.add(p.stem)
    return stems


def parse_sources(content: str) -> list[str]:
    m = SOURCES_RE.search(content)
    if not m:
        return []
    return [s.strip() for s in m.group(1).split(",") if s.strip()]


def parse_wiki_links(content: str) -> list[str]:
    """Extract target page names from [[Page]] and [[Display|Page-Name]] links."""
    raw = WIKI_LINK_RE.findall(content)
    targets: list[str] = []
    for r in raw:
        if "|" in r:
            # [[Display|Page-Name]] — the second half is the target.
            target = r.split("|", 1)[1].strip()
        else:
            target = r.strip()
        targets.append(target)
    return targets


def title_to_stem(title: str) -> str:
    """GitHub wiki convention: spaces in titles become hyphens in filenames."""
    return title.replace(" ", "-")


def main() -> int:
    if not WIKI_DIR.is_dir():
        print(f"error: {WIKI_DIR} does not exist", file=sys.stderr)
        return 1

    findings = {
        "missing_source": [],
        "broken_wiki_link": [],
        "stale_wiki": [],
    }

    wiki_stems = collect_wiki_page_stems()
    dirty = dirty_paths()

    pages = sorted(p for p in WIKI_DIR.glob("*.md") if p.name not in WIKI_NON_PAGES)
    for page in pages:
        content = page.read_text(encoding="utf-8")

        # 1. Source-manifest validation
        sources = parse_sources(content)
        wiki_ts: int | None = None
        if sources:
            wiki_ts = git_last_modified_ts(page)

        for src in sources:
            src_path = REPO_ROOT / src
            if not src_path.exists():
                findings["missing_source"].append(f"{page.name} → {src} (does not exist)")
                continue
            page_rel = str(page.relative_to(REPO_ROOT))
            if src in dirty:
                if page_rel not in dirty:
                    findings["stale_wiki"].append(
                        f"{page.name} is unchanged while dirty source {src} has edits"
                    )
                continue
            if page_rel in dirty or wiki_ts is None:
                continue  # current wiki content has been refreshed or is new
            src_ts = git_last_modified_ts(src_path)
            if src_ts is None:
                continue  # source is untracked; skip
            if src_ts > wiki_ts:
                findings["stale_wiki"].append(
                    f"{page.name} (ts={wiki_ts}) is older than {src} (ts={src_ts})"
                )

        # 2. Wiki internal links
        for target_title in parse_wiki_links(content):
            stem = title_to_stem(target_title)
            if stem not in wiki_stems:
                findings["broken_wiki_link"].append(
                    f"{page.name} → [[{target_title}]] (no wiki/{stem}.md)"
                )

    # Report
    total = sum(len(v) for v in findings.values())
    hard_break_total = len(findings["missing_source"]) + len(findings["broken_wiki_link"])

    if total == 0:
        print("Wiki parity: OK")
        return 0

    for category, items in findings.items():
        if not items:
            continue
        label = category.replace("_", " ").title()
        print(f"\n## {label} ({len(items)})")
        for item in items:
            print(f"  - {item}")

    print()
    print(f"Summary: {total} findings "
          f"({hard_break_total} hard break(s), "
          f"{len(findings['stale_wiki'])} staleness warning(s)).")

    if hard_break_total > 0:
        return 1
    return 2  # staleness-only — non-zero but distinguishable from hard breaks


if __name__ == "__main__":
    sys.exit(main())
