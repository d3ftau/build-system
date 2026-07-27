Read BRIEF.md and EXPLORE.md. Don't write a spec yet.

EXPLORE.md already establishes what the candidate tools actually do and which
it ruled out. Build the options on those findings, not on recall.

Identify the genuinely distinct ways this could be built. Not variations on
one idea — different shapes, with different centres of gravity. However many
actually exist: if that's two, give me two; if it's five, give me five; if
there's honestly only one sensible shape, say so and explain why the obvious
alternatives don't hold up.

For each:
- The one-line description of what it fundamentally is
- What it makes easy, and what it makes hard or forecloses
- What it'd be good at in a year that the others wouldn't
- Roughly how much work v1 is

Then say which you'd pick and why — and what would change your mind.

The bar is that each option would be a defensible choice if I picked it. If
you find yourself padding to make a list look fuller, stop and tell me you
only found N.

I'll pick one or a hybrid. Then write DESIGN.md recording the options, my
choice, and the reasoning — including what we rejected and why.

Downstream reads this file as settled and can't tell prose from evidence, so:

- **Never assert what a product or tier can't do beyond what EXPLORE.md
  found.** If an option turns on a capability EXPLORE.md doesn't cover, say so
  and stop — that's a check to run, not a gap to fill with recall.
- **Mark every prediction about model judgment as untested** — classifying
  text, spotting intent, detecting a decision. Unmarked, /contract turns it
  into a schema field and it stops being a guess anyone questions.
