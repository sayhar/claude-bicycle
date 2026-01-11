# Agent Framework

A bicycle for Claude Code.

---

## Why This Exists

Has this happened to you? You're three hours into a Claude Code session, making real progress, and then -- oops, you hit a context limit. You spin up a fresh conversation. Claude has no idea what you just did, decided, learned.

So you start copy-pasting things. Keeping notes. TELLING Claude to take notes. Maybe you start with a scratch "Bootup.md" file that says "remember: we're using approach X because of Y."

Then that scratch file gets more complicated. You split "things that you should always remember on bootup" from session notes from "things worth looking up."

You create different personas. The code reviewer. The engineer. The librarian. Each with their own bootup files. And they need to talk to each other. You set up inboxes for them to coordinate. The inboxes get fancier.

Now hooks to stop them from being dumb. Special subagents. More rigorous code reviews.

And then... wait, this works for your next project too. You port this between projects. You have a "team" of agents that you trust and bring to new tasks.

This repo is what that all became. A bicycle for Claude Code.

---

## What You Get

You close your laptop, come back three days later, and Claude offers to continue "swift-falcon: fixing the auth module" -- already knowing what it tried, what worked, what didn't. No re-explaining.

You get code reviewed by a different Claude. Not the same one wearing a "critic hat" -- a separate instance that wasn't in the room when you made the decisions. It catches that your parser assumes a field that doesn't exist in half the test cases. Builder-brain would've missed it.

You spin up five agents and they coordinate. One builds, one reviews, one keeps notes on decisions and mistakes. They leave each other messages through inboxes. You go make coffee. When you come back, there's a review waiting.

Three weeks in, Claude asks "are we still using the retry pattern from the auth module?" It checks decisions.md. Yes. Proceeds correctly without asking you.

You bring this to your next project. The roles you've defined, the patterns that work, the review calibration you trust. It's markdown files and a Python script -- you can read every file and understand what's happening.

Without this, Claude forgets your architectural decisions the moment the session ends. Reviews feel hollow because the reviewer has builder-brain. You re-explain the same context for the fifth time. The bicycle gives you leverage.

---

## Quick Start

```bash
cp -r agent-framework/ your-project/
cd your-project
claude
```

Say "meta" -- it walks you through setup.

Or work through `SETUP.md` manually.

---

## What's In The Box

```
agents/
  *.agent.md           # Role definitions (portable)
  this.*.agent.md      # Your project's instructions
  *.context.md         # Your project's facts
  principles/          # Engineering methodology

  oracle/
    decisions.md       # "We chose X because Y"
    learnings.md       # "This broke because Z"

  state/
    sessions/          # Session continuity
    inboxes/           # Agent coordination

hooks/                 # Guardrails
src/
  inbox.py             # Coordination CLI
  agent_name.py        # Session name generator
```

---

### Roles

Say a word, load a mindset.

**engineer** -- Build things. Write code, fix bugs, ship features.

**oracle** -- Review things. Critique code, find bugs, maintain the knowledge base.

**meta** -- Modify the system itself. Update agent files, fix patterns, add new roles.

Each role loads its own files:
- `{role}.agent.md` -- portable, bring to any project
- `this.{role}.agent.md` -- instructions for THIS project
- `{role}.context.md` -- facts about THIS project
- `principles/engineering.md` -- shared methodology

---

### Sessions

Each work thread gets a name like "swift-falcon" and a file:

```markdown
# Engineer Session: swift-falcon

## TL;DR
**Task:** Fixing the auth module
**Status:** In progress
**Completed:** Fixed token refresh, added retry logic
**Next:** Handle edge case when token is expired mid-request
**Files Modified:** src/auth.py, src/retry.py
```

Lines 1-20 are a living summary (edited each time). Lines 21+ are append-only log.

When you come back, Claude reads this and offers to continue. When context limits hit, Claude updates it before stopping.

---

### Inboxes

Agents coordinate through `src/inbox.py`:

```bash
# Send a message
uv run python src/inbox.py add oracle "Review auth module" \
  --from engineer:swift-falcon --priority HIGH

# Check your inbox
uv run python src/inbox.py read engineer

# Claim an item (prevents double-processing)
uv run python src/inbox.py claim engineer abc123

# Block until a message arrives
uv run python src/inbox.py wait engineer --from oracle --timeout 300

# Respond (atomic: deletes original + sends reply)
uv run python src/inbox.py respond engineer abc123 --token xyz --body "Done."
```

Handles concurrent access. No race conditions.

---

### Knowledge Base

Oracle maintains two files:

**decisions.md** -- Architectural choices:
```markdown
### [2024-01-15] Authentication
Using JWT with refresh tokens because session storage
doesn't scale for our use case.
```

**learnings.md** -- Mistakes and discoveries:
```markdown
### Parser Edge Cases
Empty input returns null, not empty array.
Found this when user submitted blank form.
```

Agents grep these when relevant -- not loaded at boot.

---

### The Oracle System

Engineers should check in with oracle before and after significant work. Design review before coding, code review after. (You can remind them if they forget.)

**Daemon mode:** Have an oracle tab open to the side. It monitors its inbox, responds to reviews, and keeps you informed.

```
"Enter daemon mode. Monitor the reviews inbox and respond to requests."
```

Oracle will loop: check inbox -> wait for reviews -> respond -> repeat. It tells you what engineers are asking about.

---

### Typical Setup

**Tabs:**
1. 2-3 engineer tabs -- doing the work
2. Oracle tab -- daemon mode, handling reviews
3. Meta tab -- restructuring, reading retrospectives, tweaking the system

**How it flows:**

Engineers boot up and either:
- Continue a previous session ("swift-falcon: fixing auth module")
- Grab tasks from inbox
- Work interactively with you

As they work, they ask oracle for help -- via inbox if daemon is running, via subagent if not.

Oracle and engineers spawn subagents to investigate problems, then break ideas into subtasks.

Some engineers can auto-run: grab inbox items, decompose them, orchestrate subagents.

When something goes wrong:
- Process issue -> message to meta (fix the system)
- Code bug -> message to oracle (document in learnings)

---

### Hooks

Optional guardrails in `hooks/`:

| Hook | What it does |
|------|--------------|
| `no-compound-bash.py` | Blocks `cmd1 && cmd2` -- forces single debuggable commands |
| `no-heredoc.py` | Blocks heredocs -- forces proper file writes |
| `require-uv.py` | Blocks bare `python`/`pip` -- forces `uv run` |
| `warn-conventional-commit.py` | Warns on non-conventional commit messages |
| `no-new-md-files.py` | Warns when creating .md files |

Enable in `.claude/settings.local.json`. They teach Claude your preferences by blocking bad patterns.

---

### Subagents

Spawn focused workers via Task tool:

```
Parent: "Task tool, engineer subagent, fix the parser in src/parse.py"

Subagent:
  - Loads context files
  - Cannot commit/push (parent handles git)
  - Scoped to ~15 tool calls
  - Reports back when done
```

Subagents that try to do too much will refuse and suggest how to break down the task.

---

## License

MIT
