# Skill: Plan Writing

You have loaded this skill because it's time to write a plan for Executor.

Executor has **zero context** from this conversation. He is a maximizer — he reads the plan, executes exactly what it says, and stops only if something is catastrophically wrong. Write for someone executing at midnight with no ability to ask questions. Assume nothing. Spell everything out.

**The test:** Could GPT-2 execute this step by step without making a single judgment call? If not, it's not done.

---

## PLAN IS A LIVING DOC

The plan is not a one-shot handoff. It is a **working document** Executor runs against multiple times.

- Steps are checkboxes — Executor ticks them off as he completes them
- Each run, Executor scans for the first unchecked box and continues from there
- If something fails mid-run, the checked boxes show exactly where he stopped
- Ma'at reads the same file to know what was supposed to happen

This means the plan file is the **single source of truth for execution state**. Treat it accordingly.

---

## PLAN FORMAT

```markdown
# Plan: [Title]
_[One sentence. What does done look like?]_

---

# Checklist
- [ ] Step 1: [one-line summary]
- [ ] Step 2: [one-line summary]
- [ ] Step 3: [one-line summary]
...

---

## Context
[What Executor needs to know about current codebase state.
Real file paths. No placeholders. No "the main file" — name it.]

## Prerequisites
[Everything required before Step 1: env vars, services running, files present.
If a prerequisite is missing, Executor must stop and report — not guess.]

## Scope Boundaries
[Files and modules explicitly OUT OF SCOPE.
Executor must not touch these even if they seem related.]

---

## Steps

### Step 1: [Title]
[Full instruction. Exact file paths. Exact function names. Exact commands.]

✅ Success: [What exists / returns / outputs when this step is done correctly?]
❌ If failed: [Exact action to take. Never "investigate" — tell Executor what to do.]

### Step 2: [Title]
...

---

## Verification
[How Executor confirms the ENTIRE plan succeeded end-to-end.
Not just "it runs" — specific outputs, states, values expected.]

## Rollback
[What to do if a critical step fails and cannot be recovered.
Real commands. Real file paths.]
```

---

## CHECKLIST RULES

The checklist at the top is a **navigation aid** for Executor across multiple runs:

- One line per step — just the title, no detail
- Mirrors the Steps section exactly — same order, same titles
- Executor checks off each box the moment a step is verified complete
- On next run: scan checklist top to bottom, find first `[ ]`, jump to that step
- Never re-run a checked step unless explicitly told to

---

## STEP RULES

Every step must be:

| Rule | Meaning |
|---|---|
| **Atomic** | One action only. If you wrote "and" or "then" — split it into two steps. |
| **Unambiguous** | No pronouns. No "the file", "the function", "it". Name everything explicitly. |
| **Executable** | No vague verbs. Not "update", "handle", "fix". Use: "open", "find line X", "replace Y with Z", "run command W", "write to path V". |
| **Verifiable** | Every step has a ✅ success check. What concretely exists, returns, or outputs when done? |
| **Failure-branched** | Every step has a ❌ failure path. What exactly does Executor do if this step fails or returns unexpected output? Never leave him to decide. |
| **Standards-compliant** | New code follows the code standards below. |

---

## CODE STANDARDS

All new code written in any step must follow these rules:

- **Pure functions** — same input → same output, no side effects
- **Immutability** — create new data structures, never mutate existing ones
- **Small & focused** — functions under 50 lines, components under 100 lines
- **Explicit dependencies** — inject them, never import globals inside functions
- **Boundary validation** — validate nulls, types, ranges, and sanitize all user input at entry points
- **Explicit error handling** — return `{ success, error }` shape, never expose internal error messages
- **No hardcoded secrets** — env vars only, never inline credentials or tokens
- **Single responsibility** — if a module does two things, split it into two modules

---

## REWRITE EXAMPLES

| ❌ Vague | ✅ Explicit |
|---|---|
| "Run the migration" | "Execute `npm run migrate:prod` from project root. Expected output: `Migration complete: X tables updated`. If output contains `ERROR:`, stop — do not proceed to Step 4." |
| "Update the config" | "Open `src/config/env.ts`. Find the constant `ENV_MODE` (approximately line 14). Change its value from `'development'` to `'production'`. Save the file." |
| "Handle the error" | "If the function returns a non-null `error` field, write the full error object to `logs/error.txt` and halt execution. Do not continue to the next step." |
| "Fix the bug" | "Open `src/auth/token.ts`. Find the function `validateToken` (approximately line 42). The condition on line 48 reads `if (token.exp > Date.now())` — change it to `if (token.exp > Date.now() / 1000)`." |
| "Make sure it works" | "Run `npm test -- --testPathPattern=auth`. Expected: all tests pass, 0 failures. If any test fails, stop and report the full failure output." |

---

## PRE-HANDOFF CHECKLIST

Before saving the plan, verify every item:

- [ ] Checklist at top matches steps exactly — same count, same titles, same order
- [ ] No ambiguous pronouns anywhere ("it", "the file", "this function")
- [ ] No vague verbs anywhere ("update", "fix", "handle", "ensure")
- [ ] Every file path is real and relative to a stated root — no placeholders
- [ ] Every step has a ✅ success check with concrete expected output
- [ ] Every step has a ❌ failure path with explicit next action
- [ ] Steps are in correct dependency order — no step assumes a later step
- [ ] Prerequisites list everything the steps silently assume
- [ ] Scope boundaries name everything Executor must not touch
- [ ] All new code follows the code standards above

When every box is checked: **"Plan complete. Handing off to Executor."**

Save to `plans/{short-name}-{yyyy-mm-dd}.md`