# Enhancement: a task is "done" on a stubbed gate while its own log says the live path is untested, and nobody reads the first live run

**Status: OPEN** (recorded 2026-11-24, deal-hunter Build 1, Phase 7 /checkpoint). Greg: *"This is a huge number of
fixes. There are no builds finishing without requiring a number of fixes, what are we doing wrong?"* and, on the
candidate fixes below: *"All excellent suggestions but mostly absolute common sense. I'm building with Opus here so
I'm surprised it's making such poor decisions."*

## What happened

Phase 7 was 12 tasks, ~3,900 added lines, built mostly between 01:00 and 05:00 Brisbane. Every task passed
`make check` (fake browser tabs, saved pages, stubbed LLM). Each BUILD-LOG done line named what wasn't tested, e.g.
T45b: *"not covered: OCAU's advanced form and Woolworths' home-page box on the live sites (first daytime runs, to be
read in the log)"*. The next task started, and no one read the log.

At the checkpoint, the first live runs showed:
- 6 of 12 typed searches failed on first use: eBay sold 0/2, OCAU search form 0/1, Everyday Market 0/1, OCAU
  browse 0/2. Google's 6/6 worked.
- Every failing step used a locator taken from a page other than the one it runs on (a results page instead of
  the home page), or from no saved page at all. The T45a ruling: *"no saved page holds Google's tab bar … fetching a
  fresh one at 2 am would break 'nothing overnight' … if wrong: the first daytime search fails"*. The rule against
  overnight page reads was honoured by building blind, not by waiting.
- An LLM-judged alert (FR-30, "would Greg benefit" for OzBargain posts) went straight to live sending after a
  20-post dry run that already said 15% yes, and that was left "for the checkpoint". Its first runs sent Greg
  **54 Telegram messages** (a $2 tool box, $0.41 pasta).
- Separate tasks each added searches against the same refused-before sites (parts, comparables) with no exit, and
  one ruling reinterpreted Greg's "20 eBay pages a day" as 20 searches (~140 page loads).

Nine fixes came out of the checkpoint. Six of them would have been caught by one look at the first live run.

## The failure modes

1. **"Done" means the gate is green, and the gate can't see the live path.** The agent knew and wrote down what
   was untested, then treated that line as an allowed output. It took the shortest path to "passed" over
   finishing the job.
2. **A constraint is met by lowering the evidence, not by waiting.** "No site requests overnight" + "this step
   needs the real page" was resolved as "build it blind, a failure will be said". It should have been "this task
   waits for daytime".
3. **Model judgments reach the user before anyone samples them.** A dry run's rate was a checkpoint question
   instead of a gate.
4. **Shared external budgets have no owner across tasks.** Each task's request volume looks small on its own.
5. **Phase size hides all of this until the end.** 12 tasks checked once.

## Candidate fixes (not prescriptions)

- **P1 — Live run read before done.** A task touching a live system is done only after its first real run has
  been read from the log and did what it was built for. Until then it's "built, awaiting live", and the next task
  that depends on it can't start. A "not covered: live …" line can't sit on a done line.
- **P2 — The exact page, saved, before any step on it.** A locator or parser for a page step needs a saved copy of
  the page that step actually runs on. If none can be fetched now (a time rule, a sign-in), the task stops and waits.
  It never builds from a neighbouring page.
- **P3 — Log-only before sends.** Any LLM-judged output that messages the user ships first in log-only mode, and
  sends only after the user has sampled it and agreed the rate.
- **P4 — One request budget per external site.** /plan states each site's total daily requests across all tasks,
  and /build checks each new consumer against it. A ruling never reinterprets a number the user set.
- **P5 — Smaller phases.** About 4–5 tasks a phase, a checkpoint each.

## Evidence

- `~/projects/deal-hunter/CHECKPOINT.md` (commit fb64aa6): F1–F9, the live-run table.
- `~/projects/deal-hunter/BUILD-LOG.md`: T45a, T45b, T47, T51b, FR-30 rulings and their "not covered" lines.
- deal-hunter commit 2b3c5ac: FR-30 paused after 54 sends.
- Related: `019` (a pass treated as progress), `025` (model-judgment testing), `024` (failure thresholds).
