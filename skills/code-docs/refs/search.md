# How to Search Documentation

The documentation is a **graph**, not a flat pile. You find things by walking the graph — starting at INDEX.md nodes, following links to leaves, using tags as signposts.

---

## The Graph-Walking Method

This is the primary, intended way to find anything:

### Step 1: Start at the root
Read `docs/INDEX.md`. It tells you what each top-level folder contains.

### Step 2: Drill into the relevant folder INDEX.md
Each folder's INDEX.md lists every document and subfolder with one-line summaries. Read the summaries — don't open files yet.

### Step 3: Follow links to leaves
When you find a promising document, open it. Check its frontmatter `links:` — `depends_on` tells you what to read first for context. `documents` tells you what code it describes.

### Step 4: Walk sideways via tags
If you need related docs in other folders, check the tags section of the INDEX.md. Tags are cross-cutting — `auth` might appear in `spec/`, `architecture/`, and `guides/`.

### Step 5: Navigate up via `part_of`
If a document feels too narrow, check if it has `links: part_of` pointing to a parent index or overview doc.

```
INDEX.md (map)
  └─ summary: "Authentication — login, sessions, 2FA [auth, security]"
       └─ open file
            └─ links.depends_on: [/overview/product.md]
            └─ links.documents: [/src/auth/]
            └─ body links: "See [Session Management](sessions.md)"
```

---

## Tag-Based Search

Tags are the fastest cross-cutting search. Every document declares tags in frontmatter:

```yaml
tags: [auth, security, api, sessions]
```

### Finding by tag from INDEX.md
Every INDEX.md has a tags section at the bottom. Scan it to find which documents share a tag:
```
## Tags
`auth` `security` `api` `sessions` `rate-limiting`
```
If you see the tag you want, the documents above tagged with it are your targets.

### Finding by tag via ripgrep
```bash
# Find all docs with a specific tag
rg "^tags:.*auth" docs/ --no-ignore

# Find docs with multiple tags (AND)
rg "^tags:.*auth.*api|^tags:.*api.*auth" docs/ --no-ignore
```

---

## Full-Text Search (when graph-walking isn't enough)

When you need to find something by keyword across ALL docs:

### Search frontmatter (titles, summaries)
```bash
# All document titles
rg "^title:" docs/ --no-ignore

# Titles containing a keyword
rg "^title:.*auth" docs/ --no-ignore -i
```

### Search body text
```bash
# Search all docs for a keyword
rg "session timeout" docs/ --no-ignore -i

# Search only spec files
rg "MUST" docs/spec/ --no-ignore

# Search only architecture files
rg "component" docs/architecture/ --no-ignore
```

### Search by node_type
```bash
# All specs
rg "^node_type: spec$" docs/ --no-ignore

# All ADRs
rg "^node_type: adr$" docs/ --no-ignore

# All active docs
rg "^status: active$" docs/ --no-ignore
```

---

## When to Use Each Method

| Method | Best for | When |
|--------|---------|------|
| **INDEX.md graph-walking** | Finding where something lives, exploring structure | Always start here. Read INDEX.md before opening files. |
| **Tag scanning** | Cross-cutting topics that span multiple folders | When you need everything about "auth" or "security" |
| **Frontmatter search** | Finding docs by type, status, or title | When you know the doc type but not the exact file |
| **Full-text ripgrep** | Finding a specific term or phrase across all docs | Last resort — when graph-walking didn't find it |

---

## The Golden Rule

**Read INDEX.md before opening individual files.** The index is the map. It tells you what exists, where it is, and what it's about — all without opening a single document. Treat opening a file without checking its INDEX.md first as a navigation failure.
