---
description: Scout the codebase by delegating specialists, accumulate findings into a single staging file, auto-fix safe items, report what's left for decisions
---

## Phase 0 — Read existing state

If `.agents/issues-staging.md` exists, read it. Note:
- What's already listed in both sections (so you don't duplicate)
- The highest ID number (so new items continue from there)

If it does NOT exist, create it with this skeleton:

```markdown
# Issues Staging

_0 items total — 0 auto-fix, 0 need decision_

## ✅ Auto-Fix

_No items yet._

---

## 🔴 Needs Decision

_No items yet._
```

Also read (if present) for awareness of already-walked territory:
- `.agents/neith/ActivityLog.md`
- `.agents/reports/` — all files

---

## Phase 1 — Seek & Accumulate

You are running at the top level. You **can** dispatch specialists. You **can** also read files yourself. Choose the right tool.

User specified focus: $ARGUMENTS

### Scope

- If a focus was given: zero in on that area. Be surgical.
- If no focus: run a broad sweep. Dispatch Anubis on core modules, Osiris on high-risk test gaps, Explorer on tangled areas.

### How to seek

| Situation | Action |
|---|---|
| Broad code audit — bugs, smells, security across a module | **Anubis** — bounded scope, ask Location/Observation/Severity |
| Test coverage gaps — untested paths, brittle tests | **Osiris** — scope to specific modules |
| Feature / improvement ideas | **Hathor** |
| Mapping unknown territory | **Explorer** |
| Narrow check — one file, one function | **DIY** — read files directly |
| Quick surface scan — glob/grep | **DIY** |

- Run at most 2-3 specialists in parallel.
- Give each a bounded prompt: exact scope, exact concern.
- If the user asked for a specific number of passes — do that many. Otherwise run at least 2 passes, or until you've found a meaningful batch (aim for 10+ items if the codebase warrants it).
- If a specialist surfaces a new area worth digging into — queue another pass.

### Categorize immediately

As each finding comes in, sort it right now into the correct block. Don't batch-categorize later.

### The litmus test

Ask yourself one question for every item:

> **"If I applied all these changes and ran the app, would a user be surprised by different behavior — or would something break that worked before?"**

- **No surprises, no breakage** → it's safe → Auto-Fix
- **A user would notice different behavior, or something might break** → it's not safe → Needs Decision

This is the only test that matters. Categories follow directly from it.

### ✅ Auto-Fix — safe, invisible changes

Anything that leaves the app behaving **exactly the same** from the outside:

- **Bugs** — null checks, inverted booleans, off-by-one, missing awaits, broken links, typos that cause misbehavior. Fixing a bug is restoring intended behavior, not changing it.
- **Missing tests** — adding tests is purely additive. Doesn't change how the app runs.
- **Small QoL additions** — better error messages, cleaner logs, JSON formatting, improved output. Additive only, nothing removed or altered.
- **Stability** — error handling, edge cases, defensive null checks. The app was already supposed to handle these; you're just making it actually do so.
- **Performance** — optimisations that produce the same result faster. Same output, less time.
- **Code quality** — dead code removal, unused imports, formatting, clearer naming. Invisible to the user.

**Golden rule: if the change would make a user say "huh, that's different" — it's NOT auto-fix.**

### 🔴 Needs Decision — the app would behave differently

Anything that changes what the user sees, experiences, or depends on:

- **New features or behaviors** — adding something the app didn't do before. Even if it seems obviously good, it's a product decision.
- **Changing current behavior** — modifying how an existing flow works, altering output format, adjusting UX, changing API responses. If a user would notice, I need to approve it.
- **New abstractions** — introducing a pattern, layer, or structure that changes how future code is written. Architectural decisions are never auto-fix.
- **Risky structural changes** — rewrites of core logic, dependency upgrades, renames touching many files, public API changes.
- **Security-sensitive fixes** — auth bypasses, injection vulnerabilities, data-loss risks, race conditions. The fix direction matters too much to guess.

**When in doubt, it goes in Needs Decision.** No auto-fixing anything you're not 100% sure about.

### Append to the staging file

Before appending each item, scan the existing staging file — is this already there? Skip duplicates. If it amplifies an existing finding, update that entry instead.

Write each new item into `.agents/issues-staging.md` immediately as you categorize it:

- Auto-fix → append a checkbox to the `✅ Auto-Fix` block:
  ```
  - [ ] #NNN — one clear sentence
  ```
- Needs Decision → append a row to the `🔴 Needs Decision` table:
  ```
  | #NNN | Short title | Severity | Why decision | Recommendation |
  ```

Update the totals line at the top after each batch. Keep IDs sequential.

---

## Phase 2 — Auto-Fix

Go through every `[ ]` item in the ✅ Auto-Fix block. One at a time:

1. Fix it.
2. Verify the fix works.
3. Mark it `[x]`.
4. If mid-fix you realize it's NOT actually auto-fixable (more complex than expected, touches risky code, would change behavior) — do NOT force it. Move it down to the 🔴 Needs Decision block instead.
5. Apply the litmus test mid-flight: would a user notice? If yes → move it down.

When all auto-fix items are either `[x]` or moved to Needs Decision → done.

---

## Phase 3 — Report

Tight summary:

> "Auto-fixed X items. Y items turned out to need a decision and were moved. Z items total now waiting for your review in the Needs Decision section."
>
> "Open `.agents/issues-staging.md` to review decisions."

Quick list of what was fixed — one line per item. Then list what's waiting for decisions (IDs + titles only, no detail).

---

> **The staging file is persistent.** Run this command again with a different focus — it reads what's already there, avoids duplicates, appends more, and auto-fixes the new batch. The file grows across sessions.
