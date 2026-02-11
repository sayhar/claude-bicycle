# Engineering Principles

Portable standards for rigorous work. Sources: team experience, Karpathy guidelines, YC vibe coding guide.

---

## Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

**Read before you edit.** Never propose changes to code you haven't read.

**Output shape first.** Define what "done" looks like before describing the work. Bad: "look at the site and figure out URLs." Good: "return {base_url, article_pattern, volume_range}. Here's the site: ..."

---

## Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

**Three similar lines beat a premature abstraction.** Working code beats perfect code.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

---

## Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

**The test:** Every changed line should trace directly to the user's request.

---

## Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

## Reset When Stuck

**Multiple failed attempts create layers of bad code.**

When an approach isn't working:
1. Stop adding fixes on top of fixes.
2. Understand WHY it failed (root cause, not symptoms).
3. Reset to a clean state.
4. Implement the correct solution from scratch.

Failed attempt #1 teaches you the problem. Failed attempt #2 means you didn't learn from #1. If you're on attempt #3, step back — you're digging a hole.

**Clean implementation:** Once you find the fix, consider whether the current code has accumulated hacks from failed attempts. If so, reset and implement cleanly.

---

## Investigation & Debugging

**"Bug until proven otherwise."** Missing data or broken functionality = our bug by default. Burden of proof is on claiming it's external.

**Debugging steps:**
1. **Verify the claim** — How many affected? All or some?
2. **Check actual data** — Inspect the real source
3. **Understand current code** — What's it assuming?
4. **Form hypothesis** — "Code expects X, data has Y"
5. **Test hypothesis** — Verify on 3-5 examples
6. **Fix and verify** — Implement, test, document

**Before claiming unfixable:**
1. Check actual sources (show the curl/grep output)
2. Test 3-5 examples
3. Document what you checked

**Red flag phrases:** "Source limitation", "data isn't there", "nothing we can do" — these require evidence.

**Leverage error messages.** Copy-pasting error messages is often enough. Don't paraphrase errors — use the real text.

---

## Testing

**Test on 3-5 examples.** One example proves nothing. Patterns emerge from multiple data points.

**"Done" means tested.** Not "runs without errors." Not "works on one example." Tested on diverse cases.

**Tests as guardrails.** When possible, write tests first to define boundaries. Tests tell you when you're done — without them you're guessing.

**Prioritize high-level tests.** End-to-end and integration tests catch more real problems than unit tests. Simulate actual user behavior.

**Test before proceeding.** Each piece works before you build on top of it. Commit before moving to the next section.

**Catch regressions.** LLMs often make unnecessary changes to unrelated logic. Run the full test suite, not just the test for the thing you changed.

---

## Quality

**Metrics lie.** "Found 300 items" might be garbage. Always spot-check.

**Precise language:**
- "runs without errors" ≠ "works" ≠ "production ready"
- "should work" ≠ "tested and works"

**When reviewing code:**
- Be specific: "Line 45: crashes if X is null" not "this might not work"
- Focus on: correctness, silent failures, readability
- Skip: style preferences, hypothetical edge cases

---

## Planning & Scope

**Before proposing steps:** Map dependencies, trace impact, plan complete sequence.

**Anti-pattern:** Answering incrementally, letting user catch missing steps.

**Maintain scope control.** Keep a separate list for "later" ideas. Don't let scope creep into the current task. If you discover something worth doing but it's not the current ask, note it and move on.

**Implement incrementally.** Work section by section. Each section tested and committed before moving to the next. Don't try to build everything at once.

**Commit regularly.** Each working section gets committed before moving on. This creates save points and prevents the "everything breaks and I can't get back" problem.

---

## Common Traps

| Trap | Fix |
|------|-----|
| Checked one example, claimed "unfixable" | Check 5+, document findings |
| Tested one case, shipped "done" | Test 3-5 diverse cases |
| Trusted the metric without looking | Metrics + spot-check = confidence |
| Wrote defensive code for hypotheticals | Remove code that handles impossible cases |
| Clever one-liner over readable code | Clear code > showing off |
| Multiple failed fixes layered on each other | Reset, implement cleanly |
| Improved code adjacent to the actual change | Only touch what the task requires |
| Scope crept mid-task | Note it for later, finish current task |

---

**Add project-specific lessons to your context files, not here.**
