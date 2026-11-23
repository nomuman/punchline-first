# punchline-first

[![CI](https://github.com/nomuman/punchline-first/actions/workflows/ci.yml/badge.svg)](https://github.com/nomuman/punchline-first/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

English | [日本語版 README](README.ja.md)

**An agent skill that makes AI slop structurally impossible.**
Documents fail in one way: they are generated before their point is
decided. This skill fixes the order — and then *scores* the result.

## The problem

Managers drowning in AI-generated documents ("AI slop") use a simple
triage. Send it back when any of these holds:

1. The reviewer would need **10 or more fixes**
2. The author **cannot explain** their own document
3. The **direction is off** — it argues the wrong point

Endless feedback loops on slop waste everyone's time. The fix is not
better prompting for prettier prose. It is a process that makes a
pointless document impossible to finish.

## The one rule

Every document has exactly **one punchline** — the single sentence the
reader must walk away with. It is never dropped, never buried.

**All details go to the supplement.** Caveats, background, data tables,
edge cases: a clearly marked supplement (補足), not the main flow.
The main text carries only what the punchline needs.

## The workflow

0. **Punchline gate** — one sentence, agreed before any drafting.
   Can't write it? No document yet: bullets first, then an alignment
   conversation if even bullets fail.
1. **Bullets before prose** — decision wanted, conclusion, strongest
   evidence with sources, out-of-scope. Approved before drafting.
2. **Structure** — every section must serve the punchline; the
   demotion test sends everything else to the supplement.
3. **Draft** — conclusion first; punchline as title or first line.
4. **Three anti-slop gates** — explainability, the ten-fix test,
   direction (see the triage above, applied to yourself).
5. **Scored reader loop** — synthetic readers + SSR scoring. Below.

## The scored reader loop (SSR)

Borrowed from [ssr-lab](https://github.com/nomuman/ssr-lab): instead of
asking "is this document good?", give it to 3–5 synthetic reader
personas. Each reads only the main text and writes a free-text
**takeaway** and **reaction**. The scorer then measures:

- **Recall** — cosine similarity between the reader's takeaway and the
  punchline. Did the point land?
- **Conviction** — an SSR score of the reaction against approval
  anchors (Semantic Similarity Rating: free text → Likert via
  embeddings, running locally).

Gates: mean conviction ≥ 3.8, mean recall ≥ 0.70, min recall ≥ 0.55.
Fail → fix the structure, not the wording, and re-run. Max 3 rounds.

Real run, on this repo's own examples (4 readers each):

| Document | Mean recall | Mean conviction | Verdict |
| --- | --- | --- | --- |
| Background-first draft (`examples/sample-doc-bad.md`) | 0.583 | 2.19 | REVISE |
| Punchline-first draft (`examples/sample-doc-good.md`) | 0.839 | 3.92 | PASS |

The budget-holder reader scored lowest even on the good draft (3.14 —
"approvable, but show me the money figures next time"), which is
exactly the kind of signal the loop exists to surface.

## Install

```
npx skills add nomuman/punchline-first
```

or copy `skills/punchline-first/` into your agent's skills directory
(Claude Code, Codex, Cursor, and other skills-compatible agents).
The scorer runs locally with fastembed: no API key, and your documents
never leave your machine.

## Score a document yourself

```
# 1. Write reactions.json: punchline + readers (takeaway + reaction)
# 2. Score it
uv run --with fastembed --with numpy \
  python skills/punchline-first/scripts/score_document.py \
  examples/reactions-good.json --lang ja
```

Anchors ship in Japanese and English, in two flavours matched to what
the document asks of its reader: `approval_*` for decision documents
(default) and `understanding_*` for explanatory ones
(`--anchors understanding`).

## Design notes — what we borrowed from popular skills

- **Staged workflow with a reader test** — from Anthropic's
  `doc-coauthoring` (context → structure → reader test). We made the
  reader test *scored* instead of impressionistic.
- **A rubric you can fail** — from `stop-slop`'s scoring idea: our
  three gates and the SSR thresholds are pass/fail, not vibes.
- **A named anti-pattern list** — from `humanizer`'s pattern approach:
  slop signals are enumerated in the skill so the agent can check
  against them.
- **Process before production** — from `superpowers`
  (brainstorming / writing-plans): settle the design before generating
  the artefact.
- **An anti-AI-default design gate** — from `frontend-slides`
  (32.7K stars; curated styles against generic AI aesthetics),
  `hallmark` (~46.5K stars; names the cream background + eyebrow
  label + card look as the tell), and Anthropic's `frontend-design`
  (commit to the subject's own direction; even flags the terracotta
  clay accent as a tell). Our skill applies the same thinking to
  slides: declare the design from the subject, blocklist the
  defaults, and run a swap-the-name delivery check.
- **The manager's triage** — the 10-fix / can't-explain / wrong-direction
  rules circulating among managers reviewing AI documents, turned into
  self-checks for the author.
- **Deck content checks** (0.4.0) — title–chart agreement, say it
  once, reuse the deck's framework, same level same form — from
  @fujikururi's 「スライドの『AIっぽさ』図解」
  (https://x.com/fujikururi/status/2124647602448982268). The visual
  deck-level checks from the same source live in the companion
  skill design-urawaza.

## Repository layout

```
skills/punchline-first/
  SKILL.md          the workflow (the skill itself)
  scripts/          score_document.py — the SSR reader-loop scorer
  anchors/          approval anchors, Japanese + English
  assets/           a worked before/after example
examples/           sample documents + reader reactions + their scores
tests/              dataset/anchor validation
```

## Limitations

- Synthetic readers are a smoke test. For a high-stakes document they
  complement — never replace — a real reader.
- SSR scores compress at both ends; the gates are relative signals
  that a document has a structural problem, not absolute grades.
- The workflow cannot supply a point you do not have. If the punchline
  gate fails, the honest output is "talk first", and the skill says so.

## License

MIT
