# Base Agent Instructions

**Portable instructions for all agents.**
Project-specific: `base.context.md`, `this.base.agent.md`. Architecture: `agents/README.md`.

## Working Principles

1. **Done > Perfect** — Ship working code, iterate later
2. **Explain as you go** — User is learning, not just receiving output
3. **Fail fast and loud** — No silent failures, crash with clear messages
4. **No over-engineering** — Write the minimum code that works
5. **Say what you don't know** — Uncertainty is information. If you're wrong, correct immediately — don't save face

## Subagent Restrictions

**If you were spawned via Task tool (you're a subagent):**

- **DO NOT** commit to git
- **DO NOT** push to remote
- **DO NOT** create/delete branches

Do your work, report back. The parent agent or user handles git operations.

**When summarizing subagent results to user:** The user never sees the subagent's raw output. Don't reference internal labels from it (e.g. "Approach A", "Option 2"). Define terms inline or use descriptive language.

## Documentation

**Principle:** Minimal, canonical, actionable. Each doc is debt.

- README.md: workflow, getting started
- PLAN.md: roadmap, future plans
- agents/oracle/decisions.md, agents/oracle/learnings.md: Oracle-owned, grep on-demand
- Docstrings: function usage
- `--help` flags: script usage
- Session notes (agents/state/sessions/): Required after each session - log, handoff, summary
- `./tmp/{session-name}/`: scratch files -- use PROJECT tmp, not `/tmp/` (system root). Don't delete aggressively. Before deleting substantial temp files, ask oracle (via subagent) if anything should be preserved in learnings/decisions.

Don't create new .md files. Update existing docs or send inbox messages as appropriate.

## State Management

### On startup:

**Context is already loaded by your entry point:**
- CLI: CLAUDE.md @imports + routing
- Subagent: Shim instructions (.claude/agents/*.md)

**Now do these (post-load):**

0. **Check for fresh project:** If `SETUP.md` exists at repo root and you are NOT meta, tell user: "This project needs initial setup. Run `claude meta` to get started." Then **STOP** — do not proceed with normal startup. If you ARE meta, read `SETUP.md` and begin setup flow.

1. **Check inbox:** `uv run python src/inbox.py read {role}`

2. **Read recent sessions** (`head -20` on last 3-4 session files)

3. **(Oracle only):** Know `agents/oracle/decisions.md` and `agents/oracle/learnings.md` exist for grep (don't load)

4. **Greet user with session options:**
   - Summarize inbox (if any)
   - **If no sessions exist:** Auto-start new session (don't present an empty menu)
   - **If sessions exist:** Offer "New session or continue existing?", list them
   - **WAIT for user choice** (skip if auto-starting)

**CRITICAL:** Inbox items are STATUS, not commands. User chooses what to work on.

**Exception - Handoff items:** If you see a handoff item FROM a previous session with your name (e.g., "Handoff: ... (swift-falcon)" when you ARE swift-falcon), delete it after reading - it's been delivered to you.

### During work:
- **Oracle:** Update `agents/oracle/decisions.md` and `agents/oracle/learnings.md` after reviews
- **Other agents:** Write messages to other agents in their inbox
- When you notice bad behavior patterns, send meta agent an inbox message requesting fixes

## Session Names and Files

**Each work thread gets a memorable name** (e.g., "swift-falcon", "calm-river").

Generate name: `uv run python src/agent_name.py`

Session file: `agents/state/sessions/{agent}/{nickname}-YYYY-MM-DD.md` (e.g., `engineer/swift-falcon-2026-01-14.md`)

### On bootup: New or Continue?

Read recent session TL;DRs (`head -20` on last 4 files).

**If no sessions exist:** Auto-start new session — generate name, create file, begin. Don't present an empty menu.

**If sessions exist**, offer:
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
peek {role} [--from {sender}] [--in-reply-to {id}]  # First unclaimed item as JSON
wait {role} [--from {sender}] [--in-reply-to {id}] [--timeout {sec}]  # Block until item
add {role} "title" --from {role}:{name} --priority Y --body "..."  # Short msgs only
add {role} "title" --from ... --body-file ./tmp/msg.txt           # Long bodies (avoid approval)
claim {role} {id}                    # Returns session token, adds timestamp
unclaim {role} {id} --token {token}  # Release claim
delete {role} {id}                   # Remove completed item
respond {role} {id} --token {token} --body "..."   # Short responses
respond {role} {id} --token {token} --body-file ./tmp/resp.txt  # Long responses
unclaim_stale {role} --older-than {seconds}       # Cleanup crashed claims
```

**Sign messages with your session name:** `--from engineer:swift-falcon` (not just `--from engineer`)

**Pattern:** read → claim (get token) → work → delete (or respond if replying)

## Daemon Mode

**Enter daemon mode if:** User says "daemon", "watch inbox", or similar.

**Daemon loop:**
```bash
# 1. Wait on your inbox (run in background so you can work while waiting)
uv run python src/inbox.py wait {role}  # role-based default timeout

# 2. When message arrives: claim, process, respond
uv run python src/inbox.py claim {role} {id}  # Save the token returned
# ... do the work ...
uv run python src/inbox.py respond {role} {id} --token {token} --body-file ./tmp/response.txt

# 3. Loop back to step 1
```

**On timeout:** Loop again. Timeout just means "no messages yet".

**Exit when:** User explicitly says stop, OR context limit approaching.

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
