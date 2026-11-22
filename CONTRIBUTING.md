# Contributing

Contributions welcome — especially:

- **Reader-reaction sets for new document types** (proposals, incident
  reports, specs): add `examples/reactions-<type>.json` with a
  punchline, 3–5 reader personas, takeaways and reactions, plus the
  `.scores.json` produced by the scorer. The bad/good pair format in
  `examples/` is the template.
- **Approval anchors in more languages**: mirror
  `anchors/approval_ja.json` (5 levels × 6 statements each). Keep the
  statements natural for a manager deciding on a document, and keep the
  level semantics aligned across languages.
- **Workflow improvements**: open an issue first if the change alters
  the order of the steps — the order is the point of this skill.

Run `python -m unittest discover -s tests` before submitting.
