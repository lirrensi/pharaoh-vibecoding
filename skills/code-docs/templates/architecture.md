---
node_type: architecture
title: {System/Component Name} Architecture
status: active
updated: YYYY-MM-DD
tags: []
links:
  depends_on: []
  documents: []
---

# {System/Component Name} Architecture

## Overview
{What this component/system is and why it exists in the architecture}

## Scope Boundary
**Owns:** {what this component is responsible for}
**Does not own:** {what it explicitly does NOT handle}
**Boundary interfaces:** {how it connects to other components}

## Components
| Component | Responsibility | Key Files |
|-----------|---------------|-----------|
| name | what it does | `src/path/` |

## Data Models / Storage
| Entity | Storage | Schema Location | Notes |
|--------|---------|----------------|-------|
| entity_name | PostgreSQL, Redis, etc. | `src/path/schema.ts` | description |

## Relationships and Flow
{How data and control move through the system. Use ASCII diagrams.}

```
Client → Gateway → Service → DB
                ↓
              Cache
```

## Dependencies
| Dependency | Version | Purpose | Integration Level |
|-----------|---------|---------|------------------|
| dep_name | version | why we use it | stable/upstream/external/unstable |

## Contracts / Invariants
| Invariant | Description | Implementation Status |
|-----------|------------|----------------------|
| invariant_name | what must hold | implemented / partial / discarded |

## Configuration / Operations
| Config | Default | Environment | Notes |
|--------|---------|------------|-------|
| KEY_NAME | value | all/prod/dev | description |

## Design Decisions
| Decision | Rationale | Confidence | Status |
|----------|----------|-----------|--------|
| what we chose | why we chose it | high/medium/low | implemented / partial / discarded |
