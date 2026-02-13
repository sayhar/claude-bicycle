# Base Context for {PROJECT_NAME}

**This file contains PROJECT-SPECIFIC CONTEXT.**
For portable agent instructions, see `base.agent.md`.

## Project Purpose

<!-- Customize: What does this project do? -->

## Key Documents

| Need | Read |
|------|------|
| Project overview, how to run | `README.md` |
| Messages for you | `agents/state/inboxes/{your-type}.md` |
| Previous session handoff | `agents/state/sessions/{your-type}/*.md` |

## Tech Stack

<!-- Customize: List your tech stack -->

- Python 3.12+
- `uv` for package management

## Workflow Commands

<!-- Customize: Add common commands -->

```bash
# Example commands
uv run agents/tools/inbox.py read engineer
uv run agents/tools/agent_name.py
```
