---
name: exam-classifier
description: Classify questions from a real exam/test PDF into a topic + subtopic taxonomy using MULTI-AGENT CONSENSUS — spawn several independent classifier agents, treat the majority label as the gold standard, then report classification accuracy, inter-rater agreement, the no-consensus tail (the only items a human must adjudicate), and confusion hotspots, resolving fuzzy boundaries with deterministic rules. Use when the user wants to label/tag exam questions by topic & subtopic, build or validate a gold standard for LLM-classifier evaluation, measure classification accuracy or inter-rater agreement, find which taxonomy boundaries are ambiguous, or run topic-coverage analysis on a math competition test (mathleague, AMC, MATHCOUNTS, AIME, etc.). Trigger on "classify this test/exam", "tag questions by subtopic", "build a gold standard", "classification accuracy", "label this exam", "topic coverage of this test", "cross-validate the labels". Ships a 54-subtopic math taxonomy, deterministic disambiguation rules, per-subtopic key-point rules, and a consensus/accuracy script — the math taxonomy is swappable for any domain.
---

# exam-classifier

Classify the questions in a real exam into a topic+subtopic taxonomy, and produce
an honest **classification-accuracy** number — without an answer key — by using
**multi-agent consensus**: several independent raters label the same questions,
the majority is the gold standard, and disagreements become deterministic rules.

## When to use
A user hands you a test PDF (or a folder of them) and wants the questions tagged
by subtopic, a coverage/blueprint, OR a measure of how reliable that tagging is.
This is also the method for evaluating *any* LLM classifier when there is no
ground-truth label set.

## Assets (in this skill dir)
- `assets/taxonomy.json` — 7 topics / 54 subtopics (math competition; swappable).
- `assets/rules.md` — tie-breaks + **deterministic boundary rules** (read this before labeling).
- `assets/keypoints.json` — a one-line teaching rule per subtopic (handy for a learning guide).
- `scripts/consensus.py` — computes consensus, per-rater accuracy, confusion hotspots, the human-review tail.
- `examples/` — three sample rater files you can run `consensus.py` on.

## Workflow

1. **Read the test.** Open the PDF question pages (skip cover, bubble sheet,
   answer key, solutions). Note the rounds/sections and number each question with
   a stable `ref` (e.g. `NS-1`, `SP-12`, `TG-3`, `TM-7`).

2. **Spawn N≥3 INDEPENDENT classifier agents.** Give each the *same* prompt:
   the PDF, the full subtopic list from `assets/taxonomy.json`, and the rules from
   `assets/rules.md`. Each agent must **solve-then-label** (per the primary-label
   rule): briefly sketch the solution, name the single decisive step, then assign
   the primary subtopic = the topic of *that step* — labeling by **solving method,
   not surface appearance** (this is what stops a disguised algebra-as-geometry or
   number-theory-as-algebra problem from being mislabeled). It writes
   `rater_<X>.json` = a JSON list of `{"ref": "...", "subtopic_id": "...",
   "key_step": "...", "secondary": "..."}` (key_step/secondary optional but
   recommended). Independence matters — do not let them see each other's output.

3. **Run consensus.** `python scripts/consensus.py rater_*.json`. This prints:
   - **topic** + **subtopic** agreement (unanimous / has-majority / no-consensus),
   - each rater's **accuracy vs the consensus** (your classifier's score),
   - the **no-consensus tail** — the only items a human must adjudicate,
   - the **top confusion pairs** — where the taxonomy is fuzzy.
   It writes `gold.json` (the consensus label per question).

4. **Adjudicate the tail.** A human (or a senior judge agent) resolves only the
   handful of no-consensus items. Everything else is auto-accepted.

5. **Sharpen the worst boundary.** Take the #1 confusion pair, write a
   deterministic `IF … → A, ELSE → B` rule into `assets/rules.md`, re-run the
   raters, and confirm subtopic accuracy climbs. (In the reference build this one
   move lifted subtopic accuracy 67% → 91%.) Repeat until only the irreducible
   ambiguous tail remains.

## What "good" looks like
- **Topic** agreement ~99% is normal and easy.
- **Subtopic** agreement is the real test; with sharp rules it lands ~90%+.
- A residual **~2–3%** no-consensus tail is the natural ceiling — those questions
  are genuinely cross-subtopic. Don't force them.

## Output to give the user
The labeled gold set (`gold.json`), the accuracy report, the confusion hotspots,
and any new rule you added. Optionally render a coverage blueprint or a
key-point learning guide from `assets/keypoints.json`.

## Adapting to another domain
Swap `assets/taxonomy.json` for your own topic/subtopic list and replace the
math-specific lines in `assets/rules.md`. The consensus method and
`scripts/consensus.py` are domain-agnostic.
