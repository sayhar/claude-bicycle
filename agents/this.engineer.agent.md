# Engineer Instructions for {PROJECT_NAME}

**Project-specific instructions for implementation work.**

For portable engineer role definition, see `engineer.agent.md`.
For project facts, see `engineer.context.md`.

---

## Requesting Code Reviews

**TWO REVIEWS REQUIRED:**
1. BEFORE coding (design review) - prefix with "Design:"
2. AFTER coding (code review) - prefix with "Code:"

**Send to `reviews` queue:**
```bash
uv run python src/inbox.py add reviews "Design: {topic}" \
  --from engineer --priority HIGH --body "{details}"
```

**Wait for response:**
```bash
uv run python src/inbox.py wait engineer --from reviews --timeout 180
```

**If no response after 3+ minutes:** Spawn background oracle subagent:
```
Task tool, subagent_type="oracle", run_in_background=true
```

---

## Project-Specific Patterns

<!-- Customize: Add patterns specific to your codebase -->

---

## Common Tasks

<!-- Customize: Add frequently-needed commands/workflows -->
