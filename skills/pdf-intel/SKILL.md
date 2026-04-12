---
name: pdf-intel
description: >
  Internal capability skill — not user-invocable. Provides PDF intelligence
  operations (TOC extraction, PDF splitting, content extraction) used by
  scaffold-project and teaching-session. Do not invoke directly from user
  prompts.
---

# PDF Intelligence

This skill provides shared PDF processing capabilities for other skills. It is
not meant to be invoked directly by users — it is called by scaffold-project and
teaching-session when they need PDF operations.

---

## Operation 1 — Extract TOC

Extract the embedded table of contents (bookmarks/outlines) from a PDF.

```bash
python ${CLAUDE_SKILL_DIR}/scripts/extract_toc.py <pdf_path>
```

**Output (YAML to stdout):**
```yaml
toc:
  - level: 1
    title: "Chapter 1: Introduction"
    page: 1
  - level: 2
    title: "1.1 Motivation"
    page: 3
quality:
  entry_count: 42
  page_count: 500
  coverage_ratio: 0.95
  max_gap: 15
```

**Exit codes:**
- `0` — TOC found, YAML output on stdout
- `1` — no embedded TOC in this PDF
- `2` — usage error (missing argument, file not found)

### Interpreting quality metrics

| Metric | Good | Suspect |
|--------|------|---------|
| `coverage_ratio` | > 0.5 | < 0.5 (TOC doesn't cover most of the book) |
| `max_gap` | < 100 pages | > 100 pages (large unindexed sections) |
| `entry_count` relative to `page_count` | reasonable | < 5 entries for a 500-page book |

**If quality is good:** Use the TOC directly. Examine the hierarchy levels and
select the appropriate granularity for lessons — chapter-level (level 1) for
broad surveys, section-level (level 2-3) for deep dives.

**If quality is suspect:** Present the TOC to the user and ask whether to use it
or fall back to NotebookLM.

**If no TOC (exit code 1):** Fall back to NotebookLM query or manual entry.

### Matching a topic to a TOC entry

When a user asks to study a specific topic (e.g., "backpropagation"), match it
against TOC entry titles. Use semantic similarity, not exact string matching —
"backpropagation" should match "6.5 Back-Propagation and Other Differentiation
Algorithms". If multiple entries match, prefer the one with the most specific
(highest level number) match.

---

## Operation 2 — Split PDF by curriculum map

Split a textbook PDF into section-level files based on page ranges in the
curriculum map.

```bash
python ${CLAUDE_SKILL_DIR}/scripts/split_pdf.py [--map MAP_FILE] [--output-dir OUTPUT_DIR]
```

**Defaults:**
- `--map`: `teacher/curriculum_map.yaml`
- `--output-dir`: `course_material/sections`

**Requires:** `curriculum_map.yaml` with populated `sections` list including
`textbook`, `start_page`, `end_page`, `unit`, and `topic` fields.

The script:
1. Reads `curriculum_map.yaml`
2. Opens each referenced PDF from `course_material/`
3. Extracts page ranges using PyMuPDF
4. Writes section PDFs to the output directory
5. Updates `curriculum_map.yaml` with `section_pdf` filenames

---

## Operation 3 — Extract section content

For extracting readable text from specific pages of a PDF, invoke the
**liteparse** skill. This is not a script in this skill — it uses the
externally installed `lit` CLI.

```bash
lit parse <pdf_path> --target-pages "<start>-<end>" --format text -o <output_path>
```

**Prerequisites:**
- `@llamaindex/liteparse` installed globally: `npm i -g @llamaindex/liteparse`
- The `lit` CLI available in the terminal

**Typical usage pattern (ad-hoc sessions):**
1. Run TOC extraction (Operation 1) to find the page range
2. Run `lit parse` to extract content to a file in the knowledge point directory
3. The teaching session reads from that file

**Typical usage pattern (boundary verification):**
1. After splitting PDFs (Operation 2), run `lit parse` on section boundaries
2. Verify the first/last pages contain expected content
3. Adjust page ranges if boundaries are off

---

## Fallback chain

When determining curriculum structure from a PDF:

```
1. PyMuPDF TOC extraction  (fast, no external dependency)
       ↓ if no TOC or suspect quality
2. NotebookLM query        (requires NLM setup, slower)
       ↓ if NLM unavailable
3. Manual entry            (user provides structure)
```

---

## Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| `pymupdf` | TOC extraction, PDF splitting | `pip install pymupdf` |
| `pyyaml` | Curriculum map YAML parsing | `pip install pyyaml` |
| `@llamaindex/liteparse` | Content extraction (Operation 3) | `npm i -g @llamaindex/liteparse` |
