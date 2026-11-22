---
name: punchline-first
description: "Write documents that cannot become AI slop. Use whenever drafting or revising a document, proposal, report, spec, slide outline, or business summary for a human reader — especially when the user asks for a document without first stating its point. Enforces one workflow: fix the punchline before any drafting, build the body only to support it, demote every detail to a supplement, pass three anti-slop gates, and finish with a scored reader loop (SSR) that must clear its thresholds before delivery."
---

# Punchline-First Writing

A document fails in one way: it was generated before its point was decided.
This skill fixes the order. **No punchline, no document.**

## The one rule

Every document has exactly **one punchline**: the single sentence the
reader must walk away with — what you want decided, approved, or
understood. It is never dropped, never buried, and never diluted.
**All details go to the supplement** (補足): caveats, background, data
tables, edge cases, and process notes live in a clearly marked
supplement or appendix, not in the main flow.

If the punchline cannot be written in one sentence, the document is not
ready to draft. Stop and align first (see Step 0).

## Workflow

### Step 0 — Punchline gate

Write the punchline in one sentence, in this shape:

> [Reader] should [decide / approve / understand] [what], because
> [the one strongest reason].

Show it to the user and get agreement before anything else. If the user
cannot settle the punchline, do not draft: fall back to a bullet list of
what the document must contain, and if even that fails, recommend an
alignment conversation instead of a document. Generating text to "see
how it feels" is how slop is born.

### Step 1 — Bullets before prose

List, as bullets only:

- The decision or understanding the document must produce
- The conclusion
- The 2–4 strongest pieces of evidence (each with its source)
- What is explicitly out of scope

The user approves the bullets. Bullets are cheap to fix; prose is not.

### Step 2 — Structure that serves the punchline

Build the outline so every section exists to support the punchline.
Apply the demotion test to every candidate section or paragraph:

- Does the reader need this to accept the punchline? → main text
- Is it needed only if challenged? → supplement
- Is it background, history, or completeness for its own sake? →
  supplement, or cut

The punchline itself appears as the title or the first line. Conclusion
first, always.

### Step 3 — Draft

Write the body from the approved bullets, in the approved structure.
Keep the main text to what the demotion test passed. Write the
supplement after the main text, and label it plainly (補足).

### Step 4 — Three anti-slop gates (all must pass before delivery)

1. **Explainability**: the author (or the user) can explain every
   paragraph in their own words, out loud, without reading it. Any
   paragraph nobody can explain gets rewritten or cut.
2. **Ten-fix test**: would a reviewer plausibly need 10 or more fixes?
   If yes, the draft is not ready — return to Step 1, not to polishing.
3. **Direction**: every section points at the punchline. A section that
   argues a different document's point is cut or moved to the
   supplement.

Also check: facts and opinions are distinguishable; every number has a
source; no section exists only because "documents usually have one".

### Step 5 — Scored reader loop (SSR)

Do not ship on a feeling. Score the document with synthetic readers,
the way SSR scores purchase intent:

1. Create 3–5 reader personas matching the real audience (the decider,
   a sceptic, an implementer, a budget holder).
2. Each reader reads **only the main text** and writes, in free text:
   their takeaway ("what this document wants, in my words") and their
   reaction (would they approve / accept it, and why).
3. Run the scorer:

   ```
   uv run --with fastembed --with numpy \
     python scripts/score_document.py reactions.json --lang ja
   ```

   It reports, per reader: **recall** (cosine similarity between the
   takeaway and the punchline — did the point land?) and **conviction**
   (an SSR score of the reaction against anchors). Pick the anchors
   that match what the document asks of its reader: `--anchors approval`
   (default) for decision documents, `--anchors understanding` for
   explanatory ones. For explanatory documents recall is the primary
   gate; a conviction around 3 there means "understood, with open
   questions" — read the reactions before grinding more rounds.
4. Gates (defaults): mean conviction ≥ 3.8, mean recall ≥ 0.70, and
   min recall ≥ 0.55. If the verdict is REVISE, fix the **structure
   and bullets** (Steps 1–2), never just the wording, and re-run with
   fresh readers. At most 3 rounds; if the score plateaus, report the
   plateau honestly instead of grinding.

Synthetic readers are a smoke test, not a substitute for a real reader
on a high-stakes document — the same caveat SSR carries. Scores
compress at both ends, so treat the gates as relative: a document that
cannot pass them has a structural problem, whatever its prose quality.

## Design gate — no AI-default look (slides and visuals)

A document's design is also an argument. The moment a deck *looks*
AI-generated, the reader discounts the content — the visual equivalent
of slop. The model's defaults are a statistical average, not a design
decision, and they are recognisable on sight.

Before building any slide or visual, declare three things in writing:
(1) the subject's own world (its brand, product, physical context),
(2) one committed design direction in a single line, and (3) a palette
and typefaces with roles, each traceable to (1). If a choice cannot be
traced to the subject, it is a default — replace it.

**The AI-default look — never ship these unless the brief demands them:**

- Cream / beige background with a terracotta-orange accent (the
  current house default of AI tools, the clay family around #D97757)
- Purple or blue gradients on white
- A small-caps "eyebrow" label above every heading
- Rows of identical rounded cards with soft shadows; cards inside cards
- A coloured accent stripe down the side of every slide or card
- Inter / Roboto / system fonts as the only typeface; everything
  centred; 01/02/03 numbering on content that is not a sequence;
  emoji used as icons

**Instead:**

- Typography with a point of view: a display face chosen for the
  subject, paired with a quiet body face
- One dominant colour with a sharp accent, not an evenly timid palette
- At least one layout that breaks the grid — scale, overlap, asymmetry,
  or deliberate density
- Texture and detail taken from the subject itself (for a notebook
  product: ruled lines, date stamps, the physical page), never generic
  "warm paper" atmosphere

**Delivery check:** if the subject's name were swapped for another
product's, would the design work unchanged? If yes, it is a template.
Return to the design decision, not to decoration.

(The user's or brand's explicit brief always wins over this list —
including when it asks for one of the looks above.)

## Punchline patterns (Japanese business documents)

- Decision: 「Xを承認いただきたい。理由はYで、見送るとZが起きる」
- Report: 「結論、Aは失敗した。原因はB。再発防止はCまでやる」
- Proposal: 「AではなくBを推す。決め手はC、コストはD」
- Status: 「予定通りではない。遅れはE、回復策はF、判断が要るのはG」

## Anti-patterns (slop signals)

- Opens with background or history instead of the conclusion
- Comprehensive coverage with no ranking ("網羅したが結論がない")
- Sections at different temperatures — one detailed, one hand-waved
- Numbers without sources; adjectives doing the work of evidence
- The real ask appears for the first time on the last page
- A supplement's content promoted into the main text "just in case"

## Notes for the agent

- Enforce the order even when the user asks to "just draft it": return
  the punchline and bullets first — that *is* the fastest route.
- The user's corrections to the punchline outrank everything else in
  this skill.
- Keep the main text short on purpose. Length is not thoroughness;
  the supplement is where thoroughness lives.
