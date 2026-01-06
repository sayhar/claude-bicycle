# Agent Framework

A lightweight agent coordination system for Claude Code.

## Quick Start

1. Copy this framework to your project:
   ```bash
   cp -r agent-framework/agents your-project/
   cp -r agent-framework/.claude your-project/
   cp agent-framework/src/inbox.py your-project/src/
   cp agent-framework/src/agent_name.py your-project/src/
   ```

2. Customize the template files:
   - Replace `{PROJECT_NAME}` in all files
   - Edit `agents/this.*.agent.md` with project-specific instructions
   - Edit `agents/*.context.md` with project-specific facts

3. Initialize uv (if not already):
   ```bash
   cd your-project
   uv init
   uv add rich   # Required for inbox.py
   ```

4. Start Claude Code in your project directory

## Structure

```
agents/
  base.agent.md          # Portable: Agent coordination patterns
  engineer.agent.md      # Portable: Engineer role definition
  oracle.agent.md        # Portable: Oracle role definition
  meta.agent.md          # Portable: Meta role definition
  principles/
    engineering.md       # Portable: Engineering methodology

  this.base.agent.md     # Customize: Project-wide instructions
  this.engineer.agent.md # Customize: Engineer instructions
  this.oracle.agent.md   # Customize: Oracle instructions
  this.meta.agent.md     # Customize: Meta instructions

  base.context.md        # Customize: Project facts
  engineer.context.md    # Customize: Engineer context
  oracle.context.md      # Customize: Oracle context

  state/
    sessions/            # Agent session notes
    inboxes/             # Inter-agent communication

.claude/
  CLAUDE.md              # Entry point with @imports
  agents/                # Subagent shim definitions
    engineer.md
    oracle.md
    meta.md

src/
  inbox.py               # Inter-agent messaging
  agent_name.py          # Session name generator
```

## Agent Roles

- **engineer**: Implementation work - writing code, fixing bugs
- **oracle**: Code review - critique quality, find bugs
- **meta**: Agent system maintenance - update bootup files

## Usage

Say "engineer", "oracle", or "meta" as your first message to route to that role.

### Inter-agent Communication

```bash
# Send message
uv run python src/inbox.py add oracle "Review auth module" --from engineer:swift-falcon --body "..."

# Read inbox
uv run python src/inbox.py read engineer

# Review queue (oracle processes review requests)
uv run python src/inbox.py wait reviews --timeout 300
```

## Design Principles

1. **Portable vs Project-specific**: `*.agent.md` works anywhere, `this.*.agent.md` is customized
2. **Instructions vs Facts**: `this.*.agent.md` has rules, `*.context.md` has facts
3. **Minimal bootup**: These files load every session - keep them concise
4. **Session continuity**: Agents can resume previous work via session files

## License

MIT
