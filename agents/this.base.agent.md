# Project-Wide Instructions for {PROJECT_NAME}

**This file contains project-specific instructions that apply to ALL agents.**

For portable agent coordination patterns, see `base.agent.md`.
For project facts, see `base.context.md`.

---

## Tool Preferences

<!-- Customize: Add project-specific tool preferences -->

**Python:**
- Always use `uv` (never vanilla python or pip)
- Commands: `uv run`, `uv add`, `uv pip install`
- Dependencies in `pyproject.toml` (not requirements.txt)

**Git:**
- Feature branches for significant work
- Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`

---

## Code Formatting

<!-- Customize: Add project-specific formatting rules -->

- Run `uv run ruff format` before committing
- Line length: 100 characters
- Type hints on function signatures

---

## File Creation

- **Minimize new files.** ALWAYS prefer editing existing files to creating new ones.
- Exception: Code files when adding genuinely new functionality.
