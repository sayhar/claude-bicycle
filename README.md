# Agent Framework

A lightweight coordination system for Claude Code agents. Provides role-based routing, inter-agent messaging, session continuity, and code review workflows.

## Quick Setup

```bash
claude   # Start Claude Code
> meta   # Say "meta" to load the meta agent
> help me set up this project
```

Or work through `SETUP.md` manually.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                         .claude/CLAUDE.md                           │
│                    (Entry point - routes by role)                   │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
              ┌──────────┐  ┌──────────┐  ┌──────────┐
              │ engineer │  │  oracle  │  │   meta   │
              └────┬─────┘  └────┬─────┘  └────┬─────┘
                   │             │             │
                   ▼             ▼             ▼
              ┌─────────────────────────────────────┐
              │           agents/*.agent.md         │
              │     (Portable role definitions)     │
              ├─────────────────────────────────────┤
              │        agents/this.*.agent.md       │
              │    (Project-specific instructions)  │
              ├─────────────────────────────────────┤
              │         agents/*.context.md         │
              │       (Project-specific facts)      │
              └─────────────────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  state/inboxes  │  │ state/sessions  │  │ oracle/*.md     │
│  (messages)     │  │ (continuity)    │  │ (knowledge)     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Features

### Role-Based Agents

| Role | Purpose |
|------|---------|
| **engineer** | Implementation - writing code, fixing bugs, building features |
| **oracle** | Code review - critique quality, find bugs, suggest improvements |
| **meta** | System maintenance - update agent bootup files, fix patterns |

Say the role name as your first message to route to that agent.

### Inter-Agent Messaging

Agents communicate via inbox files managed by `src/inbox.py`:

```bash
uv run python src/inbox.py add oracle "Review auth module" --from engineer:swift-falcon
uv run python src/inbox.py read oracle
uv run python src/inbox.py claim oracle <id>
uv run python src/inbox.py delete oracle <id>
```

### Session Continuity

Each work thread gets a memorable name (e.g., "swift-falcon") and a session file:

- **Lines 1-20:** Living TL;DR (updated each continuation)
- **Lines 21+:** Append-only log

When context limits approach, agents update their session file for handoff.

### Review Workflow

Engineers can request reviews and block until response:

```bash
# Engineer sends review request
uv run python src/inbox.py add reviews "Design: new auth" --from engineer:swift-falcon
uv run python src/inbox.py wait engineer --from reviews --timeout 180

# Oracle processes reviews queue
uv run python src/inbox.py wait reviews --timeout 3000
uv run python src/inbox.py respond reviews <id> --token <tok> --body "Approved with notes..."
```

### Subagent Spawning

Parent agents can spawn scoped subagents via `.claude/agents/*.md` shims. Subagents have restrictions (no git operations, tool limits) and report back to parent.

### Knowledge Base

Oracle maintains persistent knowledge in `oracle/`:
- `decisions.md` - Architectural choices, tagged by date
- `learnings.md` - Domain discoveries, bug patterns

---

## File Structure

```
agents/
  *.agent.md           # Portable role definitions (copy to new projects)
  this.*.agent.md      # Project-specific instructions
  *.context.md         # Project-specific facts
  principles/          # Engineering methodology
  state/
    inboxes/           # Inter-agent messages
    sessions/          # Session continuity files

oracle/
  decisions.md         # Technical decisions log
  learnings.md         # Domain learnings log

.claude/
  CLAUDE.md            # Entry point with @imports and routing
  agents/              # Subagent shim definitions

src/
  inbox.py             # Messaging CLI
  agent_name.py        # Session name generator

tmp/                   # Session scratch files (gitignored)
```

---

## Design Principles

1. **Portable vs Project-specific**: `*.agent.md` files work in any project. `this.*.agent.md` and `*.context.md` are customized per project.

2. **Instructions vs Facts**: Rules go in `*.agent.md`. Facts go in `*.context.md`.

3. **Minimal bootup**: These files load every session. Keep them concise.

4. **Session continuity**: Agents can resume previous work via session files.

---

## License

MIT
