# Classification rules

Every rater applies these rules so the labeling is reproducible. When the
consensus study surfaces a confusion hotspot, you **add a rule here** rather than
hoping a "smarter" rater guesses right — that is how the gold standard improves.

## Assign exactly one PRIMARY subtopic per question
Key it on the *operative mathematical object* in the question — the thing the
student actually has to do — not on surface vocabulary.

## Tie-break rules (resolve cross-topic ambiguity)
- A **remainder / mod / divisibility** question → `nt.*` (Number Theory), even if it looks like arithmetic.
- Anything with a **sample space / "probability"** → `prob.*`.
- **Roman numerals** → `arith.roman`.
- **median / mean / mode** → `stat.*`.
- A counting question whose whole method is combinations/permutations → `comb.*`; if it asks "what is the probability", it is `prob.count` instead.

## Deterministic boundary rules
These exist because the consensus study found them to be the biggest source of
rater disagreement. Each turns a judgment call into a mechanical decision.

### `arith.ops` vs `arith.numlit`  (resolved a 67% → 91% subtopic-accuracy gap)
- → **`arith.ops`** (Order of operations & mixed-operation expressions) IF the
  expression **mixes different operation types** (×/÷ together with +/−), OR
  contains **parentheses**, an **exponent inside a larger expression**, or
  **absolute value**. PEMDAS governs the answer.
  Examples: `5 + 5×10`, `14×13 + 26×3`, `3 + 4×2 − (8÷4)`.
- → **`arith.numlit`** (Mental computation & number-sense shortcuts) OTHERWISE:
  a **single operation** (one ×, +, −, or ÷), a **standalone square** (`85²`), a
  **chained same-operation product** (`6×8×13×17`), or a **multi-term
  same-operation sum** (`13+26+47+34`). The skill is a mental shortcut, not
  operation order.
  Examples: `87×11`, `17²`, `23+37+45`.

## How to add a new rule
1. Run `scripts/consensus.py` over the rater files.
2. Read the **TOP CONFUSION PAIRS**. The biggest one is your next rule.
3. Write a deterministic `IF … → A, ELSE → B` rule for that pair here.
4. Re-run the raters with the updated rules and confirm the lift.

Irreducible tail: a few percent of questions are genuinely cross-subtopic (the
raters split 3 ways with no majority). Don't force a rule for these — send them
to a human. That tail is the natural ceiling of classification accuracy.
