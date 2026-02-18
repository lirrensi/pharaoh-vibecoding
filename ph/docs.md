# Documentation Specification

This spec defines the canonical documentation structure for projects. Anyone can read this to understand **where docs live, what they contain, and how to write them**.

---

## Core Philosophy

**Documentation is the canon. Code is derivative.**

- If a behavior is not documented, it does not officially exist.
- If code and docs disagree, docs win — or docs are updated intentionally.
- Documentation can be used to completely rebuild the codebase.

---

## File Organization

### Primary Canon

```
docs/
├── product.md          ← Human soul. Short, high-level, the "what is this thing"
├── arch.md             ← Single file if simple
│   OR
├── arch_index.md       ← Index if multiple arch files
├── arch_core.md        ← Core/foundation component
├── arch_*.md           ← Additional components (arch_api, arch_cli, etc.)
│
└── adr/                ← Architecture Decision Records
    ├── 0001-*.md
    ├── 0002-*.md
    └── ...
```

### Glossary

```
docs/glossary.md        ← Single source of truth for all terminology
```

**Purpose**: Define terms once, link everywhere. Prevents inconsistent re-definitions across multiple arch files.

**When Required**: Any project with >1 arch file OR specialized domain terminology.

**Format** — use headings for stable anchors (tables don't link reliably):

```markdown
# Glossary

## Agent

An autonomous process that handles tasks. See [arch_agent.md](arch_agent.md).

## Session

A single execution context from start to finish.
```

**Usage**: Link to glossary instead of re-defining: "Uses the [Agent](glossary.md#agent) pattern."

**Conflict Rule**: If a term is used in a way that contradicts its glossary definition:
- The glossary definition wins.
- Flag the inconsistent usage as a discrepancy.
- Do NOT silently redefine in the glossary to match misuse.

### Secondary Canon

Other docs maintained alongside primary spec:

```
README.md               ← Project entry point
CONTRIBUTING.md         ← How to contribute
CHANGELOG.md            ← Version history
docs/
├── guides/             ← Tutorials and how-tos
├── api/                ← API references (if separate from arch)
├── schemas/            ← Formal interface contracts (OpenAPI, AsyncAPI, JSON Schema)
└── troubleshooting.md  ← Common issues
```

**Interface Contracts** (if applicable):
- `schemas/openapi.yaml` — REST API spec
- `schemas/asyncapi.yaml` — Event/message spec
- `schemas/*.json` — JSON Schema for messages/config
- `migrations/*.sql` — Database migrations

These formal artifacts supplement arch docs but don't replace them.

---

## Split Rules

### When to Split arch.md

A single `arch.md` splits into `arch_*.md` files when:

1. **Replaceability test**: A component could be rewritten in a different language/library without touching other components.
2. **Size threshold**: `arch.md` exceeds 500 lines — consider splitting. Exceeds 800 lines — split it.

### When to Create arch_index.md

- **Required** when there are >1 `arch_*.md` files.
- Single `arch.md` has an inline overview at the top instead.

### When to Create a Folder

If a component has >2 related files, create a folder:

```
docs/
├── arch_index.md
├── arch_core.md
└── arch_mcp/
    ├── index.md        ← Component index
    ├── protocol.md     ← Specific aspect
    └── handlers.md     ← Specific aspect
```

---

## Document Specifications

### product.md — The Human Soul

**Purpose**: High-level explanation of what the product is, how it works, and who it's for. Contains the soul of the project. Readable in one sitting.

**Audience**: Humans — developers, users, stakeholders

**Tone**: Warm, approachable, conversational but professional

**Length**: Keep under 1000 lines

**Required Sections**:

| Section | What it Contains |
|---------|------------------|
| Overview | One-paragraph elevator pitch. What is this thing and why does it exist? |
| Features | Bullet list of core capabilities. What can users do? |
| Architecture Summary | High-level design. Main components and how they connect. Diagram encouraged. |
| User Flows/Stories | How different users interact with the system. Key journeys. |

**Optional Sections**:
- Quick Start / Getting Started
- Philosophy / Design Principles
- Non-Goals / Out of Scope ← **Recommended** — what this is deliberately NOT. Prevents scope creep and stops agents from hallucinating features that were consciously rejected.
- Unresolved Questions ← **Recommended** — known unknowns. Stops agents from hallucinating solutions for unsolved problems.
- Roadmap / Future Direction

---

### arch*.md — The Machine Canon

**Purpose**: Complete technical specification. Machine-readable, exhaustive. You could throw away the code and rebuild it entirely from these docs.

**Audience**: Agents/machines primarily, but also developers needing deep reference

**Tone**: Clinical, direct, no fluff. Facts and structure over narrative.

**Required Core Sections**:

| Section | What it Contains |
|---------|------------------|
| Overview | 10,000ft view. What this component/system does and its boundaries. |
| Scope Boundary | What this component owns vs. does NOT own. Prevents functionality creep. |
| Dependencies | External packages, internal modules, services consumed. Versions if relevant. |
| Data Models | Schemas, types, structures, database tables, state shapes. |
| Component Relationships | How this connects to other parts. Data flow, communication patterns. |
| Contracts / Invariants | Behaviors that MUST hold. Breaking these is a bug, not a refactor. |
| Design Decisions | Important choices and why they were made. Reference ADRs for major ones. Include confidence levels. |

**Scope Boundary Format**:

```markdown
### Scope Boundary

**This component owns**: request routing, middleware chain, response serialization
**This component does NOT own**: business logic, data persistence, auth decisions
**Boundary interfaces**: receives validated config from arch_core, calls services in arch_services
```

**Contracts / Invariants Format**:

```markdown
### Contracts / Invariants

| Invariant | Description |
|-----------|-------------|
| Idempotent retries | Any task MUST be retriable without side effects |
| Auth required | No endpoint MUST return data without valid token |
| Ordering | Events MUST be processed in receipt order |
```

These give agents hard boundaries — they know what they can never deviate from versus what's flexible.

**Design Decisions Format** — include confidence levels so readers know which decisions are settled vs. open for revisiting:

| Decision | Why | Confidence |
|----------|-----|------------|
| Use JWT for auth | Stateless, works across services | High |
| Redis for caching | Familiar, fast enough for now | Medium — revisit at scale |
| Single DB instance | Simple to start | Low — will need sharding |

- **High**: Settled. Won't change without major new requirements.
- **Medium**: Works for now but may need revision at scale/growth.
- **Low**: Quick choice, expects change. Flag for human review before rebuilding.

**Flexible/Optional Sections** (add as needed):

| Section | When to Add |
|---------|-------------|
| Implementation Pointers | Paths/files to check in codebase. Not canon — just helps sync. Format below. |
| API Surface | If component exposes functions/endpoints. Full signatures. |
| Configuration | If component has config options. All options documented. |
| Error Handling | If component has specific error states/behaviors. |
| Security | If component handles auth, encryption, permissions. |
| Performance | If component has performance constraints/optimizations. |
| Testing | If component has specific testing strategies/fixtures. |
| Examples | If usage isn't obvious from API surface alone. |

**Implementation Pointers Format** — helps agents find code during sync without treating code as canon:

```markdown
### Implementation Pointers

- **Repos/paths**: `src/core/*`, `src/config/*`
- **Entry points**: `src/core/init.ts`
- **Generated artifacts**: `dist/*` (do not edit)
```

---

### arch_index.md — The Map

**Purpose**: Quick navigation to all arch files. One-line descriptions.

**Format**:

```markdown
# Architecture Index

## Components

| File | Description |
|------|-------------|
| [arch_core.md](arch_core.md) | Shared foundation — logging, config, utils |
| [arch_api.md](arch_api.md) | REST API layer — routes, handlers, middleware |
| [arch_mcp.md](arch_mcp.md) | MCP protocol implementation |
```

---

### ADRs (Architecture Decision Records)

**Location**: `docs/adr/`

**Naming**: `NNNN-short-description.md` (e.g., `0001-use-postgres-not-mongo.md`)

**Template**:

```markdown
# ADR-NNNN: [Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Context

What is the issue we're facing? What options were considered?

## Decision

What did we decide? Be specific.

## Consequences

What changes? Benefits? Trade-offs?
```

**When to Write an ADR**:
- Choosing between significant alternatives
- Making a non-obvious technical decision
- Establishing a pattern others should follow
- Reversing a previous decision

---

## Writing Standards

### Language

- Use precise, unambiguous terms
- Define terms in `glossary.md`, link to it instead of re-defining
- Consistent terminology throughout — same word means same thing
- Avoid "usually", "might", "should generally" — be definitive

**Normative Language (RFC 2119)**:

- **MUST** / **MUST NOT** — absolute requirement, binding
- **SHOULD** / **SHOULD NOT** — recommended, valid exceptions exist
- **MAY** — optional

Statements using these keywords are normative (binding). Everything else is informative (context, explanation).

Example:
- "The API MUST return 401 on missing token." (normative — breaking this is a bug)
- "We typically deploy weekly." (informative — just context)

### Code Examples

- Must be copy-pasteable and functional
- Include language tag in code block
- Show expected output when relevant
- **Placeholder policy**: All placeholders MUST use `<placeholder_name>` format and include a warning:

```python
client.login(username="<your_username>", token="<api_token_from_dashboard>")
# ⚠️ Replace placeholder values. Copy-pasting as-is will fail.
```

Agents scan for unannotated placeholders and flag them as discrepancies.

### Diagrams

- Any format: Mermaid, PlantUML, ASCII art
- Prefer Mermaid for GitHub-native rendering
- Diagrams must be version-controllable (no binary images)

### Links

- Cross-link related sections
- Link to ADRs for design decisions
- External dependencies: reference by name only, don't document their internals

### Cross-Repository Boundaries

When documenting external services or multi-repo components:

| DO | DON'T |
|----|-------|
| Document interface, contract, expected behavior | Document internal implementation |
| Link to other repo's `product.md` or `arch.md` if public | Document private APIs or internals |
| Note latency, SLA, version expectations | Assume external repo's doc structure |

**Example**:

```markdown
Integrates with [Auth Service](https://github.com/org/auth-repo/blob/main/docs/product.md) 
via OAuth2. Expected latency <200ms. Contract defined in `schemas/auth.yaml`.
```

**Flag if**: External service lacks docs → "⚠️ Undocumented dependency — risk of drift"

### Deprecation

- Never silently delete documented behavior
- Mark deprecated sections clearly:

```markdown
> ⚠️ **Deprecated since vX.Y** — Use [new-thing] instead. Will be removed in vX.Z.
```

### Intentionally Undocumented

When something is deliberately not documented (internal implementation details, unstable APIs, etc.):

```markdown
> 🔇 **Intentionally undocumented** — implementation detail, subject to change without notice.
```

This prevents sync processes from flagging it as a discrepancy forever.

---

## Document Lifecycle

### Creating New Docs

1. Propose file structure before writing
2. Human approves structure
3. Draft content
4. Human reviews and approves
5. Docs become the build contract

### Syncing Docs with Code

Triggered when:
- Human requests sync after a session
- Human requests regeneration after massive changes

Process:
1. Read existing docs
2. Read relevant code
3. Identify discrepancies
4. For each: is code correct (update docs) or docs correct (flag for code fix)?
5. Update affected sections, noting what changed and why

### Inquiring About Docs

**Agent Reading Order** — when approaching a project cold:

1. `product.md` — understand what this is
2. `docs/glossary.md` — learn the vocabulary
3. `arch_index.md` — understand the component map
4. Relevant `arch_*.md` — deep dive on area of interest
5. Relevant `adr/` entries — understand why decisions were made
6. Code — only if docs are silent or ambiguous

**Reporting**: Always report what docs say, what code does, and whether they agree.

---

## Quick Reference

| Doc Type | Audience | Length | Tone |
|----------|----------|--------|------|
| product.md | Humans | <1000 lines | Warm, approachable |
| arch*.md | Machines | No limit | Clinical, direct |
| arch_index.md | Both | Minimal | Factual |
| glossary.md | Both | As needed | Definitive |
| ADRs | Humans | Short | Structured |

---

## Documentation Agent Boundaries

When using agents to manage docs, they should NOT:

- Write or modify source code
- Make architectural or technical decisions (documents them only)
- Assume undocumented behavior is intentional
- Leave discrepancies unresolved without flagging
- Document internals of external systems/repositories
