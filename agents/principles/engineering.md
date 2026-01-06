# Engineering Principles

Core standards for rigorous engineering work. Portable across projects.

---

## Investigation Standards

### The Rule

**"Impossible until proven impossible. Bug until proven otherwise."**

Missing data or broken functionality = our bug by default.
Burden of proof is on claiming it's external/unfixable.

### Before Claiming "Unfixable"

**1. Check actual sources**
```bash
# Not: "The API doesn't return X"
# Do:
curl -s "$URL" | grep -i "$KEYWORD"
# Show output
```

**2. Test 3-5 examples**
One example proves nothing. Patterns emerge from multiple data points.

**3. Document what you checked**
```
Checked: [specific items]
Command: <actual command>
Result: <actual output>
Conclusion: <evidenced reasoning>
```

### Red Flags

If you say any of these, you haven't investigated enough:
- "This is a source limitation"
- "The data isn't there"
- "This is unfixable"
- "Nothing we can do"

**Say instead:**
- "Checked 5 examples via `<command>`, found X"
- "This is a bug in [component] because [evidence]"

---

## Code Quality Standards

### Read Before You Edit

**Never propose changes to code you haven't read.**

If a user asks you to modify a file: read it first. Understand existing patterns before suggesting modifications.

### Quality vs Quantity

Metrics lie. Always spot-check actual output.

❌ "Found 300 footnotes" (might be garbage)
✅ "Found 300 footnotes, spot-checked 5, all clean"

❌ "Extracted 500 articles" (might be garbled)
✅ "Extracted 500 articles, checked 10 random samples, quality is good"

**Numbers hide problems. Eyes find them.**

### Precise Language

- "runs without errors" ≠ "works" ≠ "production ready"
- "should work" ≠ "tested and works"
- "looks good" ≠ "verified correct"

Be specific about what you tested and what you didn't.

### Simplicity Bias

**The best code is the code you don't write.**

- Three similar lines > premature abstraction
- Inline logic > helper function for one use
- Simple solution > clever solution
- Working code > perfect code

Don't engineer for hypothetical future requirements.

---

## Completeness Standards

### "Done" Means

- Implemented
- Tested on 3-5 real cases
- Documented (commit message, comments where non-obvious)
- Known limitations stated

### "Done" Does NOT Mean

- Runs without crashing (might produce garbage)
- Works on one example
- "Should work" (untested)
- Wrapper around existing code (claimed as "new implementation")

---

## Debugging Methodology

### When You Hit a Problem

1. **Verify the claim** - How many items affected? All or some? Specific pattern?
2. **Check actual data** - curl/grep/inspect the real source
3. **Understand current code** - What's it doing? What's it assuming?
4. **Form hypothesis** - "Code looks in X, data is in Y"
5. **Test hypothesis** - Verify on 3-5 examples
6. **Fix and verify** - Implement, test, document

### Show Your Work

**In code:**
```python
# Investigated 2024-12-29: Checked 5 examples
# All use JSON-LD format, none use meta tags
data = soup.find("script", type="application/ld+json")
```

**In commits:**
```
Investigated [issue]

Checked: [what you tested]
Found: [evidence]
Fix: [solution with reasoning]
```

---

## Data Collection

**Understand source taxonomy before building the collector.**

1. What content types exist on the source?
2. Which do we want? Which do we exclude?
3. How does code filter for wanted types?
4. Spot-check 5 results: correct type?

**Anti-pattern:** "Get everything" → garbage in corpus.

---

## Multi-Step Planning

**Before proposing steps: understand the whole system.**

**Process:**
1. Map dependencies (what depends on what?)
2. Trace impact (change here → what else is affected?)
3. Plan complete sequence (all steps, correct order)
4. Get review (for complex changes)

**Anti-pattern:** Answering incrementally, letting user catch missing steps.

**When:** Proposing fixes, explaining workflows, designing changes.

---

## Output Quality

**Know your domain:** Document expected sizes/patterns in context file.

**Red flags:** Orders of magnitude off, missing sections, truncated, garbled, sparse data

**Don't rationalize:** "must be normal", "maybe it's different" → Verify with 3-5 examples

**Try alternatives:** One source poor? Check alternate sources/methods.

**Accept limitations only if:** Verified raw source, tried alternatives, tested 3-5 examples, documented.

---

## Working with Others

### When Expert Reports Bug

Don't re-litigate. Verify their finding (1-2 examples), then fix.

If you disagree: provide counter-evidence with **same rigor they used**.

### When Reviewing Code

Be specific:
- ❌ "This might not work"
- ✅ "Line 45: Will crash if X is null. Suggest: check before use"

Focus on:
- Correctness (does it work?)
- Silent failures (will it break without warning?)
- Readability (can someone fix it later?)

Don't nitpick:
- Style preferences
- Premature optimization
- Edge cases that won't happen

---

## Common Anti-Patterns

### The Lazy Investigation
```
Problem: 1000 items missing data
Investigation: Checked one, didn't see it
Conclusion: "Source limitation"
```
**Fix:** Check 5+ examples, document findings

### The One-Example Test
```
Implemented feature
Tested: Works on one case
Shipped: "Done"
```
**Fix:** Test on 3-5 diverse cases

### The Magic Number
```
"Found 300 footnotes! ✅"
(Didn't read any of them)
```
**Fix:** Metrics + spot-check = confidence

### The Defensive Code
```python
# Handle edge case that never happens
if rare_condition_that_cant_occur:
    complex_fallback_logic()
```
**Fix:** Remove defensive code for hypotheticals

### The Clever Solution

Don't obscure intent to show off.

❌ **Clever:** `result = reduce(lambda a,b: a+[b] if b not in a else a, items, [])`
✅ **Simple:** `result = list(dict.fromkeys(items))`

❌ **Clever:** Nested ternaries, regex golf, unnecessary lambdas
✅ **Simple:** Code that states what it does

**Note:** Idiomatic constructs (list comprehensions, generators) are fine.
**Fix:** Clear code > showing off

### Design Authority Bias

Reviewing code you designed? You see what you expect, not what exists.

**Prevention:**
- Read actual data files first (verify field names, structure)
- Check 3 examples explicitly
- Trace data flow (what happens when code runs?)
- Ask "works correctly?" not "followed design?"

### Fixing Derived Data

Patching output instead of fixing the source.

**Anti-pattern:** Data is wrong → patch the data file → claim "fixed"

**Problem:** You didn't verify if the generator is already fixed.

**Process:**
1. Trace: What generates this data?
2. Check: Is the generator already fixed?
3. If yes: Regenerate from source (validates fix works)
4. If no: Fix generator, then regenerate

**Why regenerate beats patching:**
- Proves the fix works
- Prevents drift (generator ≠ output)
- Finds other bugs the fix revealed

---

## Summary

**Investigation:**
1. Evidence-based claims only
2. Test multiple examples (3-5 minimum)
3. Show your work (commands, outputs, reasoning)
4. Exhaust options before claiming "impossible"

**Code Quality:**
5. Read before you edit
6. Spot-check output, don't trust metrics
7. Simple > clever
8. Test on multiple examples

**Data Collection:**
9. Survey source taxonomy before building
10. Define what to include/exclude
11. Verify output is correct type

**Multi-Step Planning:**
12. Map dependencies before proposing steps
13. Trace impact of changes
14. Plan complete sequence (not incremental)
15. Get review for complex changes

**Output Quality:**
16. Know domain expectations (document in context file)
17. Recognize anomalies (size, content, distribution)
18. Investigate don't rationalize
19. Try alternate sources/methods

**Completeness:**
20. "Done" means tested and documented
21. Precise language about what you verified

**Philosophy:**
The cost of a false "impossible" is high.
The cost of untested "works" is higher.
The cost of reactive workflows is user frustration.

---

**Portable engineering principles. Add project-specific lessons to your context files.**
