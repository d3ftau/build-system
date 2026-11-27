# Enhancement: a core redesign is built beside the code it replaces

**Status: OPEN** (recorded 2026-11-27, deal-hunter Build 1, whole-build review). Greg, after Phase 2: *"The store
lookup step is painful. Google shopping does this instantly. I feel like we are trying too hard as usual"*.

## What happened

- Phase 2 built an hourly sweep of store pages: a listing per store, a daily deep read, and stand-in listings for
  stores with no readable page. After Phase 2 the core flow was reset to Google Shopping first (SPEC.md: "We
  really are overthinking this").
- **Phase 2 never had a checkpoint.** The re-plan started Phase 3 on top of Phase 2's code.
- The old machinery stayed beside the new flow, and fixes kept landing on the join:
  - stand-in listings taken for real stores (Phase 3 F1, T44 F1 and F9);
  - T27's plan said of the old failure rows "nothing produces them now". The deep read recreated 16 of them;
  - failure notices that cleared only by accident.
- At the end, switched-off paths remain in the code (eBay Buy It Now, the deep OCAU read, OCAU keyword search,
  OzBargain benefit), next to an open bug on the full hunt path.

## The failure modes

1. **A redesign is planned as additions.** Nothing lists what the new design makes dead.
2. **A skipped checkpoint is never made up.** The redesign skips the review that would have seen the stack.
3. **"Off" is a resting state.** Switched-off paths are kept for later with no keep-or-cut decision.

## Candidate fixes (not prescriptions)

- **P1: A core redesign triggers a checkpoint** before the re-plan, including any that was skipped.
- **P2: The re-plan starts from "what survives".** List every module, table and scheduled job, and mark each one
  survive or remove. Removal is the first task, with its own gate: the removed path is gone from the code, the
  database and the schedule.
- **P3: A switched-off path gets a fate (keep, cut or next build) at the next checkpoint.**
- **P4: Find out why `bin/build-state` let Phase 3 start with no Phase 2 checkpoint**, and close that gap.

## Evidence

- deal-hunter PLAN.md: Phase 2 (T5–T11) has no checkpoint line. CHECKPOINT.md's history has Phases 1 and 3–7.
- BUILD-LOG.md: T27, Phase 3 F1, T44.
- ARCHITECTURE.md (26 Nov): "Off" O1–O4.
- Related: `026` stops the wrong design being built; this covers what happens after it was.
