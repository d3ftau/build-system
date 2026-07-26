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

When I do, write EXPLORE.md: each claim, what I found, and a verdict —
**CONFIRMED**, **WRONG** (with what's actually true), or **UNRESOLVED**.
Anything left UNRESOLVED is a bet, and must say what it costs if it's wrong.
/contract and /plan both read this file. A bet that survives into the build
gets resolved first, before anything that assumes its answer.
