# Project Setup

You are setting up an agent coordination framework for Claude Code. No agent roles exist yet — you're just Claude with these instructions. Work through each section with the user.

When done, you'll write the real `.claude/CLAUDE.md` and delete this file. The agent system bootstraps itself into existence through this process.

---

## 1. Git Setup

- [ ] **Rename origin to upstream** (keep for pulling framework updates):
  ```bash
  git remote rename origin upstream
  git remote set-url --push upstream DISABLE
  ```

Keeps `upstream` for pulling framework updates (`git fetch upstream && git merge upstream/main`) but blocks accidental pushes. Add your own `origin` later.

---

## 2. Project Identity

> **Ask the user:** What should we call this project?

Replace `{PROJECT_NAME}` with the answer in these files (line 1 of each):
- `agents/base.context.md`
- `agents/this.base.agent.md`
- `agents/this.engineer.agent.md`
- `agents/this.meta.agent.md`
- `agents/this.oracle.agent.md`
- `agents/engineer.context.md`
- `agents/oracle.context.md`

Also: `README.md` line 1 — `# Agent Framework` → `# {project name}`

---

## 3. Dependencies

- [ ] **Install uv** (if needed): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] **Test inbox**: `uv run agents/tools/inbox.py read engineer` (should show empty)
- [ ] **Test name gen**: `uv run agents/tools/agent_name.py` (should output a name)

---

## 4. Project Context

This is a kickoff conversation. Take time here.

### 4.1 What & Why → `agents/base.context.md`

- What are we building? (1-2 sentences, what type — CLI, web app, library, API, script)
- Why? (Problem, who has it, why it matters)
- Goals? (Success criteria, scope, what we're NOT doing)

### 4.2 Domain Knowledge → `agents/engineer.context.md`

- Domain, terminology, concepts, gotchas?
- External deps? APIs, data sources, quirks?

### 4.3 Constraints & Quality → `agents/oracle.context.md`

- Tech preferences, performance requirements, must-use/avoid deps?
- Quality bar: correctness vs speed vs readability? MVP or production?

### 4.4 Existing Codebase

Adding to an existing project? Write tech stack and architecture as facts in context files, skip to section 6.

New project? Continue to section 5.

---

## 5. Architecture Review (new projects only)

Spawn a reviewer subagent:

```
Use Task tool with subagent_type="reviewer" to review:
- Tech stack, architecture, key libraries, tradeoffs
Include the filled-in context files for full context.
```

Update context files based on feedback.

---

## 6. Plan

Fill in `PLAN.md` at the repo root. Vision and Approach should be clear from the conversation so far. Phases can be rough — they'll sharpen as work begins.

---

## 7. Finalize

Write `.claude/CLAUDE.md` with the contents below (replacing `{PROJECT_NAME}` with the actual project name), then delete this file (`SETUP.md`).

Tell the user: "Setup complete! Type `/exit` and run `claude engineer` to start building."

**Contents for `.claude/CLAUDE.md`:**

````
# {PROJECT_NAME} Agent System

**Base context (always loaded):**

@../agents/base.agent.md
@../agents/this.base.agent.md
@../agents/base.context.md

---

**Role routing (load based on user's first message):**

If user says "**engineer**" or asks for implementation/coding help:
- Read `agents/engineer.agent.md`
- Read `agents/this.engineer.agent.md`
- Read `agents/engineer.context.md`
- Read `agents/principles/engineering.md`

If user says "**oracle**" or asks for code review/critique:
- Read `agents/oracle.agent.md`
- Read `agents/this.oracle.agent.md`
- Read `agents/oracle.context.md`
- Read `agents/principles/engineering.md`

If user says "**meta**" or asks about the agent system itself:
- Read `agents/meta.agent.md`
- Read `agents/this.meta.agent.md`
- Read `agents/meta.context.md`
- Read `agents/principles/engineering.md`

**Default:** If unclear, assume engineer (implementation work).
````
