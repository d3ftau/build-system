# Enhancement: one cadence is set for every input, never from how fast each one changes

**Status: OPEN** (recorded 2026-11-27, deal-hunter Build 1, whole-build review). Greg: *"does running it this
frequently add any real value (do we really believe retailers are changing prices every hour?)"*

## What happened

- Discovery recorded "Hourly at minimum" (Greg, against a proposed nightly OzBargain check). Every input then ran
  on that one cadence: Google Shopping searches, store pages, delivery, cashback portals.
- No stage asked how often each input changes, or what a late read costs. Nobody checked once there was data,
  though six days of it existed by 15 Nov.
- What the data showed (deal-hunter database and its pre-wipe backup, 9–27 Nov):
  - Store pages: 25 price changes in 3,144 reads across 85 listings, never two in a day for the same listing.
  - Google Shopping prices: changed in 1.2% of hour-to-hour comparisons, and a quarter of those reverted the next
    hour.
  - Cashback: boosts came and went within 3–6 hours (Woolworths ShopBack 25% from about 6 to 11 pm on 16 Nov).
  - Alerts: 13 of 16 included a cashback rate, and 6 came within an hour of a boost starting. None came from a
    shelf price change.
- So the hourly reads that bought nothing (searches and store pages) were the ones sites refused (`033`). The
  hourly reads that mattered (portals) were a minority of the load.

## The failure modes

1. **Cadence is a property of the app, not of each input.** One number covers sources that change at very
   different rates.
2. **A cadence the user states is taken as a requirement for every input** without asking what it is for.
3. **Nothing compares the cadence with the data once it exists.**

## Candidate fixes (not prescriptions)

- **P1: /spec lists each input with three things:** how fast it changes (from knowledge, then data), what a late
  read costs the user, and the cadence that follows. A stated cadence ("hourly at minimum") is asked about once:
  which input is it for?
- **P2: /plan sizes the load from those cadences** and feeds it into `033`'s usage pattern.
- **P3: The first checkpoint with a week of data measures each input's real rate of change** and proposes a
  cadence change where reads outrun changes.

## Evidence

- deal-hunter DISCOVERY.md ("Hourly at minimum"); `data/deal-hunter.db` and
  `data/backup-before-wipe-stopped-20261122.db` (`offers`, `readings`, `cashback`, `alerts`).
- Related: `033` (usage pattern), `026` (the manual process: a person doesn't re-read a shelf price hourly).
