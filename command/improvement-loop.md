---
description: Run Neith with a focus, write a full task list, auto-fix safe items, leave decisions in the file for me to edit
---
Read all currently open and recently found issues from (if present):
- Neith (`.agents/neith`)
- Reports (`.agents/reports`, all files regardless of format)
- Pending tasks and TODO markers in the codebase

Why: need initial check of what we already have in mind so Neith does not waste time going over the same issues.
---

## Phase 1 — Run Neith With Focus

Run Neith first if there's a specific objective. If no objective is specified, skip to Phase 2 and work with existing reports.

User specified goal: $ARGUMENTS

When running Neith:
- **Objective:**  what should Neith hunt for? Be explicit about scope.
- Run at minimum once. Run multiple passes if the scope is broad or Neith's first pass surfaces areas that need deeper investigation.
- Let Neith accumulate findings across passes. Each pass builds on the last.
- Neith's job is to find, not to fix. It writes findings to `.agents/neith/` — scratchpad for state, report_issues for findings, report_activity for what was covered.

---

## Phase 2 — Read Everything & Cross-Check

Read every report, every finding, every TODO, every Neith file. Do not skip anything.

Then cross-check against the actual codebase:
- Is this finding still real? Or was it already fixed?
- Is it obsolete because the relevant code was removed or refactored?
- Is it invalid because the assumption was wrong?

Discard anything stale, fixed, or invalid silently. Do not include it in the task file. Only real, current issues survive.

---

## Phase 3 — Write the Task File

Write everything into `.agents/issues-staging.md`. This file is both the report and the control surface — I will open it, edit it, mark decisions, and add corrections directly. Make it clean and scannable.

### File format:

```markdown
# Issues Staging — [brief title / date]

_N items total — X auto-fix, Y need decision_

---

## ✅ Auto-Fix

_These have unambiguous correct solutions. No behavior changes. Will be fixed automatically in Phase 4._

- [ ] #001 — [one clear sentence describing the issue]
- [ ] #002 — [one clear sentence]
...

---

## 🔴 Needs Decision

_These require a product or architectural call. Do not fix until I review._

| # | Title | Severity | Why this needs a decision | Recommendation |
|---|---|---|---|---|
| #003 | Short title | High | The actual tradeoff or ambiguity — no padding. Why can't this just be auto-fixed? | What you'd do if it were your call |

...
```

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

Do not ask me anything during this phase. Just write the file completely, then proceed to Phase 4.

---

## Phase 4 — Auto-Fix Section A

Go through every `[ ]` item in the Auto-Fix section and fix it.

Rules while fixing:
- **One item at a time.** Fix → verify → mark `[x]` → next.
- **If an item turns out not to be auto-fixable** — the fix is more complex than expected, touches risky code, or you realize it needs a decision — do NOT force it. Move it to the Needs Decision section instead.
- **Apply the litmus test mid-flight.** After each fix, ask: would a user notice different behavior? If yes — move it to Needs Decision. Same goes if a fix breaks an existing test.

When all auto-fix items are either `[x]` done or moved to Needs Decision, proceed to Phase 5.

---

## Phase 5 — Report

Give me a tight summary:

> "Auto-fixed X items. Y items moved to Needs Decision during fixing. Z items total now waiting for your review in Section B."
>
> Quick list of what was fixed — one line per item, no detail needed.
>
> "Open `.agents/issues-staging.md` to review decisions and edit directly."

Do not present the decision items to me in the chat. Do not ask me to decide inline. The file is the interface — I'll open it, review, and mark decisions there myself. This keeps the conversation clean and the work documented in one place.
