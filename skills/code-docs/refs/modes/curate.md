# Mode: Curate

**Trigger:** Asked to create, update, move, or deprecate individual documents. Handles single-doc changes. For multi-doc feature changes, use Propose mode instead.

---

## Before Any Write — Search First

1. Read the folder's `INDEX.md` to see what already exists.
2. If the topic already has a document → **edit the existing one**, don't create a second.
3. If a similar topic exists → check whether this belongs as a new section in an existing doc.

---

## CREATE — New Document

### 1. Classify
Determine the `node_type` and folder from `../ontology.md` and `../folder-structure.md`.

### 2. Place
Put it in the correct folder. If unsure:
- Behavioral spec → `docs/spec/` or `docs/spec/features/`
- How-to → `docs/guides/`
- Architecture → `docs/architecture/` or `docs/architecture/components/`

### 3. Frontmatter
Add full frontmatter per `../ontology.md`:
```yaml
---
node_type: <type>
title: <Human Name>
status: active
updated: YYYY-MM-DD
tags: [domain, topic]
links:
  depends_on: [/path/to/parent.md]
---
```

### 4. Content
Write content following the format for the `node_type`:
- `spec` → use `../spec-format.md`. Focus on behavior, protocol contracts, internal processing — NOT UI details.
- `overview` → free-form but concise, warm tone. Focus on user experience, not interface.
- `architecture` / `component` → structural, factual. Focus on internal behavior, processing pipelines, and communication protocols.
- `guide` → step-by-step, task-oriented
- `adr` → Status, Context, Decision, Consequences

### 5. Link
Add at least one incoming link in frontmatter:
- Add `links: depends_on` in frontmatter to parent/related docs.
- INDEX.md entries are auto-generated from frontmatter `title` and `status` — you do NOT manually add entries.

### 6. Rebuild INDEX.md
Run `python scripts/index.py` to regenerate all INDEX.md files from frontmatter.
**Never hand-edit an INDEX.md — the script wipes and overwrites every INDEX.md.** Any manual change you make will be lost.

---

## UPDATE — Edit Existing Document

1. **Read first.** Load the current doc and any `depends_on` links.
2. **Check layer.** Don't put implementation detail in spec, don't put behavioral requirements in architecture.
3. **Bump updated.** Change `updated: YYYY-MM-DD` in frontmatter.
4. **Report.** After editing, say what changed, which doc was touched, and any conflicts.

### When to update vs deprecate + replace
- **Update** if the change is small (adding a scenario, fixing a description).
- **Deprecate + create new** if the change is fundamental (new approach, different architecture).

---

## MOVE — Relocate a Document

1. **Use git mv** to preserve history: `git mv docs/old/path.md docs/new/path.md`
2. **Rewrite every link** pointing to the old path — check all frontmatter `links:` and body markdown links.
3. **Run `python scripts/index.py`** to regenerate all INDEX.md files — the script will pick up the new location from frontmatter and the old folder's INDEX.md will drop the entry automatically.

---

## DEPRECATE — Mark as Outdated

1. Set `status: deprecated` in frontmatter.
2. Add `supersedes: [old-file.md]` in the replacement doc's frontmatter (if applicable).
3. Run `python scripts/index.py` — the script reads `status: deprecated` from frontmatter and adds the 🔴 emoji automatically.
4. **Never physically delete a file.** No text must be lost as a result of any operation. Git preserves history; the doc stays for reference. Moving to `archive/` is allowed (the file still exists).

---

## Reference Files

Always load for Curate mode:
- `../ontology.md` — node_type vocabulary, frontmatter spec, link types, status values
- `../index-spec.md` — INDEX.md format and script usage (`python scripts/index.py`)

Load as needed:
- `../folder-structure.md` — if placing a new doc or reorganizing
- `../spec-format.md` — if writing a behavioral spec
- `../principles.md` — if unsure about layer boundaries
