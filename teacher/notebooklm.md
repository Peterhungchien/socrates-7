# NotebookLM Integration

*This file is OPTIONAL. Delete it if you are not using NotebookLM.*

---

## Notebook

| Field | Value |
|---|---|
| **Notebook Title** | |
| **Notebook ID** | |
| **NLM Mode** | off |
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
- [ ] Copy notebook ID to `teacher/system.md` → `NOTEBOOKLM_NOTEBOOK_ID`
- [ ] Set `NLM_MODE: passive` or `active` in `teacher/system.md`
