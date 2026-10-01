# Enhancement: principles in PLAYBOOK.md prose don't reach the commands

**Status: DONE** — closed 2026-10-01 by redefining what PLAYBOOK.md is,
not by building a checker. See "Implementation status" at the end.

## Where this came from

Session on `build-system`, 2026-07-26, reviewing the `PLAN.md` that `/plan`
had produced for `file-cleanup` (the task-extractor build). The plan was 41
tasks. Nothing ran end to end until roughly task 31.

It built infrastructure first — schema, locks, regime-safe queries — then each
pipeline stage fully in dependency order: real ingestion, then real screening,
then real describe, then real sync. Textbook horizontal layering: no way to
verify anything as a whole until almost all of it existed.

That is precisely what PLAYBOOK.md Phase 4 tells you not to do, in a bolded
line that had been in the file since the first commit (`333c972`, 2026-07-24):
*"Vertical slices, not horizontal layers."*

## The general failure mode

**PLAYBOOK.md is documentation. The command files are the program.** A
principle that lives only in the playbook's prose has no effect on what any
agent actually produces, because no agent reads the playbook while working —
it reads the slash command it was invoked as.

`commands/plan.md` as originally written (`333c972`) asked for:

> "An ordered task list, each task small enough to complete and verify
> independently."

That is the entire instruction about ordering. Nothing about vertical slices,
nothing about end-to-end, nothing about build philosophy. `/plan` did not
disobey the playbook — it was never shown it. And `/slice` cannot recover
from this later, because `/slice` follows the numbers in `PLAN.md`; by the
time the build starts, the ordering decision is already frozen.

The generalizable version: **for every principle in PLAYBOOK.md, ask which
file makes it happen.** If the answer is "the playbook says so," it doesn't
happen. There are three ways for a principle to actually bind — a command
file, a hook, or `CLAUDE.md` in the target project — and prose in the
playbook is none of them.

## Audit of the other Phase 4 principles

Checked at the time this was written, for the same gap:

| Principle | Where it binds | Status |
|---|---|---|
| Scaffold first, always | `commands/plan.md` item 2 | Bound |
| Never accept "it works" as evidence | `hooks/verify-before-stop.sh` (runs `make check` before the turn can end) | Bound, enforced |
| Guard against gate-gaming | `hooks/no-skipped-tests.sh`, plus verbatim in generated `CLAUDE.md` | Bound, enforced |
| Vertical slices, not horizontal layers | *was nowhere* → now `commands/plan.md` item 3 | Fixed here |
| One unknown at a time | **nowhere** | **Still orphaned** |

"One unknown at a time" (a slice combining a new API, a new library and a new
pattern should be split) appears in no command file and no hook. `/plan`
is never told to split such tasks and `/slice` is never told to refuse them.
It is the same bug as the vertical-slice one, still open.

## Second failure, in the fix itself

The first fix (`d1511c6`) added this to `commands/plan.md`:

> "Sequence it so something runs end to end as early as possible, with the
> hard parts faked — a stubbed API response, three rows of sample data."

Greg rejected the fake-data half: *"i disagree with pumping fake data through
the whole thing — but i agree in principle that the build order should get to
a working end to end solution as quickly as possible."*

He's right, and the reason is worth keeping. Two separate ideas had been
fused into one instruction:

1. **Get to end-to-end fast** — the actual principle.
2. **Fake the hard parts** — one possible way of achieving it, and the way
   that produces a wide pipe full of pretend data.

A pipeline that runs end to end on stubs proves the wiring and nothing else.
Every stage still has its first contact with reality later, and they all have
it at once — which is the exact failure the ordering was supposed to prevent.
It converts "nothing has ever run together" into the more dangerous
"everything appears to work and none of it has met reality."

The correct slice is **narrow, not fake**: fewer cases, real code at every
stage. One real conversation becoming one real ClickUp task, handled badly,
beats forty tasks of scaffolding around sample rows. Note that PLAYBOOK.md's
own first line already said this — *"one complete path from input to output,
even handling a single case badly"* — and the fake-the-hard-parts rule
underneath it is what dragged the meaning sideways.

Faking now has to earn its place: only where the real thing is genuinely
unavailable at that point in the build (an export that hasn't arrived, an API
that costs money per call), and the plan must name the task that makes it
real.

## What was changed

- `commands/plan.md` item 3 — rewritten. Narrow-but-real is the default;
  "narrow means fewer cases, not pretend data"; faking is a named exception
  requiring the plan to say which task makes it real.
- `PLAYBOOK.md` Phase 4 — "Fake the hard parts first" replaced by "Narrow and
  real, not wide and fake" plus "Fake only what isn't available yet."
- `PLAYBOOK.md` Phase 3 — now states that the ordering is the point, not just
  the task contents, and puts "how far down the list is the first end-to-end
  run" at the top of the review checklist.

## Still open

- ~~**`one unknown at a time` is still orphaned.**~~ **Closed 2026-10-01** —
  `commands/plan.md` (one unknown per task; split if two) and
  `commands/slice.md` (names a second unknown and proposes a split before any
  code).
- **`file-cleanup/PLAN.md` has not been regenerated.** It is still the
  41-task horizontal plan with the first end-to-end run at ~31. The fixed
  `/plan` has never been run against it. Deciding whether to regenerate it or
  hand-reorder it is a separate call, and is entangled with the fact that four
  of that project's open questions are BLOCKED on export data nobody has
  looked at yet (see `commands/explore.md` and the `f0a0b3f` commit).
- **No mechanism prevents a recurrence.** Both fixes so far have been
  "someone noticed and edited a file." Nothing checks that a new principle
  added to PLAYBOOK.md also lands somewhere binding, and nothing would catch
  the next orphaned principle. Worth considering in the same session as
  `enhancement1.md`, since both are about the system trusting its own prose.

## Implementation status (2026-10-01)

**Resolved by reframe, decided by the user:** *"the commands themselves are
the source of truth now and the Playbook just explains how they work and
should be used."*

That dissolves the recurrence problem rather than policing it. The failure
was a rule that existed only in the playbook; under this framing there is no
such thing — an agent-facing rule that isn't in a command was never adopted,
and the playbook describing it is just stale. The tag-plus-script checker
proposed earlier the same day (option A) was dropped as unnecessary.

The split that makes it workable: **guidance for the agent** must bind in a
command or hook; **guidance for the user** (phone vs desk, model choice, kill
criteria) is the playbook's own and needs no binding.

- `PLAYBOOK.md` intro — states the commands are the source of truth, the
  playbook explains them, a disagreement means the playbook is stale, and new
  agent rules go into a command first. Closing line now says to fix the
  command, then the playbook.
- **One unknown at a time** — `commands/plan.md`, `commands/slice.md`.
- **Two orphans found while checking** (neither had been noticed by the
  fold-in session that preceded this, which is this file's thesis in action):
  - two failed attempts → stop and explain, `/stuck`-style —
    `commands/slice.md`;
  - no devbox-specific paths/IPs/hostnames in code — the project `CLAUDE.md`
    `/contract` writes (previously only the compose file, via `/deploy`).
- Kill criteria checked and left in the playbook alone, deliberately: it's a
  decision for the user, not agent behaviour.
- **`file-cleanup/PLAN.md` regeneration — closed as moot.** That build
  finished on the old plan (README and doc sync committed 2026-08-01).

**What this doesn't catch:** the playbook going stale relative to the
commands. That now misleads a reader rather than silently dropping a rule,
which is a much cheaper failure — and the intro tells the reader which file
to believe.
