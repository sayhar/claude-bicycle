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

### Review Workflow

**Engineer sends review request:**
```bash
uv run python src/inbox.py add reviews "Design: new auth module" \
  --from engineer:swift-falcon --priority HIGH --body "..."
uv run python src/inbox.py wait engineer --from reviews --timeout 180
```

**Oracle processes reviews (daemon mode):**
```bash
# 1. Check oracle inbox
uv run python src/inbox.py peek oracle

# 2. Block on reviews queue
uv run python src/inbox.py wait reviews --timeout 3000

# 3. If message arrives: claim, review, respond
uv run python src/inbox.py claim reviews {id}
uv run python src/inbox.py respond reviews {id} --token {token} --body "..."
```

### General Inter-agent Communication

```bash
# Send message to any role
uv run python src/inbox.py add {role} "title" --from {sender}:{name} --body "..."

# Read inbox
uv run python src/inbox.py read {role}

# Claim work item
uv run python src/inbox.py claim {role} {id}

# Delete completed item
uv run python src/inbox.py delete {role} {id}
```

## Design Principles

1. **Portable vs Project-specific**:
   - `*.agent.md` — Generic role definitions, work in any project (copy to new projects)
   - `this.*.agent.md` — Project-specific overrides (should be minimal/template-like)
   - `*.context.md` — Project facts (what's true about this project)

2. **Instructions vs Facts**:
   - Rules ("always do X") → `*.agent.md` or `this.*.agent.md`
   - Facts ("X is true") → `*.context.md`

3. **Minimal bootup**: These files load every session - keep concise
   - Verbose explanations → README or other docs
   - Dense principles → bootup files

4. **Session continuity**: Agents can resume previous work via session files (`agents/state/sessions/`)

## License

MIT
