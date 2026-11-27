# Enhancement: each checkpoint judges its phase alone, so a run of bad verdicts never adds up

**Status: OPEN** (recorded 2026-11-27, deal-hunter Build 1, whole-build review). Greg, 24 Nov: *"There are no
builds finishing without requiring a number of fixes, what are we doing wrong?"*

## What happened

- Verdicts by phase:

  | Phase | Verdict |
  |---|---|
  | 1 | proceed |
  | 2 | no checkpoint |
  | 3 | fix first (F1–F5) |
  | 4 | fix first (F1–F4) |
  | 5 | fix first (T44 took 15 fixes, then more from chat on 16–18 Nov) |
  | 6 | re-plan |
  | 7 | fix first (8 fixes, 6 decisions) |

- The worth-it step (checkpoint step 6) fired once, at Phase 6, about eBay. No checkpoint asked whether used
  items, spec hunts or "would Greg benefit" belonged in this build, or why four phases in a row needed fixing
  first.
- The patterns sections named shapes (failure notices that clear only by accident, queues with no way out). Each
  shape came back as one more fix.
- The biggest cut came from Greg, not a checkpoint. He stopped every watch but one, then said *"Wipe the stopped
  watches. I want them gone"* (20 models, 12,868 offers).

## The failure modes

1. **A checkpoint reads the phase, not the trend.**
2. **"Fix" is the default fate for a finding,** so a pattern gets fixed one instance at a time.
3. **The worth-it question is asked about the phase's tasks, not the build.**

## Candidate fixes (not prescriptions)

- **P1: Each checkpoint reads the earlier verdicts and fix counts,** kept as a table in CHECKPOINT.md. Two
  fix-first verdicts in a row, or a fix count that isn't falling, makes the worth-it step judge the whole build
  against the brief (`029`).
- **P2: A pattern gets a design-change fate.** The same shape in two or more findings becomes one task that
  changes the design, not N fixes.
- **P3: The worth-it step lists each part the user receives** and asks keep, cut or next build, with evidence
  from the log of what each part has produced.

## Evidence

- deal-hunter: `git log -- CHECKPOINT.md` (5a2733f, 2b02ea7, 334f4fc, 84fd2bb, 04dcca2, fb64aa6). PLAN.md T44.
- BUILD-LOG.md: 23 Nov, the wipe.
- Related: `009` (no stage owns "good enough"), `017`, `019`.
