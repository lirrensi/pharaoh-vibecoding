# Documentation Principles

## The Core Philosophy

**Documentation is the semantic digital twin of the codebase.** Docs define what the system is, why it exists, how it behaves, and how it's structured. Code is one rendering of that truth.

**If code and docs disagree, docs win** — or docs are updated intentionally, never silently. If you had to choose between keeping the code or the docs, keep the docs. You can rebuild code from docs. You cannot rebuild docs from code.

## The Documentation Stack

The stack refines downward — each layer adds precision while preserving the truth of the layer above:

```
overview/  →  spec/  →  architecture/  →  code
(why)        (what)     (how)             (rendering)
```

- `overview/` is written first. It defines product identity, purpose, value, users, and non-goals.
- `spec/` is derived from `overview/`. It defines exact, testable behavior in BDD+RFC format.
- `architecture/` is derived from `spec/`. It defines how the current implementation realizes the behavior.
- Code may be discarded and regenerated from the docs. The docs are the valuable artifact.

## Layer Ownership

| Layer | Owns | Does NOT own |
|-------|------|-------------|
| **overview/** | Product identity, purpose, user value, major flows, non-goals | Exact behavior, implementation detail |
| **spec/** | Exact behavior, contracts, edge cases, state rules, data schemas, conformance | Implementation structure, framework choices |
| **architecture/** | Implementation structure, components, dependencies, boundaries, runtime shape | Product positioning, behavioral requirements |

## Conflict Resolution

- If `architecture/` and `spec/` disagree on behavior → **spec/ wins**.
- If `spec/` and `overview/` disagree on identity, purpose, or non-goals → **overview/ wins**.
- If code and docs disagree → **docs win**, or docs are updated intentionally.
- Lower layers MUST preserve the truth of the layer above while adding precision.

## Behavior-First, Goal-Driven

Every spec must answer three questions in order:

1. **WHY** — What is the goal? What problem does this behavior solve? (Purpose, Goals)
2. **WHAT** — What must the system do? What are the requirements? (Requirements, MUST/SHOULD/MAY)
3. **HOW** — How does the behavior manifest? What are concrete scenarios? (Given/When/Then)

This ensures docs are strong enough to:
- Rebuild the system in any language from scratch
- Verify correctness independently of the implementation
- Onboard new contributors without reading code

## Each Surviving Layer Matters

- If only `overview/` survives → you can recover product intent and derive a likely spec.
- If only `spec/` survives → you can rebuild the product behaviorally in any language.
- If only `architecture/` survives → you can reconstruct the current implementation shape.

The stronger the docs, the more disposable the code becomes.

## Writing Philosophy

- **Precise over vague.** Define limits, ordering, retries, idempotency, error codes explicitly.
- **Concrete over abstract.** Use scenarios with actual values, not placeholders.
- **Testable over aspirational.** Every scenario should be verifiable — you could write a test for it.
- **Declarative over imperative.** Describe what happens, not how to click through a UI.
- **Behavior over implementation.** `spec/` never mentions classes, functions, frameworks, or file names.
- **Internal behavior over UI.** Document what the system *does* internally (state machines, processing pipelines, decision logic) — not what buttons a user clicks. A UI redesign should never require a spec update.
- **Protocol over presentation.** Document message formats, API contracts, wire protocols, state transitions, and data schemas. The presentation layer (colors, layout, components) is implementation detail.
- **User experience over interface.** Document what the user *experiences* and *perceives* — not the interface they use to get there. "The user is authenticated" not "The user clicks the login button and a modal appears".

## Document Lifecycle

- **Never physically delete a file.** No text must be lost as a result of any operation. Mark deprecated docs with `status: deprecated` and add `supersedes` links. Moving to `archive/` is allowed — the file still exists, it just changes location. `git rm` followed by no trace is forbidden.
- **Never silently change.** Every meaningful update bumps `updated:` and explains what changed.
- **Archive preserves history.** Completed change proposals move to `archive/` with full context.
- **INDEX.md is always current.** After any doc change, run `python scripts/index.py` to regenerate all INDEX.md files. **Never hand-edit INDEX.md — the script wipes and overwrites them completely.**
