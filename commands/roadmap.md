Read DISCOVERY.md (or the pasted discovery conversation above). Write
ROADMAP.md for this product.

## What this is
Two sentences.

## The spine
The one capability everything else hangs off. If there isn't one, say so —
that's a sign this is several products, not one.

## Builds, in order
For each: what it delivers, and "if nothing after this ever got built, would
this still be worth using?" Any build answering no needs re-scoping or merging
with the next.

That test only catches a build that's too small, so every build also gets the
inverse: **what's the smallest part of this that still earns a yes?** Ask it of
the pieces, never the bundle — a bundle passes on its best component and
carries the rest through unexamined. If the answer is smaller than what you
wrote, that smaller thing is the build.

**Build 1 contains only what tests the spine.** Everything else is plumbing or
a separate bet, and neither belongs in the build whose job is finding out
whether the spine works. Where something is genuinely needed to evaluate the
spine, say why in one line.

For each build, list what you cut and where it went. A build that cut nothing
wasn't examined.

## Why this order
What each build unlocks or de-risks for the ones after it.

## Explicitly not doing
Things that came up in discovery and were consciously set aside, and why.

Be honest if this doesn't decompose — if there's no useful version short of
the whole thing, say so and roughly how big it is.

## Then read it against itself

- **Spine vs builds.** Name anything in a build that your own spine paragraph
  calls plumbing or a separate bet. Move it.
- **Discovery vs builds.** Name anything a build needs that DISCOVERY.md says
  isn't available from me — effort I won't sustain, steps I won't keep doing.
  **That's a re-scope trigger, not a risk to note.** "The risk to watch is…"
  followed by a constraint discovery already ruled out means change the plan.
- **Requirements I never asked for.** DISCOVERY.md marks what you proposed and
  I merely agreed to. List every build serving one, and what it costs.
