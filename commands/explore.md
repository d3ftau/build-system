Read BRIEF.md and DESIGN.md. Don't write a spec, don't plan, don't code.

Your job is to find every claim about the outside world this build rests on,
and turn each into something I can go and check myself. Not to answer them.

A load-bearing external claim is anything about:

- What an external service, app, or API can or cannot do — including tier
  limits, rate limits, and whether a feature exists on the free plan
- What real data actually looks like: its format, its fields, whether the thing
  the build depends on is even present in it
- Whether an export, integration, or permission actually works for my account,
  as opposed to working in general

For each one, give me:

1. The claim as it currently stands, quoted from BRIEF.md or DESIGN.md
2. What gets built differently — or built at all — if it turns out false
3. Exactly how I check it: a direct link to the specific feature, pricing, or
   API page, or the concrete physical action ("request the export, open the
   zip, tell me whether each message records who wrote it")

Rank them. Anything that invalidates a design choice or adds a whole subsystem
if it's wrong goes first.

## The second kind: claims about your own judgment

Separately, list every claim the build rests on about **how well a model will
judge something** — that you can reliably tell one category of text from
another, spot intent, score relevance, detect that a decision was made, or
classify tone. These are as load-bearing as anything about an API, and they
are more dangerous, because they arrive already dressed as architecture.

The tell: a sentence in DESIGN.md that reads like a settled conclusion about
structure ("the load-bearing signal is X, so every record must carry X") but
is actually a prediction about a classifier's accuracy on messy real text that
nobody has run.

These do not go on my list to check — I cannot settle them by clicking
anything, and neither can you by thinking harder about them. For each:

1. The claim, quoted, and the structure that currently depends on it — the
   field, the validation rule, the rejection reason, the pipeline stage.
2. **The smallest real test that would settle it**: usually a handful of
   genuine examples run through the actual prompt. Name the number and where
   the examples come from.
3. What survives if it's false. Be specific about whether the mechanism
   adjusts or disappears.

Then find your own counterexample before I have to. Take the claim and try to
break it against one concrete, realistic case — not a clean one. If you can
break it in a sentence, the claim was never sound and no amount of structure
built on top will fix it. **When a counterexample lands, question whether the
mechanism should exist at all before you reach for a special case to
accommodate it.** Adding a category, an enum value, or an escape hatch to a
mechanism that just failed its first real test keeps a broken idea alive by
making it more complicated.

Every one of these is a BET — they cannot be CONFIRMED by looking, only by
running something. Which means the ones that invalidate the build get the
smallest-slice treatment below, and they get it before any schema, validation
rule, or dedicated failure mode is written around them.

**Do not answer these from what you already know.** Your training data is stale
on product features, pricing, and free-tier limits, and a marketing page won't
tell me what a free tier actually does in practice. Your recall and sales copy
are both worth less than me spending ten minutes clicking. Where a
documentation page genuinely settles something, cite it — but say plainly that
it's documentation, not something either of us watched work.

The single most expensive kind of error here is asserting that some product
category can't do a thing, when a five-minute look would show it's a standard
feature. That mistake doesn't just pick the wrong option — it invents a whole
subsystem to work around a limitation that was never real.

Then stop and wait. I'll go look and report back.

When I do, write EXPLORE.md. Each claim gets one of four verdicts:

- **CONFIRMED** — checked against the real thing. Say what was actually looked
  at.
- **WRONG** — checked, and false. Record what's actually true; the spec gets
  written against that.
- **BLOCKED** — not checked yet, but checkable. The check is now the next
  action, and nothing that assumes the answer gets built until it lands. If
  the check is slow to come back (a scheduled export, a delivery window),
  start it immediately and work on something independent meanwhile — never
  proceed on the assumption to fill the time.
- **BET** — genuinely cannot be settled without building something. Must state
  what it costs if it's wrong.

**Something is only a BET if checking it is impossible, not inconvenient.**
Slow, fiddly, needs-an-account, needs-me-to-click-through-a-signup — all still
BLOCKED. If you find yourself writing a justification for why a checkable
thing can be assumed instead, that justification is the error; delete it and
mark it BLOCKED.

For each BET, say plainly which it is:

- Wrong is survivable — the build adjusts, nothing already written gets
  thrown away. Proceed, and note it.
- Wrong invalidates the build — then the smallest possible thing that tests
  it gets built first, everything around it faked, before any real work
  depends on it. Never "build it and find out at the end."
- Wrong kills the build and can't be tested cheaply — say so directly. That's
  a fact about the project, not a task to sequence, and I need to decide
  whether it's worth starting at all.

/contract and /plan both read this file.
