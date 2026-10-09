# Enhancement: `/roadmap` has no real trigger, so scope cut by `/brief` has no home

**Status: OPEN**

## Where this came from

fashion-bot, 2026-10-09. After `/plan`, the user asked whether a roadmap file
existed. It didn't. The user:

> *"That's another complete whiff - roadmap has no real trigger despite brief
> demanding everything be cut"*

## Evidence

- **DISCOVERY.md, "How big is it":** "One build, sequenced. Not a platform.
  **[Claude, unconfirmed]**". It then lists five ordered stages: outlet
  access, plain-fetch sources, code filters, vision, feedback. It also hands a
  decision forward explicitly: "/roadmap should decide whether the first
  shippable slice must include at least one outlet."
- **`/roadmap` never ran.** BRIEF.md notes it: "There is no ROADMAP.md, so
  this brief covers the build discovery describes."
- **`/brief`** asked its mandatory smallest-version question and cut to build
  1: one outlet, code filters, a daily email. Everything else went into a
  prose "Out of scope" list: vision colour and style, reason-based feedback,
  department stores and the brand allow-list, more retailers, Lucy and
  multi-user, Telegram. Nothing orders those, names them as builds, or
  records what was cut where.
- **The only triggers for `/roadmap` are soft:**
  - `PLAYBOOK.md:141`: "is this one build, or a product with several pieces?
    If it's a product, run `/roadmap` next."
  - `discovery.md` asks the same question.
  - `bin/build-state` reads ROADMAP.md if it exists, and never flags a
    missing one.

## The general failure mode

**The one-build-or-several decision is made before the cut that answers it.**

- Discovery classifies the idea while scope is at its largest. Here the
  call was "one build, sequenced", Claude's call and unconfirmed. A
  five-stage sequence was classed as a single build, so `/roadmap` was
  skipped.
- `/brief` then always cuts to the smallest usable version, by design
  (`brief.md`: "those steps can only make a build bigger"). **Any brief whose
  out-of-scope list holds deferred features has made the project multi-build
  after the fact.** Nothing re-asks the question at that point.
- The result is that the cut scope survives only as prose in BRIEF.md and
  DISCOVERY.md.
  - The project dashboard shows one build.
  - The next build has no named starting point.
  - A decision discovery explicitly delegated to `/roadmap` (does build 1
    need an outlet?) was settled ad hoc in `/brief`. It happened to be
    settled right; the user insisted on the outlet. But no stage owned it.

Related to `003` (scope only ratchets up): `/brief`'s cut is the fix for that,
and this is the cut's missing other half. What gets cut needs to land
somewhere that carries it forward.

## Candidate fixes

Not prescriptive.

- **Trigger on the cut, not the classification.** If BRIEF.md's "Out of
  scope" defers anything the user wants later, as opposed to rejecting it,
  `/brief` ends by saying "run `/roadmap`". Alternatively, `/brief` writes
  or updates a minimal ROADMAP.md itself: build 1 = this brief, plus the
  deferred items as later builds.
- **`bin/build-state` flags it.** A DISCOVERY.md that mentions stages or
  `/roadmap`, or a BRIEF.md with deferred out-of-scope items, plus no
  ROADMAP.md, gives a dashboard nudge.
- **`/brief`'s Out of scope** distinguishes *later* (goes to the roadmap)
  from *never* (rejected), so the trigger has something concrete to read.
- **Keep it light (see `011`):** for a small product the roadmap can be a
  short ordered list. The point is that cut scope has a home, not a new
  heavyweight document.

## Still open

- `commands/brief.md`, `commands/discovery.md` and `bin/build-state` are
  unchanged.
- fashion-bot still has no ROADMAP.md.
