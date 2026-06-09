# Spec Format — BDD + RFC

Every behavioral specification document (`node_type: spec` or `feature-spec`) follows this merged format: BDD's Given/When/Then scenarios + RFC 2119 normative keywords + goal-driven structure.

---

## Document Template

```markdown
# {Feature Name} Behavior

## Purpose
{1-3 sentences: what this spec covers, why it matters}

## Goals
- **G1:** {measurable, testable goal}
- **G2:** {measurable, testable goal}

## Requirements

### Requirement: {Name}
The system MUST {behavior}. Use RFC 2119: MUST, SHOULD, MAY.

**As a** {role}
**I want** {feature}
**So that** {benefit or value}

#### Scenario: {Happy path — what working looks like}
- **GIVEN** {initial context}
- **WHEN** {triggering event}
- **THEN** {expected outcome}
- **AND** {additional outcome}

*Definition of working: If this scenario passes, the requirement is met.*

#### Scenario: {Edge case or error}
- **GIVEN** {context for this edge case}
- **WHEN** {trigger}
- **THEN** {expected outcome}

*Definition of working: If this scenario fails to produce the expected error, the system is broken.*

## Data Contracts

### {Interface Name}
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| field | string | yes | description |

## State Transitions
| From State | Event | To State | Side Effects |
|-----------|-------|----------|-------------|
| logged_out | login | authenticated | JWT issued |

## Error Handling
| Error Code | HTTP | When | Response |
|-----------|------|------|---------|
| invalid_creds | 401 | Wrong credentials | `{ "error": "..." }` |

## Security Considerations
- {Security requirement using MUST/SHOULD/MAY}

## Limits
| Constraint | Value | Reason |
|-----------|-------|--------|
| Max attempts | 5 / 15 min | Brute force prevention |
```

---

## Section Guide

### Purpose
1-3 sentences. What does this spec cover, and why is it important?

### Goals
Numbered goals (G1, G2...). Each must be:
- **Measurable** — can verify whether it's met
- **Testable** — a test could confirm compliance
- **Behavioral** — describes outcome, not implementation

Good: "No plaintext credentials touch persistent storage."
Bad: "Use bcrypt for hashing." (implementation detail)

### Requirements
Each requirement states a single behavior with an RFC 2119 keyword:

| Keyword | Meaning |
|---------|---------|
| **MUST / MUST NOT** | Absolute, non-negotiable |
| **SHOULD / SHOULD NOT** | Recommended default; exceptions need justification |
| **MAY** | Optional, implementation's choice |

Follow each requirement with:
1. A user story (As a / I want / So that)
2. At least one scenario (Given / When / Then)

### User Stories
Capture WHO benefits, WHAT they want, and WHY it matters. Keeps specs grounded in user value.

### Definition of Working

Every scenario includes a *"Definition of working"* — a one-line statement of what confirms the behavior is correct. This is NOT a success message or a test assertion. It is a contract:

- **Happy path:** "If this scenario passes, the requirement is met."
- **Error path:** "If this scenario fails to produce the expected error, the system is broken."
- **Conflict path:** "If this scenario throws a different error, we cannot proceed — the conflict must be resolved first."
- **Boundary path:** "If the input exceeds the limit, the system MUST reject it. Accepting it means the limit is not enforced."

This turns every scenario from "here's a nice example" into "here's exactly what working means, and here's exactly what broken means."

### Scenarios
Every requirement has ≥1 scenario. Scenarios must be:
- **Concrete** — specific values, not placeholders
- **Testable** — could write an automated test from it
- **Declarative** — what happens, not UI clicks (see below)
- **Cover both paths** — minimum: happy path + error/edge case
- **Have a definition of working** — what confirms this behavior is correct

Pattern:
- **GIVEN** — preconditions, existing state before the event
- **WHEN** — triggering event (action, system event, timer)
- **THEN** — expected outcomes (state changes, responses, side effects)
- **AND** — additional context or outcomes (anywhere after GIVEN/WHEN/THEN)

### Declarative vs Imperative — Critical Rule

Scenarios MUST be declarative (business language), NEVER imperative (UI/implementation details).

**Declarative (correct):**
> GIVEN a registered user with valid credentials  
> WHEN they submit the login form  
> THEN they are redirected to the dashboard

**Imperative (wrong):**
> GIVEN the login page is loaded  
> WHEN the user types "user@example.com" in the email field  
> AND clicks the "#login-button"  
> THEN the browser navigates to "/dashboard"

Why this matters: declarative scenarios survive UI redesigns, framework changes, and implementation rewrites. Imperative scenarios break the moment you change a CSS selector. If a scenario mentions a button, a field name, a URL path, or a DOM element, rewrite it declaratively.

### Data Contracts
Tables of inputs/outputs with types and constraints. Use real field names — implementers code against this.

### State Transitions
`From State | Event | To State | Side Effects`. For stateful behavior: auth, workflows, ordering.

### Error Handling
Exhaustive table: error codes, conditions, response bodies. Every error the system can produce.

### Security Considerations
Required even if brief. If no special concerns: "No special security considerations beyond standard practices."

### Limits
Every spec defines boundaries: rate limits, sizes, timeouts, retries, with exact values and reasons.

---

## What Does NOT Belong in a Spec

- ❌ Class names, function names, file paths, framework choices
- ❌ Step-by-step implementation instructions
- ❌ UI layout, CSS, pixel values
- ❌ Database queries, ORM configuration
- ❌ Non-behavioral trivia ("this file was created by Bob in 2023")

**Quick test:** If the implementation can change without changing externally visible behavior, it does NOT belong in a spec.

---

## Spec vs Architecture vs Overview

| Layer | Answers | Contains | Does NOT contain |
|-------|---------|----------|-----------------|
| **overview/** | WHY does this exist? | Identity, purpose, users, value, non-goals | Behavior details, tech choices |
| **spec/** | WHAT must it do? | Requirements, scenarios, contracts, errors | Implementation structure |
| **architecture/** | HOW is it built? | Components, dependencies, boundaries, ADRs | Behavioral requirements |

A good way to test: could you hand the spec to an independent team and they'd build the right thing without seeing the code? If yes, the spec is strong enough.
