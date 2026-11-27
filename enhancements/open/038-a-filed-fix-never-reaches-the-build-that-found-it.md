# Enhancement: a fix filed mid-build never reaches the build that found it

**Status: OPEN** (recorded 2026-11-27, deal-hunter Build 1, whole-build review). Greg's theory: *"Not enough
asking - how would a person do this, what process are we recreating"*. That had been filed as `026` 18 days
earlier.

## What happened

- `026` (the build never maps the manual process it replaces) was filed on 9 Nov, after Phase 2, with Greg's own
  words on what it should make the agent do.
- Its fix never reached a command. `grep` finds no "manual process" or "design map" in `commands/`, and its README
  row still says "(not yet)".
- deal-hunter ran Phases 3–7 under the same commands and hit the same failure again: spec hunts rebuilt what
  shortlister already does (24 Nov, *"Have we effectively just built another form of shortlister?"*).
- `028` (filed 24 Nov) is in the same state.

## The failure modes

1. **An enhancement is a note for a future fix session.** Until that session runs, the build that found it carries
   on unchanged.
2. **The build that found the failure is the one most likely to hit it again,** and the last to benefit.

## Candidate fixes (not prescriptions)

- **P1: Filing an enhancement mid-build also writes its candidate fix, in short, into the project's CLAUDE.md or
  PLAN.md** as a working rule, labelled with the enhancement number. It stays until the command fix lands.
- **P2: /checkpoint lists the open enhancements filed against this project** and asks whether each one's working
  rule held this phase.
- **P3: The README's status table shows how old each open item is.** An item open across several builds is
  flagged for a fix session.

## Evidence

- `enhancements/README.md` rows `026` and `028`; `git log` for both (enhancements files only).
- deal-hunter BUILD-LOG.md, 24 Nov (the spec hunts redesign).
- Related: `002` (principles that don't reach commands; this is the same gap, for enhancements).
