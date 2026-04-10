# Scaffold Project — Session Transcript

**Skill:** scaffold-project  
**Date:** 2026-04-09  
**User request:** "I have a deep learning textbook (Goodfellow et al.) in my course_material/ directory. I want to set up a learning project with a full curriculum. Use hybrid NotebookLM mode."

---

## Step 1 — Project name and location

**Skill asks:**
> "What should we call this project? (e.g., 'deep-learning', 'stats-101'). This will be the directory name — use lowercase with hyphens."

**User:** `deep-learning`

**Skill asks:**
> "Where should the project live? Provide the full path, or I'll create it in your current working directory."

**User:** (uses default eval output path)

**Action:** Created project directory structure:

```
deep-learning/
  course_material/          ← (empty placeholder; user's PDF lives here)
  progress.md
  curriculum_map.yaml
  linear-algebra/
  probability-theory/
  ml-basics/
  feedforward-networks/
  regularization/
  optimization/
  convolutional-networks/
  recurrent-networks/
```

### `progress.md` (created)

```markdown
# Progress — Deep Learning

**Subject:** Deep Learning (Goodfellow, Bengio, Courville)
**Started:** 2026-04-09

## Curriculum

*Updated at each session end by the teacher.*

---
```

### `curriculum_map.yaml` starter (before NLM query)

```yaml
# Curriculum Map — Deep Learning
# ...

lessons: []
```

---

## Step 2 — Course material

**Skill asks:**
> "Do you have course material to add? You can drop textbook PDFs into `deep-learning/course_material/`. I'll scan it once you're ready."

**User:** "Yes, Goodfellow et al. deep_learning.pdf is already there."

**Scan result:** `course_material/deep_learning.pdf` detected.

---

## Step 3 — NotebookLM mode

**Skill asks:**
> "Which NotebookLM mode do you want?
> - **Passive:** NLM called for cross-chapter lookups and verification (~3–5 queries/session).
> - **Active:** NLM is the primary source for all factual content.
> - **Hybrid (recommended for 2–3 textbooks):** Section PDFs loaded for each topic; NLM handles cross-chapter retrieval. Requires a one-time PDF split."

**User:** "Hybrid."

**Action:** Recorded `nlm_mode: hybrid` in `curriculum_map.yaml`.

### Hybrid setup checklist (from `teacher/notebooklm.md`)

1. `uv tool install notebooklm-mcp-cli` — instructed user to run
2. `nlm setup add claude-desktop` — instructed user to run
3. `nlm login` — instructed user to run
4. `notebook_create` called → notebook ID: `nlm-deep-learning-goodfellow` *(simulated)*
5. `source_add deep_learning.pdf` → source added to notebook *(simulated)*

**Skill offers:**
> "I can query NotebookLM to extract the chapter/section structure from your textbook. Want me to do that now?"

**User:** "Yes."

### NLM query (simulated)

**Query sent to `notebook_query`:**
```
List all chapters and sections of "Deep Learning" (Goodfellow, Bengio, Courville)
with page ranges. Format as: Chapter number, Section name, Start page - End page.
```

**Simulated NLM response:**

```
Part I — Applied Math and Machine Learning Basics
  Chapter 2: Linear Algebra, pp. 1–36
  Chapter 3: Probability and Information Theory, pp. 37–66
  Chapter 4: Numerical Computation + Chapter 5: Machine Learning Basics, pp. 67–148

Part II — Modern Practical Deep Networks
  Chapter 6: Deep Feedforward Networks, pp. 163–220
  Chapter 7: Regularization for Deep Learning, pp. 221–268
  Chapter 8: Optimization for Training Deep Models, pp. 269–321
  Chapter 9: Convolutional Networks, pp. 322–380
  Chapter 10: Sequence Modeling: Recurrent and Recursive Nets, pp. 381–444
```

**Skill presents curriculum for review:**
> "Here's the structure I found. Review and correct any page numbers that look off."

**User:** "Looks good, proceed."

### `curriculum_map.yaml` (final, after NLM population)

```yaml
# Curriculum Map — Deep Learning
# Each entry maps a lesson slug to its source material location.
# Format: slug: {name, source_file, pages}

nlm_mode: hybrid  # passive | active | hybrid

lessons:
  - slug: linear-algebra
    name: "Linear Algebra"
    source_file: "deep_learning.pdf"
    pages: "1-36"

  - slug: probability-theory
    name: "Probability Theory and Information Theory"
    source_file: "deep_learning.pdf"
    pages: "37-66"

  - slug: ml-basics
    name: "Numerical Computation and Machine Learning Basics"
    source_file: "deep_learning.pdf"
    pages: "67-148"

  - slug: feedforward-networks
    name: "Deep Feedforward Networks"
    source_file: "deep_learning.pdf"
    pages: "163-220"

  - slug: regularization
    name: "Regularization for Deep Learning"
    source_file: "deep_learning.pdf"
    pages: "221-268"

  - slug: optimization
    name: "Optimization for Training Deep Models"
    source_file: "deep_learning.pdf"
    pages: "269-321"

  - slug: convolutional-networks
    name: "Convolutional Networks"
    source_file: "deep_learning.pdf"
    pages: "322-380"

  - slug: recurrent-networks
    name: "Sequence Modeling: Recurrent and Recursive Nets"
    source_file: "deep_learning.pdf"
    pages: "381-444"
```

**Action:** PDF split instructed:
```bash
python tools/split_pdf.py
```
*(Simulated — would split deep_learning.pdf into 8 section PDFs.)*

---

## Step 4 — Generate lesson meta.yaml stubs

For each of the 8 lessons in `curriculum_map.yaml`, a subdirectory and `meta.yaml` were created. Dependencies follow the linear textbook order (each lesson depends on the previous).

### `linear-algebra/meta.yaml`

```yaml
name: "Linear Algebra"
description: "Vectors, matrices, tensors, decompositions, and the geometric intuition underlying neural network operations."
status: not-started
depends: []
tags: [math, foundations]
sources:
  - "deep_learning.pdf, 1-36"
created: 2026-04-09
last_reviewed: null
review_count: 0
```

### `probability-theory/meta.yaml`

```yaml
name: "Probability Theory and Information Theory"
description: "Probability distributions, Bayes' rule, entropy, and the probabilistic foundations of machine learning models."
status: not-started
depends: ["Linear Algebra"]
tags: [math, foundations, probability]
sources:
  - "deep_learning.pdf, 37-66"
created: 2026-04-09
last_reviewed: null
review_count: 0
```

### `ml-basics/meta.yaml`

```yaml
name: "Numerical Computation and Machine Learning Basics"
description: "Numerical stability, gradient-based optimization fundamentals, bias-variance tradeoff, and supervised learning concepts."
status: not-started
depends: ["Linear Algebra", "Probability Theory and Information Theory"]
tags: [ml, foundations, optimization]
sources:
  - "deep_learning.pdf, 67-148"
created: 2026-04-09
last_reviewed: null
review_count: 0
```

### `feedforward-networks/meta.yaml`

```yaml
name: "Deep Feedforward Networks"
description: "Architecture of multilayer perceptrons, activation functions, backpropagation, and universal approximation."
status: not-started
depends: ["Numerical Computation and Machine Learning Basics"]
tags: [neural-networks, architecture, backprop]
sources:
  - "deep_learning.pdf, 163-220"
created: 2026-04-09
last_reviewed: null
review_count: 0
```

### `regularization/meta.yaml`

```yaml
name: "Regularization for Deep Learning"
description: "Techniques to reduce overfitting: L1/L2 penalties, dropout, batch normalization, data augmentation, and early stopping."
status: not-started
depends: ["Deep Feedforward Networks"]
tags: [regularization, generalization, overfitting]
sources:
  - "deep_learning.pdf, 221-268"
created: 2026-04-09
last_reviewed: null
review_count: 0
```

### `optimization/meta.yaml`

```yaml
name: "Optimization for Training Deep Models"
description: "SGD variants, momentum, Adam, learning rate schedules, second-order methods, and challenges of non-convex optimization."
status: not-started
depends: ["Regularization for Deep Learning"]
tags: [optimization, training, sgd, adam]
sources:
  - "deep_learning.pdf, 269-321"
created: 2026-04-09
last_reviewed: null
review_count: 0
```

### `convolutional-networks/meta.yaml`

```yaml
name: "Convolutional Networks"
description: "Convolution operation, pooling, translation equivariance, and CNN architectures for image recognition tasks."
status: not-started
depends: ["Optimization for Training Deep Models"]
tags: [cnn, computer-vision, architecture]
sources:
  - "deep_learning.pdf, 322-380"
created: 2026-04-09
last_reviewed: null
review_count: 0
```

### `recurrent-networks/meta.yaml`

```yaml
name: "Sequence Modeling: Recurrent and Recursive Nets"
description: "RNN architectures, BPTT, vanishing gradients, LSTMs, GRUs, and encoder-decoder models for sequential data."
status: not-started
depends: ["Convolutional Networks"]
tags: [rnn, lstm, sequence-modeling, nlp]
sources:
  - "deep_learning.pdf, 381-444"
created: 2026-04-09
last_reviewed: null
review_count: 0
```

---

## Step 5 — Verify Jupyter MCP

**Action:** Called `list_files` via Jupyter MCP server.

**Result (simulated):** Success.

**Skill confirms:**
> "Jupyter MCP is connected."

---

## Completion Summary

> "Project 'deep-learning' is scaffolded. Here's what was created:
> - `course_material/` — add your PDFs here
> - `progress.md` — tracks session progress
> - `curriculum_map.yaml` — NLM mode: hybrid
> - 8 lesson directories, each with a `meta.yaml` stub
>
> Next step: say 'let's study linear algebra' to begin your first session."

---

## File tree

```
deep-learning/
├── course_material/
├── progress.md
├── curriculum_map.yaml
├── linear-algebra/
│   └── meta.yaml
├── probability-theory/
│   └── meta.yaml
├── ml-basics/
│   └── meta.yaml
├── feedforward-networks/
│   └── meta.yaml
├── regularization/
│   └── meta.yaml
├── optimization/
│   └── meta.yaml
├── convolutional-networks/
│   └── meta.yaml
└── recurrent-networks/
    └── meta.yaml
```
