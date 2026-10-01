# Enhancement: `/slice` settles the plan's open decisions silently, mid-build

**Status: DONE** — `/slice` stops before code; `/plan` marks open decisions.

## Where this came from

Autopantry Build 1, 2026-08-06/07, across several consecutive slices. The user,
after the third round of stripping out work that had just been built:

> *"record feedback for slice that before starting work it should give a
> summary of the plan task it is performing and the approach it will use. then
> ask for approval before proceeding"*

The pattern behind that request, all within one day:

- **Task 16's revision.** `PLAN.md` said "shelf life must be per (product,
  location)". It did not say what should happen for a location a product
  shouldn't be kept in. The slice invented a mechanism where an absent row
  meant the household *may not* store it there, built it, tested it, and
  reported it. Reversed on sight: *"why are we forbidding anything? the goal is
  pre filling data, not telling people what to do with things."*
- **A contradiction check and a safety-flagging tier**, built on top of that
  mechanism across two slices. Both stripped: *"there's way too much focus on
  the location in general. we don't need to be making decisions for people -
  they aren't morons."*
- **Task 17's RLS policy.** The plan said "wire the app to Realtime". Whether
  `pantry_items` should get an anon read policy, and how scoped, was decided
  inside the slice.
- **Task 18's `notifications` schema**, its column-level grants, and the
  decision that FR-11 alerts are not household-scoped — all chosen in-slice.
- **Task 17b added a mobile typecheck to `make check`** — defensible, and
  anticipated by SPEC.md, but not asked for.

Every reversed item was one sentence's worth of intent. None of them needed the
implementation to exist before the user could reject them.

## The general failure mode

**`/slice`'s first instruction is "Implement the next unstarted task from
PLAN.md."** There is no checkpoint between reading the task and writing code.
The command's entire reporting apparatus — run the gate, tick the FRs, show the
diff — fires *after* the work exists, so the only moment the user sees the
approach is the moment the cost of changing it is highest.

That would be tolerable if plan tasks were complete specifications. They are
not, and structurally cannot be: `/plan`'s own job is ordering and scoping, and
it explicitly records "ambiguous / my own judgment calls" as a section, which
is an admission that tasks ship with open questions attached. The slice is
where those get answered, and it answers them without saying so.

The decisions that get reversed share a signature: they are **not** the thing
the task named. Nobody disputed per-location shelf life or wiring up Realtime.
What got rejected was the unasked-for adjacent choice — a policy, a
prohibition, a schema, a flagging tier. So the checkpoint that matters is not
"here is what the task says" (already agreed, in the plan) but "here is what
the task *doesn't* say that I am about to decide."

Related to `002` — a principle that exists in prose but not in a command file
does not bind — except the principle here does not exist in prose either.

## Candidate fix

`/slice` opens by stating, before any edit: which task it is picking up, what
will actually change (files, schema, contracts), and — the load-bearing part —
**any decision the plan leaves open that the implementation will have to
settle**. Then it stops and waits.

Short. A checkpoint, not a design document. It replaces nothing: the existing
after-the-fact reporting, the gate, and the FR ticks all stay.

## Open, not resolved here

- **Approval fatigue is a real risk.** Some slices genuinely have no open
  decisions (a migration the plan fully specifies). Always pausing trains the
  user to approve reflexively, which is worse than not pausing. Whether the
  stop should be conditional on there being an open decision to name — and
  whether an agent can be trusted to judge that — is undecided.
- Whether this belongs in `slice.md` alone, or whether `/plan` should
  additionally be required to mark tasks that carry known-open decisions, so
  the slice has something to point at rather than deriving it.
- The same argument applies to any command that writes code from a prior
  document. It is being scoped to `/slice` because that is where the evidence
  is, which is exactly the narrow-special-case risk the README names.

## Still open

- `commands/slice.md` is unchanged.
- Recorded in Autopantry's project memory so it applies there in the
  meantime — which is a project-level fix, not a binding one, and will not
  reach any other build.

## Implementation status (2026-10-01)

- `commands/slice.md` — new "Before writing any code" section: which task,
  what will change, **every decision the task forces that PLAN.md and SPEC.md
  don't settle**, and any second unknown. Then it stops and waits. After the
  work, it lists any decision made that wasn't on the approved list.
- `commands/plan.md` — every task carries a **Leaves open:** line, so the
  slice has something to point at rather than deriving it alone.
- **Approval fatigue, decided: always stop** — the user's original request,
  confirmed 2026-10-01. Kept cheap by making the summary short and allowing
  "nothing open".
- **Knock-on fix:** `hooks/verify-before-stop.sh` only ran `make check` when
  the latest user message was `/slice`. With a pause, code lands in the turn
  answering "go ahead", so the gate would never have fired. It now runs when
  `/slice` is the most recent pipeline command (excluding `/stuck`) and the
  turn used a file-changing tool. Tested against synthetic transcripts for
  each case and timed at ~0.75s on a 74MB real one. Checking real Autopantry
  transcripts showed the old detection was already missing follow-up turns
  inside a slice.
