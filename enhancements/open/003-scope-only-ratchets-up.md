# Enhancement: the pipeline can grow a build's scope but never shrink it

**Status: OPEN** — not implemented. Diagnosed 2026-07-26, no command changed yet.

## Where this came from

Session on `build-system`, 2026-07-26, reviewing the build docs for
`file-cleanup` (the task-extractor build) against PLAYBOOK.md and the command
set. Greg's framing: the MVP is *"a list of candidate tasks and nothing more,"*
and the process *"bullied me into saying i wouldnt get benefit without
reminders, which is ridiculous."*

He's right on both counts, and the second one has an identifiable line of
origin.

## The originating line

`DISCOVERY.md:25`:

> Started with email... Stress-tested against the original failure mode: a
> single notification is structurally the same event as the original chat —
> seen once, still forgettable. **User confirmed it needs to *nag until marked
> done***, not fire once.

Read the structure rather than the content:

1. The agent constructed an argument ("a single notification is structurally
   the same event as the original chat").
2. The user agreed with the agent's argument.
3. The agreement was recorded as a **user requirement**, indistinguishable in
   the document from something the user raised unprompted.

Two lines later (`DISCOVERY.md:27`) the user *did* push back, on the OneNote
comparison. The document records the pushback, concedes it — *"a fair
distinction"* — and then retains the conclusion regardless: *"The
notification/nag layer still does most of the work of solving 'forgetting'."*
Pushback absorbed, nothing changed.

## The general failure mode

**`[STATED]` conflates two different provenances.** It currently means
"traceable to the human's mouth." It does not distinguish:

- **the user raised this unprompted** — a real requirement
- **the user assented to an argument the agent authored** — the agent's
  reasoning with a signature on it

The second is not a requirement. But once written into DISCOVERY.md as "User
confirmed," it is permanently indistinguishable from the first, and every
later stage treats it as a fixed input.

This is a sibling of `001`, with a different provenance class. `001` found
`[STATED]` conflating "user decided" with "an earlier document asserted."
This one adds a third: "user agreed with something I argued for."

Note that `/discovery` actively *induces* this. Its instructions say *"Push on
it,"* *"Suggest angles I haven't considered,"* *"If you think I'm converging
too early... say so."* Pushing is correct and should stay. The bug is that
what the user says *while being pushed* gets recorded with exactly the same
weight as what they volunteered.

## The structural amplifier: every scope question ratchets one way

`/roadmap` asks, for each build:

> "if nothing after this ever got built, would this still be worth using?"

The only failure state this can detect is a build that is **too small**.
PLAYBOOK.md:122 makes the remedy explicit:

> "Re-scope it or merge it forward until the answer is yes."

There is no question in any of the twelve command files that can make a build
**smaller**. The pipeline has a growth mechanism and no shrink mechanism.

Compounding it, the test was applied to Build 1 **as a bundle** and returned
"yes." Nothing ever asked the dual question: *what is the smallest subset of
this build that still returns yes?*

## The contradiction was already in the document

`ROADMAP.md:7`, the spine section, states the right answer before scope grew:

> Extraction: correctly telling, from raw unstructured text, "this was a
> decision or solution that never got executed." **Everything else — which
> source, how many sources, where it lands, how it surfaces — is either
> plumbing around this judgment call or a separate bet that doesn't depend on
> it.**

Eighteen lines later, Build 1 bundles in the plumbing anyway: `describe`,
ClickUp sync, status model, dependency links, hand-set reminders. The document
names its own spine correctly and then contradicts itself within the same
file, and no stage in the pipeline reads a document against itself.

## Three more places it should have been caught

**1. Preservation is framed as a virtue.** `ROADMAP.md:25`: *"The nag
requirement from discovery is **preserved rather than dropped** — it is
delegated to ClickUp."* No stage ever asks whether an inherited requirement
should still exist. Each stage's job is to honour the previous document.

**2. `/brief`'s one shrinking question is structurally skipped.** `/brief`
lists *"the smallest version I'd actually use"* among its topics — under the
instruction *"Cover only what isn't already answered."* Because `/discovery`
and `/roadmap` had run, that question read as settled and was skipped.
`BRIEF.md` has no smallest-version section; its Definition of Done is the
entire pipeline including the nag. **The more of the process you run, the less
likely the one question that could shrink the build gets asked.**

**3. A plan-invalidating finding was filed as a risk.** `ROADMAP.md:26` notices
that the hand-set ClickUp reminder is a per-item manual step, and that
*"per-item manual steps are exactly what discovery said isn't available from
you"* — then argues it away and files it under *"The risk to watch."*
PLAYBOOK.md's own "Breaks it" list (line 556) names this exact move: *"letting
a finding that invalidates the plan get recorded as a note instead of
reordering the plan."* The principle exists in prose and binds nothing —
which is `002`'s thesis, recurring.

## What it cost

Downstream of one confirmed-under-pressure sentence:

- ClickUp as a hard Build 1 external dependency
- the `sync` stage, the status model, dependency links
- the `describe` stage — and this one is worth isolating. Review reads cited
  turns straight from the ledger; `ROADMAP.md:24` says explicitly *"no
  re-fetch, no cost."* So `describe` exists **only** to write a task body for
  ClickUp. `ROADMAP.md:70` identifies it as *"the part of Build 1 that scales
  with API spend."* The most expensive component of the MVP serves only the
  delivery layer that isn't the MVP.
- a completion gate outside the software. `SPEC.md:957`: Build 1 is not done
  until *"the hand-set reminder has pushed to your phone on **two
  consecutive** intervals."* The MVP cannot be declared finished until a manual
  step performed by hand in a third-party app fires twice on consecutive days.

Resulting size: 45 FRs, 41 planned tasks, first end-to-end run at ~task 31.
(That last number is also `002`'s open item — the two compound: an inflated
scope planned horizontally.)

## The gap in the system, stated generally

`/explore` was built to catch a claim about **the world** that was false. It
works — it caught the ClickUp nag-capability error.

Nothing checks the other class. There is no step that asks *"is this
requirement actually the user's, or did I talk them into it?"* The nag
requirement was never a factual error and `/explore` would pass it without
comment. It was a requirement the agent authored and then attributed.

## Candidate fixes, not yet decided

Raw material for the dedicated session, deliberately not prescribed:

- **`/discovery`** — when the user agrees with a requirement *the agent argued
  for*, record it distinctly from one they raised unprompted (e.g.
  `[AGREED-UNDER-ARGUMENT]`). Downstream stages treat those as the first
  candidates to cut. This needs to survive a fresh session, so it has to change
  what the command asks for, not be a lesson anyone remembers.
- **`/roadmap`** — add the inverse of the existing test: *"what is the smallest
  subset of this build that still returns yes?"* If the answer is smaller than
  the build, that subset **is** the build and the remainder moves to the next
  one. Stronger variant: refuse to put anything in Build 1 that isn't required
  to test the spine `/roadmap` just wrote. That alone would have cut this build
  to a candidate list.
- **`/brief`** — remove the smallest-version question from the "don't re-ask
  what's settled" exemption. It is the one question that must be asked every
  time, and most of all when discovery has run.
- **Reading a document against itself.** The spine paragraph and the Build 1
  paragraph contradict each other in the same file. No command checks internal
  consistency of a document it just wrote. Possibly a `/roadmap` self-check,
  possibly a broader pass.

## Relationship to the other enhancements

- **`001`** — same root: provenance tags that record traceability rather than
  reliability. `001` covers document-asserted claims; this covers
  agent-argued-then-assented claims. A single fix to the tagging scheme could
  plausibly cover both, which is an argument for doing them in one session.
- **`002`** — the "recorded as a note instead of acting on it" failure here is
  a live instance of a PLAYBOOK principle that binds nothing. Also, the 41-task
  horizontal plan is `002`'s open item applied to this build's inflated scope.

## Not yet decided for `file-cleanup` itself

Whether to re-cut Build 1 to the candidate list and push ClickUp/`describe`/
reminders to Build 1.5, and what that does to the existing SPEC (45 FRs) and
PLAN (41 tasks, already partially scaffolded — commit `661e6c4`). Separate
call from the build-system fix, and entangled with `002`'s open item about
regenerating that PLAN.
