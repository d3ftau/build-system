# Enhancement: `/slice` is too small a unit of work for a build this size

**Status: OPEN** — diagnosed, not built.

## Where this came from

Autopantry Build 2 Stage 1, 2026-08-18/19. The user, after a two-day session
that overturned an architectural decision made three tasks earlier:

> *"record feedback in build system directory that slice is arguably too
> small in a build this big"*

"This big" is measurable, and the trend matters more than the absolute number:

| | FRs | Tasks |
|---|---|---|
| Build 1 | 35 | ~35 |
| Build 2 Stage 1 | 63 | 61 (incl. sub-tasks 18a–18j, 20a–20d) |

Build 2 is roughly double Build 1 and had **14 of 63 FRs ticked** when this was
recorded — i.e. this is the shape of the problem at ~20% through, not at the end.

## The evidence

**Task 12 passed its own gate while being 33.6% correct, and nothing noticed for
two days.** `canonicalResolve.ts` (ingredient → canonical identity) was built
2026-08-16, ran its tests, ticked FR-6, and reported a real measured hit rate of
~45%. That number went into `SPEC.md` as a build note. What it did *not* record
— because no gate asked — is how often a "hit" was the **right** ingredient.
Measured on 2026-08-18: **33.6% strictly correct**, with failures like `butter`
→ *Bean, butter, raw* (a legume), `milk` → *Chocolate, milk* (a confection),
`prawns` → *Prawn cracker, commercial, fried*. The task was locally correct —
it did what the plan said, its tests passed, and its own test file even
documented one of the failure modes as a known limitation. It was the
foundation for FR-14's nutrition math and FR-42's *allergy exclusion*, and it
was wrong enough to make both meaningless.

**The thing that exposed it was not a slice.** Task 19 (unit conversion) was
built and verified normally. Its gate passed. Only when its output was pointed
at real data did the user observe that every recipe reported incomplete
nutrition — and chasing *that* symptom, through work that is not a task in any
plan (measuring four resolution approaches against 137 real ingredient names),
is what surfaced the 33.6%. No per-task lens would have found it, because no
individual task was defective.

**An architectural error spanned three tasks, each individually correct.**
`recipe-query/index.ts` resolves ingredients *at query time*. That pattern was
introduced by task 16, extended by task 18d, and extended again by
2026-08-18's resolver rewrite — which swapped the matcher and preserved the
call sites without questioning them. The user, on seeing it: *"why would this
be running on find recipes. it should run on recipe import."* Correct. Each
slice honoured the shape it inherited; the shape was wrong; three passes over
the same file left it wrong.

**The session's most valuable output was work no slice would have produced.**
Retiring the matcher, the write-time correction, the avoid-list merge, the
category layer, and the Ollama access design all came from conversation and
measurement against real data — not from executing a numbered task. All of it
is now documented, but none of it originated inside the pipeline.

**Second instance, same day, outside `/slice` entirely — worth its own bullet
because it shows the failure isn't confined to the pipeline.** After the
write-up above was committed, the agent wrote a new hard rule
(build-2 `CLAUDE.md`, "ingredient resolution runs at write time, never read
time") and immediately built against it — including a fail-closed
recipe-eligibility exclusion for the case where an ingredient hadn't resolved
yet. The user had already, in the same continuous conversation, dismissed
that exact scenario as not worth engineering around ("unless someone is
speed running the app it should never be an issue anyway"). The agent built
it anyway, a few exchanges later, citing the hard rule it had itself written
that morning as if it were settled external authority — not noticing the
conversation had already moved past the premise. Caught by the user, not by
any gate; the code had already typechecked and passed 102 tests. This did
not happen via `/slice` — it was ordinary conversational "let's build the
next thing" work, with no task boundary, no gate, no plan file in the loop
at all. A fix scoped only to `commands/slice.md` or `plan.md` would not have
prevented it.

**The correction itself needed a second correction, same conversation.**
Asked to remove the offending piece, the agent proposed three named items
(the eligibility exclusion; the read/write split it sat inside; a
quantity-negligibility helper the exclusion shared with an unrelated fix)
and asked which the user meant. The user's shorthand reply named only one
item by number and asked for two others explained "in plain English" — the
agent executed against a plausible but wrong reading of which numbered list
the shorthand referred to (there were two, from two different messages),
removed only the exclusion, and left the shared helper and its second
caller in place with documentation asserting they were being kept
deliberately. The user had to correct a second time — "2 is fine. 3 is
absolutely not needed" — to get the rest removed. Not a new mechanism, but
a compounding instance of the same one: once again, no gate existed to
check the agent's own read of an ambiguous instruction against what was
actually meant before code (and, this time, prose *asserting the code was
correct*) shipped.

## The general failure mode

`/slice`'s contract is explicit: **"Implement the next unstarted task from
PLAN.md. Only that task."** Its verification is per-task and local — run
`make check`, tick the FRs this task satisfies, show the diff, stop. That is a
good contract for *correctness of a task*. It has no lens for three things that
only exist above the task level:

1. **Output quality of an already-shipped task.** Task 12's gate could only ask
   "does the resolver run and return something." Nothing asked "is what it
   returns good enough for what depends on it." A hit rate went into the spec
   as a fact with no threshold attached, so no later step could fail against it.
2. **A pattern repeated across tasks.** Resolve-at-read-time was never one
   task's decision; it was three tasks agreeing with each other.
3. **Whether the plan's own decomposition still holds.** Tasks 22/23 were
   planned against a three-field allergy/intolerance/avoid model that this
   session collapsed into one. Nothing in the pipeline re-examines a plan
   mid-flight; `/plan` runs once, at the start.

In a ~16-task build these close by accident: you reach the end soon, `/audit`
runs, and the whole thing gets exercised together. **In a 61-task build, a
weak early task is load-bearing for weeks.** Build 1 has an `AUDIT.md`; Build 2,
at 20% through, has none and will not have one until the end — which is exactly
when finding this class of problem is most expensive.

## Candidate fixes

Deliberately several, none scoped to the exact symptom (README's own rule).

- **A checkpoint whose unit is not the task.** At phase boundaries — `PLAN.md`
  already has them ("Narrow spine", "Widen — …") — verify the *output* of what
  the phase built against real data, not that its gates passed. Note the
  existing `/audit` is post-build and checks document truthfulness, which is a
  different question from "is this component's output good enough to build on."
- **Make quality thresholds part of a task, not a number in a build note.**
  `/plan` (or `/contract`) could require that any task producing a *measurable
  quality* output declares what value would be unacceptable — so 33.6% would
  have failed something instead of being recorded as an interesting fact. This
  is closest to `008`'s thesis: evidence was produced that tested something
  adjacent to the claim.
- **A re-plan trigger.** Nothing currently lets the pipeline notice that a
  decision invalidated later tasks. Tasks 22/23 are stale right now and stayed
  stale until a human said so.
- **Larger or differently-shaped slices for later phases.** Weakest option and
  recorded mainly to be argued against: small slices are what make per-task
  verification honest. The problem is not that a slice is small, it is that
  *nothing else is bigger*.

## Open, not resolved here

- **This pulls against `007`.** `007` argues `/slice` needs an *approval
  checkpoint before* work — making each slice heavier. This argues the
  per-slice unit is too small for the build. Both can be true (more ceremony
  per slice, plus a coarser periodic check), but a fix for one should not be
  written without reading the other; naïvely doing both makes a 61-task build
  substantially slower.
- **Directly downstream of `003`.** If scope can only ratchet up, builds keep
  getting bigger, and this problem gets worse mechanically over time. Build 1 →
  Build 2 already doubled. A fix here that assumes builds stay ~60 tasks is
  betting against `003` staying open.
- **Whether an agent can self-trigger this.** A periodic quality checkpoint the
  same agent decides to run, on work it built, has the same self-trust problem
  the README's "common thread" names for `001`/`003`/`008`. It may need to be a
  hook, a human-invoked command, or explicitly a fresh-context session.
- **The second instance above may be `008`'s failure mode, not `009`'s, and
  worth re-examining once `008` gets a fix.** `009`'s core diagnosis is about
  `/slice`'s per-task lens across a multi-task pipeline; the second instance
  had no task, no gate, no pipeline — just an agent citing its own
  minutes-old prose as settled authority inside one conversation, which is
  closer to `008`'s "claims accepted on evidence that tests something
  adjacent to the claim" and the README's "common thread" (the system trusts
  its own prose) one level in. Left here rather than filed separately only
  because the user's own instruction was to add it as evidence to this file;
  whoever picks up `008` or `009` should decide whether it wants to move.
- **What "real data" means as a gate.** The 33.6% only became visible by running
  against a real 19-recipe library and 1,740 real AUSNUT rows. A synthetic
  fixture would have shown 100%. Whether that can be required generally, or
  only for components whose whole job is matching messy real input, is
  undecided.

## Still open

- `commands/slice.md` is unchanged.
- No phase-boundary or mid-build quality checkpoint exists in any command.
- Recorded in Autopantry's own documents (`SPEC.md` FR-6, build-2 `CLAUDE.md`
  hard rule 12) so the specific defects are tracked there — which is a
  project-level record, not a binding fix, and will not reach any other build.
