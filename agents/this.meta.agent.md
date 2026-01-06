# Meta Instructions for {PROJECT_NAME}

**Project-specific instructions for meta-engineering work.**

For portable meta role definition, see `meta.agent.md`.

---

## File Structure Maintenance

**Three-file pattern for each agent:**
- `{role}.agent.md` - Portable (HOW to be this role, any project)
- `this.{role}.agent.md` - Project instructions (DO X for {PROJECT_NAME})
- `{role}.context.md` - Project facts (X is true about {PROJECT_NAME})

**Checking portability:**
If `{role}.agent.md` mentions project-specific terms -> move to `this.{role}.agent.md` or `{role}.context.md`.

---

## Bootup File Size Limits

**Target sizes:**
- `{role}.agent.md`: <100 lines (portable role definition)
- `this.{role}.agent.md`: <80 lines (project instructions)
- `{role}.context.md`: <100 lines (project facts, distilled)

**If exceeded:** Refactor for conciseness (bootup files load every session).
