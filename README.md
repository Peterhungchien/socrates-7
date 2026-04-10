# Socrates-7

A collection of Claude skills that scaffold and manage AI-powered Socratic learning.

## What This Is

Socrates-7 is a **skills repo** — not a learning project itself. It provides four Claude
skills that you install once and use across any number of learning projects. Each skill
handles a distinct part of the learning workflow:

| Skill | Purpose |
|-------|---------|
| `create-teacher` | Design a teacher persona and learner profile |
| `scaffold-project` | Set up a learning project from a textbook or course |
| `teaching-session` | Run a full Socratic study session |
| `knowledge-base` | Navigate prerequisites and learning status |

Your actual learning lives in a separate directory that the skills create and manage.

## How It Works

```
my-learning/                        ← your learning root (anywhere on disk)
  teacher/                          ← created by create-teacher
    persona_linus.md
    learner_profile.md
    session_log.md
    knowledge_gaps.md
  deep-learning/                    ← created by scaffold-project
    course_material/
    progress.md
    curriculum_map.yaml
    multi-layer-networks/           ← one directory per lesson
      meta.yaml                     ← knowledge point metadata
      session_2026-04-09.ipynb      ← session notebook lives with the lesson
    backpropagation/
      meta.yaml
  t-distribution-review/            ← ad-hoc standalone (user creates manually)
    meta.yaml
    material.pdf
    session_2026-04-10.ipynb
```

Every lesson directory has a `meta.yaml` that tracks its status, dependencies, and
review history. The knowledge graph is discovered by searching all `meta.yaml` files —
no index, no fixed structure.

## meta.yaml Schema

Required fields:

```yaml
name: "Multi-Layer Networks"
description: "Feedforward networks with hidden layers, universal approximation"
status: not-started   # not-started | in-progress | reviewed | mastered
depends:
  - "Linear Algebra Basics"   # matched by name, not path
  - "Gradient Descent"
```

Optional fields (extend freely):

```yaml
tags: [neural-networks, deep-learning]
sources:
  - "course_material/deep_learning.pdf, Ch. 6"
created: 2026-04-09
last_reviewed: null
review_count: 0
notes: |
  Focus on activation functions and vanishing gradients.
```

See `examples/meta.yaml` for a full example.

## Installation

```bash
# Clone the repo
git clone <repo-url> ~/.claude/skills/socrates-7

# Symlink the skills so Claude can find them
ln -s ~/.claude/skills/socrates-7/skills/create-teacher ~/.claude/skills/
ln -s ~/.claude/skills/socrates-7/skills/scaffold-project ~/.claude/skills/
ln -s ~/.claude/skills/socrates-7/skills/teaching-session ~/.claude/skills/
ln -s ~/.claude/skills/socrates-7/skills/knowledge-base ~/.claude/skills/
```

## Prerequisites

All three MCP servers are required for full functionality:

- **Filesystem MCP server** — read/write access to your learning directory
- **Jupyter MCP server** — live notebook blackboard for formulas, code demos, exercises
- **NotebookLM MCP CLI** — full-corpus knowledge retrieval from your textbooks

### Claude Desktop config

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "/absolute/path/to/my-learning"]
    },
    "jupyter": {
      "command": "uvx",
      "args": ["jupyter-mcp-server@latest"],
      "env": {
        "JUPYTER_URL": "http://localhost:8888",
        "JUPYTER_TOKEN": "MY_TOKEN",
        "ALLOW_IMG_OUTPUT": "true"
      }
    },
    "notebooklm-mcp": {
      "command": "notebooklm-mcp"
    }
  }
}
```

### Jupyter

```bash
pip install uv
jupyter lab --port 8888 --IdentityProvider.token MY_TOKEN
```

### NotebookLM MCP CLI

See [notebooklm-mcp-cli installation](https://github.com/jacob-bd/notebooklm-mcp-cli?tab=readme-ov-file#installation).

## First-Time Setup

1. Create your learning directory (anywhere on disk)
2. Open Claude Desktop with filesystem access to that directory
3. Say: **"Set up my teacher"** → runs `create-teacher`
4. Say: **"Scaffold a project for [textbook]"** → runs `scaffold-project`
5. Say: **"Let's study [topic]"** → runs `teaching-session`

## Workflow

```
create-teacher    →  scaffold-project  →  teaching-session  (repeat)
(one-time setup)     (per textbook)       (each study session)

knowledge-base    ←  invoked by teaching-session + user queries
```

## Reference Files

These files in the repo are templates the skills reference:

- `examples/persona_example.md` — example teacher persona (Linus)
- `examples/learner_profile_example.md` — example learner profile
- `examples/meta.yaml` — annotated meta.yaml with all fields
- `teacher/system.md` — original monolithic system prompt (reference only)
- `teacher/system_detail.md` — original extended rules (reference only)
- `docs/init_prompt.md` — original initialization prompt (reference only)

## License

MIT — see [LICENSE](LICENSE).
