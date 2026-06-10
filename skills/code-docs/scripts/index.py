#!/usr/bin/env python3
"""Generate INDEX.md files for every folder in docs/.

Scans docs/ recursively, reads YAML frontmatter from each .md file,
and writes an INDEX.md in each folder with:
- Links to every .md file with title + status emoji
- Graph annotations: outgoing links (→) and incoming links (←) per doc
- Links to every subfolder's INDEX.md
- A tags section aggregating all tags

Usage:
    python scripts/index.py           # scan docs/ and rebuild all INDEX.md
    python scripts/index.py --dry-run  # show what would be generated
    python scripts/index.py docs/spec  # rebuild only docs/spec/ and below
"""

import sys
from pathlib import Path
from collections import defaultdict

from _ontology import (
    STATUS_EMOJI,
    parse_frontmatter,
    get_title,
    find_project_root,
    resolve_links,
    build_reverse,
    today_str,
)


def shorten_path(target: Path, base: Path) -> str:
    """Show a target path compactly, relative to docs root or as filename."""
    try:
        rel = target.relative_to(base)
        return str(rel).replace("\\", "/")
    except ValueError:
        try:
            rel = target.relative_to(base.parent)
            return "../" + str(rel).replace("\\", "/")
        except ValueError:
            return target.name


def format_links(filepath: Path, docs_root: Path, reverse: dict, all_docs: dict) -> str:
    """Build a compact link annotation line for a single document.

    Shows outgoing (→) and incoming (←) links, one per type.
    Returns empty string if no links.
    """
    resolved_fp = filepath.resolve()
    out_links = resolve_links(filepath, all_docs.get(resolved_fp, {}))
    in_links = reverse.get(resolved_fp, [])

    if not out_links and not in_links:
        return ""

    parts = []

    # Outgoing: → target (type)
    for link_type in ["depends_on", "documents", "implements", "supersedes", "relates_to", "part_of", "implemented_by"]:
        targets = out_links.get(link_type, [])
        for t in targets:
            label = shorten_path(t, docs_root)
            parts.append(f"→ {label} ({link_type})")

    # Incoming: ← source (type)
    seen = set()
    for src, link_type in in_links:
        if src == resolved_fp:
            continue
        key = (src, link_type)
        if key in seen:
            continue
        seen.add(key)
        label = shorten_path(src, docs_root)
        parts.append(f"← {label} ({link_type})")

    if not parts:
        return ""

    return "  " + "  ·  ".join(parts)


def get_summary(filepath: Path, docs_root: Path, reverse: dict, all_docs: dict):
    """Get a one-line summary: title + status emoji, with graph annotations.
    Returns (display_string, tags_set)."""
    try:
        text = filepath.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        title = fm.get("title", "")
        status = fm.get("status", "active")
        emoji = STATUS_EMOJI.get(status, "")
        display = title or filepath.stem.replace("-", " ").replace("_", " ").title()
        if emoji:
            display = f"{display} {emoji}"

        # Build link annotation line
        link_line = format_links(filepath, docs_root, reverse, all_docs)

        tags = set(fm.get("tags", [])) if isinstance(fm.get("tags"), list) else set()
        return display, tags, link_line
    except Exception:
        return filepath.stem, set(), ""


def build_index(folder: Path, docs_root: Path, reverse: dict, all_docs: dict, dry_run: bool = False) -> tuple[int, int]:
    """Build INDEX.md for a single folder. Returns (files_indexed, tags_found)."""
    if not folder.is_dir():
        return 0, 0

    md_files = sorted([f for f in folder.iterdir() if f.suffix == ".md" and f.name != "INDEX.md"])
    subfolders = sorted([d for d in folder.iterdir() if d.is_dir() and not d.name.startswith(".")])

    if not md_files and not subfolders:
        return 0, 0

    entries = []
    all_tags = set()

    # Document entries with graph annotations
    for f in md_files:
        display, tags, link_line = get_summary(f, docs_root, reverse, all_docs)
        entries.append(f"- [{display}]({f.name})")
        if link_line:
            entries.append(link_line)
        all_tags.update(tags)

    # Subfolder entries
    for d in subfolders:
        entries.append(f"- [{d.name}/]({d.name}/INDEX.md)")

    # Build content
    today = today_str()
    folder_name = folder.name if folder.name != "docs" else "Documentation"

    lines = [
        "---",
        "node_type: index",
        f"updated: {today}",
        "---",
        "",
        f"# {folder_name} Index",
        "",
    ]

    if entries:
        lines.append("## Contents")
        lines.append("")
        lines.extend(entries)
        lines.append("")

    if all_tags:
        tag_list = " ".join(f"`{t}`" for t in sorted(all_tags))
        lines.append("## Tags")
        lines.append("")
        lines.append(tag_list)
        lines.append("")

    lines.append("---")
    lines.append(f"*Auto-generated. Last rebuilt: {today}*")
    lines.append("")

    content = "\n".join(lines)

    if dry_run:
        print(f"\n--- {folder / 'INDEX.md'} ---")
        print(content)
    else:
        index_file = folder / "INDEX.md"
        index_file.write_text(content, encoding="utf-8")
        print(f"  ✓ {index_file}")

    return len(md_files), len(all_tags)


def build_all(root: Path, dry_run: bool = False):
    """Walk docs/ and build INDEX.md for every folder.

    Processes deepest folders first (depth-first) so parent INDEX.md
    can link to already-generated child INDEX.md files.
    Also computes the full doc graph so entries show incoming/outgoing links.
    """
    # ── First pass: collect all docs and build the graph ──

    all_docs = {}  # resolved_path → frontmatter
    for f in sorted(root.rglob("*.md")):
        if f.name == "INDEX.md":
            continue
        try:
            text = f.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            all_docs[f.resolve()] = fm
        except Exception:
            pass

    # Build graph + reverse index
    from _ontology import build_graph as bg
    docs_list = [(fp, fm) for fp, fm in all_docs.items()]
    graph = bg(docs_list)
    reverse = build_reverse(graph)

    # ── Second pass: generate indexes with link annotations ──

    total_files = 0
    total_folders = 0

    # Collect all folders, sort by depth (deepest first)
    folders = []
    for folder in root.rglob("*"):
        if folder.is_dir() and not folder.name.startswith("."):
            depth = len(folder.relative_to(root).parts)
            folders.append((depth, folder))

    folders.sort(key=lambda x: -x[0])

    for depth, folder in folders:
        files, tags = build_index(folder, root, reverse, all_docs, dry_run=dry_run)
        if files > 0 or any(
            d.is_dir() for d in folder.iterdir() if not d.name.startswith(".")
        ):
            total_files += files
            total_folders += 1

    print(f"\nIndexed {total_files} files across {total_folders} folders.")


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        if __doc__:
            print(__doc__.strip())
        sys.exit(0)

    dry_run = "--dry-run" in sys.argv

    # Determine root
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        root = Path(args[0]).resolve()
    else:
        script_dir = Path(__file__).resolve().parent
        project = find_project_root(script_dir)
        root = (project / "docs") if project else (Path.cwd() / "docs")

    if not root.exists():
        print(f"Error: {root} does not exist. Create docs/ first or specify a path.")
        sys.exit(1)

    mode = "DRY RUN" if dry_run else "BUILDING"
    print(f"{mode} INDEX.md files for {root}/")
    build_all(root, dry_run=dry_run)


if __name__ == "__main__":
    main()
