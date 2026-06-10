---
description: Reindex docs against code, flag direction of discrepancies, and fix
---
Run Thoth to reindex/sync documentation against the current codebase. Read all canonical docs (product.md, spec.md, arch*.md), then scan the actual code for every discrepancy. For each mismatch, flag which direction the error went — was the doc outdated, or did the code drift from spec? Then fix it. Report what changed and why.
Supposed fresher version: $ARGUMENTS