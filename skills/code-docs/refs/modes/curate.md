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
  depends_on: [../path/to/parent.md]
---
```

### 4. Content
Write content following the format for the `node_type`:
- `spec` / `feature-spec` → use `../spec-format.md`
- `overview` → free-form but concise, warm tone
- `architecture` / `component` → structural, factual
- `guide` → step-by-step, task-oriented
- `adr` → Status, Context, Decision, Consequences

### 5. Link
Add at least one incoming link:
- Add an entry to the folder's `INDEX.md`: `- [Title](file.md) — one-line summary`
- Add `links: depends_on` in frontmatter to parent/related docs

### 6. Rebuild INDEX.md
Update the folder's `INDEX.md` — add the new document entry and rebuild the tags section.

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
3. **Update both INDEX.md files** — remove from old folder, add to new folder.
4. **Rebuild both INDEX.md files** — tags and summaries.

---

## DEPRECATE — Mark as Outdated

1. Set `status: deprecated` in frontmatter.
2. Add `supersedes: [old-file.md]` in the replacement doc's frontmatter (if applicable).
3. Update the INDEX.md entry: add 🔴 status emoji.
4. **Never delete.** Git preserves history; the doc stays for reference.

---

## Reference Files

Always load for Curate mode:
- `../ontology.md` — node_type vocabulary, frontmatter spec, link types, status values
- `../index-spec.md` — INDEX.md format for rebuilding

Load as needed:
- `../folder-structure.md` — if placing a new doc or reorganizing
- `../spec-format.md` — if writing a behavioral spec
- `../principles.md` — if unsure about layer boundaries
