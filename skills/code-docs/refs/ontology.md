# Documentation Ontology

Every document in `docs/` is a typed **object** in the ontology — inspired by Palantir Foundry's ontology model and GitMark's code-ontology. Each document has a `node_type` (what kind of thing it is), frontmatter **properties** (metadata), and typed **links** (relationships to other docs and code).

---

## Node Types

Each document has exactly one `node_type`. Choose based on what the document IS, not what it contains.

| `node_type` | What it is | Lives in |
|-------------|-----------|----------|
| `overview` | Product identity, purpose, users, non-goals | `docs/overview/` |
| `spec` | Behavioral specification (requirements + scenarios) | `docs/spec/` |
| `feature-spec` | Per-feature behavioral spec | `docs/spec/features/` |
| `architecture` | Implementation structure description | `docs/architecture/` |
| `component` | Per-component architecture detail | `docs/architecture/components/` |
| `adr` | Architectural decision record | `docs/architecture/decisions/` |
| `guide` | How-to / tutorial | `docs/guides/` |
| `runbook` | Operational procedure | `docs/ops/` |
| `reference` | Cross-cutting reference (glossary, conventions) | `docs/reference/` |
| `change-proposal` | Proposal for a change (why + scope) | `docs/changes/<name>/proposal.md` |
| `change-behavior` | Delta behavior spec (ADDED/MODIFIED/REMOVED) | `docs/changes/<name>/behavior.md` |
| `change-design` | Technical approach for a change | `docs/changes/<name>/design.md` |
| `change-tasks` | Implementation checklist | `docs/changes/<name>/tasks.md` |
| `index` | Folder table of contents | Any `INDEX.md` |

**Creating new types:** You MAY create new `node_type` values if none of the existing types fit your document. However, every new type MUST be:
1. Documented in `docs/ontology.md` (the project's ontology registry) with a clear explanation of what it is, where it lives, and why it exists.
2. Added to the table above so the vocabulary stays current.
3. Justified by having ≥3 documents that use it (no single-document types).

**The ontology registry (`docs/ontology.md`) is the single source of truth for what document types exist and what they mean.** If a type isn't in the registry, it doesn't exist. If a new type is created, the registry must be updated.

**Fallback rule:** If unsure and you don't want to create a new type, a behavioral spec is `spec`, a how-to is `guide`.

---

## Frontmatter Specification

Every document MUST have YAML frontmatter. Minimal for index/non-load-bearing docs, full for all others.

### Minimal (for `index` and lightweight docs)

```yaml
---
node_type: index
updated: 2026-06-09
---
```

### Full (for all load-bearing docs)

```yaml
---
node_type: spec
title: Authentication Behavior
status: active
updated: 2026-06-09
tags: [auth, security, sessions]
confidence: certain
links:
  depends_on: [../overview/product.md]
  documents: [../../src/auth/]
  supersedes: [old-auth-spec.md]
---
```

### Field Reference

| Field | Required | Values | Notes |
|-------|----------|--------|-------|
| `node_type` | **Yes** | See table above | Determines where the doc lives and how it's treated |
| `title` | Recommended | Free text | Human-readable name; used in INDEX.md |
| `status` | Recommended | `active`, `draft`, `deprecated`, `archived` | Defaults to `active` if absent |
| `updated` | Recommended | `YYYY-MM-DD` | Last meaningful content edit |
| `tags` | Optional | `[lowercase, hyphenated]` | Free-form for search and grouping |
| `confidence` | Optional | `decided`, `tentative`, `exploratory` | Whether a decision has been made, or it's open to change |
| `links` | Optional | See below | Typed links to other docs and code |
| `implementation_status` | Optional | `implemented`, `partial`, `discarded` | For ADRs and architecture docs: is this decision realized in code? |

### Confidence Field

Describes whether a decision has been finalized, not how sure you are:

| Value | Meaning | When to use |
|-------|---------|------------|
| `decided` | Decision is made and settled | Architecture choices, spec requirements, accepted ADRs |
| `tentative` | Decision is made but may change | New features, experimental components, early-stage specs |
| `exploratory` | No decision yet — exploring options | Research spikes, prototype docs, pre-ADR analysis |

Do NOT use `confidence` to express how sure you are about facts. Use it to signal whether a decision is locked or still in play. A spec with `confidence: tentative` says "this is the current plan but expect changes."

---

## Link Types

Links are markdown links `[text](path.md)` declared under `links:` in frontmatter. Inline links in body text default to `relates_to`.

| Link type | Meaning | Direction |
|-----------|---------|-----------|
| `depends_on` | Read that first to understand this | doc → doc |
| `documents` | This doc describes that code/service | doc → code |
| `implemented_by` | Where this behavior lives in code | spec → source |
| `supersedes` | Replaces a stale document | new → old |
| `relates_to` | Adjacent topic (default for inline links) | doc ↔ doc |
| `part_of` | Belongs to a larger index | doc → index |
| `implements` | This code satisfies that requirement | code → spec |

### Link Examples

```yaml
links:
  depends_on: [../overview/product.md]
  documents: [../../src/auth/, ../../src/sessions/]
  supersedes: [../archive/old-auth-flow.md]
  implemented_by: [../../src/auth/login.ts]
```

---

## Status Values

| Status | Meaning | When to use |
|--------|---------|------------|
| `active` | Current, authoritative | Default for all live docs |
| `draft` | Work in progress, not yet authoritative | New docs still being shaped |
| `deprecated` | No longer current, kept for history | Old behavior replaced by newer doc; set `supersedes` on replacement |
| `archived` | Historical record only | Moved to `docs/archive/` after a change is completed |

---

## Tags

Tags enable cross-cutting search and grouping. Use lowercase, hyphenated, stable tags.

Good tag categories:
- **domain:** `auth`, `api`, `cli`, `ui`, `storage`
- **type:** `spec`, `decision`, `incident`, `workflow`
- **quality:** `security`, `performance`, `reliability`

```yaml
tags: [auth, security, api, spec]
```

---

## Invariants (enforced by Audit mode)

These must hold for a healthy documentation ontology:

- **I1:** Every folder in `docs/` has an `INDEX.md` with `node_type: index`.
- **I2:** Every doc (except `index`) has frontmatter with a valid `node_type`.
- **I3:** No broken cross-references (markdown links to missing files).
- **I4:** No orphans — every load-bearing doc is linked from at least one `INDEX.md`.
- **I5:** A `supersedes` target has `status: deprecated` or `status: archived`.
- **I6:** Layer coherence — `spec/` doesn't contradict `overview/`, `architecture/` doesn't contradict `spec/`.
