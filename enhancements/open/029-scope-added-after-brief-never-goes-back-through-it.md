# Enhancement: scope added after /brief never goes back through the brief

**Status: OPEN** (recorded 2026-11-27, deal-hunter Build 1, whole-build review after Phase 7). Greg: *"This build
did not go well. There were patches and fixes required everywhere and I'm still not convinced the structure is
sound."*

## What happened

BRIEF.md described Build 1 in one paragraph: hourly new-price alerts, used items left for Build 2, done when 3
real watches run. It has one commit. Over the next 19 days the build took in:
- Build 2's used prices (eBay, OCAU), at /plan (PLAN.md line 4: "brought in from Build 2 (Greg, at /plan)");
- a web app with charts, photos and a Research tab (Phase 5);
- spec hunts, "would Greg benefit" reads of OCAU threads and OzBargain posts, price guides and house context
  (Phase 7, "Fold it into Phase 7"; FR-30 added at the phase end).

SPEC.md went from 18 FRs ("six past the usual dozen", justified at the top as /spec asks) to 31 (FR-1 to FR-30
plus FR-28b). Its header still says 18. Near the end Greg asked *"Have we effectively just built another form of
shortlister?"*. It had: hunt planning moves to shortlister (24 Nov). At the end, one product watch and one hunt
run, short of the brief's own done line. BRIEF, DISCOVERY, EXPLORE and ROADMAP were never revised.

## The failure modes

1. **Scope and proportion are checked only upstream.** /discovery, /brief and /spec's first draft weigh scope.
   After that, every request is built into the current build.
2. **A "Later" item pulled forward keeps the current build's done line.** "Done" never moves to match.
3. **The requirement count is justified once, not limited.** Its stated number goes stale and nothing notices.
4. **`003`'s fix binds only in roadmap.md, brief.md and discovery.md.** Nothing downstream reads BRIEF.md again.

## Candidate fixes (not prescriptions)

- **P1: New scope is a stop** in /plan, /build and /checkpoint: a new requirement, a pulled-forward Later item,
  or a new stream the user receives. The default offer is "next build" (ROADMAP.md). "This build" means rewriting
  the brief's paragraph and done line first.
- **P2: The brief's done line is read at every checkpoint.** How far is the build from it, and is this phase's
  work on the way there?
- **P3: A check compares the spec's FR count with the brief's limit** (hook or `bin/build-state`) and fails past
  it, so the justification is rewritten rather than kept.
- **P4: The phase report says in one line what the build covers now against the brief.**

## Evidence

- deal-hunter: `git log --oneline -- BRIEF.md` (1 commit) against SPEC.md (75) and PLAN.md (103).
- SPEC.md header against its FR list.
- BUILD-LOG.md: 23 Nov "Fold it into Phase 7"; FR-30; the spec hunts redesign ("another form of shortlister").
- ARCHITECTURE.md (26 Nov): watched today, one product and one spec hunt.
- Related: `003` (upstream only), `011` (proportion), `017` (a snag grows the goal).
