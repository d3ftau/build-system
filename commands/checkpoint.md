This runs in a brand-new session. If this conversation has history above this
message, stop and tell me to start a fresh one — the point is a reader who
didn't build it and hasn't inherited its assumptions.

Read PLAN.md, SPEC.md and CLAUDE.md, and BUILD-LOG.md and DESIGN.md if they exist.
A build started before 2026-10-11 has no BUILD-LOG.md; its decisions are in the
plan's and spec's own notes, and you read those instead.
The phase being checked is everything above the first unticked `/checkpoint`
line in PLAN.md, back to the previous checkpoint. Every task in it passed its
own gate on the code as it was then; step 5 asks whether that still holds.
The question is
**whether what this phase built is good enough to build the next phase on.**

Scale this to the app. A personal app gets judged on whether it does the job
for me, not on production polish.

1. **Real output.** For each thing the phase built that produces output, run
   it on real data — the project's actual inputs, not test fixtures — and look
   at what comes out. Measure every **Fails if** threshold PLAN.md set. Where
   output has a measurable quality and no threshold was set, measure it anyway
   and say what number you'd consider failing. Show samples, including the
   worst ones. A rate of "returned something" is not a rate of "returned the
   right thing".

2. **Read the code fresh.** Review this phase's diff (`git log` and
   `git diff` from the previous checkpoint) as a reviewer who didn't write
   it. Grade every problem by what it does to me using the app — not by
   whether the spec mentions the case. A spec's silence isn't permission for
   something to break in a way any reasonable person would expect to work.
   Sort into: **breaks it for me**, **worth fixing**, and **minor** (listed,
   not pushed).

3. **The rulings.** Read BUILD-LOG.md's `Ruling:` lines for this phase (or,
   for an older build, the decisions recorded in PLAN.md and SPEC.md notes). Any
   you'd have decided differently, or that quietly changed what I get, name
   them.

4. **Patterns no task decided.** Shapes several tasks share — where work
   happens, what gets trusted, how failure is handled. Decided anywhere, or
   inherited task to task? Would you choose it starting fresh?

5. **Is the rest of the plan still true?** For each remaining task, does it
   still rest on decisions that hold? Which earlier passes does it rely on,
   and has anything they ran on changed since? If the real run happens once,
   does the plan still end with the full rehearsal on frozen code? A plan or
   re-plan without it is **re-plan**. Check CLAUDE.md's hard rules for
   anything added mid-build by the agent rather than by me.
   If this phase redesigned the build's core approach, re-run /explore's
   existence search (domain and generic, commercial and open source) with the
   new understanding of the job. A redesign often lands on something that
   already exists.

6. **Is it still worth it?** A challenge, every checkpoint, to what's built
   and what's still to come, limited to the expensive automation: the pieces
   that brought a new secret, permission, cross-machine link, mode or
   rehearsal rig, or that exist to fix a problem another piece created.
   Ordinary code isn't weighed. For each, the effort it has taken and will
   take (building, testing, upkeep, and the problems it caused that needed
   solving in turn) against what it saves me over its life (the manual
   step's length times how often it happens) or the mistakes it prevents.
   The chain of fixes is the warning sign. If the remaining plan rests on
   one, the verdict is **re-plan**, not proceed with trims. If I've asked
   whether this is over-engineered, answer from this step and say plainly
   what was over-built, before what to keep.

7. **Can a person use what exists?** Re-run PLAN.md's human surface table
   against the code as it is now. If this phase was meant to end deployed,
   check it's running, comes back after a restart, and that a failed run
   would reach me.

Report only. Don't fix code or edit PLAN.md. Rank findings by consequence and
end with one of: **proceed**, **fix first** (what), or **re-plan** (which
tasks). When I've decided, tick the `/checkpoint` line and write my decision
under it in one line.
