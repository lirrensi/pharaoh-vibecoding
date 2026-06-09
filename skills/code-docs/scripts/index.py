#!/usr/bin/env python3
"""Generate INDEX.md files for every folder in docs/.

Scans docs/ recursively, reads YAML frontmatter from each .md file,
and writes an INDEX.md in each folder with:
- Links to every .md file with title + status emoji
- Links to every subfolder's INDEX.md
- A tags section aggregating all tags

Usage:
    python scripts/index.py           # scan docs/ and rebuild all INDEX.md
    python scripts/index.py --dry-run  # show what would be generated
    python scripts/index.py docs/spec  # rebuild only docs/spec/ and below
"""

import sys
import re
from pathlib import Path
from datetime import date


STATUS_EMOJI = {
    "active": "",
    "draft": "[draft]",
    "deprecated": "[deprecated]",
    "archived": "[archived]",
}


def parse_frontmatter(text: str) -> dict:
    """Extract YAML-like frontmatter between --- delimiters."""
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm_text = parts[1].strip()
    data = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        # Parse list values like [auth, security]
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip().strip("'\"") for v in value[1:-1].split(",") if v.strip()]
        # Remove quotes
        elif value.startswith('"') or value.startswith("'"):
            value = value[1:-1]
        data[key] = value
    return data


def get_title(filepath: Path) -> str:
    """Extract title: frontmatter title > first # heading > filename stem."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return filepath.stem

    fm = parse_frontmatter(text)
    if fm.get("title"):
        return fm["title"]

    for line in text.split("\n"):
        match = re.match(r"^#\s+(.+)", line)
        if match:
            return match.group(1).strip()

    return filepath.stem


def get_summary(filepath: Path):
    """Get a one-line summary: title from frontmatter or filename stem.
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
        return display, set(fm.get("tags", [])) if isinstance(fm.get("tags"), list) else set()
    except Exception:
        return filepath.stem, set()


def build_index(folder: Path, dry_run: bool = False) -> tuple[int, int]:
    """Build INDEX.md for a single folder. Returns (files_indexed, tags_found)."""
    if not folder.is_dir():
        return 0, 0

    md_files = sorted([f for f in folder.iterdir() if f.suffix == ".md" and f.name != "INDEX.md"])
    subfolders = sorted([d for d in folder.iterdir() if d.is_dir() and not d.name.startswith(".")])

    if not md_files and not subfolders:
        return 0, 0

    entries = []
    all_tags = set()

    # Document entries
    for f in md_files:
        summary, tags = get_summary(f)
        entries.append(f"- [{summary}]({f.name})")
        all_tags.update(tags)

    # Subfolder entries — always link (serves as reminder that subfolder needs INDEX.md)
    for d in subfolders:
        entries.append(f"- [{d.name}/]({d.name}/INDEX.md)")

    # Build content
    today = date.today().isoformat()
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
    can link to already-generated child INDEX.md files."""
    total_files = 0
    total_folders = 0

    # Collect all folders, sort by depth (deepest first)
    folders = []
    for folder in root.rglob("*"):
        if folder.is_dir() and not folder.name.startswith("."):
            depth = len(folder.relative_to(root).parts)
            folders.append((depth, folder))

    # Process deepest first so children exist when parents link to them
    folders.sort(key=lambda x: -x[0])

    for depth, folder in folders:
        files, tags = build_index(folder, dry_run=dry_run)
        if files > 0 or any(
            d.is_dir() for d in folder.iterdir() if not d.name.startswith(".")
        ):
            total_files += files
            total_folders += 1

    print(f"\nIndexed {total_files} files across {total_folders} folders.")


def main():
    dry_run = "--dry-run" in sys.argv

    # Determine root
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        root = Path(args[0]).resolve()
    else:
        # Default: docs/ relative to project root (3 levels up from scripts/)
        script_dir = Path(__file__).resolve().parent
        project_root = script_dir.parent.parent.parent  # scripts/ -> code-docs/ -> skills/ -> root
        root = project_root / "docs"

    if not root.exists():
        print(f"Error: {root} does not exist. Create docs/ first or specify a path.")
        sys.exit(1)

    mode = "DRY RUN" if dry_run else "BUILDING"
    print(f"{mode} INDEX.md files for {root}/")
    build_all(root, dry_run=dry_run)


if __name__ == "__main__":
    main()
