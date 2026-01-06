# Engineer Instructions for {PROJECT_NAME}

**Project-specific instructions for implementation work.**

For portable engineer role definition, see `engineer.agent.md`.
For project facts, see `engineer.context.md`.

---

## Requesting Code Reviews

<!-- Customize: Add project-specific review workflow -->

**Option 1: Daemon (if oracle is running in daemon mode)**
```bash
uv run python src/inbox.py add oracle-daemon "Review {topic}" \
  --from engineer:{session-name} --priority 2 \
  --body "Files: {paths}..."

uv run python src/inbox.py wait engineer --from oracle-daemon --timeout 180
```

**Option 2: Subagent (fallback)**
Use Task tool with `subagent_type=oracle`.

---

## Project-Specific Patterns

<!-- Customize: Add patterns specific to your codebase -->

---

## Common Tasks

<!-- Customize: Add frequently-needed commands/workflows -->
