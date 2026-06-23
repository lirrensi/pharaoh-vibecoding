# Mode: Sync

**Trigger:** Code has changed and docs may be out of sync, or asked to reconcile docs with existing code.

You read code passively. You never edit it. You update docs to match code, or write discrepancies to a throwaway `code-flags.md` for a code agent to fix.

---

## Workflow

### Step 1: Read docs first
Load the canonical docs in order:
1. `docs/overview/` — product identity
2. `docs/spec/` — behavioral requirements
3. `docs/architecture/` — implementation structure

### Step 2: Read relevant code
Read only the source files related to the docs you're checking. Don't read the entire codebase.

### Step 3: Diff — find every desynchronization
For each requirement/scenario in the spec:
- Does the code implement this behavior? **Check.**
- Does the code do something the spec doesn't mention? **Flag.**
- Does the code contradict the spec? **Flag as conflict.**
- Does the architecture doc match the actual file structure? **Check.**

### Step 4: Classify each discrepancy

| Type | Example | Action |
|------|---------|--------|
| **Missing behavior** | Spec says MUST validate email, code doesn't | Write flag to code-flags.md |
| **Extra behavior** | Code implements rate limiting, spec is silent | Update spec to document the behavior |
| **Contradiction** | Spec says MUST expire in 15 min, code uses 30 min | If doc is correct → write flag to code-flags.md. If code is correct → update doc |
| **Stale architecture** | Arch doc references `src/old/`, code is in `src/new/` | Update architecture doc |
| **Undocumented feature** | Whole feature exists in code, zero spec coverage | Create spec via Curate mode |

### Step 5: Decide and act
For each discrepancy:
- **If code is correct** → Update docs to match. Add missing requirements, correct stale values.
- **If doc is correct** → Collect the discrepancy into a flag (see Step 7). Do NOT edit code.
- **If uncertain** → Ask the user. Don't guess.

### Step 6: Update docs
- Apply changes following Curate mode procedures.
- Bump `updated:` dates on modified docs.
- Never silently delete documented behavior — use MODIFIED/REMOVED deltas.

### Step 7: Write throwaway code-flags.md
For every discrepancy where **docs are correct and code is wrong**, write a flag into `code-flags.md` at the **project root** (NOT inside `docs/`). This is a temporary handoff file — never committed, never kept.

Use the format from `../../templates/code-flags.md`. Each flag MUST include:
- **Source doc** (absolute path from docs root)
- **Doc requirement** (quote or tight paraphrase with RFC 2119 keyword)
- **Code location** (file path + line number + function name — precise enough to jump to)
- **What code does** (the wrong behavior)
- **Resolution** (actionable instruction — "Change X to Y on line N")
- **Status: pending**

After writing, hand the file to a code agent: *"Fix every pending flag in code-flags.md, then delete the file."*

The code agent:
1. Reads `code-flags.md`
2. Fixes each flag in code
3. **Deletes `code-flags.md`** — the file is throwaway, never committed

### Step 8: Report to user
Summarize what was found and what was done:

```
## Sync Report — YYYY-MM-DD

### Docs checked
- overview/product.md — synced, no issues
- spec/features/auth.md — 2 discrepancies (1 doc updated, 1 flagged for code)
- architecture/components/agent.md — 1 discrepancy (doc updated)

### Doc updates applied
- spec/features/auth.md — corrected session timeout (15 min → code had 30)
- architecture/components/agent.md — corrected file paths (src/agent/ → src/agents/)

### Code flags written
Wrote code-flags.md at project root with 1 flag:
- Password validation not implemented (spec/features/auth.md → src/auth/register.ts:45)

→ Hand off code-flags.md to a code agent. File is deleted after fixes are applied.
```

---

## When to Sync vs Other Modes

| Situation | Use |
|-----------|-----|
| "Check if docs are up to date" | **Sync** |
| "Update docs to match the new API" | **Sync** (or Curate if you already know the changes) |
| "Write docs for this new feature" | **Propose** (or Curate for small additions) |
| "The architecture changed, update the docs" | **Sync** (check code, then update docs) |

---

## Reference Files

Load:
- `../principles.md` — layer ownership and conflict resolution
- `../ontology.md` — for updating frontmatter on modified docs
- `../../templates/code-flags.md` — throwaway flag file format

Load as needed:
- `../spec-format.md` — if writing new behavioral requirements
- `../folder-structure.md` — if reorganizing docs to match code structure
