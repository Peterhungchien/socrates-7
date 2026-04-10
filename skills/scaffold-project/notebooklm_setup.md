# NotebookLM Integration

*NotebookLM integration is a core component of Socrates-7. This file tracks the NLM notebook configuration and source manifest.*

---

## Notebook

| Field | Value |
|---|---|
| **Notebook Title** | |
| **Notebook ID** | |
| **NLM Mode** | passive |
| **Created** | |

---

## Source Manifest

| Source ID | Filename | Type | Status |
|---|---|---|---|

---

## Artifacts Generated

| Artifact ID | Type | Chapter | Date | File Path |
|---|---|---|---|---|

---

## Setup Checklist

- [ ] Install: `uv tool install notebooklm-mcp-cli`
- [ ] Run: `nlm setup add claude-desktop`
- [ ] Run: `nlm login`
- [ ] Create notebook: use `notebook_create` in Claude Desktop
- [ ] Upload sources: use `source_add` for each file in `course_material/`
- [ ] Copy notebook ID into `curriculum_map.yaml` → `notebook_id` field
- [ ] Set `nlm_mode: passive`, `active`, or `hybrid` in `curriculum_map.yaml`

---

## Usage Requirements

The teacher MUST call `notebook_query` via the `notebooklm-mcp` server:
- At **session start** — to retrieve key concepts for the current section
- At each **topic transition** — before introducing new section content
- For **cross-chapter lookups** and **formula verification** as needed

See the teaching-session skill's `session-protocol.md` for full NLM mode rules. If queries fail,
the teacher must surface errors explicitly — never silently fall back to parametric knowledge.
