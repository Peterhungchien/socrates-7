---
name: knowledge-base
description: >
  Use when the user asks about prerequisites, what to study next, what depends on a
  topic, or wants to query their learning status across knowledge points. Trigger on:
  "what should I study next?", "what are the prerequisites for X?", "what depends on X?",
  "show me stale topics", "am I ready to study X?", "show me the knowledge graph for X",
  "what's my progress?". Also invoked by the teaching-session skill before each session
  to check prerequisite status. Use this skill any time the user is thinking about
  navigation, readiness, or learning order — even if they don't say "knowledge base".
---

# Knowledge Base

Knowledge points are directories containing a `meta.yaml` file. They can live anywhere
in the workspace — inside a project, as standalone ad-hoc directories, or nested. There
is no fixed `knowledge/` directory. Discovery is always by search.

## Discovery

Find all knowledge points by searching the workspace:

```bash
rg --glob '*/meta.yaml' -l .
```

Or equivalently, use `Glob` with pattern `**/meta.yaml`. Each result is a knowledge
point; its directory is the point's home.

Read the `meta.yaml` to understand it.

## Schema

**Required fields:**

| Field | Type | Values |
|-------|------|--------|
| `name` | string | Human-readable name (used to resolve `depends`) |
| `description` | string | One-line summary |
| `status` | enum | `not-started` \| `in-progress` \| `reviewed` \| `mastered` |
| `depends` | list of strings | `name` values of prerequisites |

**Optional fields:** `tags`, `sources`, `created`, `last_reviewed`, `review_count`,
`notes`. Read all fields for context but only reason about the required four for
navigation logic.

**Dependency resolution:** `depends` entries match by `name`, not by path or slug.
To find a dependency, scan all `meta.yaml` files for `name: "..."`. If no file matches,
the dependency is dangling — note it and continue.

---

## Navigation Behaviors

### Before studying a topic

When the user wants to study a specific topic, or the teaching-session skill asks you to
check prerequisites:

1. Find the topic's `meta.yaml` (search by `name` field or by path if the user named a
   directory).
2. For each entry in `depends`, find its `meta.yaml` via name-based search.
3. Classify each dependency:
   - **Ready:** status is `reviewed` or `mastered`, and `last_reviewed` (if present) is
     within threshold (30 days for `reviewed`, 90 days for `mastered`).
   - **Stale:** status is `reviewed`/`mastered` but `last_reviewed` exceeds threshold.
   - **Incomplete:** status is `not-started` or `in-progress`.
   - **Dangling:** no `meta.yaml` found matching that name.
4. Report to the user: list each dep with status and recommendation.
5. This is **advisory only** — never block the user from proceeding.

### "What should I study next?"

Scan all `meta.yaml` files. Return topics where:
- Topic's own status is `not-started`
- All entries in `depends` have status `reviewed` or `mastered`

Sort by number of unlocked dependents (topics that will become ready after completing
this one) — highest unlock value first.

### "What depends on X?"

Scan all `meta.yaml` files. Return topics where `depends` includes the name matching X.
This answers: "if I learn X, what does it unlock?"

### "Show me stale topics"

Scan all `meta.yaml` files. Return topics where `last_reviewed` is set and:
- Status is `reviewed` and `last_reviewed` > 30 days ago
- Status is `mastered` and `last_reviewed` > 90 days ago

### "Show me the graph for X"

List:
- X itself (name, status, description)
- Its dependencies, each with status
- Topics that depend on X (reverse lookup), each with status

One level deep by default. Go deeper if the user asks.

### "Show me my progress" / status summary

Scan all `meta.yaml` files. Count by status. Group by project (by directory prefix if
discernible). Present as a brief table.

---

## Rules

1. **Read-only.** The teaching-session skill handles status updates. Never write or
   modify `meta.yaml` files here.
2. **Advisory, not blocking.** Always present findings and let the user decide.
3. **Graceful with missing data.** Dangling `depends` references → note and skip.
   Missing optional fields → skip related logic (no `last_reviewed` = no staleness check).
4. **No teaching methodology.** Present findings neutrally. Don't assume Socratic method,
   flashcards, or any pedagogy.
5. **Discovery is always live.** Never cache or assume a fixed list of knowledge points.
   Always search at runtime.
