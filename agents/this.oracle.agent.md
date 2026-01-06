# Oracle Instructions for {PROJECT_NAME}

**Project-specific instructions for code review work.**

For portable oracle role definition, see `oracle.agent.md`.
For project review calibration, see `oracle.context.md`.

---

## Review Queue Processing

**When user says "enter daemon mode" or "process reviews":**

**Loop:**
1. `uv run python src/inbox.py wait reviews --timeout 300` -> **blocks until message arrives**
2. When message returns: claim -> review -> respond
3. Loop back to wait

**On timeout:** Loop again (keep waiting). Timeout just means "no messages yet", not "stop".

**Exit when:** User explicitly says stop, OR context limit approaching.

**Review types** (engineers prefix their messages):
- "Design: ..." -> design/architecture review (BEFORE coding)
- "Code: ..." -> code review (AFTER coding)

**Commands:**
```bash
# Block until message (returns JSON when one arrives)
uv run python src/inbox.py wait reviews --timeout 300

# Process message
uv run python src/inbox.py claim reviews {id}        # -> save token
uv run python src/inbox.py respond reviews {id} --token {token} --body "..."
```

---

## Review Calibration

<!-- Customize: Add project-specific review focus -->

**DO review for:**
- Silent failures (will it break quietly?)
- Logic correctness
- Evidence-based claims (did they test 3-5 examples?)

**DON'T review for:**
- Test coverage (unless project requires it)
- Comprehensive error handling
- Edge cases that won't happen
