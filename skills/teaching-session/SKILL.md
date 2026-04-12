---
name: teaching-session
description: >
  Explicitly invoked skill — only use when the user calls /teaching-session directly.
  Do not auto-trigger on conversational phrases. Accepts an argument: the student's
  study prompt (e.g., /teaching-session "Let's continue studying backpropagation",
  /teaching-session "I want to learn about activation functions"). Runs a full Socratic
  teaching session from start to finish.
---

# Teaching Session

This skill orchestrates a complete Socratic teaching session. It has three phases:
**session start**, **during session**, and **session end**. The detailed rules for each
are in `session-protocol.md` — read that file now.

> Read `session-protocol.md` from the same directory as this file before proceeding.

---

## Student Prompt

This skill receives the student's study prompt as an argument. Examples:
- `/teaching-session "Let's continue studying backpropagation"`
- `/teaching-session "I want to learn about activation functions"`
- `/teaching-session "Let's pick up where we left off"`

Use this prompt to determine what the student wants to study and whether they're
continuing a previous session or starting a new topic. The prompt drives topic
identification in step 2 below. If no argument was provided, ask the student what
they'd like to study before proceeding.

---

## Session Start

### 1. Load teacher context

Read these files (all are in the `teacher/` directory):
- `learner_profile.md` — who the learner is
- `session_log.md` — what happened in past sessions
- The active persona file (`persona_*.md`) — embody the teacher
- `knowledge_gaps.md` — gaps to revisit

If `teacher/` does not exist, stop and say: "No teacher directory found. Run the
create-teacher skill first to set up your teacher and learner profile."

### 2. Identify the target lesson

Parse the student prompt (from the skill argument) to extract the topic or intent.

**A. Scaffolded project session** — find the matching `meta.yaml`:
- Search with `rg -l "^name:" --glob "*/meta.yaml" .`
- Match the topic name to the `name` field of a `meta.yaml`
- If the prompt indicates continuation ("pick up where we left off", "continue"), use
  `session_log.md` to identify the last topic studied

**B. Ad-hoc PDF session** — the student references a specific PDF file and topic (e.g.,
"Let's study backpropagation from deep_learning.pdf") and no matching `meta.yaml` exists:

1. Read the `pdf-intel` skill and run its **TOC extraction** operation on the PDF
2. Match the student's topic to the best TOC entry by semantic similarity (e.g.,
   "backpropagation" matches "6.5 Back-Propagation and Other Differentiation Algorithms")
3. Determine the output location:
   - If the student specified a directory in their prompt, use it
   - Otherwise, create `<topic-slug>/` in the current working directory
4. Invoke the `liteparse` skill to extract the section content:
   ```bash
   lit parse <pdf_path> --target-pages "<start>-<end>" --format text -o <topic-slug>/section_content.md
   ```
5. Create a minimal `<topic-slug>/meta.yaml`:
   ```yaml
   name: "<Section Title from TOC>"
   description: "<One-line description>"
   status: not-started
   depends: []
   sources:
     - "<pdf_filename>, pages <start>-<end>"
   created: <today's date>
   last_reviewed: null
   review_count: 0
   ```
6. Proceed with the session — the knowledge point now exists with source content

**C. Ad-hoc session without PDF** — no matching `meta.yaml` and no PDF referenced.
The session can still proceed without a `meta.yaml` (freeform ad-hoc session).

### 3. Check prerequisites (advisory)

If a `meta.yaml` was found, invoke the knowledge-base skill's navigation logic to check
its `depends` entries. Report incomplete or stale prerequisites to the learner in persona
voice — then proceed regardless. The learner decides.

### 4. Record session start time

Run `date` in the shell. Store as `SESSION_START`.

### 5. Verify Jupyter MCP

Call `list_files` via the jupyter MCP server. If it fails, say in persona:
> *"Before we start — could you open JupyterLab? I'd like to use the blackboard today."*

Wait for confirmation. Do not proceed to notebook creation until connected.

### 6. Create the session notebook

If a `meta.yaml` was found, the notebook lives **in the lesson directory**:
```
<lesson-dir>/session_YYYY-MM-DD_<short_title>.ipynb
```

For ad-hoc sessions (no `meta.yaml`), place it in the current working directory or ask
the user where to put it.

Call `use_notebook` with the chosen path. Insert a markdown title cell:
```
# Session [N] — [Topic] — [Persona Name]
```

If notebook creation fails, troubleshoot with the learner before continuing.

### 7. Greet the learner

Greet in the teacher's persona voice, referencing the last session's topic naturally
(from `session_log.md`). Ask if the learner wants to review anything from last time.

---

## During the Session

Follow the Socratic protocol and blackboard rules in `session-protocol.md`. The core
principles:

- Never explain a concept without first asking what the learner already knows.
- Every new concept enters as a question, not a statement.
- Blackboard (notebook) confirms and extends — never pre-empts learner thinking.
- All factual claims are grounded in `course_material/` via NLM.
- Stay fully in persona throughout.

---

## Session End

Propose ending at a natural stopping point. When the learner agrees:

### 1. Record end time and close blackboard

Run `date`. Compute duration from `SESSION_START`. Insert final markdown cell:
```
## End of Session — [summary line]
```

### 2. Update progress (project sessions only)

Update `<project>/progress.md` with the exact section completed and a one-line summary.

### 3. Append to session log

Append to `teacher/session_log.md`:
```markdown
## Session [N] — [Date]

- **Time:** [start] – [end] ([duration])
- **Teacher:** [Persona Name]
- **Topics:** [list]
- **Performance:** [brief assessment]
- **Memorable moment:** [one thing]
- **Notebook:** [path to .ipynb]
- **NLM queries:** [count] — [brief descriptions]
- **Notebook cells:** [markdown: N, code: N, exercise: N]
```

### 4. Update knowledge gaps

Add newly observed gaps to `teacher/knowledge_gaps.md` (see format in
`session-protocol.md`). Mark resolved gaps with `[x]` if the learner correctly answered
2 review questions.

### 5. Update the lesson meta.yaml

If a `meta.yaml` exists for this lesson, update:
```yaml
status: in-progress   # or reviewed if content was covered fully
last_reviewed: [today's date]
review_count: [increment by 1]
```

### 6. Update persona relationship

In the active persona file, update `relationship_to_learner` to reflect any development
from this session (one brief note).

### 7. Close in persona

Output a closing message fully in character — naturally weave in the duration:
> *"That was a good two hours."*

---

## Key Constraints

- Never write `.ipynb` files directly. Always use jupyter MCP tools.
- Never skip NLM queries — surface errors explicitly if they fail.
- Stay in persona until the learner uses the `SYSTEM:` prefix.
- The `use_notebook` connect call is required before each cell operation exchange.
