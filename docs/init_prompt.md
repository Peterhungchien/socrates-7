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
7. **Jupyter blackboard:** Do I want to use a live Jupyter notebook as a blackboard for formulas, code demos, and exercises? (Explain briefly what this provides.) If yes, ask for blackboard style preference: minimal (key formulas only), moderate (formulas + diagrams), or rich (code + plots + annotations).
8. **NotebookLM:** Do I want to use NotebookLM for full-corpus search across my textbooks? (Explain briefly what this provides.)

After I've answered all questions, do the following:

1. Update `teacher/system.md` — replace all `[PLACEHOLDER]` values with my answers. Set `JUPYTER_ENABLED` and `NLM_MODE` based on my choices.
2. Populate `teacher/learner_profile.md` with my background, knowledge level, goals, and preferences.
3. Create `teacher/persona_[name].md` — a full persona file with all required fields (see the example in `examples/persona_example.md` for the format).
4. Update `teacher/progress.md` — fill in the subject, list the source textbooks, and build a curriculum outline by scanning `course_material/`.
5. Update `teacher/knowledge_gaps.md` — replace `[LEARNER_NAME]` with my name.
6. If Jupyter is enabled: verify the kernel is running with `list_kernels`, create a test notebook, and confirm it works.
7. If NLM is enabled: guide me through the setup checklist in `teacher/notebooklm.md`.

Once everything is set up, run a short 5-minute demo session to show me how it works — greet me in persona, ask a Socratic question about my subject, and demonstrate the blackboard if enabled. Then end the demo cleanly.
