This runs in a brand-new session. If this conversation has history above this
message, stop and tell me to start a fresh one — the point is a reader who
didn't build it and hasn't inherited its assumptions.

Read PLAN.md, SPEC.md, CLAUDE.md, BUILD-LOG.md, and DESIGN.md if it exists.
The phase being checked is everything above the first unticked `/checkpoint`
line in PLAN.md, back to the previous checkpoint. Every task in it passed its
own gate — that's already known and isn't the question. The question is
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

3. **The rulings.** Read BUILD-LOG.md's `Ruling:` lines for this phase. Any
   you'd have decided differently, or that quietly changed what I get, name
   them.

4. **Patterns no task decided.** Shapes several tasks share — where work
   happens, what gets trusted, how failure is handled. Decided anywhere, or
   inherited task to task? Would you choose it starting fresh?

5. **Is the rest of the plan still true?** For each remaining task, does it
   still rest on decisions that hold? Check CLAUDE.md's hard rules for
   anything added mid-build by the agent rather than by me.

6. **Can a person use what exists?** Re-run PLAN.md's human surface table
   against the code as it is now. If this phase was meant to end deployed,
   check it's running, comes back after a restart, and that a failed run
   would reach me.

Report only. Don't fix code or edit PLAN.md. Rank findings by consequence and
end with one of: **proceed**, **fix first** (what), or **re-plan** (which
tasks). When I've decided, tick the `/checkpoint` line and write my decision
under it in one line.
