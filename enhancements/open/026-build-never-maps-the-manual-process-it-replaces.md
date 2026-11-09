# Enhancement: the build never maps the manual process it replaces, and /plan's design is never seen

**Status: OPEN** (recorded 2026-11-09, deal-hunter Build 1, after the Phase 2 report). Greg: *"What
you've built is incredibly over engineered. And this is really a recurring theme. It looks good on
paper but the way it gets implemented is a mess that misses the core point of the build and tries too
hard to be "complete" instead of being useable. I was about to wait half an hour to find out what
typing something in google tells me in 2 seconds"*. On what to record: *"The recorded feedback should
be for me to challenge myself to think about the manual process this is replacing and what that looks
like. Do it for real and map it out. The plan step also needs a proper high level design map drawn for
me as I'm usually so over the design work by that stage I don't bother reading it properly if at all."*

## What happened

deal-hunter's spec said Google Shopping prices are "indicative, never alerted on" (Greg's words, which
he says he was responsible for). From that, every offer's store page was opened in the shared Chrome,
4–9 s apart. That needed a shipping reader per store, a cashback page lookup per store (web searches),
SearXNG when Google refused the searches, then 30–90 s spacing between searches, then a pause switch.
Each piece fixed the cost of the one before it. A new watch's first answer would have taken ~30 min.

Greg's actual manual process, as he described it afterwards (not yet done for real and timed):

1. Search the product on Google Shopping and take the best price he can find (seconds).
2. Check whether it's actually a good price against OzBargain: recent all-time lows, regular sale
   prices.
3. (Usually forgotten) Look at Woolworths: Everyday Market less ~30% when ShopBack/TopCashback have
   it upsized. Not permanent, so it's a "wait for the next cashback event" price.
4. Decide: buy now, or wait.
5. If waiting: usually forgets. **This is the only step the tool really has to take over.**

Mapped this way, the tool needs about three page reads per watch, plus one confirmation read of the
winning store before an alert. Greg: "the only check required was the best price and you went and
checked literally every merchant". Steps 1 and 2 were never slow, and only step 5 failed when he did
it by hand. The build automated a thoroughness the manual process never had and didn't need.

The design existed on paper (SPEC.md, PLAN.md), but as long prose. By /plan Greg is "so over the design
work" that he doesn't read it properly, so nobody looking at it would have seen the chain.

## The failure modes

1. **No stage maps the manual process.** /discovery and /brief ask what the tool is for, never "do it
   by hand now, once, and write down every step, its time and what you look at". So the build can't be
   held to "faster and no worse than by hand", and nobody sees which manual step actually fails (here:
   remembering, not finding prices).
2. **Completeness is rewarded over the time to an answer.** No gate asks how long the first useful
   answer takes against the manual process. Each /build task passes its own check while the whole
   gets slower.
3. **A rule about trusting a source turns into per-item work.** "Prices are indicative" should have
   meant "confirm the one that matters". It was applied to every item instead, and no one asked
   which items could change the answer.
4. **/plan's design is prose the user won't read.** At the point the shape is fixed, the user gets a
   wall of tasks, not a picture. An over-built shape is easy to see in a diagram (a box per store per
   portal) and invisible in a task list.

## Candidate fixes

- `discovery.md` / `brief.md`: before the brief is written, ask the user to **do the job by hand for
  real, once**, and map it in the brief: each step, what they look at, how long it takes, and which
  step fails or gets forgotten. The brief states which manual step(s) the tool replaces; everything
  else is an extra that must justify itself.
- `spec.md` / `plan.md`: a **"against by hand"** line: the time to the first useful answer by hand
  vs by the tool, and the tool may not be slower. /checkpoint measures it on real data.
- `plan.md`: a **high-level design map drawn for the user**: one diagram (inline SVG/mermaid or an
  artifact the user can open on a phone) of the flow from input to answer, every page read or external
  call as a box with how many per run, alongside the manual process map. It comes first in the plan
  report, before the task list, and the plan's survey asks about it.
- `build.md`: a ruling that adds per-item work (a read, lookup or search per store, offer or item)
  is the "expensive automation" stop: it says what the manual process does at that step.
- `checkpoint.md` step 6 ("Is it still worth it?"): compare against the manual process map, not just
  effort against time saved.

Related: `017` (a nice-to-have becomes the spine; every snag adds machinery), `011` (completeness over
proportion).
