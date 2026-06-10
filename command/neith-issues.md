---
description: Intake all issues, categorize everything, work through decisions with me in batches. Produces a complete staged fix list ready for execution.
---

Read all currently open and recently found issues from:
- Neith (`.agents/neith`)
- Reports (`.agents/reports`, all files regardless of format)
- Pending tasks and TODO markers in the codebase
- Scout the actual code where needed to understand context — don't just trust the reports

---

## Phase 1 — Intake & Categorize

Read everything. Cross-check against the actual codebase — is this still real? Already fixed? Obsolete? Discard anything stale or invalid silently.

Write every single remaining issue — critical to low, nothing skipped — into `.agents/issues-staging.md`.

**Process in this order:** Critical → High → Medium → Low

For each issue, record:
- **ID** — numbered sequentially (#001, #002, ...)
- **Title** — one clear sentence
- **Severity** — Critical / High / Medium / Low
- **Bucket** — `auto-fix` or `needs-decision` (see criteria below)
- **Recommendation** — one line on what you'd do
- **Status** — `pending`

### ✅ auto-fix — anything with an obvious correct solution
- Bug fixes where the correct behavior is unambiguous
- Stability fixes, error handling, edge cases
- Performance / optimization with no behavioral change
- Code quality, refactoring, cleanup
- QoL improvements (better formatting, JSON output, cleaner logs) — things that add or fix without changing product behavior or direction

### 🔴 needs-decision — anything requiring a product or architectural call
- Fix requires introducing new behavior or a new abstraction to properly resolve
- Feature affects product direction, UX, or architecture
- "Right" approach is genuinely unclear with competing valid options
- Structural bad practice that needs a rethink, not just a patch
- Change large enough that getting it wrong is costly to undo

Do not fix anything. Do not ask me anything yet. Just write the file completely, then report:
> "Staged N issues — X need your decision, Y are auto-fix. Ready for Phase 2."

---

## Phase 2 — Work Through Decisions Together

Present all `needs-decision` items to me in batches of up to 10 at a time, numbered clearly.

For each item show:
1. **#ID — Title**
2. **Severity**
3. **Why it needs a decision** — the actual tradeoff or ambiguity, no padding
4. **Your recommendation** — what you'd do if it were your call

Keep the list ruthlessly honest. If something has a clearly correct answer, it belongs in `auto-fix`, not here. Do not pad the decision pile.

I'll reply with the number and my call, e.g.:
- `1. approve` — go with your recommendation
- `3. dismiss` — drop it entirely
- `5. discuss` — we talk it through before deciding

After each batch, immediately update the staging file in place:
- Record my decision verbatim
- Update status to `decision-cleared` or `dismissed`
- If discussed and resolved, record the conclusion

Then load the next batch. Repeat until every `needs-decision` item is marked `decision-cleared` or `dismissed`. No item escapes without a status.

Once the final batch is processed, stop and report:
> "All decisions cleared. Staging file is complete and ready for execution."
>
> Tally:
> - 🔴 Needs your decision: N items — X approved, Y dismissed
> - ✅ Auto-fix: N items queued
> - ❌ Invalid / stale / discarded during intake: N items

Do not begin fixing anything. Execution is my call.

## Phase 3 - Remove noise and convert the file into a proper task list.

Clean the staging file in place — delete all dismissed and invalid entries, reformat remaining items as a flat executable checklist. 
The staging file should serve as a clear enough and understandable checklist of tasks to do, ready to submit for execution. It should contain enough data to focus on a specific issue, but free of an invalid, stale, discarded crap so it does not pollute the noise and getting picked up by accident. 


---

> **Goal:** work through every single blocking and decision-required issue, weed out the bullshit, and end with a complete annotated staging file where everything is accounted for — either cleared for auto-execution or explicitly decided on. Nothing escapes. Nothing is forgotten. 🐾