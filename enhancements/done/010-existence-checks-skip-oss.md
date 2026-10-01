# Enhancement: "does this exist" checks skip GitHub/OSS as a search category

**Status: DONE** — both commands run commercial and OSS as separate searches.

## Where this came from

`usecasebot` discovery/explore session, 2026-09-12/13 (the testimonial/
idea-mining pipeline). The user, after `/explore` had already run one
existence check and moved on:

> *"Please see https://github.com/Akhan521/Reddit-Crawler and do more
> research. Reddit crawling is not a novel problem and it doesn't seem
> like you've looked hard enough for existing solutions"*

and then, once the gap was fixed for that session only:

> *"Create a note in the build system project folder under feedback that
> GitHub projects and other open source work should be specific search
> targets as part of explore - not just commercial solutions"*

## What actually happened

`/discovery`'s existence check ran first and found GummySearch's own
published alternatives list — BuzzAbout, PainOnSocial, Clearbox,
RedReach, SubredditSignals, ReplyAgent, Outpost. Every one is a
commercial lead-gen/marketing SaaS product. The check concluded "this
doesn't exist" on the strength of that list alone, without ever
searching GitHub, PyPI, or any OSS category. Both categories were
findable with the same effort — a GitHub search was one more query, not
a harder one.

The linked repo (`Akhan521/Reddit-Crawler`) was not, in the end, a
tool worth adopting — 1 star, a four-person student project, no
checkpointing, no structured store. But searching GitHub properly, once
prompted to, surfaced `ArthurHeitmann/arctic_shift` (1,509 stars,
committing the same day) — a free, unauthenticated Reddit archive that
resolved two separate BLOCKED items in `EXPLORE.md` and changed the
recommended harvest architecture. The near-miss and the real find came
from the same missing search category.

## The general failure mode

Neither command file names OSS/GitHub as a search category to check
against.

- `commands/discovery.md`'s existence-check instruction says "ask
  whether this already exists. Name the closest things that already do
  it" — no guidance on *where* to look, so the search defaults to
  whatever comes to mind first (commercial products, in this session).
- `commands/explore.md`'s "what do they actually do now" section (item
  2) verifies features of candidates *already named* — it has no step
  that generates the candidate list in the first place, so it inherits
  whatever `/discovery` handed it.

Same shape as `002`: a thing that should bind in a command file doesn't,
so it depends on whoever is running the check happening to think of it.
Commercial-alternative research and OSS-project research are genuinely
different queries with different result sets and different signals for
quality (pricing/feature pages vs. star count and commit recency) —
skipping one is not "less thorough," it's a whole category of answer
never generated.

## Candidate fix

`commands/discovery.md`'s existence-check line, and/or `commands/
explore.md` section 1 ("what kinds of tool could solve this"), should
name OSS/GitHub as its own required search pass — not a fallback run
only if commercial search comes up empty, and not merged into a single
generic "look for existing solutions" instruction that will keep
defaulting to whichever category is easier to think of first (commercial,
on this evidence). Suggested framing for whichever file ends up owning
it: run commercial-alternative search and GitHub/OSS search as two
separate passes, and for OSS results use star count plus last-commit
recency as the first-pass signal for "maintained tool" vs. "abandoned
student project" before evaluating fit.

## Open, not resolved here

- Whether this belongs in `/discovery` (where the existence check
  currently lives), `/explore` (where deeper verification happens), or
  both. `/discovery`'s check is the first and sometimes only one that
  runs — a request framed as "just thinking out loud" may never reach
  `/explore` — so the fix arguably has to bind there regardless of
  whether `/explore` also gets it.
- Whether other categories are missing the same way. This session only
  surfaced the OSS gap because the user happened to have a specific
  repo in hand; no audit has been done of what other search categories
  (academic tools, abandoned-but-forkable projects, adjacent-domain
  tools solving the same sub-problem) get skipped by the same default-
  to-commercial pattern.

## Still open

- Neither `commands/discovery.md` nor `commands/explore.md` changed.
- Recorded in `usecasebot`'s own session only as it happened; no
  project-level document updated, since the fix belongs in the build
  system, not in that project.

## Implementation status (2026-10-01)

- `commands/discovery.md` — existence check is now searched rather than
  recalled, as two separate passes (commercial; GitHub/open source judged first
  on stars and last-commit date), plus tools solving one hard part even in
  another domain. "Doesn't exist" can't be concluded from one category. This
  also fixes a conflict with `~/.claude/CLAUDE.md`'s "search first" rule —
  the old wording handed checks to the user instead of searching.
- `commands/explore.md` section 1 — generates candidates with the same two
  searches, and doesn't inherit DISCOVERY.md's list as complete.
- Committed alongside an unnumbered `/discovery` fix: if the user already named
  the existing product and framed the idea as an improvement, existence is
  closed and the question becomes whether the improvement is sellable.
