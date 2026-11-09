# Enhancement: /spec designs in silent failure: invented thresholds hold back failure notices, filed as harmless assumptions

**Status: OPEN** (recorded 2026-11-09, deal-hunter Build 1 /spec). Greg: *"Designing
a spec that lets something fail 3 times then silently removes it completely is
borderline insane and we need to stop it happening again in case I don't catch it."*

## What happened

BRIEF.md named the failures Greg cares about: **missing a deal**, and the watch
**going quiet** when a sweep breaks. It said "a stale alert beats a missed deal".
The first SPEC.md still wrote:

- **FR-13:** a store is reported only after its pages fail in **3 sweeps running**
  (3 hours on an hourly sweep). Until then, nothing reached Greg.
- **FR-9:** a price from Google Shopping alone would alert as "unconfirmed",
  quietly overriding Greg's stated must that every alert is confirmed by a page
  load.

The listing wasn't removed; it was marked stale on the watch page. That doesn't
change the failure: for three hours a broken reader looked exactly like "no
deals", which is the failure Greg named. Greg caught both and overrode them:
every failure is notified the first time, and only a 404 or out-of-stock page
counts as "no price".

## The failure modes

1. **A generic habit beat the stated priority.** Debouncing alerts to avoid noise
   is a standard monitoring habit. Greg never named noise as a concern. He named
   missed deals and going quiet. The spec optimised for an unstated concern, and
   against a stated one.
2. **The invented threshold was presented as harmless.** It was tagged `[ASSUMED]`,
   so the provenance rule was followed. But the review list asks for each
   assumption's **cost to build**, so it read "Cost: none", one line among
   fifteen. What it cost Greg if wrong (three silent hours on his top failure)
   was never stated. The tag existed; the consequence was hidden.
3. **"What would bite me" marked its own assumption as the fix.** Scenario 3 (a
   retailer changes its page) said "Covered" by FR-13: the 3-strike rule. The
   self-check validated the thing it should have caught.
4. **/spec frames failure at the run level.** "When it breaks" asks what counts as
   a failed *run*. A partial failure (one store, one page) inside a run that
   otherwise succeeds has no rule. Whatever the agent invents fills the gap. And
   "No invented thresholds" in the command didn't stop it.

## Candidate fixes

- `spec.md` "When it breaks": any page, source or reader that fails to give what
  it was loaded for counts as a failure, not only a whole run. **The default is
  to tell Greg the first time.** Any rule that delays, batches, debounces or
  suppresses a failure notice needs Greg's own words quoted beside it, or it
  doesn't go in.
- `spec.md` §4 (the `[ASSUMED]` list): each item states **what happens to Greg if
  it's wrong**, not only what it costs to build. An assumption that touches a
  failure the brief names goes at the top, marked as such.
- `spec.md` §3 ("What would bite me"): a scenario can't be called covered by an
  `[ASSUMED]` item. It's listed as open until Greg keeps it.
- Check, across commands: does `/plan` or `/build` invent retry counts, grace
  periods or "fail after N" anywhere? Same rule there.
- Considered: a hook that greps SPEC.md for "N times / in a row / consecutive"
  near "fail". Probably too narrow on its own; the binding fix is the command
  text.

## Evidence

- deal-hunter `SPEC.md`, first version (2026-11-09): FR-13 "3 sweeps running
  [ASSUMED 3]", FR-9 "unconfirmed — Google Shopping only [ASSUMED]". The
  assumptions list items 11 and 14 were both "Cost: none" or "small".
- deal-hunter `BRIEF.md`: "What I'd care about going wrong: missing a deal …,
  and going quiet when a sweep breaks."
- Related: `003` (provenance tagging; this is the case where the tag existed but
  the consequence didn't), `011` (proportion: "no invented thresholds" was already
  in `spec.md` and didn't hold).
