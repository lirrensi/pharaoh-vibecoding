#!/usr/bin/env python3
"""Documentation health dashboard — structural issues, coverage, staleness.

Usage:
    python scripts/status.py              # full health report
    python scripts/status.py --short       # summary only, no detail
    python scripts/status.py docs/         # specify docs path
"""

import sys
from pathlib import Path
from datetime import date, timedelta
from collections import Counter, defaultdict

from _ontology import (
    STATUS_EMOJI,
    walk_docs,
    read_doc,
    is_load_bearing,
    resolve_links,
    collect_index_links,
    find_project_root,
    build_graph,
    build_reverse,
    today_str,
)


def status_emoji(status: str) -> str:
    return STATUS_EMOJI.get(status, "")


# ── Report generators ─────────────────────────────────────────────


def header(text: str) -> str:
    return f"\n  {text}\n  {'─' * len(text)}"


def build_index_lookup(index_files: dict[Path, list[Path]]) -> set[Path]:
    """Build a set of all .md files referenced by any INDEX.md."""
    linked = set()
    for targets in index_files.values():
        linked.update(targets)
    return linked


def build_incoming_links(docs: list[tuple[Path, dict]], index_files: dict[Path, list[Path]]) -> dict[Path, list[tuple[Path, str]]]:
    """Build reverse index using shared graph utilities."""
    graph = build_graph(docs, index_files)
    return build_reverse(graph)


def check_orphans(docs: list[tuple[Path, dict]], incoming: dict[Path, list]) -> list[Path]:
    """Find load-bearing docs with no incoming links."""
    orphans = []
    for fp, fm in docs:
        if not is_load_bearing(fm):
            continue
        resolved = fp.resolve()
        if resolved not in incoming or not incoming[resolved]:
            orphans.append(fp)
    return orphans


def check_broken_links(docs: list[tuple[Path, dict]], index_files: dict[Path, list[Path]]) -> list[tuple[Path, str, Path]]:
    """Find links pointing to non-existent files.
    Returns list of (source, link_type, broken_target)."""
    broken = []
    all_existing = {fp.resolve() for fp, _ in docs}
    # Also include INDEX.md files as existing
    all_existing.update(idx.resolve() for idx in index_files)

    for src_path, fm in docs:
        resolved = resolve_links(src_path, fm)
        for link_type, targets in resolved.items():
            for target in targets:
                if target not in all_existing:
                    broken.append((src_path, link_type, target))
    return broken


def check_unsynced(docs: list[tuple[Path, dict]]) -> list[Path]:
    """Find docs where sync_status is unchecked or absent."""
    unsynced = []
    for fp, fm in docs:
        if not is_load_bearing(fm):
            continue
        sync = fm.get("sync_status", "")
        if sync in ("", "unchecked"):
            unsynced.append(fp)
    return unsynced


def check_drifted(docs: list[tuple[Path, dict]]) -> list[Path]:
    """Find docs where sync_status is drifted."""
    return [fp for fp, fm in docs if fm.get("sync_status") == "drifted"]


def check_untagged(docs: list[tuple[Path, dict]]) -> list[Path]:
    """Find load-bearing docs with no tags."""
    return [fp for fp, fm in docs if is_load_bearing(fm) and not fm.get("tags")]


def check_missing_dod(docs: list[tuple[Path, dict]]) -> list[Path]:
    """Find spec docs that might be missing Definition of Done."""
    missing = []
    for fp, fm in docs:
        nt = fm.get("node_type", "")
        if nt != "spec":
            continue
        try:
            text = fp.read_text(encoding="utf-8")
            if "Definition of Done" not in text and "Definition of working" not in text:
                missing.append(fp)
        except Exception:
            pass
    return missing


def check_staleness(docs: list[tuple[Path, dict]]) -> tuple[list[tuple[Path, str, int]], Path | None, int]:
    """Return (stale_docs_list, oldest_path, oldest_days). Stale = untouched > 90 days."""
    stale = []
    oldest_path = None
    oldest_days = 0
    cutoff = date.today() - timedelta(days=90)

    for fp, fm in docs:
        if not is_load_bearing(fm):
            continue
        updated_str = fm.get("updated", "")
        if not updated_str:
            continue
        try:
            d = date.fromisoformat(updated_str)
            days = (date.today() - d).days
            if days > oldest_days:
                oldest_days = days
                oldest_path = fp
            if d < cutoff:
                stale.append((fp, updated_str, days))
        except (ValueError, TypeError):
            pass

    return stale, oldest_path, oldest_days


def layer_coverage(docs: list[tuple[Path, dict]]) -> dict[str, int]:
    """Count load-bearing docs per top-level folder under docs/."""
    coverage = Counter()
    for fp, fm in docs:
        if not is_load_bearing(fm):
            continue
        # Get top-level folder: docs/overview/... → overview
        parts = fp.parts
        try:
            docs_idx = parts.index("docs")
            if len(parts) > docs_idx + 1:
                top = parts[docs_idx + 1]
                coverage[top] += 1
        except ValueError:
            pass
    return dict(coverage)


# ── Main ───────────────────────────────────────────────────────────


def main():
    short = "--short" in sys.argv

    # Determine docs root
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        root = Path(args[0]).resolve()
    else:
        script_dir = Path(__file__).resolve().parent
        project = find_project_root(script_dir)
        root = (project / "docs") if project else (Path.cwd() / "docs")

    if not root.exists():
        print(f"Error: {root} does not exist.")
        sys.exit(1)

    # Collect data
    docs = walk_docs(root)
    index_files = {
        idx: collect_index_links(idx)
        for idx in sorted(root.rglob("INDEX.md"))
    }
    incoming = build_incoming_links(docs, index_files)

    # Counts
    status_counts = Counter(fm.get("status", "active") for _, fm in docs)
    type_counts = Counter(fm.get("node_type", "?") for _, fm in docs if fm.get("node_type"))
    load_bearing = sum(1 for _, fm in docs if is_load_bearing(fm))

    # Issues
    orphans = check_orphans(docs, incoming)
    broken = check_broken_links(docs, index_files)
    unsynced = check_unsynced(docs)
    drifted = check_drifted(docs)
    untagged = check_untagged(docs)
    missing_dod = check_missing_dod(docs)
    stale, oldest_path, oldest_days = check_staleness(docs)
    coverage = layer_coverage(docs)

    # ── Output ───────────────────────────────────────────────

    print(f"\n  DOCUMENTATION HEALTH — {today_str()}")
    print(f"  {'═' * 50}")

    # Counts
    print(f"\n  {len(docs)} documents ({load_bearing} load-bearing) across {len(set(fp.parent for fp, _ in docs))} folders")

    status_line = "  ".join(
        f"{status_emoji(s)} {s}: {c}" for s, c in sorted(status_counts.items())
    )
    print(f"  {status_line}")

    if not short:
        type_line = "  ".join(f"{t}: {c}" for t, c in sorted(type_counts.items()))
        print(f"  {type_line}")

    # ── Structural Issues ────────────────────────────────────

    issues_found = bool(orphans or broken or drifted or untagged or missing_dod)

    if issues_found:
        print(header("STRUCTURAL ISSUES"))

    if orphans:
        print(f"\n  ❌ {len(orphans)} orphan{'s' if len(orphans) > 1 else ''} (no incoming links)")
        for fp in orphans:
            print(f"     • {fp.relative_to(root)}")

    if broken:
        print(f"\n  ❌ {len(broken)} broken link{'s' if len(broken) > 1 else ''}")
        for src, lt, target in broken:
            src_rel = src.relative_to(root)
            target_rel = target.relative_to(root) if target.is_relative_to(root) else str(target)
            print(f"     • {src_rel} → ({lt}) → {target_rel}  (not found)")

    if drifted:
        print(f"\n  ⚠️  {len(drifted)} doc{'s' if len(drifted) > 1 else ''} drifted (sync_status: drifted)")
        for fp in drifted:
            print(f"     • {fp.relative_to(root)}")

    if untagged:
        print(f"\n  ⚠️  {len(untagged)} doc{'s' if len(untagged) > 1 else ''} with no tags")
        if not short:
            for fp in untagged:
                print(f"     • {fp.relative_to(root)}")

    if missing_dod:
        print(f"\n  ⚠️  {len(missing_dod)} spec{'s' if len(missing_dod) > 1 else ''} missing Definition of Done")
        if not short:
            for fp in missing_dod:
                print(f"     • {fp.relative_to(root)}")

    # ── Sync Status ─────────────────────────────────────────

    if unsynced:
        print(header("SYNC STATUS"))
        print(f"\n  ⚠️  {len(unsynced)} doc{'s' if len(unsynced) > 1 else ''} never synced (sync_status: unchecked)")
        if not short:
            for fp in unsynced:
                print(f"     • {fp.relative_to(root)}")

    # ── Staleness ───────────────────────────────────────────

    if oldest_path:
        print(header("STALENESS"))
        print(f"\n  🕐  oldest update: {oldest_days} days ago — {oldest_path.relative_to(root)}")
        if stale:
            print(f"  🕐  {len(stale)} doc{'s' if len(stale) > 1 else ''} untouched > 90 days")
            if not short:
                for fp, d, days in sorted(stale, key=lambda x: -x[2]):
                    print(f"     • {fp.relative_to(root)} ({days}d)")

    # ── Layer Coverage ──────────────────────────────────────

    if coverage:
        print(header("LAYER COVERAGE"))
        expected = {"overview", "spec", "architecture", "guides", "ops", "reference", "changes", "archive"}
        for layer in sorted(expected | set(coverage.keys())):
            count = coverage.get(layer, 0)
            mark = "✅" if count > 0 else "⚠️ "
            print(f"  {mark}  {layer}/  — {count} doc{'s' if count != 1 else ''}")

    # ── Summary ─────────────────────────────────────────────

    total_issues = len(orphans) + len(broken) + len(drifted) + len(untagged) + len(unsynced) + len(missing_dod)
    print()
    if total_issues == 0:
        print("  ✨  No issues found. Docs are healthy!")
    else:
        print(f"  📋  {total_issues} issues to investigate. Run with --short to hide details.")
    print()


if __name__ == "__main__":
    main()
