#!/usr/bin/env python3
"""Graph query tool — walk the documentation graph via frontmatter links.

Usage:
    python scripts/map.py docs/spec/auth.md       # incoming + outgoing for one doc
    python scripts/map.py --orphans                # list all orphan docs
    python scripts/map.py --broken                 # list all broken links
    python scripts/map.py docs/spec/auth.md --depth 2  # walk 2 hops out
    python scripts/map.py --from docs/spec/auth.md      # outgoing only
    python scripts/map.py --to docs/spec/auth.md        # incoming only
"""

import sys
from pathlib import Path

from _ontology import (
    walk_docs,
    read_doc,
    resolve_links,
    collect_index_links,
    find_project_root,
    get_title,
    build_graph,
    build_reverse,
)


def display_path(p: Path, root: Path) -> str:
    """Human-readable path relative to root, or absolute fallback."""
    try:
        return str(p.relative_to(root))
    except ValueError:
        return str(p)


def print_edges(label: str, edges: list[tuple[Path, str]], root: Path, docs_index: dict[Path, dict]):
    """Print a list of graph edges with titles."""
    if not edges:
        print(f"  {label}\n  {'─' * len(label)}\n  (none)\n")
        return

    print(f"  {label}")
    print(f"  {'─' * len(label)}")
    for target, link_type in sorted(edges, key=lambda x: x[1]):
        title = ""
        if target in docs_index:
            title = docs_index[target].get("title", "")
        title_str = f" — {title}" if title else ""
        print(f"  {display_path(target, root)}  ({link_type}){title_str}")
    print()


def find_broken(graph: dict[Path, list], reverse: dict[Path, list], docs_index: dict[Path, dict], root: Path):
    """List all broken links (target doesn't exist in docs_index or as index)."""
    all_targets = set(docs_index.keys())
    # INDEX.md files are also valid targets
    for p in graph:
        if p.name == "INDEX.md":
            all_targets.add(p)

    broken = []
    for src, edges in graph.items():
        for target, link_type in edges:
            if target not in all_targets:
                broken.append((src, target, link_type))

    if broken:
        print(f"  BROKEN LINKS ({len(broken)})\n  {'─' * 30}")
        for src, target, lt in broken:
            print(f"  {display_path(src, root)}  → ({lt}) →  {display_path(target, root)}  ❌ not found")
        print()
    else:
        print("  ✨  No broken links found.\n")


def find_orphans(graph: dict[Path, list], reverse: dict[Path, list], docs_index: dict[Path, dict], root: Path):
    """List docs with no incoming links and not an INDEX.md."""
    orphans = []
    for fp, fm in docs_index.items():
        if fp.name == "INDEX.md":
            continue
        # Only load-bearing docs
        status = fm.get("status", "active")
        if status in ("deprecated", "archived"):
            continue
        if fp not in reverse or not reverse[fp]:
            orphans.append(fp)

    if orphans:
        print(f"  ORPHANS ({len(orphans)})\n  {'─' * 30}")
        for fp in sorted(orphans, key=lambda p: display_path(p, root)):
            title = docs_index.get(fp, {}).get("title", "")
            title_str = f" — {title}" if title else ""
            print(f"  {display_path(fp, root)}{title_str}")
        print()
    else:
        print("  ✨  No orphans found.\n")


def walk_hops(start: Path, graph: dict[Path, list], depth: int, root: Path, docs_index: dict[Path, dict]):
    """BFS walk from start, printing nodes at each depth."""
    visited = {start}
    frontier = {start}

    for hop in range(1, depth + 1):
        next_frontier = set()
        for node in frontier:
            for target, _ in graph.get(node, []):
                if target not in visited:
                    next_frontier.add(target)
                    visited.add(target)

        if not next_frontier:
            print(f"  (no nodes reachable at depth {hop})")
            break

        print(f"  Depth {hop} ({len(next_frontier)} node{'s' if len(next_frontier) > 1 else ''})")
        print(f"  {'─' * 20}")
        for node in sorted(next_frontier, key=lambda p: display_path(p, root)):
            title = docs_index.get(node, {}).get("title", "")
            title_str = f" — {title}" if title else ""
            print(f"  {display_path(node, root)}{title_str}")
        print()

        frontier = next_frontier


# ── Main ───────────────────────────────────────────────────────────


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        if __doc__:
            print(__doc__.strip())
        sys.exit(0)

    # Determine docs root — first positional arg that's a directory wins
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    script_dir = Path(__file__).resolve().parent

    root = None
    doc_args = []
    for a in args:
        p = Path(a).resolve()
        if p.is_dir():
            root = p
        else:
            doc_args.append(a)

    if root is None:
        project = find_project_root(script_dir)
        root = (project / "docs") if project else (Path.cwd() / "docs")

    if not root.exists():
        print(f"Error: {root} does not exist.")
        sys.exit(1)

    # Collect data
    docs = walk_docs(root)
    docs_index = {fp.resolve(): fm for fp, fm in docs}
    index_files = {
        idx: collect_index_links(idx)
        for idx in sorted(root.rglob("INDEX.md"))
    }

    graph = build_graph(docs, index_files)
    reverse = build_reverse(graph)

    # Modes
    orphans_only = "--orphans" in sys.argv
    broken_only = "--broken" in sys.argv
    outgoing_only = "--from" in sys.argv
    incoming_only = "--to" in sys.argv
    depth_arg = None

    for i, arg in enumerate(sys.argv):
        if arg == "--depth" and i + 1 < len(sys.argv):
            try:
                depth_arg = int(sys.argv[i + 1])
            except ValueError:
                pass

    # Target doc
    target_path = None
    for a in doc_args:
        p = (Path.cwd() / a).resolve()
        if p.exists() and p.suffix == ".md":
            target_path = p
            break
        # Try relative to root
        p2 = (root / a).resolve()
        if p2.exists() and p2.suffix == ".md":
            target_path = p2
            break

    print(f"  Docs root: {root}")
    print(f"  {len(docs)} documents, {len(index_files)} index files")

    if broken_only:
        find_broken(graph, reverse, docs_index, root)
        return

    if orphans_only:
        find_orphans(graph, reverse, docs_index, root)
        return

    if not target_path:
        print("\n  Usage: map.py <path-to-doc.md>  (or --orphans / --broken)")
        print("  Run with --help for full usage.\n")
        return

    resolved = target_path.resolve()
    if resolved not in docs_index:
        print(f"\n  Error: {target_path} not found in docs index.\n")
        sys.exit(1)

    fm = docs_index[resolved]
    title = get_title(resolved, fm)
    nt = fm.get("node_type", "?")
    status = fm.get("status", "?")
    print(f"\n  {display_path(resolved, root)}")
    print(f"  node_type: {nt}  |  status: {status}  |  title: {title}")

    # Outgoing
    out = graph.get(resolved, [])
    # Incoming
    inc = reverse.get(resolved, [])

    if outgoing_only:
        print_edges("OUTGOING", out, root, docs_index)
    elif incoming_only:
        print_edges("INCOMING", inc, root, docs_index)
    elif depth_arg:
        print(f"\n  WALKING {depth_arg} hops from {display_path(resolved, root)}")
        print(f"  {'═' * 40}")
        walk_hops(resolved, graph, depth_arg, root, docs_index)
    else:
        root_display = root
        print_edges("INCOMING", inc, root_display, docs_index)
        print_edges("OUTGOING", out, root_display, docs_index)
        if inc or out:
            print(f"  📊  {len(inc)} incoming, {len(out)} outgoing")
            print()


if __name__ == "__main__":
    main()
