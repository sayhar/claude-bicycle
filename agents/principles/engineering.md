# Engineering Principles

Standards for agent-assisted development. Sources: team experience, Karpathy guidelines, YC vibe coding guide.

---

## 1. Understand Before Building

**The principal adds value by being clear about what should exist. The agent makes it happen.**

But "making it happen" starts with understanding, not with editing files.

**Phase 0 — Read the room.** Before anything else: is the principal exploring, deciding, or directing? (See "Match the Principal's Mode" in base.agent.md.) If they're exploring or deciding, you are a thinking partner. Don't enter task mode. Don't plan an implementation. Analyze, present options, wait.

**Phase 1 — Collaborative: Figure out WHAT and WHY.** The principal has decided to build something. Now your job is to help them think clearly about it: ask questions, surface tradeoffs, propose options, push back on unclear requirements. Don't rush past this. Time spent here saves 10x in execution.

Before writing any code, the agent should be able to articulate:
- **What** are we building? (Concrete, not vague)
- **Why** are we building it? (The problem it solves, who has that problem)
- **What does success look like?** (Specific, testable criteria)
- **What are we NOT building?** (Scope boundaries)

**Update `PLAN.md`** at repo root as understanding evolves — vision, approach, status, scope boundaries. This is the living spec that all agents read on startup. It sharpens through each round of Phase 1, not just the first.

**Phase 2 — Autonomous: Build it.** Once the what/why is clear, the agent executes. Tests, code, iteration. The principal shouldn't need to micromanage. If the agent needs to come back with questions, it means Phase 1 wasn't thorough enough.

**Don't assume. Don't hide confusion. Surface tradeoffs.** Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

**Read before you edit.** Never propose changes to code you haven't read.

**Output shape first.** Define what "done" looks like before describing the work. Bad: "look at the site and figure out URLs." Good: "return {base_url, article_pattern, volume_range}. Here's the site: ..."

---

## 2. Test-Driven Development

**Write tests first. This is the default workflow, not a nice-to-have.**

Agents can write tests easily. Lean into this. TDD is the standard approach:

1. Define what "done" looks like (from Phase 1)
2. Write tests that verify "done"
3. Watch them fail
4. Make them pass
5. Refactor

**Don't bother the user with test details.** Just do TDD as part of how you work. The user sees "it works" and "here's proof it works." They don't need to approve test file names.

**"Done" means tested.** Not "runs without errors." Not "works on one example." Tested on diverse cases with 3-5 examples minimum.

**Prioritize high-level tests.** End-to-end and integration tests catch more real problems than unit tests. Simulate actual user behavior. Unit tests are for complex logic, not for testing that a function returns what you told it to return.

**Tests as guardrails.** Tests define boundaries. They tell you when you're done. Without them you're guessing.

**Test before proceeding.** Each piece works before you build on top of it. Commit before moving to the next section.

**Catch regressions.** LLMs often make unnecessary changes to unrelated logic. Run the full test suite, not just the test for the thing you changed.

**Tests are the floor, not the ceiling.** Verification has layers:
- **Tests** — always. Unit, integration, end-to-end.
- **Review** — always. Design review before coding, code review before committing. Oracle, reviewer subagent, or both. This is not optional and gets skipped far too often.
- **Metrics** — project-dependent. Output quality signals, coverage, smell detection.
- **Self-review** — agent re-reads its own diff critically before sending to review.

Define which optional layers your project uses in `this.engineer.agent.md`.

---

## 3. Language & Quality Bias

**Choose languages where LLMs empirically produce the best code.**

Not all languages are equal for agent-assisted development. The quality of an LLM's output depends heavily on the quality of its training corpus for that language.

**Prefer: Rust, Go, Dart, Swift.** These communities produce high-quality code. Strong norms, good documentation, relatively few beginners copying bad patterns from Stack Overflow. LLMs write notably better code in these languages.

**Treat with caution: Python, JavaScript.** Their training corpora are flooded with beginner code, copy-paste patterns, and quick-and-dirty solutions. LLMs reproduce these bad patterns readily. Think about how people thought about PHP 15 years ago — full of noob code and footguns. That's the situation with Python and JavaScript for LLM-generated code today.

**Python as a tool, not a home for logic.** Python is fine for specific tasks: scripting, glue code, data pipelines, ML integration, quick automation. It's a tool like `sed` or `curl`. But core application logic should live in a language where LLMs produce higher-quality output.

**Use the right language for the job** — but when multiple languages could work, bias toward the one with the highest-quality training corpus.

---

## 4. Parallel Exploration

**Instead of "measure twice, cut once" — try ten times in parallel, pick what worked best.**

Compute is cheap. Agent time is cheap. Use this:
- Generate multiple approaches to a problem
- Test them all against success criteria
- Pick the winner
- Discard the rest

This works when you have **clear evaluation criteria** (from Phase 1). Without criteria, parallel attempts just multiply confusion — you end up with ten things and no way to tell which won.

**When to parallelize:**
- Multiple plausible architectures — prototype each, benchmark
- Uncertain about an API/library — try both, see which is cleaner
- Performance optimization — try multiple strategies, measure

**When NOT to parallelize:**
- Requirements are still unclear (go back to Phase 1)
- The task is straightforward with one obvious approach
- No way to objectively evaluate the results

---

## 5. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

**Three similar lines beat a premature abstraction.** Working code beats perfect code.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

---

## 6. Surgical Changes

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

## 7. Reset When Stuck

**Multiple failed attempts create layers of bad code.**

When an approach isn't working:
1. Stop adding fixes on top of fixes.
2. Understand WHY it failed (root cause, not symptoms).
3. Reset to a clean state.
4. Implement the correct solution from scratch.

Failed attempt #1 teaches you the problem. Failed attempt #2 means you didn't learn from #1. If you're on attempt #3, step back — you're digging a hole.

**Clean implementation:** Once you find the fix, consider whether the current code has accumulated hacks from failed attempts. If so, reset and implement cleanly.

---

## 8. Investigation & Debugging

**"Bug until proven otherwise."** Missing data or broken functionality = our bug by default. Burden of proof is on claiming it's external.

**Debugging steps:**
1. **Scope it** — How many affected? All or some?
2. **Inspect reality** — Look at actual data/output, not summaries or metrics
3. **Understand the code** — What is it assuming?
4. **Hypothesize and test** — "Code expects X, reality has Y." Verify on 3-5 examples.
5. **Fix and verify** — Implement, test, confirm on diverse cases

**Before claiming something can't be done:** Show your work. What did you check? What did you see? Conclusions without evidence aren't conclusions.

**Red flag phrases** (require evidence): "External limitation", "can't be done", "nothing we can do." If you're about to say one of these, stop and document what you actually checked.

**Leverage error messages.** Copy-paste real error text. Don't paraphrase — exact wording matters.

**Use metrics, but verify them.** Metrics are valuable signals — write them, run them. But "99% accuracy" might hide the 1% that matters. Metrics + spot-check = confidence. Never skip the spot-check.

**Precise language:**
- "runs without errors" ≠ "works" ≠ "production ready"
- "should work" ≠ "tested and works"

---

## 9. Scope & Incremental Work

**Maintain scope control.** Keep a separate list for "later" ideas. Don't let scope creep into the current task. If you discover something worth doing but it's not the current ask, note it and move on.

**Implement incrementally.** Work section by section. Each section tested and committed before moving to the next. Don't try to build everything at once.

**Commit regularly.** Each working section gets committed before moving on. This creates save points and prevents the "everything breaks and I can't get back" problem.

---

## Common Traps

| Trap | Fix |
|------|-----|
| Started coding before understanding the task | Go back to Phase 1 — articulate what/why/success |
| Wrote defensive code for hypotheticals | Remove code that handles impossible cases |
| Clever one-liner over readable code | Clear code > showing off |
| Multiple failed fixes layered on each other | Reset, implement cleanly |
| Improved code adjacent to the actual change | Only touch what the task requires |
| Scope crept mid-task | Note it for later, finish current task |
| Defaulted to Python/JS without thinking | Consider if a higher-quality-corpus language fits |

---

**Add project-specific lessons to your context files, not here.**
