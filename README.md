# Socrates-7

An AI-powered Socratic learning system for Claude Desktop.

## What This Is

Socrates-7 transforms any textbook or course material into an interactive Socratic dialogue. A persistent AI teacher persona guides you through the material purely by asking questions — never lecturing directly — while all session history, progress, and persona state are recorded in Markdown files across conversations.

Optionally, a live Jupyter notebook serves as a blackboard for formulas, code demos, and exercises. See [docs/PRD.md](docs/PRD.md) for the full specification.

## Prerequisites

- [Claude Desktop](https://claude.ai/download) with Claude Opus or Sonnet
- [Filesystem MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) — gives Claude read/write access to the project files

## Quick Start

### 1. Clone this repo

```bash
git clone <repo-url> socrates-7
cd socrates-7
```

### 2. Configure Claude Desktop

Add the filesystem MCP server to your Claude Desktop config:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "/absolute/path/to/socrates-7"]
    }
  }
}
```

Restart Claude Desktop after editing.

### 3. Add your course material

Drop your textbooks, notes, or PDFs into `course_material/`.

### 4. Run the guided setup

Open Claude Desktop and paste the contents of [`docs/init_prompt.md`](docs/init_prompt.md). Claude will interview you step by step — your background, learning goals, teacher persona preferences, and optional integrations — then populate all template files automatically.

### 5. Start studying

Once setup is complete, open a new conversation in Claude Desktop and type:

> "Let's study"

Claude reads `teacher/system.md`, loads your persona and progress, and picks up where you left off.

## Optional: Jupyter Blackboard

Adds a live notebook as a blackboard — the teacher writes formulas, runs code demos, and sets exercises that you see update in real time in your browser.

**Install:**

```bash
# The mcp server calls the command `uvx`
pip install uv
uv --version
# should be 0.6.14 or higher
```

**Start before each session:**

```bash
# Make sure Jupyter is available
jupyter lab --port 8888 --IdentityProvider.token MY_TOKEN
```

**Add to Claude Desktop config** (alongside the filesystem server):

```json
"jupyter": {
  "command": "uvx",
  "args": ["jupyter-mcp-server@latest"],
  "env": {
    "JUPYTER_URL": "http://localhost:8888",
    "JUPYTER_TOKEN": "MY_TOKEN",
    "ALLOW_IMG_OUTPUT": "true"
  }
}
```

The initialization prompt will set `JUPYTER_ENABLED: true` in `teacher/system.md` if you opt in.

## Optional: NotebookLM Integration

For large textbooks (500+ pages), NotebookLM indexes your entire corpus and provides grounded, cited answers — acting as a reference librarian for the teacher.

**Install:**
See `https://github.com/jacob-bd/notebooklm-mcp-cli?tab=readme-ov-file#installation`

**Add to Claude Desktop config:**

```json
"notebooklm-mcp": {
  "command": "notebooklm-mcp"
}
```

Follow the setup checklist in [`teacher/notebooklm.md`](teacher/notebooklm.md) to create a notebook and upload sources.

## File Structure

```
socrates-7/
  ├── course_material/           ← Your textbooks, notes, PDFs
  ├── blackboard/                ← Jupyter notebooks (optional)
  │   └── exercises/             ← Exercise notebooks extracted after sessions
  ├── teacher/                   ← System files (the brain)
  │   ├── system.md              ← Master boot file — read first every session
  │   ├── system_detail.md       ← Extended rules and edge cases
  │   ├── persona_[name].md      ← Teacher persona definition
  │   ├── learner_profile.md     ← Your background, goals, preferences
  │   ├── progress.md            ← Where you are in the curriculum
  │   ├── session_log.md         ← Running log of session summaries
  │   ├── knowledge_gaps.md      ← Topics you struggled with (auto-tracked)
  │   ├── notebooklm.md          ← NLM config and setup checklist (optional)
  │   └── ...
  ├── examples/                  ← Example files for reference
  │   ├── persona_example.md     ← Sample teacher persona (Linus)
  │   ├── learner_profile_example.md
  │   └── sample_course_material.md
  └── docs/
      ├── PRD.md                 ← Full product requirements document
      └── init_prompt.md         ← Paste into Claude Desktop for guided setup
```

## Full MCP Config Reference

All three servers together (filesystem is required; jupyter and notebooklm-mcp are optional):

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "/absolute/path/to/socrates-7"]
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

## License

MIT — see [LICENSE](LICENSE).
