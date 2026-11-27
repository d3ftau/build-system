# Enhancement: an outside system is proven by answering once, not by tolerating the planned pattern

**Status: OPEN** (recorded 2026-11-27, deal-hunter Build 1, whole-build review). Greg, 21 Nov, after eBay's 403:
*"for the last time, the goal here is TO APPEAR HUMAN"*. On a timed rest: *"That's a ridiculous solution. The 403
is being triggered by whatever pattern of use led up to it."*

## What happened

- **Load was sized as time.** Discovery said "30–40 pages an hour, about 4 minutes at a person's pace", and /plan
  said "15–25 min an hour". Neither said, for each site, how many requests an hour and a day, at what hours, or how
  each request was reached.
- **The question was asked as permission.** Discovery raised "Do ShopBack/TopCashback or retailers mind hourly
  reads?", and Greg rightly dismissed it ("Not a concern"). The different question, whether each site would
  refuse that pattern, was never asked.
- **Explore loaded each source once and said "Nothing BLOCKED".** Two sites refused the real Chrome on first load
  (an Incapsula block, a 403). They were recorded as reachable because Greg loads them normally. The 403 came back
  in Phase 5, traced to a fingerprint leak in the browser library.
- **The sites then refused one at a time:**
  - Google, after ~20 searches in 20 minutes (T8), and again at a 02:00 daily find (20 uncapped searches);
  - eBay, after a day of ~100 built search addresses;
  - Amazon, whose error page rose from ~40% to ~95% of opens over a week;
  - 8 stores, on their first plain request (27 Nov).
- **Each refusal added one rule:** 4–9 s pacing, search caps, nothing overnight, typed searches instead of built
  addresses, a refusals file, per-site hourly and daily caps, store pages in Chrome only.
- **Two first reactions were wrong:** probes sent after a 403, and a 12-hour rest.

## The failure modes

1. **"Reachable" is tested by one load, but the build depends on weeks of scheduled loads.**
2. **Load is stated as the app's time, not as what each site sees.**
3. **Each refusal gets a local rule.** None is read as a sign that the pattern was designed wrong.

## Candidate fixes (not prescriptions)

- **P1: /spec writes a usage pattern for each outside system:** requests per hour and per day, at which hours, how
  each is reached (typed into the page, or a built address), and from which client. Then it asks: would a person,
  or a normal client of that API, do exactly this every day? A "no" changes the design before /plan.
- **P2: /explore tests the pattern, not the page.** That means a short run at the planned cadence, on a small
  scale, with the log read afterwards.
- **P3: The first task that hits a site on a schedule runs live at that cadence** long enough to see a refusal.
  Nothing more is built on that site until the log has been read (`028` P1, applied to the schedule).
- **P4: A refusal reopens the usage pattern.** The fix is a change to the pattern, recorded against it.

## Evidence

- deal-hunter DISCOVERY.md (the load estimate, "mind hourly reads"); EXPLORE.md (refusals on first load).
- BUILD-LOG.md: T8; Phase 4 F1; eBay 21 Nov; Amazon; Bing Lee and Patchright; 27 Nov Chrome-only.
- Related: `028` P4 (one request budget per site, the build-time half); `026`.
