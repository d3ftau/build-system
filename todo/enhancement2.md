# Enhancement: principles in PLAYBOOK.md prose don't reach the commands

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

- **`one unknown at a time` is still orphaned.** No command or hook carries it.
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
