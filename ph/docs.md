# Documentation Specification

This document defines the canonical documentation model for projects in this system: where docs live, what each file means, and how to write them.

---

## Core Philosophy

**Documentation is the canon. Code is disposable derivative.**

The documentation stack refines downward: `product.md` -> `spec.md` -> `arch*.md` -> code

- `product.md` is written first. It defines the product's purpose, value, actors, main flows, and non-goals.
- `spec.md` is written from `product.md`. It defines exact, language-agnostic behavior without committing to one implementation.
- `arch.md` / `arch_*.md` is written from `spec.md`. It defines how this repository's current implementation realizes that behavior.
- Code may be discarded and regenerated from the docs. The docs are the valuable artifact.

### Layer Ownership
- `product.md` owns product identity, purpose, user value, major flows, and non-goals.
- `spec.md` owns exact behavior, contracts, edge cases, state rules, and conformance.
- `arch.md` / `arch_*.md` owns implementation structure, components, dependencies, boundaries, and runtime shape.

### Conflict Handling
- If code and docs disagree, docs win — or docs are updated intentionally.
- If `arch*.md` and `spec.md` disagree on behavior, `spec.md` wins.
- If `spec.md` and `product.md` disagree on product identity, purpose, or non-goals, `product.md` wins.
- Lower layers must preserve the truth of the layer above while adding precision.

---

## File Organization

### Primary Canon

```text
docs/
├── product.md          ← Human-facing product truth; a second README with canon status
├── spec.md             ← Rebuildable, language-agnostic behavior spec
├── arch.md             ← Single-file current-implementation architecture canon if simple
│   OR
├── arch_index.md       ← Map of architecture documents
├── arch_core.md        ← Shared foundation
├── arch_*.md           ← Additional architecture components
├── glossary.md         ← Shared terminology when needed
│
└── adr/                ← Architecture Decision Records
    ├── 0001-*.md
    ├── 0002-*.md
    └── ...
```

### Secondary Canon

```text
README.md               ← Project entry point
CONTRIBUTING.md         ← Contribution process
CHANGELOG.md            ← Version history
docs/
├── guides/             ← Tutorials and how-tos
├── api/                ← Reference docs if kept separate
├── schemas/            ← OpenAPI, AsyncAPI, JSON Schema, etc.
└── troubleshooting.md  ← Common issues
```

Formal schemas, migrations, and interface contracts supplement the canon. They do not replace it.

---

## Split Rules

### When to Split Architecture Docs

A single `arch.md` should split into `arch_*.md` files when:

1. **Replaceability test**: a component could be rewritten independently without forcing changes to unrelated components.
2. **Size threshold**: `arch.md` exceeds 500 lines — consider splitting. Exceeds 800 lines — split it.
3. **Operational clarity**: different subsystems have separate boundaries, runtime concerns, or ownership surfaces that are easier to maintain independently.

### When to Create `arch_index.md`

- Required when there are multiple `arch_*.md` files.
- It is a map only: component name, one-line description, link.
- It must not become a second implementation document.

### Naming Rules

- Use `arch_{name}.md` for split architecture files.
- Use `arch_core.md` for shared foundations.
- Use `arch_index.md` only when a split exists.
- Never use freeform names like `architecture-final.md` or `backend-arch-notes.md`.

### When to Create `glossary.md`

Create `docs/glossary.md` when any of the following is true:

- there is more than one architecture document,
- the spec uses specialized domain terms,
- multiple agents or contributors could interpret important terms differently.

Use headings for stable anchors:

```markdown
# Glossary

## Agent

Autonomous process that executes a bounded task.

## Session

A single execution context from start to finish.
```

If a term is used inconsistently:

- the glossary wins,
- the inconsistency is a discrepancy,
- the glossary must not be silently rewritten to match misuse.

---

## Document Specifications

### `product.md` — The Human Overview

**Purpose**: Explain what the product is, who it is for, why it exists, and how it broadly works. It should feel like a second README, but it is still canonical.

**Audience**: Humans first — founders, developers, users, reviewers, new contributors

**Tone**: Warm, concise, approachable

**Length**: Aim for one sitting. Prefer under 250 lines. If it grows past 400 lines, it is probably carrying spec material that belongs elsewhere.

**Stack role**: First canonical layer. Write it before `spec.md`. If only `product.md` survives, a strong reader should still be able to reconstruct the intended product and derive a likely `spec.md`, but some thinking is still required.

**What belongs here**:

- the elevator pitch,
- the core value proposition,
- the major user journeys,
- the major system shape,
- the important non-goals.

**What does NOT belong here**:

- exhaustive edge-case behavior,
- protocol minutiae,
- line-by-line API contracts,
- implementation internals.
- source-level implementation detail.

**Required sections**:

| Section | What it contains |
|---|---|
| Overview | What this product is and why it exists |
| Core Capabilities | The few things the product fundamentally does |
| Main User Flows | Key journeys or stories |
| System Shape | High-level component view, no deep internals |
| Non-Goals | Deliberately out of scope behavior |

**Optional sections**:

- Quick Start
- Design Principles
- Target Users
- Roadmap
- Open Questions

---

### `spec.md` — The Behavioral Canon

**Purpose**: Define the product behavior in enough detail that the code could be discarded and the system reimplemented in another language or stack with the same externally observable behavior.

**Audience**: Implementers, reviewers, testers, agents

**Tone**: Precise, direct, testable, language-agnostic

**Stack role**: Second canonical layer. Write it from `product.md`, preserving product truth while removing ambiguity. If `spec.md` survives, the product can be rebuilt behaviorally in any language without needing the original code.

**Philosophy**: `spec.md` is RFC-like, not RFC cosplay. Borrow the rigor of RFCs and standards documents without cargo-culting internet publication boilerplate that does not help this repo.

### Style Sources for `spec.md`

- **RFC 7322** — structure, consistency, editorial discipline
- **RFC 2119** — normative keywords (`MUST`, `SHOULD`, `MAY`)
- **MessagePack spec** — precise tables, diagrams, and conversion rules
- **W3C QA Specification Guidelines** — conformance thinking and testability

Do **not** automatically add sections like `Status of This Memo`, `IANA Considerations`, or `Author's Address` unless the project explicitly wants them.

### Required sections for `spec.md`

| Section | What it contains |
|---|---|
| Abstract | Short summary of what the product/system specified here does |
| Introduction | Context, goals, and why this spec exists |
| Scope | What is in scope and out of scope |
| Terminology | Terms that matter for correct interpretation; link glossary when present |
| Normative Language | RFC 2119 interpretation of `MUST`, `SHOULD`, `MAY` |
| System Model | Main actors, interfaces, states, and top-level concepts |
| Conformance | What a conforming implementation must do |
| Behavioral Specification | Feature-by-feature or interface-by-interface behavior |
| Data and State Model | Important entities, states, schemas, transitions |
| Error Handling and Edge Cases | Failure modes, invalid input behavior, limits |
| Security Considerations | Security assumptions, constraints, risks |
| References | Normative and informative references when applicable |

### Recommended sections for `spec.md`

- Compatibility / Migration
- Extensibility Rules
- Deprecations
- Examples
- Diagrams / State Machines
- Open Questions

### Rules for writing `spec.md`

- Focus on **what the system must do**, not how a specific codebase currently does it.
- Use **normative language** only when requirement strength matters.
- Keep normative and informative text clearly separable.
- Prefer tables, truth tables, sequence diagrams, state diagrams, and structured examples over vague prose.
- Define limits, ordering rules, retries, idempotency, error codes, fallback behavior, and conflict resolution explicitly.
- Write so an independent team could implement from scratch without seeing the source.

### Normative Language

Use RFC 2119 meanings:

- **MUST / MUST NOT** — absolute requirement
- **SHOULD / SHOULD NOT** — recommended default; exceptions require justification
- **MAY** — optional behavior

Use these terms sparingly. They should govern interoperability, correctness, or safety — not stylistic preference.

### Conformance Guidance

Every `spec.md` should answer what counts as a conforming implementation, which behaviors are mandatory vs optional, which interfaces or actors must conform, and what variability is allowed without breaking conformance. If the product has profiles, modes, roles, extension points, deprecated behavior, or optional modules, the spec must say exactly how those affect conformance.

- When references exist, split them into **Normative References** and **Informative References**, keep citation labels consistent, cite stable sources when possible, and do not rely on a URL alone when a proper named standard exists.
- `Security Considerations` is required even when brief. If there are no special concerns, say so explicitly.

---

### `arch.md` / `arch_*.md` — The Architecture Canon

**Purpose**: Describe the current implementation architecture in enough detail that the present system could be rebuilt without the source code. Focus on structure, boundaries, flows, runtime behavior, and operational shape.

**Audience**: Implementers, maintainers, reviewers, agents

**Tone**: Structural, factual, implementation-aware

**Stack role**: Third canonical layer. Write it from `spec.md`, preserving specified behavior while describing the current implementation shape of this repository. If the architecture docs survive, the current implementation can be rebuilt far more faithfully than from `spec.md` alone.

**Key distinction from `spec.md`**:

- `spec.md` defines **behavioral truth**.
- `arch*.md` defines **implementation shape**.

The architecture layer may mention concrete frameworks, services, deployment topology, storage systems, and code organization when those details matter architecturally. It should still avoid trivia and line-by-line code narration.

### Required sections for architecture docs

| Section | What it contains |
|---|---|
| Overview | What this component or system is and why it exists |
| Scope Boundary | What it owns, what it does not own, and the interfaces at the boundary |
| Components | Internal parts and their responsibilities |
| Data Models / Storage | Important persisted or in-memory structures |
| Relationships and Flow | How data and control move through the system |
| Dependencies | External services, packages, runtimes, internal modules |
| Contracts / Invariants | Properties the implementation must preserve |
| Configuration / Operations | Runtime config, deployment, observability, failure domains |
| Design Decisions | Important implementation choices and why they exist |

### Recommended sections for architecture docs

- API Surface
- Security Model
- Performance Characteristics
- Testing Strategy
- Migration Notes
- Implementation Pointers

### Scope Boundary format

```markdown
### Scope Boundary

**Owns**: request routing, middleware chain, response serialization
**Does not own**: business rules, persistence policy, authorization decisions
**Boundary interfaces**: receives validated config from `arch_core.md`, calls services in `arch_api.md`
```

### Contracts / Invariants format

```markdown
### Contracts / Invariants

| Invariant | Description |
|---|---|
| Idempotent retries | Retried tasks MUST not create duplicate side effects |
| Ordered processing | Events MUST be handled in receipt order within a partition |
| Auth boundary | Private data MUST NOT cross an unauthenticated boundary |
```

### Design Decisions guidance

Architecture docs should capture decisions that materially shape the system. Reference ADRs when they exist.

Recommended confidence labels:

| Confidence | Meaning |
|---|---|
| High | Settled unless requirements materially change |
| Medium | Stable for now but likely to evolve |
| Low | Temporary or exploratory; verify before rebuilding |

### Implementation Pointers

This section is optional and non-canonical. It helps sync docs with code without making code the source of truth.

```markdown
### Implementation Pointers

- Repos/paths: `src/core/*`, `src/config/*`
- Entry points: `src/core/init.ts`
- Generated artifacts: `dist/*` (do not edit)
```

---

### `arch_index.md` — The Map

**Purpose**: Navigate architecture files quickly.

**Format**:

```markdown
# Architecture Index

## Components

| File | Description |
|---|---|
| [arch_core.md](arch_core.md) | Shared foundation: config, logging, runtime wiring |
| [arch_agent.md](arch_agent.md) | Agent execution model and boundaries |
| [arch_cli.md](arch_cli.md) | CLI command parsing and orchestration |
```

---

### ADRs

**Location**: `docs/adr/`

**Naming**: `NNNN-short-description.md`

**Template**:

```markdown
# ADR-NNNN: [Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Context

What issue are we solving? What options were considered?

## Decision

What did we choose?

## Consequences

What becomes easier, harder, or riskier?
```

Write an ADR when choosing between meaningful alternatives, establishing a pattern others should follow, or reversing a previous decision.

---

## Writing Standards

### Language

- Use precise, stable terminology.
- Define shared terms once in `glossary.md` when needed.
- Avoid hedging words like `usually`, `kind of`, `probably`, `roughly`, unless uncertainty is the point.
- If something is undecided, label it explicitly as undecided.

### Code Examples

- They must be copy-pasteable when presented as runnable examples.
- Include language tags.
- Use `<placeholder_name>` for placeholders and mark them clearly.

```python
client.login(username="<your_username>", token="<api_token>")
# Replace placeholder values before running.
```

### Diagrams

- Prefer text-first, versionable diagrams: Mermaid, PlantUML, ASCII.
- Use diagrams when structure or flow is easier to see than explain.

### Links and Boundaries

- Cross-link related sections.
- Link to ADRs for important design decisions.
- For external systems, document the contract and expectations, not their internals.
- If another repo has canonical docs, link to that repo's `product.md`, `spec.md`, or architecture docs instead of rewriting them locally.

### Deprecation

- Never silently delete documented behavior.
- Mark deprecated behavior clearly and state the replacement and timeline when known.

```markdown
> Deprecated since vX.Y. Use [new-thing] instead. Planned removal: vX.Z.
```

### Intentionally Undocumented

When a detail is deliberately left unstable or internal:

```markdown
> Intentionally undocumented — internal detail, subject to change without notice.
```

---

## Document Lifecycle

### Creating New Docs

1. Propose the file structure before writing.
2. Get approval on the structure.
3. Draft `product.md` first.
4. Draft `spec.md` from `product.md`.
5. Draft `arch.md` / `arch_*.md` from `spec.md`.
6. Review the stack for consistency.
7. Finalize. The docs become the build contract.

### Syncing Docs with Code

1. Read existing docs first.
2. Read relevant code.
3. Find every discrepancy.
4. Decide whether the doc should change or the code should change.
5. Update the affected layer and note what changed.

### Recommended Reading Order

1. `product.md` — orientation
2. `glossary.md` — vocabulary
3. `spec.md` — behavior contract
4. `arch_index.md` — architecture map when present
5. relevant `arch_*.md` files — implementation detail
6. ADRs — decision history
7. code — only when docs are silent, stale, or ambiguous

When reporting, say:

- what `product.md` says,
- what `spec.md` says,
- what architecture docs say,
- what code does,
- whether they agree.

---

## Quick Reference

| Doc Type | Audience | Primary Question | Tone |
|---|---|---|---|
| `product.md` | Humans | What is this and why does it matter? | Warm, concise |
| `spec.md` | Implementers, testers, agents | What must the system do? | Precise, normative |
| `arch.md` / `arch_*.md` | Implementers, maintainers, agents | How is the current system structured? | Structural, factual |
| `arch_index.md` | Both | Where do I read next? | Minimal, factual |
| `glossary.md` | Both | What do these terms mean? | Definitive |
| `adr/*` | Humans | Why was this decision made? | Structured |

---

## Documentation Agent Boundaries

Documentation agents should NOT:

- write or modify source code,
- make product or architecture decisions on their own,
- assume undocumented behavior is intentional,
- leave discrepancies unresolved without flagging them,
- document internals of external systems they do not own.
