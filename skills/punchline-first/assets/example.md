# Worked example: the same request, with and without this skill

## Request

「新機能の検討状況を資料にまとめて」 (Summarize the state of the
new-feature discussion as a document.)

## Without the skill (slop)

A five-section document appears: background of the feature area, market
overview, three candidate features described at equal length, a
technology note, and "next steps: continue discussion". Nothing is
ranked, the ask is nowhere, and the reviewer must ask what the document
wants. Review fixes: well over ten.

## With the skill

**Step 0 — punchline (agreed first):**
「候補3案のうち、B案の先行開発を承認いただきたい。決め手は工数が
A案の半分で、検証したい仮説が一番大きいこと」

**Step 1 — bullets:**
- Decision wanted: approve starting B first
- Conclusion: B > A > C for a first build
- Evidence: effort estimate (B = 0.5× A, source: dev team estimate
  2026-11-20); hypothesis size (B tests the retention question the
  team has open); C is blocked on an external API decision
- Out of scope: pricing, launch timing

**Step 2 — structure:**
1. Punchline (title + first line)
2. Why B first (the two evidence points)
3. What approving means (scope, first milestone)
- Supplement: full comparison table of A/B/C, market background,
  technology notes, risks and mitigations

**Step 4 — gates:** every paragraph explainable by the author; a
reviewer's plausible fixes are wording-level, not structural; every
section argues for B-first or supports the decision.

The main text fits on one page. Everything else is in the supplement,
where a challenger can find it — and a decider never has to wade
through it.
