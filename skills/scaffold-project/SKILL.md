---
name: scaffold-project
description: >
  Use when the user wants to create a new learning project from a textbook or course
  material, set up curriculum structure, configure NotebookLM, or organize lesson
  directories. Trigger on: "set up a project for [textbook]", "scaffold my learning
  project", "I want to study [course] systematically", "help me structure my curriculum",
  "split my PDF into sections". This skill should be used after create-teacher and before
  the first teaching session when the user has course material to organize.
---

# Scaffold Project

This skill creates a structured learning project directory from course material — a
textbook, PDF, or set of readings. It generates the project skeleton, configures
NotebookLM integration, and creates a `meta.yaml` stub for each lesson or chapter so
the knowledge-base skill can navigate them.

---

## Step 1 — Project name and location

Ask the user:
> "What should we call this project? (e.g., 'deep-learning', 'stats-101'). This will be
> the directory name — use lowercase with hyphens."

Then ask:
> "Where should the project live? Provide the full path, or I'll create it in your
> current working directory."

Create the project directory with this structure:
```
<project-name>/
  course_material/
  progress.md
  curriculum_map.yaml
```

### `progress.md` starter:
```markdown
# Progress — [Project Name]

**Subject:** [from user]
**Started:** [today's date]

## Curriculum

*Updated at each session end by the teacher.*

---
```

### `curriculum_map.yaml` starter:
```yaml
# Curriculum Map — [Project Name]
# Each entry maps a lesson slug to its source material location.
# Format: slug: {name, source_file, pages}
#
# Example:
# multi-layer-networks:
#   name: "Multi-Layer Networks"
#   source_file: "deep_learning.pdf"
#   pages: "163-190"

lessons: []
```

---

## Step 2 — Course material

Ask:
> "Do you have course material to add? You can drop textbook PDFs into
> `<project>/course_material/`. I'll scan it once you're ready."

Scan `course_material/` and list what's there. If empty, note it and continue.

---

## Step 3 — NotebookLM mode

Ask:
> "Which NotebookLM mode do you want?
> - **Passive:** NLM called for cross-chapter lookups and verification (~3–5 queries/session).
> - **Active:** NLM is the primary source for all factual content.
> - **Hybrid (recommended for 2–3 textbooks):** Section PDFs loaded for each topic;
>   NLM handles cross-chapter retrieval. Requires a one-time PDF split."

Record the chosen mode in `curriculum_map.yaml` as a top-level field:
```yaml
nlm_mode: hybrid  # passive | active | hybrid
```

### If hybrid mode:
Walk the user through `teacher/notebooklm.md` setup checklist:
1. `uv tool install notebooklm-mcp-cli`
2. `nlm setup add claude-desktop`
3. `nlm login`
4. Call `notebook_create` to create a NLM notebook
5. Call `source_add` for each file in `course_material/`
6. Note the notebook ID for use during sessions

Then offer to auto-populate `curriculum_map.yaml` via NLM:
> "I can query NotebookLM to extract the chapter/section structure from your textbook.
> Want me to do that now?"

If yes: call `notebook_query` with:
`"List all chapters and sections of [textbook title] with page ranges. Format as:
Chapter number, Section name, Start page - End page."`

Parse the response, populate `curriculum_map.yaml` lessons list, and present it for
review:
> "Here's the structure I found. Review and correct any page numbers that look off."

After confirmation, run the PDF split:
```bash
python tools/split_pdf.py
```

---

## Step 4 — Generate lesson meta.yaml stubs

For each lesson in the curriculum (from `curriculum_map.yaml`, or from user-provided
chapter list if NLM wasn't used):

1. Create a subdirectory: `<project>/<lesson-slug>/`
2. Write `<project>/<lesson-slug>/meta.yaml` with:

```yaml
name: "[Human-readable lesson name]"
description: "[One-line description of the concept or topic]"
status: not-started
depends: []
tags: []
sources:
  - "[source_file], [pages]"
created: [today's date]
last_reviewed: null
review_count: 0
```

Set `depends` entries to the `name` values of prerequisite lessons (not slugs). For
linear textbooks, each lesson depends on the previous one. For topic graphs, ask the
user or leave empty for them to fill in.

---

## Step 5 — Verify Jupyter MCP

Call `list_files` via the jupyter MCP server. If it succeeds, confirm:
> "Jupyter MCP is connected."

If it fails:
> "Jupyter MCP isn't reachable. Make sure JupyterLab is running and the MCP server is
> configured in your Claude Desktop settings before starting a session."

---

## Completion summary

> "Project '[name]' is scaffolded. Here's what was created:
> - `course_material/` — add your PDFs here
> - `progress.md` — tracks session progress
> - `curriculum_map.yaml` — NLM mode: [mode]
> - [N] lesson directories, each with a `meta.yaml` stub
>
> Next step: say 'let's study [first lesson]' to begin your first session."
