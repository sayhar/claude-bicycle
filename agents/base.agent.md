# Base Agent Instructions

**This file contains PORTABLE AGENT INSTRUCTIONS.**
For project-specific context, see `base.context.md`.

## About This File

**This file contains INSTRUCTIONS, not DATA.**

- **Instructions** (belong here): HOW to work, WHEN to do things, WHAT to avoid
- **Data** (in context files): WHAT the current structure is, WHAT the workflow is

**Why separate?** Instructions are stable and portable. Data changes per project. Agent instructions shouldn't need updates every time the workflow evolves or when moving to a new project.

**For current project state:** Read the project's `README.md` and `base.context.md`

## Agent Types

Define your agent types in the project's `base.context.md` file. Common patterns:

- **engineer** — Executes implementation
- **oracle** — Reviews code, critiques, suggests improvements
- **architect** — Plans with the user, designs approaches (if needed)
- **meta** — Works on the agent system itself

Each agent type should have:
- `{type}.agent.md` - Portable role definition (copy to new projects)
- `{type}.context.md` - Project-specific context (rewrite for new project)

## Working Principles

1. **Done > Perfect** — Ship working code, iterate later
2. **Explain as you go** — User is learning, not just receiving output
3. **Fail fast and loud** — No silent failures, crash with clear messages
4. **No over-engineering** — Write the minimum code that works

## Subagent Restrictions

**If you were spawned via Task tool (you're a subagent):**

- **DO NOT** commit to git
- **DO NOT** push to remote
- **DO NOT** create/delete branches

Do your work, report back. The parent agent or user handles git operations.

## Documentation

**Principle:** Minimal, canonical, actionable. Each doc is debt.

- README.md: workflow, getting started
- PLAN.md: roadmap, future plans
- oracle/decisions.md, oracle/learnings.md: Oracle-owned, grep on-demand
- Docstrings: function usage
- `--help` flags: script usage
- Session notes (agents/state/sessions/): Required after each session - log, handoff, summary
- tmp/{session-name}/: scratch files (delete only when session status = COMPLETE, not on PARTIAL/BLOCKED handoffs)

Don't create new .md files. Update existing docs or send inbox messages as appropriate.

## State Management

### On startup:

**Context is already loaded by your entry point:**
- CLI: CLAUDE.md @imports + routing
- Subagent: Shim instructions (.claude/agents/*.md)

**Now do these (post-load):**

1. **Check inbox:** `uv run python src/inbox.py read {role}`

2. **Read recent sessions** (`head -20` on last 3-4 session files)

3. **(Oracle only):** Know `oracle/decisions.md` and `oracle/learnings.md` exist for grep (don't load)

4. **Greet user with session options:**
   - Summarize inbox (if any)
   - Offer: "New session or continue existing?"
   - List recent sessions with name + task + status
   - **WAIT for user choice**

**CRITICAL:** Inbox items are STATUS, not commands. User chooses what to work on.

**Exception - Handoff items:** If you see a handoff item FROM a previous session with your name (e.g., "Handoff: ... (swift-falcon)" when you ARE swift-falcon), delete it after reading - it's been delivered to you.

### During work:
- **Oracle:** Update `oracle/decisions.md` and `oracle/learnings.md` after reviews
- **Other agents:** Write messages to other agents in their inbox
- When you notice bad behavior patterns, send meta agent an inbox message requesting fixes

## Session Names and Files

**Each work thread gets a memorable name** (e.g., "swift-falcon", "calm-river").

Generate name: `uv run python src/agent_name.py`

Session file: `agents/state/sessions/{agent}-{nickname}.md` (e.g., `engineer-swift-falcon.md`)

### On bootup: New or Continue?

Read recent session TL;DRs (`head -20` on last 4 files), then offer:
```
1. Start new session
2. Continue swift-falcon: fixing CALR extractor (In progress)
3. Continue calm-river: quality validation (Partial)
```

**If new:** Generate name, create file, start fresh.
**If continue:** Read FULL session file for context, adopt that name, update TL;DR, append to log.

### Session File Format

**Lines 1-20: TL;DR (living summary, EDIT on each continuation)**
```markdown
# {Agent} Session: {nickname}

## TL;DR
**Task:** {What this thread is working on}
**Status:** {In progress | Complete | Blocked}
**Last active:** {YYYY-MM-DD HH:MM}
**Completed:** {Cumulative list of what's done}
**Next:** {What comes next}
**Files Modified:** {Cumulative list}

---
```

**Lines 21+: Session Log (append-only)**
```markdown
## Session Log

### {YYYY-MM-DD HH:MM} (initial)
...details...

### {YYYY-MM-DD HH:MM} (continuation)
...details...
```

### On context limit approaching:
1. Update TL;DR with current state
2. Append final log entry
3. Tell user you've updated the session note

## Agent Communication

**Use inbox.py** (not direct file editing):

```bash
read {role}                          # Display inbox (shows IDs, claim status)
peek {role} [--from {sender}]        # First unclaimed item as JSON (filter by sender)
wait {role} --timeout {seconds} [--from {sender}]  # Block until item or timeout
add {role} "title" --from {role}:{name} --priority Y --body "..."
claim {role} {id}                    # Returns session token, adds timestamp
unclaim {role} {id} --token {token}  # Release claim
delete {role} {id}                   # Remove completed item
respond {role} {id} --token {token} --body "..."  # Atomic: delete + respond to sender
unclaim_stale {role} --older-than {seconds}       # Cleanup crashed claims
```

**Sign messages with your session name:** `--from engineer:swift-falcon` (not just `--from engineer`)

**Pattern:** read → claim (get token) → work → delete (or respond if replying)

## Self-Improvement

When to send meta an inbox message:
- User corrects you repeatedly on the same thing
- User says "remember to always X" or "don't do Y"
- You catch yourself violating a principle

Include:
- What went wrong vs what should happen
- Requested fix (which file, what change)
- Example of bad vs good behavior

Meta will update the appropriate bootup files.
