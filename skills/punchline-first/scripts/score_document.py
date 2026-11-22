#!/usr/bin/env python3
"""Score a document the SSR way: synthetic readers, free-text reactions,
embedding-based scoring, iterate until it passes.

Input JSON:
{
  "punchline": "the one sentence the document must land",
  "readers": [
    {"persona": "busy division manager",
     "takeaway": "what the reader says the document wants, in their words",
     "reaction": "the reader's free-text reaction to the document"}
  ]
}

Two scores per reader:
- recall: cosine similarity between the reader's takeaway and the
  punchline (did the point land?)
- conviction: SSR expected score of the reaction against approval
  anchors (would they approve / accept it?)

Verdict (defaults): PASS when mean conviction >= 3.8, mean recall
>= 0.70, and min recall >= 0.55. Thresholds are configurable because
SSR scores compress at both ends; treat them as relative gates, not
absolute truth.

Usage:
  uv run --with fastembed --with numpy python score_document.py reactions.json [--lang ja|en]
"""
import argparse
import json
import os
import sys

import numpy as np
from fastembed import TextEmbedding

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
T = 10


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--lang", default="ja", choices=["ja", "en"])
    ap.add_argument("--anchors", default="approval",
                    choices=["approval", "understanding"],
                    help="approval: decision documents; understanding: explanatory documents")
    ap.add_argument("--pass-conviction", type=float, default=3.8)
    ap.add_argument("--pass-recall", type=float, default=0.70)
    ap.add_argument("--pass-min-recall", type=float, default=0.55)
    args = ap.parse_args()

    data = json.load(open(args.input, encoding="utf-8"))
    anchors = {int(k): v for k, v in json.load(
        open(os.path.join(HERE, "..", "anchors", f"{args.anchors}_{args.lang}.json"),
             encoding="utf-8")).items()}

    model = TextEmbedding(model_name=MODEL)
    cache: dict[str, np.ndarray] = {}

    def embed(texts):
        todo = [t for t in texts if t not in cache]
        for i in range(0, len(todo), 32):
            chunk = todo[i:i + 32]
            for t, v in zip(chunk, model.embed(chunk)):
                e = np.array(v, dtype=np.float64)
                cache[t] = e / np.linalg.norm(e)
        return np.array([cache[t] for t in texts])

    def ssr(text: str) -> tuple[float, list[float]]:
        a_texts, a_levels = [], []
        for lvl in range(1, 6):
            for t in anchors[lvl]:
                a_texts.append(t)
                a_levels.append(lvl)
        A = embed(a_texts)
        x = embed([text])[0]
        sims = A @ x
        level_sims = [float(np.mean(sims[[j for j, l in enumerate(a_levels) if l == lvl]]))
                      for lvl in range(1, 6)]
        w = np.power(np.clip(np.array(level_sims), 0.01, None), T)
        pmf = w / w.sum()
        return float(np.dot(pmf, np.arange(1, 6))), [round(float(p), 3) for p in pmf]

    punch_vec = embed([data["punchline"]])[0]
    rows = []
    for r in data["readers"]:
        recall = float(embed([r["takeaway"]])[0] @ punch_vec)
        conviction, pmf = ssr(r["reaction"])
        rows.append({"persona": r["persona"], "recall": round(recall, 3),
                     "conviction": round(conviction, 2), "pmf": pmf})
        print(f"{r['persona']}: recall {recall:.3f} / conviction {conviction:.2f}")

    mean_recall = float(np.mean([r["recall"] for r in rows]))
    min_recall = float(np.min([r["recall"] for r in rows]))
    mean_conv = float(np.mean([r["conviction"] for r in rows]))
    passed = (mean_conv >= args.pass_conviction and mean_recall >= args.pass_recall
              and min_recall >= args.pass_min_recall)
    print(f"\nmean recall {mean_recall:.3f} (min {min_recall:.3f}) / "
          f"mean conviction {mean_conv:.2f}")
    print("VERDICT:", "PASS" if passed else "REVISE — return to the bullets, not to polishing")
    json.dump({"rows": rows, "mean_recall": round(mean_recall, 3),
               "min_recall": round(min_recall, 3),
               "mean_conviction": round(mean_conv, 2), "pass": passed},
              open(os.path.splitext(args.input)[0] + ".scores.json", "w"),
              ensure_ascii=False, indent=1)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
