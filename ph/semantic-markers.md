# Semantic Markers Framework

## What This Is

This document defines the **Semantic Markers Framework** — a system of navigation anchors embedded in source code that create a bidirectional link between implementation and documentation. It is not a coding standard. It is not a documentation strategy. It is a **navigation layer** that sits on top of your existing codebase and doc graph, making both discoverable and verifiable.

The core problem this solves: when you (or an AI agent) open a file six months after it was written, you need to know **what governs this file**, **what it owns**, and **where to look before changing it**. Without markers, every file is an island. With markers, every file is a node in a graph you can traverse.

**This document is the canonical reference.** Read it to understand the framework. Read it to implement it. Read it to audit it. Everything about semantic markers is defined here.

**Relationship to the rest of the system:** This document is standalone. It does not reference the implementation rules (Ptah), the documentation system (Thoth), or any other agent. It exists so you can return to it later and understand what the semantic markers are, how they work, and how to use them. It is purely explanatory.

---

## Core Philosophy

### 1. The Documentation Graph is the Canon

Your project documentation is not three files. It is a **graph** — potentially hundreds or thousands of documents organized by node type, linked by typed relationships, and navigable through frontmatter and cross-references. The exact shape of your doc graph is defined by your project's documentation system (which is separate from this framework).

**This framework does not care how your docs are structured.** Whether you have 10 files or 10,000, whether they are in flat folders or deep hierarchies, whether they use frontmatter or not — the only thing that matters is: there exists a documentation graph, and files in that graph define behavior, architecture, requirements, or other canonical truths. The semantic marker points into that graph.

**The rule:**
- If a file has a corresponding document in the graph, it gets a marker.
- If a file does not have a corresponding document, it gets **no marker**. The absence of a marker is a signal: "this file is not yet canonized."
- You never invent a `GOVERNS` link to a document that does not exist.

### 2. The Marker is a Compass, Not a Map

The marker does not contain the full specification. It contains:
- **What this file does** (business role, not algorithm)
- **What it owns** (responsibility boundary)
- **What it does NOT own** (negative space — critically important)
- **Where the canonical definition lives** (link to the doc graph)
- **Key contracts** (behavioral promises extracted from the spec)

The marker is **extensive enough** that you understand the file's role without opening the docs. But it always **defers to the docs** for the full truth. The marker is a compass — it points north. The docs are the map.

### 3. Extensive PURPOSE, Not Terse Comments

Traditional code comments explain the algorithm. The PURPOSE field in a semantic marker explains the **business role** of the file. It answers:
- "What problem does this file solve?"
- "Where does it sit in the system?"
- "What does it delegate to others?"

This is 2-4 sentences minimum. One sentence is too vague. A paragraph is too long. The PURPOSE should be the first thing you read and the last thing you need to read to understand the file's place in the world.

### 4. Positive and Negative Space (BOUNDARY)

Every file must define what it owns AND what it does not own. The negative space is more important than the positive space because it prevents drift. When an agent sees:

```
NOT: Authentication, user profile, email delivery
```

...it knows not to add auth logic here. Without negative space, the boundary creeps. The file becomes a god-module. The marker's BOUNDARY section is the primary defense against scope creep.

### 5. One Marker Per File, Top of File

There is exactly one marker per file. It lives at the top of the file. No inline markers. No block markers. No function markers.

**Why:**
- Single point of truth: you look at the top, you know everything
- Grep-friendly: `head -n 30 filename` shows the marker
- Forces modularity: if the marker gets too long, the file is too big
- No clutter in the middle of logic

### 6. Marker is a Live Contract

When the docs change, the marker may need updating. When the implementation changes in a way that affects the marker (new responsibilities, new boundaries), the marker must be updated. The marker is not a fossil — it is a living contract between the code and the docs.

However, the marker is **subordinate to the docs**. If the marker and the docs disagree, the docs win. Always.

### 7. Agents Read Markers Before Editing

When an AI agent (or a human) opens a file to edit it:
1. Read the marker first
2. Follow the GOVERNS link to understand the canonical behavior
3. Make the change
4. If the change affects the marker (new boundary, new contract), update the marker

When writing a new file:
1. Check if the behavior is documented in the graph
2. If yes, write the implementation and add the marker
3. If no, **do not add a marker**. Flag the missing docs.

### 8. No Docs = No Marker

This is the hardest rule to follow but the most important. If the behavior is not documented, the file is not canonized. Adding a marker without docs creates the illusion of governance where none exists. The marker is a promise: "this file's behavior is defined in the canon." If the canon doesn't define it, there is no promise.

---

## The Marker Format

### Standard Preamble

Every marker begins with a standard preamble that identifies it as a semantic marker and explains its purpose. This educates new contributors and reminds agents that these are navigation aids, not documentation.

```
// ════════════════════════════════════════════════════════════
// SEMANTIC MARKER FRAMEWORK
// This file uses semantic markers to link implementation to
// the canonical documentation graph. These markers are
// navigation aids — they point to the docs, they do not
// replace them.
//
// If this file is missing a GOVERNS tag, it means the behavior
// is not yet documented in the canon. Document it before you
// change it.
// ════════════════════════════════════════════════════════════
```

The preamble is required. It creates a recognizable pattern that agents and tools can detect. The marker block always starts with `SEMANTIC MARKER FRAMEWORK` and ends with the closing line of equals signs.

### Tag Reference

| Tag | Required | Description | Length |
|-----|----------|-------------|--------|
| `GOVERNS` | **Yes** | One or more links to canonical documents. Must be real paths to real documents. Use section anchors when possible. | 1-3 lines |
| `PURPOSE` | **Yes** | 2-4 sentences explaining the business role of this file. Not what it does technically — what it does in the system. | 2-4 sentences |
| `BOUNDARY` | **Yes** | What this file owns and what it explicitly does NOT own. Both are required. | 3-8 lines |
| `CONTRACTS` | No | Key behavioral contracts extracted from the spec. Not every function — just the critical ones. | 1-5 lines |
| `DEPENDS_ON` | No | Other files or modules this file depends on. Use module IDs if the project uses them. | 1-3 lines |
| `EXPORTS` | No | Public surfaces. Optional because code already shows this. | 1 line |
| `NOTES` | No | High-signal constraints, gotchas, or operational details. | 1-3 lines |

### GOVERNS Tag

The GOVERNS tag is the most important tag. It answers: "Where is the canonical definition of this file's behavior?"

**Format:**
```
// GOVERNS:      docs/spec/auth/session.md
//               docs/arch/auth-layer.md#session-manager
//               docs/adr/0004-session-storage.md
```

**Rules:**
- Must be real, existing documents. No invented paths.
- Can link to multiple documents (spec + architecture + ADR)
- Use section anchors when possible (`#session-manager`)
- The path is relative to project root
- If the file has no governing document, skip the marker entirely

**Finding the right document:**
The agent or developer must search the documentation graph for the document that defines this file's behavior. There is no automatic mapping — the human or agent must understand the file and find the corresponding doc. This is intentional: it forces understanding.

### PURPOSE Tag

The PURPOSE tag explains the business role of the file. It is not a code comment. It is not algorithm documentation. It is the **"why this file exists"** story.

**Good examples:**
```
// PURPOSE:      Implements the session lifecycle for authenticated
//               users — creation, validation, expiration, and teardown.
//               This is the primary boundary for all session state
//               management. It does not handle authentication tokens
//               (see M-TOKEN) or user profile data.
```

```
// PURPOSE:      Maps external provider webhook payloads into our
//               internal event object format. This is the anti-
//               corruption layer between third-party APIs and our
//               domain model. It does not process business logic —
//               it only translates and validates structure.
```

**Bad examples:**
```
// PURPOSE:      Handles sessions.            ← too vague
// PURPOSE:      This file contains the createSession, validateSession,  ← too technical
//               and teardown functions. It uses the storage adapter
//               pattern and injects dependencies via constructor.
```

**The PURPOSE is for the CEO, not the engineer.** It should be understandable by someone who knows the product but doesn't know the code.

### BOUNDARY Tag

The BOUNDARY tag defines the responsibility boundary of the file. It has two subsections:

```
// BOUNDARY:
//   OWNS:       Session state, expiration logic, storage interface
//               contract, session ID generation
//   NOT:        Authentication tokens, user profile data, email
//               delivery, password reset, OAuth flows
```

**OWNS rules:**
- List what this file is the primary home for
- Be specific — "session state" not "auth stuff"
- If the file is a coordination layer, say what it coordinates

**NOT rules:**
- This is the critical part. List what the file explicitly does NOT own.
- Be extensive. The more negative space, the better.
- Think of what a confused agent might add here. Prevent it.
- Use "NOT" not "Does not own" — shorter, clearer.

**Why negative space matters:**
Files grow because boundaries are unclear. When an agent sees "I need to add email to the session," and the marker says "NOT: email delivery," the agent knows to look elsewhere. Without the marker, the agent adds it here. The file grows. Technical debt accumulates.

### CONTRACTS Tag

The CONTRACTS tag lists key behavioral contracts extracted from the governing spec. Not every function — just the critical ones that define the file's behavior.

```
// CONTRACTS:
//   - createSession: must return valid sessionId within 100ms
//   - validateSession: must reject expired tokens per expiration-rules
//   - teardown: must clear all state, no leaks
```

**Rules:**
- One line per contract
- Format: `- functionName: must/should/may + behavioral promise`
- Extract from the spec, don't invent
- If the spec has no contracts, omit this tag

**Why this exists:**
When an agent edits a function, it needs to know what behavioral promises it must preserve. The CONTRACTS tag is the "don't break these" list.

### DEPENDS_ON Tag

The DEPENDS_ON tag lists other files or modules this file depends on.

```
// DEPENDS_ON:   src/auth/token.ts (M-TOKEN)
//               src/storage/redis.ts (M-REDIS)
```

**Rules:**
- Use module IDs if the project uses them (e.g., M-TOKEN)
- List direct dependencies only, not transitive ones
- This is for humans/agents navigating the graph, not for the compiler

### EXPORTS Tag

The EXPORTS tag lists public surfaces. This is optional because the code already shows exports.

```
// EXPORTS:      createSession, validateSession, teardown
```

Include it when:
- The file has many exports and the important ones are not obvious
- The file exports types or constants that are the primary interface
- The file is a library/module where the exports are the contract

### NOTES Tag

The NOTES tag contains high-signal constraints, gotchas, or operational details.

```
// NOTES:
//   - Storage backend is injected via config (see docs/arch/runtime.md#configuration)
//   - All timestamps use UTC internally
//   - Session IDs are UUID v4, not sequential
```

**Rules:**
- High signal only — not a todo list, not a changelog
- Operational details that affect how the file is used
- Constraints that are not obvious from the code

---

## The Complete Marker Template

```typescript
// ════════════════════════════════════════════════════════════
// SEMANTIC MARKER FRAMEWORK
// This file uses semantic markers to link implementation to
// the canonical documentation graph. These markers are
// navigation aids — they point to the docs, they do not
// replace them.
//
// If this file is missing a GOVERNS tag, it means the behavior
// is not yet documented in the canon. Document it before you
// change it.
// ════════════════════════════════════════════════════════════
//
// GOVERNS:      <path to governing doc>
// PURPOSE:      <2-4 sentences about business role>
// BOUNDARY:
//   OWNS:       <what this file owns>
//   NOT:        <what this file does NOT own>
// CONTRACTS:
//   - <function>: <behavioral promise>
// DEPENDS_ON:   <file path (module id)>
// EXPORTS:      <public surfaces>
// NOTES:
//   - <high-signal constraint>
// ════════════════════════════════════════════════════════════
```

This is the canonical template. Use it for every marker. The only variation is which tags are present (CONTRACTS, DEPENDS_ON, EXPORTS, NOTES are optional). The preamble, GOVERNS, PURPOSE, and BOUNDARY are always required.

---

## Examples by Domain

### API Route Handler

```typescript
// ════════════════════════════════════════════════════════════
// SEMANTIC MARKER FRAMEWORK
// ════════════════════════════════════════════════════════════
//
// GOVERNS:      docs/spec/api/user-profile.md
//               docs/arch/api-layer.md#route-handlers
// PURPOSE:      Exposes the user profile read/update endpoints.
//               This is the HTTP surface for profile operations.
//               It does not contain business logic — it delegates
//               to the profile service and handles HTTP concerns
//               (serialization, status codes, error mapping).
// BOUNDARY:
//   OWNS:       HTTP request handling, response serialization,
//               error mapping to HTTP status codes
//   NOT:        Business logic, database queries, validation
//               rules, authentication (assumes auth middleware)
// CONTRACTS:
//   - GET /profile: must return 200 with profile object
//   - PUT /profile: must return 200 on success, 422 on validation
//               failure per spec
// DEPENDS_ON:   src/services/profile.ts (M-PROFILE)
//               src/middleware/auth.ts (M-AUTH)
// EXPORTS:      GET /profile, PUT /profile (route handlers)
// NOTES:
//   - Auth middleware must run before these handlers
//   - Rate limiting is applied at the router level, not here
// ════════════════════════════════════════════════════════════
```

### Service Layer

```typescript
// ════════════════════════════════════════════════════════════
// SEMANTIC MARKER FRAMEWORK
// ════════════════════════════════════════════════════════════
//
// GOVERNS:      docs/spec/business/orders.md
//               docs/arch/services.md#order-service
// PURPOSE:      Implements the order placement business logic.
//               This is the primary boundary for order creation,
//               pricing calculation, and inventory reservation.
//               It coordinates between the pricing service, inventory
//               service, and payment gateway to complete a sale.
// BOUNDARY:
//   OWNS:       Order creation, pricing calculation, inventory
//               reservation, order state transitions
//   NOT:        Payment processing (delegates to payment gateway),
//               shipping logic, user authentication, email delivery
// CONTRACTS:
//   - createOrder: must reserve inventory before accepting payment
//   - calculateTotal: must apply discounts per pricing-rules
//   - confirmOrder: must transition to CONFIRMED only after
//               payment success
// DEPENDS_ON:   src/services/pricing.ts (M-PRICING)
//               src/services/inventory.ts (M-INVENTORY)
//               src/gateways/payment.ts (M-PAYMENT)
// EXPORTS:      createOrder, calculateTotal, confirmOrder, cancelOrder
// NOTES:
//   - All operations are idempotent via idempotency key
//   - Inventory reservation has a 15-minute TTL
// ════════════════════════════════════════════════════════════
```

### Data Access Layer

```typescript
// ════════════════════════════════════════════════════════════
// SEMANTIC MARKER FRAMEWORK
// ════════════════════════════════════════════════════════════
//
// GOVERNS:      docs/spec/storage/user-accounts.md
//               docs/arch/persistence.md#repositories
// PURPOSE:      Provides data access for user account records.
//               This is the repository boundary for user data —
//               all database queries for user accounts go through
//               this file. It translates between domain objects
//               and database records.
// BOUNDARY:
//   OWNS:       User account CRUD, database queries, ORM mapping
//   NOT:        Business logic, validation, authentication,
//               session management, caching
// CONTRACTS:
//   - findByEmail: must return null if not found (never throw)
//   - create: must enforce unique email constraint
//   - update: must return updated record or throw on conflict
// DEPENDS_ON:   src/db/connection.ts (M-DB)
//               src/models/user.ts (M-USER-MODEL)
// EXPORTS:      UserRepository
// NOTES:
//   - Uses Prisma ORM — all queries are type-safe
//   - Email field is indexed (unique constraint)
// ════════════════════════════════════════════════════════════
```

### Utility/Helper

```typescript
// ════════════════════════════════════════════════════════════
// SEMANTIC MARKER FRAMEWORK
// ════════════════════════════════════════════════════════════
//
// GOVERNS:      docs/arch/shared.md#utilities
// PURPOSE:      Date formatting utilities used across the API
//               layer. Provides ISO-8601 formatting, relative
//               time strings, and timezone conversion. These
//               are pure functions with no side effects.
// BOUNDARY:
//   OWNS:       Date formatting, timezone conversion, relative
//               time calculation
//   NOT:        Business logic, date arithmetic (use date-fns),
//               locale management (i18n handles that)
// CONTRACTS:
//   - toISO: must always return valid ISO-8601 string
//   - toRelative: must handle past and future dates
// DEPENDS_ON:   date-fns (external)
// EXPORTS:      toISO, toRelative, toUTC
// NOTES:
//   - All functions are pure and memoizable
//   - Uses date-fns for underlying arithmetic
// ════════════════════════════════════════════════════════════
```

### CLI Tool

```typescript
// ════════════════════════════════════════════════════════════
// SEMANTIC MARKER FRAMEWORK
// ════════════════════════════════════════════════════════════
//
// GOVERNS:      docs/spec/cli/deployment.md
//               docs/arch/cli.md#deploy-command
// PURPOSE:      Implements the CLI command for deploying
//               application versions to staging and production.
//               This is the user-facing interface for the
//               deployment pipeline. It handles argument parsing,
//               environment validation, and orchestration of the
//               deployment steps.
// BOUNDARY:
//   OWNS:       CLI argument parsing, deployment orchestration,
//               progress reporting, user confirmation
//   NOT:        The actual deployment (delegates to deployer),
//               environment provisioning, rollback logic
// CONTRACTS:
//   - deploy: must require explicit --env flag
//   - deploy: must confirm before production deployment
//   - deploy: must report progress per deployment spec
// DEPENDS_ON:   src/deployer/core.ts (M-DEPLOYER)
//               src/cli/shared.ts (M-CLI-SHARED)
// EXPORTS:      deploy command
// NOTES:
//   - Production deployment requires manual confirmation
//   - Staging deployment is automatic
// ════════════════════════════════════════════════════════════
```

### Configuration

```typescript
// ════════════════════════════════════════════════════════════
// SEMANTIC MARKER FRAMEWORK
// ════════════════════════════════════════════════════════════
//
// GOVERNS:      docs/arch/runtime.md#configuration
// PURPOSE:      Defines the runtime configuration schema and
//               validation for the application. This is the
//               single source of truth for config structure —
//               all environment variables and config files
//               must conform to this schema.
// BOUNDARY:
//   OWNS:       Config schema definition, validation, default
//               values, environment variable mapping
//   NOT:        Secret management (use secret manager), feature
//               flags (use feature flag service), runtime state
// CONTRACTS:
//   - validate: must throw on missing required fields
//   - validate: must coerce types per schema
//   - load: must support .env file and env vars
// EXPORTS:      ConfigSchema, validateConfig, loadConfig
// NOTES:
//   - Uses zod for schema validation
//   - Required fields are marked with .nonempty()
// ════════════════════════════════════════════════════════════
```

---

## Rules and Invariants

### 1. No Docs, No Marker

If a file has no corresponding document in the documentation graph, it gets no marker. The absence of a marker is a signal, not a mistake. This rule prevents the illusion of governance.

**When to skip the marker:**
- Trivial helpers (pure functions, no business logic)
- Generated files (auto-generated from schemas)
- Boilerplate (standard config files)
- Files with no documented behavior yet

**When to create the doc first:**
- New feature files
- New service files
- Any file that implements business logic

### 2. GOVERNS Must Be Real

Never invent a `GOVERNS` link. The path must point to a real document. If you're not sure which document governs a file, you have two choices:
1. Find the right document (search the doc graph)
2. Create the document first, then add the marker

**Lint rule:** A CI check should verify that every `GOVERNS` path resolves to a real file.

### 3. PURPOSE is Business-Facing

The PURPOSE tag explains the business role, not the technical implementation. If the PURPOSE reads like a code comment, it's wrong. If the PURPOSE could be understood by a product manager, it's right.

**Test:** Show the PURPOSE to someone who knows the product but not the code. Can they understand what the file does? If yes, it's good. If no, rewrite it.

### 4. BOUNDARY Must Have NOT

The BOUNDARY tag is incomplete without the `NOT` subsection. Every marker must explicitly define what the file does NOT own. This is the primary defense against scope creep.

**Test:** Read the `NOT` section. Could someone reasonably add the listed items to this file? If yes, the `NOT` section is too narrow. Expand it.

### 5. One Marker Per File

There is exactly one marker per file. No exceptions. If a file covers multiple concerns, either:
- The file is too big and should be split
- The concerns are related and the marker covers them all

**Test:** If the marker exceeds 30 lines, the file is probably too big.

### 6. Marker at Top of File

The marker always lives at the top of the file, before imports, before code, before anything. This makes it immediately visible when opening the file.

**Why:** When you open a file, the first thing you see should be the marker. Not the imports. Not the code. The marker. This is the "you are here" sign.

### 7. Update Markers When Docs Change

When a governing document changes, the marker may need updating. The marker is a live contract. When the contract changes, the marker must reflect it.

**However:** The marker is subordinate to the docs. If the docs change and you haven't updated the marker, the docs are still correct. The marker is just outdated. Fix it when you find it.

### 8. No Duplication of Spec

The marker summarizes and points. It does not contain the full spec. If the reader needs details, they follow the GOVERNS link. The marker should be understandable without the docs, but it should not replace the docs.

**Test:** If the marker contains more than 5 lines of detailed behavior, it's duplicating the spec. Move it to the docs and link to it.

### 9. Use Native Comment Style

The marker uses the native comment style of the language. In TypeScript, use `//`. In Python, use `#`. In Rust, use `//`. The content is the same; the comment syntax varies.

**Example in Python:**
```python
# ════════════════════════════════════════════════════════════
# SEMANTIC MARKER FRAMEWORK
# ════════════════════════════════════════════════════════════
#
# GOVERNS:      docs/spec/business/orders.md
# PURPOSE:      ...
# BOUNDARY:
#   OWNS:       ...
#   NOT:        ...
# ════════════════════════════════════════════════════════════
```

### 10. Consistent Formatting

All markers in a project should follow the same formatting:
- Same preamble
- Same tag order (GOVERNS, PURPOSE, BOUNDARY, CONTRACTS, DEPENDS_ON, EXPORTS, NOTES)
- Same indentation
- Same line width (80-100 characters)

This consistency makes markers machine-parseable and human-readable.

---

## Integration with Documentation

### The Marker Points Into the Doc Graph

The documentation graph is separate from this framework. The marker assumes the docs exist and points to them. The exact structure of the docs doesn't matter — what matters is that there is a canonical document for each file's behavior.

**The marker points to specific documents.** It does not point to "the docs" or "the spec." It points to a specific document that defines this file's behavior. That document could be anywhere in the graph.

### Finding the Right Document

When adding a marker, you must find the right document. This is a manual step (or assisted by search). There is no automatic mapping.

**Process:**
1. Understand what the file does
2. Search the doc graph for the relevant document
3. Use the document's path as the GOVERNS link
4. If no document exists, create it first

**Search patterns:**
- Search the doc graph for keywords related to the file
- Read `docs/INDEX.md` (or the root index) to find the relevant section
- Use the graph navigation (follow links from related docs)
- Ask: "Which document defines the behavior this file implements?"

### Doc-to-Code Navigation

The framework is bidirectional. Not only does code point to docs, but docs can point to code.

In the governing document, you can add an "Implementation" section:
```markdown
## Implementation

- `src/auth/session.ts` — session lifecycle
- `src/auth/token.ts` — token management
```

This creates a two-way link: docs → code and code → docs. The docs are the graph. The markers are the edges.

---

## Integration with Code Organization

### File Size and Modularity

The marker enforces modularity. If a file's marker becomes too long, the file is too big.

**Guidelines:**
- Marker should fit in a screenful (20-30 lines)
- File should be <500 lines
- If the file exceeds 500 lines, split it
- If the marker exceeds 30 lines, the file probably does too much

**Why this matters:**
The marker is a summary of the file. If the summary is long, the file is complex. Complex files are hard to understand, test, and maintain. Split them.

### Module Naming

If the project uses module IDs (e.g., M-SESSION), the marker should reference them:
```
// DEPENDS_ON:   src/auth/token.ts (M-TOKEN)
```

Module IDs are optional. They are useful when:
- The project has many files
- The documentation graph uses module IDs
- The team prefers IDs over paths

If the project does not use module IDs, paths are sufficient.

### Directory Structure

The marker works with any directory structure. It doesn't matter whether the code is organized by:
- Feature (`src/auth/`, `src/orders/`)
- Layer (`src/controllers/`, `src/services/`, `src/repositories/`)
- Domain (`src/domain/user/`, `src/domain/order/`)

The marker points to docs, not to directories. The directory structure is independent.

---

## AI Agent Integration

### For Reading Agents

When an AI agent opens a file to read it:
1. **Read the marker first.** If there is a marker, understand the file's role before reading the code.
2. **Follow GOVERNS.** If the marker exists, follow the GOVERNS link to the canonical document.
3. **Read the code.** Now that you understand the role and boundaries, read the implementation.

If there is no marker:
1. Check if the file is trivial (helper, generated, boilerplate)
2. If not trivial, flag it: "This file has no marker and no governing docs."
3. Do not assume you understand the file's role without docs.

### For Writing Agents

When an AI agent creates a new file:
1. **Check if the behavior is documented.** Search the doc graph for the relevant document.
2. **If documented:** Write the implementation, then add the marker pointing to the docs.
3. **If not documented:** Do not add a marker. Flag the missing docs.

When an AI agent edits an existing file:
1. **Read the marker first.** Understand the boundaries before editing.
2. **If the change affects boundaries:** Update the marker. If the file now owns more, update OWNS. If it now owns less, update NOT.
3. **If the change affects contracts:** Update CONTRACTS.

### For Review Agents

When an AI agent reviews a file:
1. **Check the marker exists.** If no marker and the file is non-trivial, flag it.
2. **Check GOVERNS resolves.** The linked document must exist.
3. **Check PURPOSE is business-facing.** Not technical, not algorithmic.
4. **Check BOUNDARY has NOT.** Every marker must have negative space.
5. **Check marker matches code.** If the code does things the marker says it doesn't, flag it.
6. **Check marker matches docs.** If the docs define behavior the marker doesn't mention, flag it.

### For Migration Agents

When migrating or refactoring:
1. **Read all markers in the affected files.**
2. **Understand the boundaries** before moving code.
3. **Update markers** after moving code. If a file's responsibilities change, the marker changes.
4. **If splitting a file:** Each new file gets its own marker. The original marker is retired.

---

## Tooling

### Grep Patterns

The marker is designed to be grep-friendly. Common patterns:

```bash
# Find all files with markers
grep -r "SEMANTIC MARKER FRAMEWORK" src/

# Find all markers that reference a specific doc
grep -r "GOVERNS.*session" src/

# Find all markers for a module
grep -r "M-SESSION" src/

# Find all files without markers (approximate)
find src -name "*.ts" -exec sh -c 'head -n 5 "$1" | grep -q "SEMANTIC MARKER" || echo "$1"' _ {} \;

# Find all markers and their PURPOSE
grep -A 5 "PURPOSE:" src/**/*.ts
```

### Lint Checks

A CI lint check should verify:
1. Every non-trivial file has a marker
2. Every GOVERNS link resolves to a real document
3. Every marker has PURPOSE, BOUNDARY, and BOUNDARY has NOT
4. No marker exceeds 30 lines
5. PURPOSE is not algorithmic (heuristic: doesn't mention function names)

### Auto-Generation (Partial)

Some parts of the marker can be auto-generated:
- `EXPORTS` can be extracted from the code
- `DEPENDS_ON` can be extracted from imports
- `GOVERNS` can be suggested by searching the doc graph

But the critical parts must be manual:
- `PURPOSE` requires understanding the business role
- `BOUNDARY` requires understanding the file's place in the system
- `CONTRACTS` requires reading the spec

**Partial automation is fine. Full automation is dangerous.** The marker is a contract. Contracts require understanding.

---

## Common Mistakes

### 1. Marking Everything

Not every file needs a marker. Trivial helpers, generated files, and boilerplate don't need markers. Adding markers to everything creates noise and makes the framework less meaningful.

**Test:** If you delete the file, does the system break? If no, it's probably trivial and doesn't need a marker.

### 2. Vague PURPOSE

```
// PURPOSE:      Handles auth stuff.
```

This is useless. The PURPOSE should explain the business role, not just name the domain.

**Fix:** "Implements the authentication boundary for the API — session validation, token refresh, and logout. This is the primary entry point for all authenticated requests."

### 3. Missing NOT

```
// BOUNDARY:
//   OWNS:       Session management
```

Without NOT, the boundary is unclear. What doesn't the file own?

**Fix:** Always add NOT. "NOT: Token generation, user registration, password hashing."

### 4. Inventing GOVERNS

```
// GOVERNS:      docs/spec/auth.md          ← doesn't exist
```

Never invent links. If the docs don't exist, the marker doesn't exist.

**Fix:** Create the doc first, then add the marker.

### 5. Duplicating the Spec

```
// CONTRACTS:
//   - createSession: must accept a userId string, validate it
//               against the user table, generate a UUID v4
//               session ID, store it in Redis with a 24-hour
//               TTL, and return the session object...
```

This is too long. The marker summarizes. The spec details.

**Fix:** "- createSession: must return valid session within 100ms" — then link to the spec for details.

### 6. Outdated Markers

The file used to handle email but now it doesn't. The marker still says it does. The marker is a lie.

**Fix:** Update the marker when the file changes. The marker is a live contract.

### 7. Technical PURPOSE

```
// PURPOSE:      This file exports the createSession,
//               validateSession, and teardown functions.
//               It uses the storage adapter pattern.
```

This is a technical description, not a business role. It tells you what the file contains, not what it does in the system.

**Fix:** "Implements the session lifecycle for authenticated users — creation, validation, expiration, and teardown."

### 8. Marking Generated Files

```
// ════════════════════════════════════════════════════════════
// SEMANTIC MARKER FRAMEWORK
// GOVERNS:      docs/generated/prisma.md
// PURPOSE:      Auto-generated by Prisma from the schema.
// ════════════════════════════════════════════════════════════
```

Generated files don't need markers. The source of truth is the generator (schema, protobuf, etc.), not the generated file.

**Fix:** Don't add markers to generated files. Add markers to the generator/schema if needed.

---

## FAQ

### Q: Do I need to add markers to every file?

No. Only files that implement documented behavior. Trivial helpers, generated files, and boilerplate don't need markers.

### Q: What if the docs don't exist yet?

Don't add a marker. The absence of a marker is a signal that the behavior is not yet canonized. Create the docs first, then add the marker.

### Q: Can I add block-level or function-level markers?

No. One marker per file, at the top. If you need more granular markers, the file is too big. Split it.

### Q: What if a file is governed by multiple docs?

List all of them in GOVERNS. It's common for a file to be governed by a spec, an architecture doc, and an ADR.

### Q: What if the docs change and the marker is outdated?

Update the marker. The marker is a live contract. However, the docs always win. If the marker and docs disagree, the docs are correct.

### Q: Should I add markers to test files?

Yes, if the test file implements documented test behavior. The marker points to the test spec or the verification plan.

### Q: What about config files?

Config files that define runtime behavior (not just values) should have markers. For example, a schema definition file that defines the config structure. A simple `.env` file does not need a marker.

### Q: Can I use this in languages without comments?

Yes. Use the language's native documentation mechanism. In Python, use docstrings. In Rust, use doc comments. In Go, use package comments. The content is the same; the mechanism varies.

### Q: Is this a replacement for code comments?

No. Code comments explain the algorithm. Semantic markers explain the file's role and boundaries. They serve different purposes. Use both.

### Q: How do I enforce this in my team?

1. Add it to your code review checklist: "Does this file have a marker? Is the marker correct?"
2. Add a CI lint check: verify markers exist for non-trivial files and GOVERNS resolves.
3. Include it in onboarding: new team members learn the framework from this document.

### Q: What if someone adds a marker without reading the docs?

The marker will be wrong. This is why the GOVERNS tag must be verified. A CI check should confirm that GOVERNS links resolve to real documents. The marker is a contract — it must be accurate.

### Q: Can I use this with existing documentation systems?

Yes. The framework is agnostic to the documentation system. It only requires that:
1. There is a documentation graph
2. Documents in the graph define behavior
3. The marker can link to a document by path

Whether your docs are in Markdown, XML, or a database doesn't matter.

### Q: Does this replace my existing doc system?

No. This is a **navigation layer** on top of your existing docs. Your docs define the behavior. The markers point to the docs. Neither replaces the other.

### Q: What if the marker and the docs disagree?

The docs win. The marker is a navigation aid. The docs are the canon. If the marker is outdated, update it. If the docs are wrong, fix the docs.

### Q: How do I migrate an existing codebase to this framework?

1. Start with new files. Add markers to every new file from day one.
2. For existing files, add markers when you edit them. Don't do a bulk migration — it's too much work and too error-prone.
3. Prioritize files that change frequently. The marker is most valuable for files that are edited often.

### Q: Can I use this for non-code files?

Yes. SQL files, infrastructure definitions, and other non-code files can have markers if they implement documented behavior. Use the native comment style of the file format.

### Q: What if the file is a framework file (e.g., React component)?

If the component implements documented behavior, it gets a marker. The marker points to the UI spec or the component architecture doc. If the component is purely presentational (no business logic), it may not need a marker.

### Q: Can I add markers to third-party code?

No. The framework is for your project's code. Third-party code is governed by its own documentation. Don't modify third-party files.

### Q: What if the file is a script (e.g., deployment script)?

Scripts that implement documented behavior get markers. For example, a deployment script that implements the deployment spec. The marker points to the deployment documentation.

### Q: Is this overkill for small projects?

The framework scales with project complexity. Small projects (1-10 files) may not need it. Medium projects (10-100 files) benefit from it. Large projects (100+ files) need it. Start using it when you find yourself asking "what does this file do?" or when you have more than 20 files.

### Q: Can I use this with AI-generated code?

Yes. In fact, the framework is designed for AI agents. When an AI agent generates code, it should:
1. Check if the behavior is documented
2. If yes, add the marker pointing to the docs
3. If no, flag the missing docs

This prevents AI agents from generating code that drifts from the spec.

### Q: What if the AI agent doesn't understand the business role?

Then the PURPOSE will be wrong. This is why the agent must read the docs first. The PURPOSE is derived from the docs, not invented. If the agent can't write a good PURPOSE, it doesn't understand the file and shouldn't be editing it.

### Q: How do I review markers in code review?

Check:
1. Does the marker exist? (for non-trivial files)
2. Does GOVERNS resolve to a real document?
3. Is PURPOSE business-facing, not technical?
4. Does BOUNDARY have NOT?
5. Does the marker match the code?
6. Does the marker match the docs?

### Q: Can I automate marker generation?

Partially. You can auto-generate EXPORTS, DEPENDS_ON, and suggest GOVERNS. But PURPOSE, BOUNDARY, and CONTRACTS require understanding. Don't auto-generate those. They are the heart of the marker.

### Q: What if the marker makes the file too long?

The marker should be 20-30 lines. If it's longer, the file is too big. Split the file. The marker enforces modularity.

### Q: Can I add the marker to the bottom of the file?

No. The marker is at the top. This is non-negotiable. The top of the file is the first thing you see. The marker must be the first thing.

### Q: What if the file is minified or generated?

Don't add markers to minified or generated files. The marker belongs to the source, not the output.

### Q: Can I use this for documentation files themselves?

No. The marker is for code files. Documentation files are the canon. They don't need markers pointing to themselves.

### Q: What if the file is a test utility?

Test utilities that implement documented behavior (e.g., a test factory that creates test data per the spec) get markers. Pure test helpers (e.g., a `assertEquals` wrapper) don't.

### Q: Is this a replacement for architecture decision records?

No. ADRs are part of the documentation graph. The marker can point to ADRs. They serve different purposes.

### Q: Can I use this for non-software projects?

Yes. Any project where you have a documentation graph and implementation files can use this framework. Data pipelines, infrastructure, documentation systems — anything with a "canon" and "implementation" split.

### Q: What if the file is a migration?

Database migrations implement documented schema changes. The marker points to the schema spec or the migration plan. However, migrations are transient — they run once and are never edited. The marker is less valuable here. Optional.

### Q: Can I use this with multiple programming languages in one project?

Yes. The marker uses the native comment style of each language. The content and format are the same across languages.

### Q: What if the file is a monorepo package?

Each package in a monorepo is its own project. The marker lives in the package's files and points to the package's docs. The monorepo root may have its own docs for cross-cutting concerns.

### Q: How do I handle versioned APIs?

If you have multiple versions of an API (v1, v2), each version's implementation files have their own markers pointing to the version-specific spec. The marker is tied to the implementation, not the abstract API.

### Q: Can I add markers to internal documentation files?

No. The marker is for code files. Internal docs are part of the canon. They don't need markers.

### Q: What if the marker is wrong?

Fix it. The marker is a live contract. Wrong markers are worse than no markers because they create false confidence. A lint check should catch outdated markers by verifying GOVERNS links and checking if the marker matches the code.

### Q: Can I use this for microservices?

Yes. Each microservice has its own code and docs. The marker lives in the service's code and points to the service's docs. Cross-service dependencies are listed in DEPENDS_ON.

### Q: What if the file is shared across multiple services?

Shared libraries should have their own docs. The marker points to the library's docs. If the library is used by multiple services, each service's code may reference the library in its own markers.

### Q: How do I handle hotfixes?

Hotfixes are temporary. If the hotfix implements documented behavior, it gets a marker. If it's a temporary workaround, the marker should note it:
```
// NOTES:
//   - This is a hotfix for issue #123. Remove when the root
//     cause is fixed (see docs/adr/0005-hotfix.md).
```

### Q: Can I use this for legacy code?

Yes. Add markers to legacy code when you edit it. Don't do a bulk migration. The marker is most valuable for files that change frequently.

### Q: What if the legacy code has no docs?

Then it has no marker. The absence of a marker is a signal: "this code is not canonized." When you need to edit it, you have two choices:
1. Reverse-engineer the behavior and document it, then add a marker
2. Edit carefully, knowing the behavior is not canonized

### Q: Is this compatible with existing code standards?

Yes. The marker is a comment block. It doesn't affect compilation, linting, or formatting. It integrates with any existing code standard.

### Q: Can I use this with JSDoc/TSDoc?

Yes. The marker is a separate block from JSDoc. Put the marker at the top, then JSDoc comments on functions. They serve different purposes.

### Q: What if the file is a CSS file?

CSS files can have markers if they implement documented design system behavior. Use CSS comments:
```css
/* ════════════════════════════════════════════════════════════
   SEMANTIC MARKER FRAMEWORK
   ════════════════════════════════════════════════════════════
   GOVERNS:      docs/design/buttons.md
   PURPOSE:      Defines the button component styles. This is
                 the primary implementation of the button design
                 system. It does not handle button behavior.
   BOUNDARY:
     OWNS:       Button styles, variants, states
     NOT:        Button behavior, form validation, accessibility
   ════════════════════════════════════════════════════════════ */
```

### Q: Can I use this for SQL files?

Yes. SQL files that implement documented schema or queries get markers. Use SQL comments:
```sql
-- ════════════════════════════════════════════════════════════
-- SEMANTIC MARKER FRAMEWORK
-- ════════════════════════════════════════════════════════════
-- GOVERNS:      docs/schema/users.md
-- PURPOSE:      Defines the user table schema. This is the
--               primary storage for user account data.
-- BOUNDARY:
--   OWNS:       User table schema, indexes, constraints
--   NOT:        Business logic, authentication, session data
-- ════════════════════════════════════════════════════════════
```

---

## Summary

The Semantic Markers Framework is a **navigation layer** that connects code to documentation. It is not a documentation system. It is not a code standard. It is a compass.

**The core rules:**
1. One marker per file, at the top
2. Markers point to real docs (GOVERNS)
3. PURPOSE explains the business role (2-4 sentences)
4. BOUNDARY defines positive and negative space
5. No docs = no marker
6. Markers are live contracts — update them when docs or code change
7. Markers are subordinate to docs — docs always win

**The goal:** When you open a file, you know immediately what it does, what it owns, what it doesn't own, and where the canonical definition lives. No guesswork. No drift. No islands.

**This is the canonical reference.** Everything about semantic markers is defined here. Read it to understand. Read it to implement. Read it to audit.

---

## Appendix: Marker Checklist

When adding a marker, verify:

- [ ] The file has corresponding documentation in the doc graph
- [ ] GOVERNS points to a real, existing document
- [ ] PURPOSE is 2-4 sentences, business-facing, not technical
- [ ] BOUNDARY has both OWNS and NOT
- [ ] NOT is extensive and prevents scope creep
- [ ] CONTRACTS (if present) are extracted from the spec, not invented
- [ ] DEPENDS_ON (if present) lists real files
- [ ] NOTES (if present) are high-signal, not todo items
- [ ] Marker is at the top of the file
- [ ] Marker uses the standard preamble
- [ ] Marker fits in a screenful (20-30 lines)
- [ ] File is <500 lines (if marker is long, split the file)
- [ ] Native comment style is used
- [ ] Formatting is consistent with other markers in the project

When reviewing a marker, verify:

- [ ] Marker exists (for non-trivial files)
- [ ] GOVERNS resolves to a real document
- [ ] PURPOSE is not algorithmic
- [ ] BOUNDARY has NOT
- [ ] Marker matches the code
- [ ] Marker matches the docs
- [ ] Marker is not outdated

---

## Appendix: Lint Rules

A CI lint check should enforce:

1. **marker_exists:** Every non-trivial file (not generated, not trivial helper) has a marker
2. **marker_preamble:** Marker starts with `SEMANTIC MARKER FRAMEWORK`
3. **governs_resolves:** Every GOVERNS path resolves to a real file
4. **purpose_length:** PURPOSE is between 2 and 4 sentences
5. **boundary_not_present:** BOUNDARY has a NOT subsection
6. **marker_not_too_long:** Marker is <30 lines
7. **marker_at_top:** Marker is within the first 10 lines of the file
8. **purpose_not_technical:** PURPOSE doesn't contain function names (heuristic)

---

## Appendix: Quick Reference

**The marker:**
```
// ════════════════════════════════════════════════════════════
// SEMANTIC MARKER FRAMEWORK
// ════════════════════════════════════════════════════════════
// GOVERNS:      <path>
// PURPOSE:      <2-4 sentences>
// BOUNDARY:
//   OWNS:       <what it owns>
//   NOT:        <what it does not own>
// CONTRACTS:   <optional>
// DEPENDS_ON:  <optional>
// EXPORTS:      <optional>
// NOTES:       <optional>
// ════════════════════════════════════════════════════════════
```

**Required tags:** GOVERNS, PURPOSE, BOUNDARY (with OWNS and NOT)
**Optional tags:** CONTRACTS, DEPENDS_ON, EXPORTS, NOTES
**Location:** Top of file, before imports
**Length:** 20-30 lines
**Format:** Native comment style of the language

**The philosophy:**
- Docs are the canon. Markers are the compass.
- No docs, no marker.
- Extensive PURPOSE, not terse comments.
- Positive and negative space in BOUNDARY.
- One marker per file.
- Markers are live contracts.
- Markers are subordinate to docs.

**The goal:** Every file is a node in a graph. Open the file, read the marker, understand the file's role without reading the code.

---

*End of Document*
