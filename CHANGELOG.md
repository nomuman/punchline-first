# Changelog

## 0.4.0 — 2026-11-23

- Deck content checks for slides: title–chart agreement, say it
  once (no triple restatement), reuse the deck's framework, same
  level same grammatical form. Distilled from @fujikururi's
  「スライドの『AIっぽさ』図解」; the visual deck-level checks live
  in the companion skill design-urawaza (Part 3, v0.2.0).

## 0.3.0 — 2026-11-22

- Design gate for slides and visuals: declare the design from the
  subject (its world, one committed direction, palette + typefaces
  with roles) before building; a blocklist of the AI-default look
  (cream + terracotta, purple gradients, eyebrow labels, identical
  rounded cards, side stripes, default fonts); and a swap-the-name
  delivery check. Borrowed from frontend-slides, hallmark, and
  Anthropic's frontend-design skill.
- Prompted by a live failure: this skill's own demo deck shipped with
  four of the blocklisted tells at once.


## 0.2.0 — 2026-11-22

- Understanding anchors (Japanese + English) for explanatory documents:
  `--anchors understanding`. Validated for discrimination on the repo
  examples (bad draft 2.30 vs punchline-first draft 3.77).
- Field note from a live trial: on an explanatory document whose
  readers understood the point (recall 0.84) but kept one substantive
  objection (no measured data), conviction plateaued at ~2.8 under
  both anchor sets — the loop correctly refused to reward polishing
  over missing evidence.


## 0.1.0 — 2026-11-22

- Initial release: the punchline-first workflow (punchline gate, bullets
  before prose, demotion test, three anti-slop gates).
- Scored reader loop (SSR): `scripts/score_document.py` with approval
  anchors in Japanese and English; worked examples with real scores
  (bad draft REVISE 0.583/2.19, punchline-first draft PASS 0.839/3.92).
