# Mode: Propose

**Trigger:** Asked to create a change proposal for a new feature, refactor, or significant modification. Produces a `docs/changes/<name>/` folder with proposal, behavior deltas, design, and tasks.

---

## Workflow

### Step 1: Gather
Read the relevant existing docs first:
- `docs/overview/` — to understand product context
- `docs/spec/` — to understand current behavior you're modifying
- `docs/architecture/` — to understand implementation constraints

Ask clarifying questions if behavior, constraints, or boundaries are unclear.

### Step 2: Create the change folder
```
docs/changes/<kebab-case-name>/
├── proposal.md      # Why + scope
├── behavior.md      # Delta spec: ADDED/MODIFIED/REMOVED
├── design.md        # Technical approach
└── tasks.md         # Implementation checklist
```

Name the folder with kebab-case, descriptive: `add-dark-mode`, `fix-auth-timeout`, `refactor-session-store`.

### Step 3: Write proposal.md

```markdown
---
node_type: change-proposal
title: Add Dark Mode
status: draft
updated: YYYY-MM-DD
tags: [ui, theming]
links:
  depends_on: [../../spec/features/ui.md]
---

# Proposal: {Title}

## Intent
{1 paragraph: why are we doing this? what problem does it solve?}

## Scope
**In scope:**
- {item 1}
- {item 2}

**Out of scope:**
- {item 1}

## Approach
{1 paragraph: high-level approach — what layers change, not how}
```

### Step 4: Write behavior.md (Delta Spec)

This is the most important artifact. It describes behavioral changes as deltas:

```markdown
---
node_type: change-behavior
title: Dark Mode Behavior Changes
status: draft
updated: YYYY-MM-DD
links:
  depends_on: [proposal.md]
  documents: [../../spec/features/ui.md]
---

# Behavior Changes: Dark Mode

## ADDED Requirements

### Requirement: Theme Persistence
The system MUST persist the user's theme preference across sessions.

#### Scenario: Theme survives page reload
- **GIVEN** a user who selected dark mode
- **WHEN** the user reloads the page
- **THEN** the page renders in dark mode

### Requirement: System Preference Detection
The system MUST detect the OS-level theme preference on first visit.

#### Scenario: First visit on dark-mode OS
- **GIVEN** a first-time visitor whose OS is in dark mode
- **WHEN** the page loads
- **THEN** the page renders in dark mode
- **AND** the preference is saved to localStorage

## MODIFIED Requirements

### Requirement: Theme Toggle
The system MUST provide a theme toggle in the header.
(Previously: theme toggle was in settings page only.)

#### Scenario: Quick toggle from header
- **GIVEN** a user on any page
- **WHEN** the user clicks the theme toggle in the header
- **THEN** the theme switches immediately
- **AND** the preference is persisted

## REMOVED Requirements

### Requirement: Per-Page Theme Override
(Removed — simplified to global theme only. Per-page overrides caused confusion.)
```

**Delta rules:**
- **ADDED** — new behavior. Archive appends to main spec.
- **MODIFIED** — changed behavior. MUST include "(Previously: ...)" note. Archive replaces the requirement.
- **REMOVED** — deprecated behavior. MUST include reason. Archive deletes from main spec.

### Step 5: Write design.md

```markdown
---
node_type: change-design
title: Dark Mode Design
status: draft
updated: YYYY-MM-DD
links:
  depends_on: [proposal.md, behavior.md]
---

# Design: {Title}

## Technical Approach
{How we'll implement this. Libraries, patterns, data flow.}

## Architecture Decisions

### Decision: CSS Custom Properties over CSS-in-JS
{Decision, rationale, alternatives considered.}

### Decision: React Context over Redux
{Decision, rationale, alternatives considered.}

## Data Flow
{ASCII diagram or description of data/control flow.}

## File Changes
- `src/contexts/ThemeContext.tsx` (new)
- `src/components/ThemeToggle.tsx` (new)
- `src/styles/globals.css` (modified)
```

### Step 6: Write tasks.md

```markdown
---
node_type: change-tasks
title: Dark Mode Tasks
status: draft
updated: YYYY-MM-DD
links:
  depends_on: [design.md]
---

# Tasks: {Title}

## 1. Theme Infrastructure
- [ ] 1.1 Create ThemeContext with light/dark state
- [ ] 1.2 Add CSS custom properties for theme colors
- [ ] 1.3 Implement localStorage persistence
- [ ] 1.4 Add system preference detection

## 2. UI Components
- [ ] 2.1 Create ThemeToggle component
- [ ] 2.2 Add toggle to header
- [ ] 2.3 Update all components to use CSS variables

## 3. Testing & Polish
- [ ] 3.1 Test contrast ratios for accessibility
- [ ] 3.2 Test persistence across page reloads
- [ ] 3.3 Test system preference detection
```

**Task best practices:**
- Group under numbered headings
- Use hierarchical numbering (1.1, 1.2)
- Keep tasks small — completable in one session
- Tasks describe work, not verification

### Step 7: Update INDEX.md
Add the change folder to `docs/changes/INDEX.md`.

### Step 8: Report
Present the proposal structure to the user. Wait for approval before implementation.

---

## When to Use Propose vs Curate

| Situation | Use |
|-----------|-----|
| Adding one behavioral requirement to existing spec | **Curate** |
| Creating a new standalone doc | **Curate** |
| A feature that touches multiple specs + architecture | **Propose** |
| A refactor with behavioral changes | **Propose** |
| A new component that needs spec, design, and tasks | **Propose** |

---

## Reference Files

Always load:
- `../spec-format.md` — for writing behavior deltas in correct format
- `../ontology.md` — for frontmatter on change artifacts
- `../folder-structure.md` — for change folder layout

Load as needed:
- `../principles.md` — for layer boundaries and conflict rules
