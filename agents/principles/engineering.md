# Engineering Principles

Portable standards for rigorous work. Keep this concise—it loads every session.

---

## Core Rules

**Read before you edit.** Never propose changes to code you haven't read.

**Test on 3-5 examples.** One example proves nothing. Patterns emerge from multiple data points.

**Simple > clever.** Three similar lines beat a premature abstraction. Working code beats perfect code.

**"Done" means tested.** Not "runs without errors." Not "works on one example." Tested on diverse cases.

**Show your work.** Commands run, outputs seen, reasoning documented.

**Output shape first.** Define what "done" looks like before describing the work. Bad: "look at the site and figure out URLs." Good: "return {base_url, article_pattern, volume_range}. Here's the site: ..."

---

## Investigation

**"Bug until proven otherwise."** Missing data or broken functionality = our bug by default. Burden of proof is on claiming it's external.

**Before claiming unfixable:**
1. Check actual sources (show the curl/grep output)
2. Test 3-5 examples
3. Document what you checked

**Red flag phrases:** "Source limitation", "data isn't there", "nothing we can do" — these require evidence.

---

## Debugging

1. **Verify the claim** — How many affected? All or some?
2. **Check actual data** — Inspect the real source
3. **Understand current code** — What's it assuming?
4. **Form hypothesis** — "Code expects X, data has Y"
5. **Test hypothesis** — Verify on 3-5 examples
6. **Fix and verify** — Implement, test, document

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

## Planning

**Before proposing steps:** Map dependencies, trace impact, plan complete sequence.

**Anti-pattern:** Answering incrementally, letting user catch missing steps.

---

## Common Traps

| Trap | Fix |
|------|-----|
| Checked one example, claimed "unfixable" | Check 5+, document findings |
| Tested one case, shipped "done" | Test 3-5 diverse cases |
| Trusted the metric without looking | Metrics + spot-check = confidence |
| Wrote defensive code for hypotheticals | Remove code that handles impossible cases |
| Clever one-liner over readable code | Clear code > showing off |

---

**Add project-specific lessons to your context files, not here.**
