# Plan Writing

A plan is the handoff from Horus to the workers. It says *what* to achieve, not *how* to code it.
The orchestrator writes goals. The executor decides implementation. The verifier checks success.

---

## Plan vs Direct vs Brief

| Situation | Produce |
|---|---|
| Micro change — rename, fix one line, obvious scope | **Direct** — no document. Dispatch to Ptah. Tell Ma'at what to check. |
| Standard feature, bug fix, concrete work | **Plan** — one document. Steps, expected outcomes, success criteria. |
| Investigation, review, exploration | **Brief** — compass, not recipe. See `./brief.md`. |

---

## Plan Format

```markdown
# Plan: [Title]
_[One sentence. What does done look like?]_

## Success
_What Ma'at verifies when everything is complete._
- [ ] [criterion]
- [ ] [criterion]

## Prerequisites
_What must exist or be true before Step 1._
- [pre-req]
- [pre-req]

## Scope *(if needed)*
_What explicitly NOT to touch. Only include when there is a real boundary to respect._
- `path/to/module` — deliberately left alone

---

## Steps

_Steps are in execution order. Horus already knows which depend on which — Ptah follows the order given._

### Step 1: [Title]

_What to achieve._
- **Expected:** [what should be true after this step]
- [ ] Complete

### Step 2: [Title]

_What to achieve._
- **Expected:** [what should be true after this step]
- [ ] Complete
```

---

## Multi-Plan: Chaining for Large Tasks

When the work is too large for one plan, break it into a chain.

**Sequential chain** — each plan depends on the previous:
```
Plan A → Plan B → Plan C
```
Run one after another. Verify between if the decision warrants it.

**Parallel plans** — independent sub-tasks can run at the same time:
```
         → Plan B
Plan A ──┤
         → Plan C
```
Only when the sub-tasks don't touch the same files or state.

Horus decides the structure. Ptah executes one plan at a time. Horus hands off the next when ready.

---

## Rules

| Rule | Meaning |
|---|---|
| **Goals, not code** | Say what changes. Don't write half the implementation. |
| **Real paths** | Name files and modules explicitly. No placeholders. |
| **Per-step expected** | Every step says what's true when it's done. Ma'at checks against this. |
| **Overall success** | Top-level criteria. What "done" means end-to-end. |
| **Scope only when needed** | Don't add an empty Scope section. Include it when there's something Ptah must not touch. |
| **Checkboxes track progress** | Ptah ticks them off. On re-run, scan for first `[ ]` and continue. |

---

## Example: Small Plan

```markdown
# Plan: Add user avatar to profile
_Users can upload and see their avatar on the profile page._

## Success
- [ ] Avatar upload endpoint accepts images under 5 MB
- [ ] Profile page displays the uploaded avatar or a default
- [ ] Existing profile data is unchanged

## Prerequisites
- `POST /profile` endpoint exists (see `src/routes/profile.ts`)
- Image storage configured (`src/storage/images.ts`)

## Scope
- `src/routes/avatar.ts` — do not touch, handled in a separate plan

## Steps

### Step 1: Add upload endpoint
- **Expected:** `POST /profile/avatar` accepts multipart image, saves to storage, returns URL.
- [ ] Complete

### Step 2: Display avatar on profile
- **Expected:** Profile page shows saved avatar. Falls back to default silhouette if none set.
- [ ] Complete
```

Save to `.agents/reports/plan_{short-name}_{yyyy-mm-dd}.md`
