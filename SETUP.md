# Project Setup Checklist

Work through this with `claude meta` or manually. When complete, delete this file.

---

## 1. Git Setup

- [ ] **Remove origin**: `git remote remove origin`

Add your own remote later when you have one.

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

- [ ] **Install uv** (if needed)
- [ ] **Install deps**: `uv sync`
- [ ] **Test inbox**: `uv run python src/inbox.py read engineer` (should show empty)
- [ ] **Test name gen**: `uv run python src/agent_name.py` (should output a name)

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

Send to oracle:
```bash
uv run python src/inbox.py add oracle "Setup Review: Technical approach for {PROJECT_NAME}" \
  --from meta:setup --priority HIGH --body "
## Technical Decisions to Review

- Tech stack: [languages, frameworks, databases]
- Architecture: [pattern, structure]
- Key libraries: [and why]

## Open Questions

[Any tradeoffs or uncertainties]
"
```

- [ ] Sent inbox to oracle

**Next:** Run `claude oracle` to review, then `claude engineer` to implement.

---

## 6. Cleanup

When setup is complete:

```bash
rm SETUP.md
uv run python src/inbox.py delete meta ba68b7c
```

Then prompt user: "Setup complete! Type `/exit` and run `claude oracle` to review technical decisions before implementing." (For existing projects with established tech stack, they can go straight to `claude engineer`.)
