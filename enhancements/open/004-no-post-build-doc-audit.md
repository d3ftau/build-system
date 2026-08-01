# Enhancement: nothing performs a post-build doc-reality audit

**Status: OPEN** — diagnosed, not built. Candidate fix and an unresolved
design disagreement recorded below; leave the actual command to a dedicated
session.

## Where this came from

`file-cleanup` (personal-rag), 2026-08-01, after Build 1 was judged
functionally complete. Greg asked: "quick check all changes made throughout
the build were reflected in the docs." Manual audit found:

- `CLAUDE.md`'s tech stack table still said the `UserPromptSubmit` hook was
  "not yet registered... deliberately deferred" — five commits after it was
  actually registered and live. It also never mentioned the OneDrive
  ingestion-scope exclusions (`.txt`/`.py`/`.sas`), the token-refresh
  redesign, or the cron/container sync setup — none of Tasks 3–11 or the
  several post-Build-1 fixes had reached it.
- `DESIGN.md`'s hook addendum had the same stale "not yet registered" status
  line.
- `SPEC.md` and `PLAN.md` were current — because `/slice`'s own discipline
  ties FR-checkbox-ticking and task-status updates to every single task, so
  those two files got touched constantly as a side effect of normal work.
- `README.md` didn't exist at all, despite PLAYBOOK.md Phase 6 stating every
  project gets one.

## The general failure mode

**Doc freshness only happens where a mechanism forces it.** This is the
same shape as `002` — a principle in prose doesn't bind — but the mechanism
gap is narrower and more specific: `/slice` forces `SPEC.md`/`PLAN.md` to
stay current because ticking a checkbox is literally part of finishing a
task. `CLAUDE.md` and `DESIGN.md` have no equivalent touchpoint — they're
written once (`/contract`, `/design`) and nothing ever revisits them, so
architectural changes and ad-hoc fixes made after that point (which this
session had several of: a real auth-token bug, an ingestion-scope reversal,
a hook redesign) don't propagate unless someone thinks to go back and check.
Phase 6 "Operate" is worse — it isn't even a command, just prose describing
what a finished project should have, so nothing ever produces it.

## Candidate fix

A new command (`/complete`, or similar) run once a build is judged done:
cross-check every project doc against actual current state — git log,
running config, real file/directory contents, not the docs' own claims —
and write/update `README.md` per Phase 6's spec (what it is, how to run it,
where data lives).

## Open design question — not resolved, disagreement on record

I (the agent) initially proposed `/complete` should run the way `/audit`
does: fresh session, no prior context, on the reasoning that removing
conversation history is what stops an invented constraint from feeling
natural (PLAYBOOK.md's own stated rationale for `/audit`).

Greg disagreed: *"I kinda disagree the final audit should be done context
free, it's the context that helps the docs be accurate."*

He's likely right, and the reason is worth keeping rather than just
overriding my own first answer. `/audit`'s fresh-context requirement solves
a specific problem: a spec's own claims can't be trusted to audit
themselves, because the same context that produced a phantom requirement
also makes it feel unremarkable on a re-read. That problem doesn't obviously
apply to a doc-freshness check — there's no phantom-requirement risk in
asking "does this file still match reality," and the session's own context
(why the token-refresh design changed, why `.txt` got excluded, what got
tried and rejected) is exactly what makes an updated doc *explain* the
current state well, not just state it. A cold session would have to
reconstruct all of that from git archaeology, or write a technically-current
but thin doc that just states facts without the reasoning this project's
docs otherwise consistently carry.

Whether `/complete` runs warm or cold — and whether that answer differs by
project or by what's being audited (README vs. CLAUDE.md vs. SPEC.md) — is
still open. Decide it before writing the command, not by analogy to `/audit`.

## Still open

- The command itself doesn't exist.
- No mechanism prevents this recurring on the *next* build — `/complete`
  fixes it retroactively per-project, same as `002`'s "someone noticed and
  edited a file" pattern, unless it's actually run as a standing step.
