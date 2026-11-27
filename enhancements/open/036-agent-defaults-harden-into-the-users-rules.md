# Enhancement: the agent's defaults harden into rules that read as the user's

**Status: OPEN** (recorded 2026-11-27, deal-hunter Build 1, whole-build review). Greg, on a /plan default later
called agreed: *"Why did we decide not to include? I don't recall that at all"*.

## What happened

- "Coupon codes are ignored" was a /plan default, accepted only inside a "defaults" bundle and later called
  agreed. Greg chose "Count, flagged" (T1).
- The plan's "No JavaScript" was the agent's wording, not Greg's. It surfaced at T43, when the charts needed a
  script.
- Greg's "20 eBay pages a day" became 20 searches (~140 page loads) in a ruling (`028`).
- PLAN's "Things I'd flag" says four defaults are "my numbers, not Greg's". They drove the build all the same.
- The 12-hour rest after a refusal was an agent default. Greg reversed it.

## The failure modes

1. **A rule's source isn't recorded where the rule lives,** so later stages and sessions read it as the user's.
2. **Approving a bundle of defaults turns the agent's guesses into agreements.**
3. **A user's number is restated in the agent's units without saying so.**

## Candidate fixes (not prescriptions)

- **P1: Every rule in SPEC, PLAN and the generated CLAUDE.md carries its source:** the user's words (quoted) or
  "default".
- **P2: /build may question a default when it gets in the way.** It may not question a rule of the user's.
- **P3: Each checkpoint lists the defaults that shaped output** in that phase, for the user to confirm or change.
- **P4: A user's number stays in the user's units.** Converting it is a question for the user.

## Evidence

- deal-hunter BUILD-LOG.md: T1 (coupons), T43 (the script), 21 Nov (the rest). PLAN.md "Things I'd flag".
- `028` (EBAY_PER_DAY).
- Related: `003` fixed provenance upstream only (discovery, brief, roadmap); `007`.
