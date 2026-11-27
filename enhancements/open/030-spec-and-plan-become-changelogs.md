# Enhancement: the spec and plan become changelogs, so no document says what the app does now

**Status: OPEN** (recorded 2026-11-27, deal-hunter Build 1, whole-build review). On ARCHITECTURE.md (26 Nov) Greg
called it *"absolute garbage"*: he was finding the app's flows only when they failed.

## What happened

- **SPEC.md** has 75 commits. Its first ~75 lines are dated rulings ("After Phase 4…"). One setting is listed
  twice. The data model is the day-one one, with later tables named in a single paragraph. The verification
  gates mostly predate the last phase.
- **PLAN.md** has 103 commits and 1,315 lines. "Greg's answers, binding on /build" runs 1–54, and many are struck
  or superseded (15–17 replaced by 19, 39 superseded, 35 reversed on 27 Nov). Tasks T12–T22 were renumbered or
  dropped at a redesign.
- PLAN's own "Things I'd flag" says *"SPEC.md and CLAUDE.md still describe the archive moving here"*.
- ARCHITECTURE.md had to be rebuilt from the code, database and log on 26 Nov.
- Rules that change behaviour live in BUILD-LOG rulings. Knowing what runs takes reading the code.

## The failure modes

1. **Changes are appended as dated rulings, not written into the text they change.** Each one is cheap to add;
   together they can't be read.
2. **"Binding" answers stay on the list after they're superseded.** The reader has to work out which still hold.
3. **No stage asks whether a fresh reader can tell from the spec what runs.** `021`'s write-down adds decisions
   to SPEC with their quotes, which deepens the layers unless it rewrites in place.
4. **`004` audits the docs once, at the end.** A build that runs for weeks drifts long before then.

## Candidate fixes (not prescriptions)

- **P1: Rewrite in place.** A change edits the sentence it changes. The date, reason and quote go to BUILD-LOG.
  SPEC and PLAN carry no dated text.
- **P2: Superseded answers come off the binding list.** BUILD-LOG keeps them.
- **P3: Each /checkpoint does a cold read.** From SPEC alone, list what runs; compare that with the code and the
  log. Any gap is a finding whose fate is "fix the doc".
- **P4: A what-runs-now document is part of the build.** It covers services, schedule, steps and what's off. It
  starts at the first phase that runs anything and changes in the same commit as any change to a flow (a hook
  can check this).

## Evidence

- deal-hunter: `git log -- SPEC.md`, `git log -- PLAN.md`; PLAN.md "Greg's answers" 1–54 and "Things I'd flag".
- BUILD-LOG.md, 26 Nov: the ARCHITECTURE.md rebuild.
- Related: `004` (end-of-build audit), `021` (write-down).
