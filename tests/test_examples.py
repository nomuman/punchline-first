"""Validate examples and anchors: schema, coverage, value ranges."""
import glob
import json
import os
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")


class TestAnchors(unittest.TestCase):
    def test_anchor_files(self):
        for path in glob.glob(os.path.join(ROOT, "skills/punchline-first/anchors/*.json")):
            with open(path, encoding="utf-8") as f:
                anchors = json.load(f)
            self.assertEqual(sorted(anchors.keys()), ["1", "2", "3", "4", "5"], path)
            for lvl, texts in anchors.items():
                self.assertEqual(len(texts), 6, f"{path} level {lvl}")
                self.assertTrue(all(isinstance(t, str) and t for t in texts))


class TestExamples(unittest.TestCase):
    def test_reaction_files(self):
        for path in glob.glob(os.path.join(ROOT, "examples/reactions-*.json")):
            if path.endswith(".scores.json"):
                continue
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            self.assertTrue(data["punchline"], path)
            self.assertGreaterEqual(len(data["readers"]), 3, path)
            for r in data["readers"]:
                self.assertTrue(r["persona"] and r["takeaway"] and r["reaction"], path)

    def test_scores_match_verdicts(self):
        bad = json.load(open(os.path.join(ROOT, "examples/reactions-bad.scores.json"),
                             encoding="utf-8"))
        good = json.load(open(os.path.join(ROOT, "examples/reactions-good.scores.json"),
                              encoding="utf-8"))
        self.assertFalse(bad["pass"])
        self.assertTrue(good["pass"])
        self.assertGreater(good["mean_conviction"], bad["mean_conviction"])
        self.assertGreater(good["mean_recall"], bad["mean_recall"])


if __name__ == "__main__":
    unittest.main()
