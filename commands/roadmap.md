Read DISCOVERY.md (or the pasted discovery conversation above). Write
ROADMAP.md for this product.

## What this is
Two sentences.

## The spine
The one capability everything else hangs off. If there isn't one, say so —
that's a sign this is several products, not one.

## Builds, in order
For each: what it delivers, and critically — "if nothing after this ever got
built, would this still be worth using?" Answer honestly for each one. Any
build where the answer is no needs re-scoping or merging with the next.

That test only catches a build that is **too small**, and its only remedy is
to grow one. Used alone it ratchets in one direction forever, so every build
also gets the inverse:

**"What is the smallest part of this build that still earns a yes?"**

If the answer is smaller than the build you just wrote, that smaller thing
*is* the build, and everything else moves to the next one. Do not answer this
for the bundle as a whole — a bundle earns a yes on the strength of its best
component while carrying everything else along unexamined. Take the pieces
apart and find the smallest one that stands up alone.

**Build 1 contains only what is needed to test the spine.** Nothing else, no
matter how obviously useful, how small it seems, or how naturally it follows.
You named the spine two sections ago as the one capability everything hangs
off — which means everything else is either plumbing around it or a separate
bet, and neither belongs in the build whose whole job is finding out whether
the spine works. Where something is genuinely required to evaluate the spine,
say why in one line.

Then, for each build, list what you cut and where it went. A build that cut
nothing was not examined.

## Why this order
What each build unlocks or de-risks for the ones after it.

## Explicitly not doing
Things that came up in discovery and were consciously set aside, and why.

Be honest if this doesn't decompose — if there's no useful version short of
the whole thing, say so and say roughly how big the whole thing is.

## Before you hand it over, read it against itself

You have just written several thousand words in one pass. Documents this size
routinely contradict themselves, and nothing later in the process ever reads
one end of this file against the other.

- **Spine versus builds.** Re-read the spine paragraph, then each build. Name
  anything sitting in a build that the spine paragraph itself describes as
  plumbing or as a separate bet. If you wrote "everything else is just
  plumbing" and then put the plumbing in Build 1, say so plainly and move it.
- **Discovery versus builds.** Name anything a build requires that DISCOVERY.md
  says isn't available — effort I won't sustain, habits I don't have, steps I
  won't keep doing. **That is a re-scope trigger, not a risk to note.** If you
  find yourself writing "the risk to watch is…" followed by a constraint
  discovery already ruled out, you are talking yourself past the thing that
  should have changed the plan. Change the plan.
- **Requirements I never asked for.** DISCOVERY.md marks which conclusions you
  proposed and I merely agreed to. List every build that exists to serve one,
  and what the build costs. Those are the cheapest things here to be wrong
  about, and the first I should get the chance to strike.
