# Socrates-7 Initialization Prompt

Paste everything below this line into Claude Desktop to start the guided setup.

---

I want to set up Socrates-7 in this project. Please read `teacher/system.md` and `teacher/system_detail.md` to understand the system architecture, then interview me to create all the required files. Ask me the following questions one at a time — wait for my answer before moving on:

1. **Subject:** What subject am I studying?
2. **Course material:** Please scan `course_material/` and list what you find. If it's empty, ask me what material I plan to add.
3. **Background:** What is my name, academic/professional background, and current knowledge level in this subject?
4. **Learning goals:** What do I want to achieve? What specific skills or understanding am I after?
5. **Learning preferences:** Do I prefer direct or gentle feedback? Any other preferences for how I like to learn?
6. **Teacher persona:** Help me design a teacher. Ask me for:
   - A name and brief description
   - Personality style: strict/efficient, warm/patient, playful/energetic, or serious/academic
   - Relationship context: mentor, TA, study partner, or something else
   - Any specific teaching quirks or traits I want
7. **Jupyter blackboard style:** The Jupyter blackboard is a core part of Socrates-7 — the teacher writes formulas, runs code demos, and sets exercises in a live notebook you watch in your browser. What blackboard style do you prefer: minimal (key formulas only), moderate (formulas + diagrams), or rich (code + plots + annotations)? Also confirm that JupyterLab is installed and running.
8. **NotebookLM mode:** NotebookLM provides full-corpus knowledge retrieval from your textbooks and is a core part of Socrates-7 — it ensures the teacher stays grounded in your actual course material. Which mode do you prefer?
   - **Passive:** NLM called for cross-chapter lookups and verification (~3–5 queries/session). Chapter files loaded into context.
   - **Active:** NLM used as the primary source for all factual content. No chapter files loaded into context.
   - **Hybrid (recommended for 2–3 textbooks):** Pre-split section PDFs are loaded into context for each topic (preserving the author's exact words, reasoning flow, and diagrams). NLM handles cross-chapter and cross-textbook retrieval. Requires a one-time PDF split — I'll help you set that up.
   If you choose hybrid mode, I'll also help you fill in `teacher/curriculum_map.yaml` with your textbook sections and page ranges, then run the split script.

After I've answered all questions, do the following:

1. Update `teacher/system.md` — replace all `[PLACEHOLDER]` values with my answers. Set `NLM_MODE` to my chosen mode (passive, active, or hybrid). Jupyter is always enabled — no toggle needed.
2. Populate `teacher/learner_profile.md` with my background, knowledge level, goals, and preferences.
3. Create `teacher/persona_[name].md` — a full persona file with all required fields (see the example in `examples/persona_example.md` for the format).
4. Update `teacher/progress.md` — fill in the subject, list the source textbooks, and build a curriculum outline by scanning `course_material/`. Let me know that this outline is a starting point — I can reorder, skip, or revisit sections at any time by just asking during a session.
5. Update `teacher/knowledge_gaps.md` — replace `[LEARNER_NAME]` with my name.
6. Verify the jupyter MCP server: call `list_files`, create a test notebook with `use_notebook`, insert and execute a test cell, and confirm it works.
7. Guide me through the NotebookLM setup checklist in `teacher/notebooklm.md` — create a notebook, upload sources, and verify a test query works.
8. If hybrid mode was chosen: help me populate `teacher/curriculum_map.yaml` using NLM-assisted generation:
   - Ask me which textbook in `course_material/` is my primary one.
   - Call `notebook_query` with: `'List all chapters and sections of [textbook title] with their page ranges. Format as: Unit number, Topic name, Start page - End page.'`
   - Parse the NLM response and auto-populate the table in `teacher/curriculum_map.yaml`.
   - Present the generated map to me: "Here's the section structure I found. Please review and correct any page numbers that look off."
   - After I confirm or correct, run `python tools/split_pdf.py` to generate the section PDFs in `course_material/sections/`.

Once everything is set up, run a short 5-minute demo session to show me how it works — greet me in persona, ask a Socratic question about my subject, demonstrate the blackboard by writing a formula or running a code cell, and run at least one NLM query to show the grounding workflow. Then end the demo cleanly.
