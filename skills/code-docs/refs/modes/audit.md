# Mode: Audit

**Trigger:** Asked to check documentation health, verify invariants, or find quality issues. Runs passive checks — never edits docs unless explicitly asked.

---

## Workflow

### Step 1: Load ontology
Read `../ontology.md` for the invariant definitions and vocabulary.

### Step 2: Run each invariant check

#### I1: Every folder has INDEX.md
Scan `docs/` recursively. Every directory must contain an `INDEX.md` file.

**Check:**
- List all directories under `docs/`
- Check for `INDEX.md` in each
- Skip `docs/changes/<name>/` folders (they don't need INDEX.md; only `docs/changes/INDEX.md` matters)

**Report:**
```
Missing INDEX.md:
- docs/guides/ — no INDEX.md found
- docs/spec/features/ — no INDEX.md found
```

#### I2: Every doc has valid frontmatter
Scan all `.md` files in `docs/`. Each must have:
- YAML frontmatter (between `---` delimiters)
- A valid `node_type` field (must be in the vocabulary)

**Check:**
- Files with no frontmatter → flag
- Files with missing `node_type` → flag
- Files with `node_type` outside vocabulary → flag (suggest closest match)

**Report:**
```
Frontmatter issues:
- spec/features/auth.md — missing node_type
- architecture/old-stuff.md — invalid node_type "legacy" (did you mean "architecture"?)
- guides/setup.md — no frontmatter at all
```

#### I3: No broken cross-references
Check every markdown link `[text](path.md)` in both body text and frontmatter `links:`.

**Check:**
- For each link, verify the target file exists
- For `links:` frontmatter arrays, verify each path resolves
- Skip external URLs (http/https)

**Report:**
```
Broken links:
- spec/features/auth.md → /overview/product.md (broken: product.md not found at that path)
- spec/features/api.md: links.documents → /src/api/ (directory exists, but no .md files there)
```

#### I4: No orphans
Every load-bearing doc (not `node_type: index` or `node_type: change-*`) must have at least one incoming link.

**Check:**
- For each doc, search all other docs' `links:` frontmatter and INDEX.md entries for a link to it
- A doc is orphaned if NOTHING links to it (not from any INDEX.md, not from any `links: depends_on`, not from any body link)

**Report:**
```
Orphaned documents (no incoming links):
- spec/features/old-feature.md — exists but nothing references it
- architecture/components/unused.md — not linked from any INDEX.md or doc
```

#### I5: Superseded docs are marked
Check frontmatter `links: supersedes` targets. The target doc must have `status: deprecated` or `status: archived`.

**Check:**
- Find all docs with `links: supersedes`
- Read the target's frontmatter
- If target `status` is `active` → flag

**Report:**
```
Supersede issues:
- spec/features/auth-v2.md supersedes auth-v1.md — but auth-v1.md is still status: active
```

#### I6: Layer coherence
Check that lower layers don't contradict higher layers.

**Check (heuristic — not exhaustive):**
- `architecture/` docs should not define behavioral requirements (that belongs in `spec/`)
- `spec/` docs should not reference implementation details (classes, files, frameworks)
- `overview/` docs should not contain detailed behavioral specs

**Report:**
```
Layer coherence issues:
- architecture/components/agent.md — contains behavioral requirements (should be in spec/)
- spec/features/api.md — references "Express middleware" (implementation detail, should be in architecture/)
```

### Step 3: Generate summary

```markdown
## Audit Report — YYYY-MM-DD

### Summary
| Invariant | Status | Issues |
|-----------|--------|--------|
| I1: INDEX.md coverage | ❌ 2 missing | guides/, spec/features/ |
| I2: Valid frontmatter | ❌ 3 issues | See below |
| I3: No broken links | ✅ Clean | — |
| I4: No orphans | ❌ 2 orphans | See below |
| I5: Supersede marking | ✅ Clean | — |
| I6: Layer coherence | ⚠️ 2 warnings | See below |

### Files checked
{N} documents across {N} folders

### Recommendations
1. Run `python scripts/index.py` to generate INDEX.md for all folders
2. Add frontmatter to: guides/setup.md, architecture/old-stuff.md
3. Link or deprecate orphaned docs: old-feature.md, unused.md
4. Move behavioral requirements from architecture/components/agent.md to spec/
```

---

## Audit Severity

| Symbol | Meaning |
|--------|---------|
| ❌ | Must fix — breaks ontology guarantees |
| ⚠️ | Should fix — degrades doc quality |
| ✅ | Clean |

---

## What NOT to do during Audit

- ❌ Edit any docs (unless explicitly asked to fix issues found)
- ❌ Run `python scripts/index.py` automatically (report the gap, don't fill it)
- ❌ Delete orphaned docs (report them, let the user decide)
- ❌ Guess at correct frontmatter values

---

## Reference Files

Load:
- `../ontology.md` — invariant definitions, node_type vocabulary, link types, status values
- `../folder-structure.md` — expected folder layout
- `../index-spec.md` — INDEX.md format expectations
