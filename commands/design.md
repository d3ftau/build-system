Read BRIEF.md. Don't write a spec yet.

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

Two things this file must not do, because everything downstream reads it as
settled and nothing downstream can tell prose from evidence:

- **Don't assert what a product, service or tier can't do.** Write it as a
  question for /explore instead. Ruling out an option on a capability claim
  you haven't checked is the single most expensive error available here: it
  doesn't just pick the wrong shape, it commits the build to replacing a
  feature that already exists behind someone else's checkbox.
- **Mark every prediction about how well a model will judge something** — that
  it can spot intent, classify text, detect that a decision was made. Say
  plainly that it's an untested prediction and not a conclusion, however
  naturally it follows from the option you're describing. Left unmarked, it
  reads as architecture, /contract turns it into a schema field, and by then
  it has stopped being a guess anyone questions.
