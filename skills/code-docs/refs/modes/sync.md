# Mode: Sync

**Trigger:** Code has changed and docs may be out of sync, or asked to reconcile docs with existing code.

You read code passively. You never edit it. You update docs to reflect reality or flag contradictions for human resolution.

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
| **Missing behavior** | Spec says MUST validate email, code doesn't | Flag: code is incomplete |
| **Extra behavior** | Code implements rate limiting, spec is silent | Propose: add to spec |
| **Contradiction** | Spec says MUST expire in 15 min, code uses 30 min | Flag: decide which is correct |
| **Stale architecture** | Arch doc references `src/old/`, code is in `src/new/` | Update architecture doc |
| **Undocumented feature** | Whole feature exists in code, zero spec coverage | Propose: create spec |

### Step 5: Decide and act
For each discrepancy:
- **If code is correct** → Update docs to match. Add missing requirements, correct stale values.
- **If doc is correct** → Flag the code for change. Do NOT edit code.
- **If uncertain** → Ask the user. Don't guess.

### Step 6: Update docs
- Apply changes following Curate mode procedures.
- Bump `updated:` dates on modified docs.
- Never silently delete documented behavior — use MODIFIED/REMOVED deltas.

### Step 7: Report
```
## Sync Report

### Docs checked
- overview/product.md — synced, no issues
- spec/features/auth.md — 3 discrepancies found
- architecture/components/agent.md — 1 discrepancy found

### Discrepancies
| Doc | Requirement | Code | Status |
|-----|------------|------|--------|
| spec/features/auth.md | Session expires in 15 min | Uses 30 min | **Doc updated to 15 min** (code was wrong) |
| spec/features/auth.md | Password validation | Not implemented | **Flagged for implementation** |
| arch/components/agent.md | Agent path: `src/agent/` | Code is `src/agents/` | **Architecture doc updated** |

### Docs updated
- spec/features/auth.md — corrected session timeout
- architecture/components/agent.md — corrected file paths
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

Load as needed:
- `../spec-format.md` — if writing new behavioral requirements
- `../folder-structure.md` — if reorganizing docs to match code structure
