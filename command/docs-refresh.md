---
description: Full doc maintenance — tidy, re-index, sync against code, make docs perfect
---
Load the `code-docs` skill. Run a complete maintenance pass over all canonical docs.
Goal: Full doc maintenance — tidy, re-index, sync against code, make docs perfect

Do whatever is needed to get the docs into perfect shape:
- Tidy structure, links, frontmatter, and ontology
- Re-index and regenerate INDEX.md files
- Sync docs against current code where code has drifted ahead
- Update docs for a new version or changed behavior
- Remove duplicates, mark stale/deprecated docs, and clean up cruft
- Fix any other doc health issues found

Read all docs, scan the relevant code, then apply all fixes directly to docs. Do not edit code.
> Must always reindex after done.

Focus (if specified): $ARGUMENTS
