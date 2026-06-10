"""Shared ontology utilities — frontmatter parsing and doc discovery.

Used by index.py, status.py, and map.py.
Single source of truth for YAML parsing, emoji mapping, and doc walking.
"""

import yaml
from pathlib import Path
from typing import Optional
from datetime import date


STATUS_EMOJI = {
    "active": "🟢",
    "draft": "🟡",
    "deprecated": "🔴",
    "archived": "⚫",
}

LINK_TYPES = {
    "depends_on", "documents", "implemented_by",
    "supersedes", "relates_to", "part_of", "implements",
}


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from markdown text. Returns empty dict if none found or invalid."""
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        result = yaml.safe_load(parts[1])
        return result if isinstance(result, dict) else {}
    except yaml.YAMLError:
        return {}


def read_doc(filepath: Path) -> Optional[dict]:
    """Read a markdown file and return its parsed frontmatter, or None if unreadable."""
    try:
        text = filepath.read_text(encoding="utf-8")
        return parse_frontmatter(text)
    except Exception:
        return None


def walk_docs(root: Path) -> list[tuple[Path, dict]]:
    """Walk docs/ recursively, return sorted list of (filepath, frontmatter). Skips INDEX.md files."""
    results = []
    for f in sorted(root.rglob("*.md")):
        if f.name == "INDEX.md":
            continue
        fm = read_doc(f)
        if fm is not None:
            results.append((f, fm))
    return results


def get_title(filepath: Path, fm: dict) -> str:
    """Extract display title: frontmatter title > filename stem."""
    title = fm.get("title", "")
    if title:
        return title
    return filepath.stem.replace("-", " ").replace("_", " ").title()


def find_project_root(start: Path) -> Optional[Path]:
    """Walk up from start until we find a docs/ folder. Returns project root or None."""
    candidate = start.resolve()
    while candidate != candidate.parent:
        if (candidate / "docs").is_dir():
            return candidate
        candidate = candidate.parent
    return None


def resolve_links(filepath: Path, fm: dict) -> dict[str, list[Path]]:
    """Extract typed links from frontmatter, resolving relative paths against the doc's directory.

    Returns {link_type: [resolved_target_paths]}.
    Handles both string values and lists of strings.
    """
    links = fm.get("links", {})
    if not isinstance(links, dict):
        return {}

    base = filepath.parent
    resolved = {}
    for link_type, targets in links.items():
        if link_type not in LINK_TYPES:
            continue
        if isinstance(targets, str):
            targets = [targets]
        if not isinstance(targets, list):
            continue
        paths = []
        for t in targets:
            if not isinstance(t, str):
                continue
            target = (base / t).resolve()
            paths.append(target)
        if paths:
            resolved[link_type] = paths
    return resolved


def is_load_bearing(fm: dict) -> bool:
    """A doc is load-bearing if it has a valid node_type and isn't deprecated/archived."""
    nt = fm.get("node_type", "")
    status = fm.get("status", "active")
    return bool(nt) and status not in ("deprecated", "archived")


def collect_index_links(index_path: Path) -> list[Path]:
    """Parse an INDEX.md to extract which .md files it links to.

    Returns resolved absolute paths for linked markdown files.
    """
    try:
        text = index_path.read_text(encoding="utf-8")
    except Exception:
        return []

    import re
    base = index_path.parent
    targets = []
    # Match markdown links: [text](path.md) or [text](path/INDEX.md)
    for match in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", text):
        href = match.group(2)
        # Resolve relative to the index's directory
        target = (base / href).resolve()
        if target.suffix == ".md" and target != index_path.resolve():
            targets.append(target)
    return targets


def today_str() -> str:
    return date.today().isoformat()


def now_ts() -> str:
    """Return HH:MM timestamp for log entries."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M")


def log_operation(docs_root: Path, operation: str, detail: str = ""):
    """Append a timestamped entry to docs/log.md. Creates the file if needed.

    Usage:
        log_operation(root, "index", "rebuilt 47 docs across 12 folders")
        log_operation(root, "sync", "spec/auth.md — verified, no drift")
        log_operation(root, "curate", "created guides/setup.md")
    """
    log_path = docs_root / "log.md"
    today = today_str()
    ts = now_ts()

    entry = f"- `{ts}` **{operation}** {detail}\n"

    try:
        existing = log_path.read_text(encoding="utf-8")
    except Exception:
        existing = ""

    lines = existing.splitlines()

    # Check if today's heading already exists
    today_header = f"## {today}"
    if today_header in existing:
        # Append to today's section
        new_content = existing.rstrip("\n") + "\n" + entry
    else:
        # Add new day heading
        separator = "\n" if existing and not existing.endswith("\n") else ""
        new_content = existing.rstrip("\n") + separator + f"\n{today_header}\n\n{entry}"

    log_path.write_text(new_content, encoding="utf-8")


def build_graph(docs: list[tuple[Path, dict]], index_files: dict[Path, list[Path]] | None = None) -> dict[Path, list[tuple[Path, str]]]:
    """Build adjacency: doc → list of (target_path, link_type).

    Sources: frontmatter links from all docs, plus INDEX.md links if provided.
    """
    from collections import defaultdict
    graph = defaultdict(list)

    for src_path, fm in docs:
        resolved = resolve_links(src_path, fm)
        for link_type, targets in resolved.items():
            for target in targets:
                graph[src_path.resolve()].append((target, link_type))

    if index_files:
        for index_path, targets in index_files.items():
            for target in targets:
                graph[index_path.resolve()].append((target, "index"))

    return dict(graph)


def build_reverse(graph: dict[Path, list[tuple[Path, str]]]) -> dict[Path, list[tuple[Path, str]]]:
    """Build reverse adjacency: doc → list of (source_path, link_type)."""
    from collections import defaultdict
    rev = defaultdict(list)
    for src, edges in graph.items():
        for target, link_type in edges:
            rev[target].append((src, link_type))
    return dict(rev)
