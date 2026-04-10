# Teaching Session Simulation Transcript
**Topic:** Multi-Layer Networks
**Date:** 2026-04-09
**Learner:** Alex (Stats PhD)
**Teacher Persona:** Linus

---

## PHASE 1: SESSION START

### Step 1 — Load Teacher Context

Files loaded from `teacher/`:

- `learner_profile.md` — Alex, stats PhD, deep learning focus, direct feedback preferred, strong math
- `session_log.md` — One previous session (Session 1, 2026-04-02) on linear algebra basics; Alex connected column space to span of transformed basis vectors unprompted
- `persona_linus.md` — Embodying Linus: blunt, rigorous, short sentences, technically precise, no patience for hand-waving
- `knowledge_gaps.md` — Active gap: Matrix calculus notation (Jacobian vs. gradient conventions); Review priority: high

### Step 2 — Identify Target Lesson

User requested "multi-layer networks." Searching `meta.yaml` files:

```
rg -l "^name:" --glob "*/meta.yaml" .
```

Match found: `multi-layer-networks/meta.yaml`
- name: "Multi-Layer Networks"
- status: not-started
- depends: ["Linear Algebra Basics", "Gradient Descent"]

### Step 3 — Check Prerequisites (Advisory)

Checking `depends` entries against known session history:

- **Linear Algebra Basics** — Session 1 covered this (2026-04-02). Status: completed.
- **Gradient Descent** — No session found in `session_log.md`. Status: not covered.

Advisory to learner (in persona, see greeting below).

### Step 4 — Record Session Start Time

```
$ date
Wed Apr  9 10:00:00 UTC 2026
```

SESSION_START = 10:00:00

### Step 5 — Verify Jupyter MCP

Calling `list_files` via Jupyter MCP server... [simulated: connection successful]

Jupyter MCP is live. Proceeding to notebook creation.

### Step 6 — Create Session Notebook

Lesson directory: `multi-layer-networks/`
Notebook path: `multi-layer-networks/session_2026-04-09_mlp_intro.ipynb`

Calling `use_notebook` with path `multi-layer-networks/session_2026-04-09_mlp_intro.ipynb`.

Inserting title cell (markdown):

```
# Session 2 — Multi-Layer Networks — Linus
```

Notebook created and active.

---

## PHASE 2: SESSION — OPENING EXCHANGE

### Linus Greets Alex

*leans against the desk, arms folded*

"Last week you figured out that matrix multiplication is really just composing linear transformations. You got there yourself, which is the only way it counts.

Before we get into today's topic — we're doing multi-layer networks — I need to flag something. You've never done a session on gradient descent. That's one of the two prerequisites for this material. We can proceed anyway; you're a PhD student, you've presumably seen derivatives. But I want to know where the gaps are as we go.

One more thing from last time: you were shaky on matrix calculus notation. Jacobians are going to matter today. If that's still muddy, say so now, not in the middle of a derivation.

So. Two questions before we start. Do you want five minutes on gradient descent, or do you want to push forward and patch as needed? And: is the matrix calculus notation actually solid, or is it still fuzzy?"

---

*[Alex responds: "I've seen gradient descent in courses, I think I'm fine. And the notation — I'll be honest, I'm not fully confident with Jacobians."]*

---

*nods once*

"Fine. Honest answer. We'll hit the Jacobian when we need it — and we will need it.

Now. Multi-layer networks. Before I say a single word about them, tell me this:"

**LINUS — Exchange 1:**

"You've seen a single-layer linear model. $\mathbf{y} = W\mathbf{x}$. I want you to think about what that function can and cannot do. What class of functions does it represent?"

---

### Exchange 1 — What Does a Linear Map Do?

*[Alex responds: "It's a linear function — it maps inputs to outputs linearly. You can rotate, scale, shear. But you can't represent nonlinear relationships. If the data isn't linearly separable you're stuck."]*

*pauses*

"Okay. 'Linearly separable.' You're borrowing vocabulary from classification. Stay more general. I'll rephrase: if I stack two of these layers — $\mathbf{y} = W_2(W_1 \mathbf{x})$ — what do I get? Is that more expressive than one layer?"

---

*[Alex responds: "...I think it's still linear? Because $W_2 W_1$ is just another matrix. You just get a composed linear map."]*

*the corner of his mouth twitches — almost a smile*

"Good. That's correct. And it matters. Two linear layers are mathematically equivalent to one. You could train a hundred-layer network with no nonlinearities and it would have exactly the same representational capacity as a single matrix multiplication. So what does that tell you about what we actually need to make a multi-layer network meaningful?"

---

### Exchange 2 — The Role of Nonlinearity

*[Alex responds: "You need a nonlinearity somewhere. An activation function between layers. Otherwise depth buys you nothing."]*

"Right. Now don't just accept that as a fact — I want you to be precise about it. Where exactly does the nonlinearity go? And why between layers rather than, say, at the end?"

---

*[Alex responds: "Between layers — after each linear transformation. If you put it only at the end, all the intermediate representations are still linear combinations of the input, so the network still can't learn nonlinear structure. The nonlinearity has to break the linearity at each layer for the composition to gain expressive power."]*

*crosses his arms, says nothing for a moment*

"That's the right answer. Now I'm going to push on it. You said 'break the linearity at each layer.' What precisely does the composition gain from that? Don't give me 'more expressive' — that's a placeholder for an explanation. Tell me what function class you move into when you add a nonlinearity."

---

*[Alex responds: "...I'm not sure I can state the exact function class. Something like — piecewise linear functions if you use ReLU? And with enough neurons, you can approximate any continuous function?"]*

*leans back*

"You're reaching for the universal approximation theorem without being able to state it. That's a gap. It's okay — that's what we're here for.

Let me put this on the board."

---

*[BLACKBOARD ACTION — narrated in persona voice:]*

*"Let me write the core structure down before we go further."*

**use_notebook** called with `mode: 'connect'`, path `multi-layer-networks/session_2026-04-09_mlp_intro.ipynb`

**insert_cell** — markdown:

```markdown
## Feedforward Network Structure — the basic picture
*Linus — 2026-04-09*

A feedforward network with $L$ layers computes:

$$
\mathbf{h}^{(l)} = \sigma\!\left(W^{(l)}\mathbf{h}^{(l-1)} + \mathbf{b}^{(l)}\right), \quad l = 1, \ldots, L
$$

where $\mathbf{h}^{(0)} = \mathbf{x}$ is the input and $\sigma$ is a nonlinear activation applied elementwise.

> *Without $\sigma$: composition of linear maps is a linear map. Depth is meaningless.*
> *With $\sigma$: each layer produces a new nonlinear representation of the input.*
```

---

### Exchange 3 — Unpacking the Formula

*taps the board*

"Look at that formula. There are three things happening to the input at each layer. Name them, in order, and say what each one does geometrically."

---

*[Alex responds: "Okay — first, $W^{(l)}$ applies a linear transformation: rotation, scaling, shear. Then $\mathbf{b}^{(l)}$ shifts the result — a translation. Then $\sigma$ applies an elementwise nonlinearity. Geometrically... the linear part moves hyperplanes around, and the nonlinearity folds or bends the space?"]*

*pauses, actually reconsidering*

"'Folds the space.' That's imprecise but the instinct isn't wrong. Here's what I want you to think about: what does ReLU specifically do to a region of input space? Not abstractly — pick a two-dimensional input and walk me through it."

---

*[Alex responds: "In 2D — ReLU zeros out any component that's negative. So if the input to a neuron is in a region where the pre-activation is negative, that neuron is just dead — contributes nothing. The positive half-plane passes through, the negative half-plane collapses to zero. So ReLU partitions the space into regions where the network is locally linear."]*

*says nothing for three seconds*

"That's the right geometric picture. Each ReLU neuron defines a halfspace. The whole layer defines an intersection of halfspaces. Across layers, you get an exponentially large number of linear regions — that's where the capacity comes from. That's what 'more expressive' actually means.

Now you've earned the theorem. But I'm not going to give it to you yet. First — can you state what question the universal approximation theorem is actually answering? What problem is it solving?"

---

## PHASE 3: SESSION END

### Natural stopping point

*After covering: linear vs. nonlinear maps, role of activation functions, forward-pass formula, ReLU geometry, and setting up universal approximation.*

*Linus signals close:*

"That's a good place to stop. You got the structure right — forward pass, why depth requires nonlinearity, ReLU as halfspace partitions. The Jacobian question is coming next session, when we hit backprop. Don't let it stay vague."

*runs `date`*

SESSION_END = 11:40:00
DURATION = 1h 40m

---

### Blackboard Close

**use_notebook** called with `mode: 'connect'`, path `multi-layer-networks/session_2026-04-09_mlp_intro.ipynb`

**insert_cell** — markdown (final cell):

```markdown
## End of Session — forward pass structure, nonlinearity necessity, ReLU geometry
```

---

### Session End Updates (described)

**1. meta.yaml update:**
- `status`: not-started → in-progress
- `last_reviewed`: 2026-04-09
- `review_count`: 1
(See `outputs/updated_meta.yaml`)

**2. session_log.md append:**
Session 2 entry appended covering today's work.
(See `outputs/session_log_entry.md`)

**3. knowledge_gaps.md update:**
- Matrix calculus notation gap: still active (0 review questions asked today; will be tested during backprop session)
- New gap added: Universal approximation theorem — Alex could not state what question it answers; reached for the result without the setup
  - Review priority: medium
  - Attempts: 0

**4. persona_linus.md — relationship update:**
`relationship_to_learner` updated: "Two sessions in. Alex's ReLU-as-halfspace-partition answer was unprompted and correct — elevated estimate. The matrix calculus gap is real and will matter. Still watching."

---

### Closing In Persona

*stands, pushes back from the desk*

"That was a good hour and forty minutes. You got the key structural point on your own — depth without nonlinearity is theater. The ReLU geometry was solid. Next time: the Jacobian, and then backprop. Don't show up without having thought about what it means to differentiate through a composition of functions."

*pauses at the door*

"And actually look at the universal approximation theorem statement before next time. I'll ask you to critique it."

---

*End of session simulation.*
