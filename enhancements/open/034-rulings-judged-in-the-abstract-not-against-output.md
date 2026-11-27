# Enhancement: the user judges rulings in the abstract, and mistakes are caught only when output is seen

**Status: OPEN** (recorded 2026-11-27, deal-hunter Build 1, whole-build review). Greg, on the Phase 3 report:
*"That entire paragraph is complete gibberish. How am I supposed the answer?"*

## What happened

- Each phase report asked Greg to keep or change its rulings, often 10 or more in a list. "Keep all" was the
  answer at least four times (Phase 4, Phase 5, 16 Nov and later).
- The rulings that changed what Greg gets were reversed only when he saw their output:
  - matching on a model code in a Google title (T23), reversed at T27 after a warranty and a $6 mount matched;
  - a 12-hour rest after a refusal;
  - OCAU searching titles only ("title search is useless", T36);
  - Approve running no sold search;
  - never searching again for a spec page.
- That many rulings per phase meant /build was doing design: the spec and plan hadn't settled what the user sees.

## The failure modes

1. **A ruling is written as a sentence about code,** not as the change it makes to what the user sees.
2. **"Keep all" is the cheapest answer,** so a list of rulings gets approved unread.
3. **Nothing reads the number of rulings as a signal** that the spec is thin there.

## Candidate fixes (not prescriptions)

- **P1: Each phase report leads with real samples** of the user's output from live runs, including the worst one.
- **P2: A ruling that changes output sits beside the sample it changed,** before and after. A ruling that changes
  nothing the user sees isn't asked.
- **P3: Rulings that change output aren't bundled as defaults.** Each one gets its own answer.
- **P4: Many output-changing rulings in one phase is a checkpoint finding:** the spec is too thin there.

## Evidence

- deal-hunter BUILD-LOG.md: the "Keep all" answers (Phase 4, Phase 5, 16 Nov); T23 and T27; T36; the 12-hour rest
  (21 Nov).
- Related: `022` (the report's form; this is its content), `007`.
