# Enhancements

Process failures found in this build system, recorded when they're diagnosed
and fixed in dedicated sessions later. Each file records **where it came from,
the general failure mode, concrete evidence, and candidate fixes** — deliberately
not a prescribed patch, because scoping the fix to the exact symptom is how you
get a system full of narrow special cases.

## Layout

```
enhancements/
  README.md    this index — the status table below is the source of truth
  open/        diagnosed, not fixed (or only partly fixed)
  done/        fully implemented; the fix is in a command file or a hook
```

A file moves to `done/` only when every item in its own "Still open" or
"Candidate fixes" section has landed **somewhere binding**. Partially-fixed
work stays in `open/` — `002` is the current example.

**Binding means a command file, a hook, or a generated project `CLAUDE.md`.**
An edit to `PLAYBOOK.md` alone does not close an enhancement. That is `002`'s
entire thesis, and applying it to this tracker is the point: the playbook is
documentation, the command files are the program.

## Status

| # | Title | Status | Fix binds in | Verified |
|---|---|---|---|---|
| [001](done/001-pipeline-over-trusts-prior-output.md) | The pipeline over-trusts its own earlier output | **DONE** | `contract.md`, `audit.md` (`9b0d2dd`, `d381b32`) | 2026-07-27 |
| [002](open/002-principles-dont-reach-commands.md) | Principles in PLAYBOOK.md prose don't reach the commands | **PARTIAL** | `commands/plan.md` (`165da12`) — 3 items still open | 2026-07-26 |
| [003](done/003-scope-only-ratchets-up.md) | Scope can grow but never shrink; agent-argued requirements recorded as the user's | **DONE** | `roadmap.md`, `brief.md`, `discovery.md` (`9b0d2dd`, `d381b32`) | 2026-07-27 |
| [004](open/004-no-post-build-doc-audit.md) | Nothing performs a post-build doc-reality audit; `CLAUDE.md`/`DESIGN.md` drift silently, no `README.md` ever gets written | **OPEN** | — | 2026-08-01 |
| [005](open/005-deploy-assumes-one-project-shape.md) | `/deploy` assumes every project is a reachable web service | **OPEN** | — | 2026-08-01 |
| [006](open/006-pipeline-has-no-concept-of-a-human-surface.md) | The pipeline has no concept of a human surface; FRs go green with no UI and nothing ever asks what it should look like | **OPEN** | — | 2026-08-07 |
| [007](open/007-slice-settles-open-decisions-silently.md) | `/slice` settles the plan's open decisions silently, mid-build, and surfaces them only after the code exists | **OPEN** | — | 2026-08-07 |
| [008](open/008-claims-accepted-without-checking-they-can-be-true.md) | Claims are accepted on evidence that tests something adjacent to what the claim says | **OPEN** | — | 2026-08-07 |
| [009](open/009-slice-is-too-small-a-unit-for-a-large-build.md) | `/slice`'s per-task lens can't see output quality, cross-task patterns, or a stale plan — and a 61-task build has no checkpoint that can | **OPEN** | — | 2026-08-19 |

## Open items in detail

**002 — playbook prose doesn't bind.** The vertical-slice principle now lives in
`commands/plan.md`. Still open:
- *"One unknown at a time"* remains orphaned — confirmed absent from `commands/`
  and `hooks/` as of 2026-07-26; it exists only in `PLAYBOOK.md:355`.
- `file-cleanup/PLAN.md` has not been regenerated — still 41 tasks, first
  end-to-end run at ~31.
- No mechanism prevents recurrence. Both fixes so far were "someone noticed and
  edited a file."

**003 — scope only ratchets up.** Nothing implemented. `/roadmap`'s test
("would this be worth using if nothing after it got built?") can only detect a
build that is too small, and PLAYBOOK.md:122 gives growing it as the only
remedy. No command can make a build smaller. Separately, a requirement the agent
argued for and the user assented to gets recorded as `[STATED]`, identical to
one the user raised unprompted.

**006 — no concept of a human surface.** Nothing implemented. Four Autopantry
FRs had a table and an endpoint and no way for a person to enter or see
anything, and the FR checkboxes went green anyway. Separately, no step in the
chain has ever asked what a build should look like, so the first screen built
becomes the design language by default. Fixes proposed at three stages
(`/contract`, `/brief`, and a new pre-build completeness audit); none written.

**007 — `/slice` decides silently.** Nothing implemented. Plan tasks ship with
open questions attached — `/plan` says so itself, in its own "ambiguous / my
own judgment calls" section — and the slice answers them without saying so,
surfacing the answer only once the code exists. Three separate pieces of work
were built and stripped in one day this way.

**008 — claims tested against an adjacent proposition.** Nothing implemented.
Least command-shaped of the three; the fix may belong in a hook or in
`~/.claude/CLAUDE.md` rather than a command file.

**009 — `/slice` is too small a unit for a large build.** Nothing implemented.
Autopantry Build 2 is 63 FRs / 61 tasks, roughly double Build 1, and was ~20%
through when this surfaced. A task that passed its own gate at **33.6%
correct** stayed load-bearing for two days and several tasks before anyone
measured it; an architectural error (resolve-at-read-time) spanned three
individually-correct tasks; and the plan's own tasks 22/23 went stale
mid-flight with nothing to notice. `/slice` verifies a task, `/audit` runs at
the end — nothing checks a *component's output quality* in between. Pulls
against `007` (which makes each slice heavier) and is mechanically downstream
of `003` (if builds only grow, this worsens on its own).

## Common thread

The first three are the same shape: **the system trusts its own prose.** A
claim becomes true by being written down confidently in a document with an
authoritative title, and every later stage's job is to honour the previous
document rather than test it. `001` and `003` are both provenance-tagging
failures and are probably one fix; `002` is why any fix has to land in a
command file to exist at all.

`008` is that thread one level in — the same substitution of a confident
assertion for a checked one, but *within* a session rather than across
documents, and with evidence actually produced that tests something adjacent
to the claim. It may ultimately be one fix with `001`.

`006` is a different shape and worth keeping distinct: there was nothing to
distrust. The spec was accurate, internally consistent, and complete as a
description of a backend. The failure was that the document format could not
represent what was missing, so no amount of reading it carefully would have
found the gap — which is also why the existing `audit.md`, which checks
truthfulness, cannot catch it.

`009` is `006`'s shape rather than the first thread's: again nothing was
untrue. Task 12's build note recorded its real measured hit rate accurately.
The failure was that **no stage owns the question "is this good enough to build
on"** — `/slice` verifies one task against its own gate, `/audit` checks
documents against reality at the end, and the gap between them is where a
33.6%-correct component sat for two days holding up nutrition *and* allergy
filtering. It also has a scale term the others don't: the same pipeline that
was adequate at 35 tasks is visibly not at 61, which makes it the first
enhancement whose severity is a function of `003` staying open.

## Adding one

Number it next in sequence, drop it in `open/`, add a row to the table above
with what would have to bind for it to close. Record the diagnosis and evidence
now while it's fresh; leave the fix to a dedicated session with a clear head.
