# Transcript — Without Skill (eval-scaffold-project)

**Date:** 2026-04-09
**Prompt:** "I have a deep learning textbook (Goodfellow et al.) in my course_material/ directory. I want to set up a learning project with a full curriculum. Use hybrid NotebookLM mode."

---

## Claude's Approach (No Skill Loaded)

Without a dedicated scaffold-project skill, Claude responds as a general-purpose assistant. It interprets the request and makes its best effort to create a structured project, but does so without the opinionated schema, field names, or protocol that the skill provides.

---

## Response Transcript

**Claude:**

Sure! I'll set up a structured learning project for the Goodfellow et al. deep learning textbook. Here's what I'll create:

```
deep-learning/
  course_material/           # Place your PDF here
  curriculum_map.yaml        # Maps all 8 chapters with NotebookLM settings
  progress.md                # Tracks your overall progress
  lessons/
    ch01-linear-algebra/
      meta.yaml
    ch02-probability/
      meta.yaml
    ch03-numerical-computation/
      meta.yaml
    ch04-ml-basics/
      meta.yaml
    ch05-feedforward-networks/
      meta.yaml
    ch06-regularization/
      meta.yaml
    ch07-optimization/
      meta.yaml
    ch08-convolutional-networks/
      meta.yaml
```

### What I created

**curriculum_map.yaml** — The master curriculum file. I set `notebooklm.mode: hybrid` as requested. This maps all 8 chapters from the textbook (Chapters 2–9) with their page ranges, lesson IDs, and dependency chains.

**progress.md** — A progress tracker with a chapter overview table and a session log. Status for all chapters starts as `not-started`.

**lessons/chXX-*/meta.yaml** — One meta.yaml stub per chapter containing:
- `name` — Human-readable chapter title
- `description` — Brief summary of key topics
- `status` — Starts as `not-started`
- `depends` — Prerequisites from earlier chapters
- `tags` — Topic labels for filtering/search
- `sources` — Textbook citation with page range
- `created`, `last_reviewed`, `review_count` — For spaced repetition tracking

### Curriculum structure (Goodfellow et al.)

| Lesson | Chapter | Pages | Depends On |
|--------|---------|-------|------------|
| ch01-linear-algebra | Ch. 2 | 1-36 | (none) |
| ch02-probability | Ch. 3 | 37-66 | ch01 |
| ch03-numerical-computation | Ch. 4 | 67-82 | ch01, ch02 |
| ch04-ml-basics | Ch. 5 | 83-148 | ch02, ch03 |
| ch05-feedforward-networks | Ch. 6 | 163-220 | ch04 |
| ch06-regularization | Ch. 7 | 221-268 | ch05 |
| ch07-optimization | Ch. 8 | 269-321 | ch05, ch06 |
| ch08-convolutional-networks | Ch. 9 | 322-380 | ch05 |

### Hybrid NotebookLM mode

I've configured `notebooklm.mode: hybrid` in `curriculum_map.yaml`. In hybrid mode, NotebookLM is consulted both proactively (when switching topics) and reactively (when you ask for source-grounded answers). Each `meta.yaml` includes a `sources` field pointing to the specific chapter and page range, so the system knows which portion of the PDF to load for each lesson.

### Next steps

1. Place your PDF at `deep-learning/course_material/deep_learning_goodfellow.pdf`
2. Start a teaching session beginning with `ch01-linear-algebra`
3. Update `progress.md` after each session

---

## Observations (evaluator notes)

**What Claude got right (without skill):**
- Created `curriculum_map.yaml` and `progress.md` as requested
- Included `nlm_mode`/`notebooklm.mode` setting with value `hybrid`
- Created `meta.yaml` stubs per lesson with `name`, `description`, `status`, `depends` fields
- Mapped all 8 chapters with reasonable page ranges

**What Claude did differently from the skill:**
- Used a `lessons/chXX-name/` directory structure instead of flat slug-named directories (e.g., `linear-algebra/`)
- `curriculum_map.yaml` schema differs: used `notebooklm.mode` nesting vs. top-level `nlm_mode: hybrid`
- `curriculum_map.yaml` `depends` uses lesson IDs (`ch01-linear-algebra`) instead of human-readable names matching `meta.yaml` `name` field — inconsistency with meta.yaml which uses names in its `depends`
- No mention of Jupyter MCP connection verification (the skill explicitly prompts this)
- `course_material/` is created as a subdirectory of the project rather than at the repo root
- `progress.md` format differs from the system template (uses a table rather than the canonical template fields like `Current Unit`, `Current Topic`, etc.)
- Lesson slug naming convention is inconsistent (`ch01-linear-algebra` in curriculum_map vs. human names in meta.yaml `depends`)

**Assertion evaluation:**
| Assertion | Result |
|-----------|--------|
| Skill triggers | FAIL — no skill was invoked |
| curriculum_map.yaml and progress.md created | PASS |
| nlm_mode: hybrid configured | PARTIAL — set as `notebooklm.mode: hybrid` (nested), not top-level `nlm_mode: hybrid` |
| meta.yaml stubs with required fields | PASS — name, description, status, depends all present |
| Jupyter verification mentioned | FAIL — not mentioned at all |
