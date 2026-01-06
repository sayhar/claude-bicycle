# {PROJECT_NAME} Agent System

**Base context (always loaded):**

@../agents/base.agent.md
@../agents/this.base.agent.md
@../agents/base.context.md
@../agents/principles/engineering.md

---

**Role routing (load based on user's first message):**

If user says "**engineer**" or asks for implementation/coding help:
- Read `agents/engineer.agent.md`
- Read `agents/this.engineer.agent.md`
- Read `agents/engineer.context.md`

If user says "**oracle**" or asks for code review/critique:
- Read `agents/oracle.agent.md`
- Read `agents/this.oracle.agent.md`
- Read `agents/oracle.context.md`

If user says "**meta**" or asks about the agent system itself:
- Read `agents/meta.agent.md`
- Read `agents/this.meta.agent.md`

**Default:** If unclear, assume engineer (implementation work).
