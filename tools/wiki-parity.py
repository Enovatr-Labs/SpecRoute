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

   Timestamp staleness is a PROXY: it fires whenever a source commit is newer
   than its mirror, even when the region that changed is not one the page
   summarizes. That is unavoidable - the script cannot read a summary and decide
   whether it still holds. A maintainer can, so a page MAY record that judgement:

       <!-- sources: README.md, AGENTS.md -->
       <!-- sources-reviewed: README.md@a1b2c3d4e5f6, AGENTS.md@0f1e2d3c4b5a -->

   Each entry pins the source's content digest at the moment a maintainer
   confirmed the summary still reflects it. While the digest matches, that source
   raises no staleness warning. Edit the source and the digest stops matching, so
   the warning returns and must be re-reviewed - the acknowledgement is per
   content state, never permanent.

   Stamp it with `--accept`, which never runs over the whole wiki: naming the
   pages is the assertion.

       python3 tools/wiki-parity.py --accept wiki/Hooks.md wiki/Sanitization.md

2. **Wiki-internal link resolution.** GitHub-wiki gollum-style `[[Page Name]]`
   links are not URLs and aren't checked by lychee. This script verifies each
   target resolves to an existing `wiki/<Page-Name>.md`.

Exit codes:
  0  — no findings
  1  — hard breaks (missing source file, unresolved [[wiki link]],
       malformed or orphaned sources-reviewed entry)
  2  — only staleness warnings (no hard breaks)

Run locally:
  python3 tools/wiki-parity.py

Or via the wiki-parity workflow on every PR.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"

# <!-- sources: a.md, b/c.md -->  (case-insensitive, multiline-safe)
# The negative lookahead keeps this from also matching `sources-reviewed:`.
SOURCES_RE = re.compile(r"<!--\s*sources(?!-reviewed):\s*(.+?)\s*-->", re.IGNORECASE)

# <!-- sources-reviewed: a.md@0123456789ab, b/c.md@fedcba987654 -->
SOURCES_REVIEWED_RE = re.compile(
    r"<!--\s*sources-reviewed:\s*(.*?)\s*-->", re.IGNORECASE | re.DOTALL
)

# Length of the source content digest recorded in a sources-reviewed entry.
DIGEST_LEN = 12

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


def source_in_repo(src: str) -> bool:
    """True when a manifest source is an existing file inside the repository.

    Rejects absolute paths and `..` escapes so a manifest cannot make the check
    stat or hash files outside the checkout.
    """
    path = (REPO_ROOT / src).resolve()
    return path.is_relative_to(REPO_ROOT) and path.is_file()


def source_digest(path: Path) -> str:
    """Content digest of a source file, as recorded in a sources-reviewed entry.

    Hashing content rather than pinning a commit sha keeps `--accept` usable
    before the reviewed change is committed - the maintainer stamps what they
    just read, and the value stays valid once it lands.
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()[:DIGEST_LEN]


def parse_sources_reviewed(content: str) -> tuple[dict[str, str], list[str]]:
    """Return ({source: digest}, [malformed entries]) from the review marker."""
    match = SOURCES_REVIEWED_RE.search(content)
    if not match:
        return {}, []
    reviewed: dict[str, str] = {}
    malformed: list[str] = []
    for raw in match.group(1).split(","):
        entry = raw.strip()
        if not entry:
            continue
        src, sep, digest = entry.rpartition("@")
        if not sep or not src or not re.fullmatch(r"[0-9a-f]{%d}" % DIGEST_LEN, digest):
            malformed.append(entry)
            continue
        reviewed[src] = digest
    return reviewed, malformed


def render_sources_reviewed(reviewed: dict[str, str]) -> str:
    body = ", ".join(f"{src}@{digest}" for src, digest in sorted(reviewed.items()))
    return f"<!-- sources-reviewed: {body} -->"


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


def accept_pages(page_args: list[str]) -> int:
    """Stamp `sources-reviewed` on the named pages from their sources' content.

    Deliberately never operates on the whole wiki: naming each page is the
    maintainer's assertion that they read it against its current sources and the
    summary still holds.
    """
    failures = 0
    for raw in page_args:
        candidate = Path(raw)
        page = candidate if candidate.is_absolute() else (REPO_ROOT / raw)
        page = page.resolve()
        try:
            page.relative_to(WIKI_DIR)
        except ValueError:
            print(f"error: {raw} is not a page under wiki/", file=sys.stderr)
            failures += 1
            continue
        if not page.is_file() or page.name in WIKI_NON_PAGES:
            print(f"error: {raw} is not a wiki page", file=sys.stderr)
            failures += 1
            continue

        content = page.read_text(encoding="utf-8")
        sources = parse_sources(content)
        if not sources:
            print(
                f"error: {page.name} declares no <!-- sources: --> manifest, "
                f"so there is nothing to review it against",
                file=sys.stderr,
            )
            failures += 1
            continue

        missing = [src for src in sources if not source_in_repo(src)]
        if missing:
            print(
                f"error: {page.name} declares missing source(s): {', '.join(missing)}",
                file=sys.stderr,
            )
            failures += 1
            continue

        reviewed = {src: source_digest(REPO_ROOT / src) for src in sources}
        marker = render_sources_reviewed(reviewed)

        if SOURCES_REVIEWED_RE.search(content):
            updated = SOURCES_REVIEWED_RE.sub(lambda _: marker, content, count=1)
        else:
            # Sit the marker directly beneath the manifest it acknowledges.
            match = SOURCES_RE.search(content)
            insert_at = match.end()
            updated = content[:insert_at] + "\n" + marker + content[insert_at:]

        if updated == content:
            print(f"  unchanged  {page.name}")
            continue
        page.write_text(updated, encoding="utf-8")
        print(f"  reviewed   {page.name} against {', '.join(sources)}")

    if failures:
        print(f"\n{failures} page(s) could not be stamped.", file=sys.stderr)
        return 1
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check parity between wiki/*.md and the source docs they summarize.",
    )
    parser.add_argument(
        "--accept",
        nargs="+",
        metavar="PAGE",
        help=(
            "Record that you have read the named wiki page(s) against their current "
            "sources and the summary still holds. Stamps a sources-reviewed marker "
            "that expires the next time a source changes. Never accepts the whole wiki."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.accept:
        return accept_pages(args.accept)

    if not WIKI_DIR.is_dir():
        print(f"error: {WIKI_DIR} does not exist", file=sys.stderr)
        return 1

    findings: dict[str, list[str]] = {
        "missing_source": [],
        "invalid_review": [],
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
        reviewed, malformed = parse_sources_reviewed(content)
        for entry in malformed:
            findings["invalid_review"].append(
                f"{page.name} → sources-reviewed entry {entry!r} is not "
                f"`<path>@<{DIGEST_LEN}-hex-digest>`"
            )
        for src in sorted(set(reviewed) - set(sources)):
            findings["invalid_review"].append(
                f"{page.name} → sources-reviewed names {src}, which is not in its sources list"
            )

        wiki_ts: int | None = None
        if sources:
            wiki_ts = git_last_modified_ts(page)

        for src in sources:
            src_path = REPO_ROOT / src
            if not source_in_repo(src):
                findings["missing_source"].append(
                    f"{page.name} → {src} (does not exist or is outside the repository)"
                )
                continue
            # A maintainer reviewed this page against exactly this source content
            # and recorded that the summary still holds. The acknowledgement dies
            # with the next edit to the source, so it cannot go permanently stale.
            if reviewed.get(src) == source_digest(src_path):
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
    hard_break_total = total - len(findings["stale_wiki"])

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
