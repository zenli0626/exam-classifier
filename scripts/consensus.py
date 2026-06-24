#!/usr/bin/env python3
"""Multi-rater consensus + classification-accuracy report.

The core of the exam-classifier skill: take several INDEPENDENT rater labelings
of the same questions, treat the majority label as the gold standard, and report
how well each rater (and the set as a whole) matches it — plus the confusion
hotspots that tell you which taxonomy boundaries to sharpen.

Usage:
    python consensus.py rater_A.json rater_B.json rater_C.json [...]

Each rater file is EITHER:
  - a JSON list of {"ref": "NS-1", "subtopic_id": "arith.ops"}, OR
  - a JSON object {"<set>": [ {"ref":..., "subtopic_id":...}, ... ], ...}
    (refs are auto-prefixed with the set name so multiple sets can be pooled).

Writes gold.json (the consensus label per question + the raw votes).
Prints: topic & subtopic agreement, per-rater accuracy vs consensus,
the no-consensus tail (the only items a human must adjudicate), and the
top confusion pairs (candidates for a new deterministic rule in rules.md).
"""
import json, sys
from collections import Counter


def load(path):
    d = json.load(open(path))
    if isinstance(d, dict):                       # {"set": [...], ...}
        out = {}
        for s, items in d.items():
            for e in items:
                out[f"{s}:{e['ref']}"] = e["subtopic_id"]
        return out
    return {e["ref"]: e["subtopic_id"] for e in d}  # flat list


def topic(sid):
    return sid.split(".")[0] if sid else "?"


def main(files):
    raters = [load(f) for f in files]
    names = [f.rsplit("/", 1)[-1].replace(".json", "") for f in files]
    refs = sorted(set().union(*[set(r) for r in raters]))
    R = len(raters)
    sub_un = sub_maj = sub_none = top_un = top_maj = N = 0
    acc = [0] * R; tacc = [0] * R
    conf = Counter(); gold = {}

    for ref in refs:
        labs = [r.get(ref) for r in raters]
        if any(l is None for l in labs):           # rater skipped this item
            continue
        N += 1
        top = Counter(labs).most_common(1)[0]
        sub_un += top[1] == R
        sub_maj += 2 <= top[1] < R
        sub_none += top[1] == 1
        cons = top[0] if top[1] >= 2 else None
        gold[ref] = {"gold": cons, "votes": labs, "has_consensus": top[1] >= 2}
        for i, l in enumerate(labs):
            acc[i] += bool(cons and l == cons)
        tl = [topic(l) for l in labs]
        tt = Counter(tl).most_common(1)[0]
        top_un += tt[1] == R
        top_maj += 2 <= tt[1] < R
        tcons = tt[0] if tt[1] >= 2 else None
        for i, l in enumerate(tl):
            tacc[i] += bool(tcons and l == tcons)
        if len(set(labs)) > 1:
            ds = sorted(set(labs))
            for i in range(len(ds)):
                for j in range(i + 1, len(ds)):
                    conf[f"{ds[i]} <-> {ds[j]}"] += 1

    if not N:
        print("No overlapping items across raters."); return
    p = lambda x: f"{100*x/N:5.1f}%"
    print(f"\n{R} raters · N={N} questions\n" + "=" * 52)
    print("TOPIC     unanimous %s | has-majority %s | none %s"
          % (p(top_un), p(top_un + top_maj), p(N - top_un - top_maj)))
    print("  per-rater accuracy vs consensus: "
          + "  ".join(f"{names[i]} {p(tacc[i])}" for i in range(R)))
    print("SUBTOPIC  unanimous %s | has-majority %s | none %s"
          % (p(sub_un), p(sub_un + sub_maj), p(sub_none)))
    print("  per-rater accuracy vs consensus: "
          + "  ".join(f"{names[i]} {p(acc[i])}" for i in range(R)))
    print("\nTOP CONFUSION PAIRS  (each is a candidate for a deterministic rule):")
    for k, v in conf.most_common(12):
        print(f"  {v:3d}  {k}")
    tail = [r for r, g in gold.items() if not g["has_consensus"]]
    print(f"\nNO-CONSENSUS TAIL — the only {len(tail)} items needing human review:")
    for r in tail:
        print(f"  {r}: {gold[r]['votes']}")
    json.dump(gold, open("gold.json", "w"), indent=2)
    print("\nWrote gold.json (consensus label + votes per question).")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    main(sys.argv[1:])
