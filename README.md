# exam-classifier

A [Claude Code](https://claude.com/claude-code) **skill** that classifies the
questions in a real exam/test into a topic + subtopic taxonomy, and produces an
honest **classification-accuracy** number *without an answer key* — by using
**multi-agent consensus**.

It answers the question every LLM-evaluation effort eventually hits:

> *"If several agents each label the data differently, whom do you trust? And if
> one agent scores higher, how do you know what it did right?"*

**You don't trust any single agent. You trust the consensus, and you turn every
recurring disagreement into a deterministic rule.**

## The idea

```
N independent agents label the same questions
        │
        ▼
Majority label  =  gold standard
        │
        ├── ≥2/N agree  → auto-accept            (~85–98% of items)
        └── all differ  → human adjudicates      (~2–3% — the only manual work)
        │
        ▼
Disagreement analysis  →  confusion hotspots
        │
        ▼
The #1 hotspot is usually ONE fuzzy definition.
Write a deterministic rule for it  →  re-run  →  accuracy jumps.
        │
        ▼
Self-improving gold standard: each fix is permanent; humans only ever
touch the shrinking irreducible tail.
```

In the reference build (math-competition tests), sharpening a **single** fuzzy
boundary lifted subtopic-classification accuracy **67% → 91%** with no model
change. Topic-level accuracy was ~99% throughout; ~2.3% of questions are
genuinely cross-subtopic (the natural ceiling).

## What's inside

| File | What it is |
|---|---|
| `SKILL.md` | The skill definition + the step-by-step workflow Claude follows |
| `assets/taxonomy.json` | 7 topics / 54 subtopics (math competition — **swappable** for any domain) |
| `assets/rules.md` | Tie-breaks + deterministic boundary rules (the gold standard's growing rulebook) |
| `assets/keypoints.json` | A one-line teaching rule per subtopic |
| `scripts/consensus.py` | Consensus + accuracy + confusion-hotspot report (domain-agnostic) |
| `examples/` | Three sample rater files to try the script on |

## Install

```bash
git clone https://github.com/zenli0626/exam-classifier ~/.claude/skills/exam-classifier
```

Then in Claude Code just say *"classify this test"* / *"tag these questions by
subtopic"* / *"what's our classification accuracy"* and the skill triggers, or
invoke it directly with `/exam-classifier`.

## Try the consensus script standalone

```bash
cd ~/.claude/skills/exam-classifier
python scripts/consensus.py examples/rater_A_sample.json examples/rater_B_sample.json examples/rater_C_sample.json
```

You'll get the agreement metrics, per-rater accuracy vs consensus, the confusion
pairs, and the no-consensus tail — written to `gold.json`.

## Adapting to another domain

Swap `assets/taxonomy.json` for your own topic/subtopic list and edit the
domain-specific lines in `assets/rules.md`. The consensus method and
`scripts/consensus.py` don't care what you're classifying.

## License

MIT — see [LICENSE](LICENSE).
