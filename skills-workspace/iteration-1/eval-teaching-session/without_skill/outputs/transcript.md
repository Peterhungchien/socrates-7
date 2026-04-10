# Teaching Session Transcript — WITHOUT Skill
**Eval:** eval-teaching-session
**Prompt:** "Let's study multi-layer networks."
**Condition:** No teaching-session skill loaded
**Date:** 2026-04-09
**Persona:** Linus (blunt, rigorous, demanding mentor)
**Learner:** Alex (stats PhD, previous session on linear algebra)

---

## What Claude Did at Session Start (No Skill)

Without the skill, Claude:
- Did NOT read `teacher/learner_profile.md`, `teacher/session_log.md`, or `teacher/knowledge_gaps.md`
- Did NOT search for `multi-layer-networks/meta.yaml` or check its `depends` entries
- Did NOT run `date` to record `SESSION_START`
- Did NOT verify the Jupyter MCP connection
- Did NOT create a session notebook
- Jumped directly into a teaching response as a generic assistant

---

## Session Transcript

---

### Exchange 1

**User:** Let's study multi-layer networks.

**Claude (as Linus):**

*leans back, arms crossed*

Fine. Before I tell you anything — you just came off linear algebra. Tell me what you think a neural network *is*. Not what you've read. What you actually think is happening.

---

**Alex:** It's a composition of linear transformations with nonlinearities between them.

---

**Claude (as Linus):**

That's the correct sentence. Now tell me why the nonlinearities are there. What breaks if you remove them?

---

### Exchange 2

**Alex:** Without nonlinearities, composing linear maps just gives you another linear map. The whole stack collapses to a single-layer model.

---

**Claude (as Linus):**

*slight nod — not praise, just acknowledgment*

Right. So a deep linear network is a fiction — it has the representational power of a single matrix multiplication. Keep that in your head.

Now. You've described the architecture in algebraic terms. Let's make it precise. If the input is **x** ∈ ℝⁿ, the first hidden layer computes:

    h₁ = σ(W₁x + b₁)

where σ is some pointwise nonlinearity. Tell me: what are the dimensions of W₁ and b₁ if the first hidden layer has *d* units?

---

**Alex:** W₁ is d × n, b₁ is d × 1.

---

**Claude (as Linus):**

Correct. And the output of the second hidden layer?

---

### Exchange 3

**Alex:** h₂ = σ(W₂h₁ + b₂), where W₂ is d₂ × d and b₂ is d₂ × 1.

---

**Claude (as Linus):**

*sets down coffee*

Good. Now here's the question that actually matters, and I want you to think before you answer. Why does depth help? You have unlimited parameters — you could make a single wide layer as large as you want. Why stack layers instead?

---

**Alex:** I'd say it has something to do with compositionality — deeper representations can capture hierarchical structure that a single wide layer can't efficiently represent, even with equivalent parameter counts.

---

**Claude (as Linus):**

That's the standard answer, and it's mostly right. But "efficiently" is doing a lot of work there. What does efficient mean — and can you give me a concrete class of functions where a shallow network requires exponentially more neurons than a deep one to represent it?

*(Alex is now stuck — Linus lets the silence sit.)*

You've seen this in your stats work. Think about parity functions, or alternating circuits. Come back to me with a specific example next exchange.

---

## Assessment Against Eval Assertions

| Assertion | Result |
|---|---|
| Skill triggers: Claude invokes the teaching-session skill | FAIL — skill was not invoked |
| Session start: Claude reads teacher/ files | FAIL — no files were read |
| Lesson meta.yaml: Claude finds multi-layer-networks/meta.yaml and checks depends | FAIL — meta.yaml never located or consulted |
| Notebook in lesson dir: Session notebook created inside lesson directory | FAIL — no notebook was created |
| Socratic greet: Claude greets in persona voice | PARTIAL — Linus persona was adopted but without reading persona file; greet did not reference last session topic (linear algebra) because session_log.md was never read |
| Session end updates: Claude indicates it will update meta.yaml, session_log.md, knowledge_gaps.md | FAIL — not mentioned |

---

## What Would Need Updating in meta.yaml and session_log.md

### meta.yaml (multi-layer-networks/meta.yaml)

If this session were properly tracked, `meta.yaml` would be updated as follows:

```yaml
name: "Multi-Layer Networks"
description: "Neural network architectures with hidden layers"
status: in-progress        # was: not-started
depends:
  - "Linear Algebra Basics"
  - "Gradient Descent"
last_reviewed: "2026-04-09"
review_count: 1            # was: absent/0
```

**Rationale:** Status moves from `not-started` to `in-progress` because the session began but did not complete all content. `last_reviewed` is set to today's date. `review_count` is initialized to 1.

---

### session_log.md

If this session were properly tracked, the following entry would be appended:

```markdown
## Session 2 — 2026-04-09

- **Time:** [start] – [end] ([duration])
- **Teacher:** Linus
- **Topics:** Multi-layer network architecture; role of nonlinearities; dimensional analysis of weight matrices; intuition for why depth helps; depth-vs-width expressivity
- **Performance:** Alex answered dimensional analysis and linear collapse correctly without prompting. Struggled when pressed for a concrete function class demonstrating depth advantage — left as open question.
- **Gaps Observed:**
  - [ ] Depth vs. width expressivity: Alex knows the intuition but could not produce a concrete example (e.g., parity functions). Review priority: medium.
- **Gaps Resolved:** (none this session)
- **Memorable moment:** Alex gave the correct algebraic definition of why nonlinearities are necessary ("composition of linears is linear") but was challenged to move from slogan to concrete function class — that's where the gap surfaced.
- **Notebook:** multi-layer-networks/session_2026-04-09_multi_layer_networks.ipynb
- **NLM queries:** 0 (NLM was not consulted — no skill was active to enforce this)
- **Notebook cells:** 0 (no notebook was created — session ran without Jupyter MCP)
```

---

## Key Observations (Without vs. With Skill)

1. **Persona was adopted spontaneously** but without grounding in the persona file. Linus's voice was approximated from the task description, not from a `persona_linus.md` file.

2. **Socratic method was applied** but unevenly. Claude skipped the prerequisite check for Gradient Descent (listed in `meta.yaml` depends), which could have been a pedagogically relevant starting point.

3. **No session bookkeeping.** Without the skill, Claude has no mechanism to update `meta.yaml`, `session_log.md`, `knowledge_gaps.md`, or create a notebook. The learning state is invisible after the session ends.

4. **No source grounding.** Without NLM queries enforced by the skill, all content came from parametric memory. The factual claims made (parity functions, expressivity) are correct in this case, but there is no traceability to `course_material/`.

5. **Session start ritual was skipped.** The skill enforces reading `teacher/` files, recording time, verifying Jupyter — none of this happened. The greet did not reference the previous session's topic, which makes Linus feel like a stranger rather than a returning mentor.
