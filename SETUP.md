# Project Setup Checklist

Work through this with `claude meta` or manually. When complete, delete this file.

---

## 1. Git Setup

- [ ] **Rename origin to upstream** (keep for pulling framework updates):
  ```bash
  git remote rename origin upstream
  git remote set-url --push upstream DISABLE
  ```

This keeps `upstream` for pulling agent-framework updates (`git fetch upstream && git merge upstream/main`) but blocks accidental pushes back to it. Add your own `origin` later when you have a repo for this project.

---

## 2. Project Identity

Replace `{PROJECT_NAME}` and "Agent Framework" with your actual project name.

- [ ] `README.md` - Line 1: `# Agent Framework` → `# YourProjectName`
- [ ] `.claude/CLAUDE.md` - Line 1: `# {PROJECT_NAME} Agent System`
- [ ] `agents/base.context.md` - Line 1
- [ ] `agents/this.base.agent.md` - Line 1
- [ ] `agents/engineer.context.md` - Line 1
- [ ] `agents/this.engineer.agent.md` - Line 1
- [ ] `agents/oracle.context.md` - Line 1
- [ ] `agents/this.oracle.agent.md` - Line 1
- [ ] `agents/this.meta.agent.md` - Line 1

> **Ask user:** What should we call this project?

**Quick replace (macOS):** `grep -rl "{PROJECT_NAME}" agents/ .claude/ | xargs sed -i '' 's/{PROJECT_NAME}/YourProjectName/g'`

**Quick replace (Linux):** `grep -rl "{PROJECT_NAME}" agents/ .claude/ | xargs sed -i 's/{PROJECT_NAME}/YourProjectName/g'`

---

## 3. Dependencies

- [ ] **Install uv** (if needed): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] **Test inbox**: `uv run agents/tools/inbox.py read engineer` (should show empty — uv auto-installs script deps on first run)
- [ ] **Test name gen**: `uv run agents/tools/agent_name.py` (should output a name)

---

## 4. Project Context (THE IMPORTANT PART)

This is a kickoff conversation. Take time here.

---

### 4.1 What & Why (`agents/base.context.md`)

**What are we building?**
- Describe it in 1-2 sentences
- What type of thing is it? (CLI, web app, library, API, script, etc.)

**Why are we building it?**
- What problem does this solve?
- Who has this problem? Who's the user?
- Why does this matter? What's the motivation?

**What are our goals?**
- What does success look like?
- How will we know it's working?
- What's the scope? (MVP, full product, experiment, etc.)
- What are we explicitly NOT trying to do?

- [ ] Filled in `agents/base.context.md`

---

### 4.2 Domain Knowledge (`agents/engineer.context.md`)

**What do we need to understand?**
- What domain is this in?
- What terminology or jargon matters?
- What concepts are essential?
- Any gotchas or counterintuitive things?

**What external things are involved?**
- APIs, data sources, third-party services?
- Their quirks or limitations?

- [ ] Filled in `agents/engineer.context.md`

---

### 4.3 Constraints & Quality (`agents/oracle.context.md`)

**What constraints exist?**
- Tech preferences? Performance requirements?
- Dependencies we must use or avoid?

**What matters most?**
- Correctness? Performance? Readability? Speed?
- What's the quality bar? (MVP, production, enterprise?)

- [ ] Filled in `agents/oracle.context.md`

---

### 4.4 Existing Codebase

**If adding agent-framework to an existing project:**

Tech stack and architecture are already decided - write them as facts in context files:
- `base.context.md` - tech stack, project structure
- `engineer.context.md` - architecture, key modules, how things connect

Skip to section 6 (Cleanup).

**If starting a new project:** Continue to section 5.

---

## 5. Architecture Review (new projects only)

For new projects, tech decisions should be reviewed before implementing.

Spawn a reviewer subagent to review the technical approach inline:

```
Use the Task tool with subagent_type="reviewer" to review:

- Tech stack: [languages, frameworks, databases]
- Architecture: [pattern, structure]
- Key libraries: [and why]
- Any tradeoffs or open questions

Include the filled-in context files in the prompt so the reviewer has full context.
```

Update context files based on reviewer feedback, then proceed to cleanup.

- [ ] Architecture reviewed

---

## 6. Cleanup

When setup is complete:

```bash
rm SETUP.md
uv run agents/tools/inbox.py delete meta ba68b7c
```

Then prompt user: "Setup complete! Type `/exit` and run `claude engineer` to start building."
