This runs in a brand-new session. If this conversation has history above this
message, stop and tell me to start a fresh one — the point is a reader who
didn't build it and hasn't inherited its assumptions.

Read PLAN.md, SPEC.md, CLAUDE.md, and DESIGN.md. The phase being checked is
everything above the first unticked `/checkpoint` line in PLAN.md, back to the
previous checkpoint. Every task in it passed its own gate — that's already
known and isn't the question. The question is **whether what this phase built
is good enough to build the next phase on.**

1. **Real output.** For each thing the phase built that produces output, run
   it on real data — the project's actual inputs, not test fixtures — and look
   at what comes out. Name what depends on it downstream. Measure every
   **Fails if** threshold PLAN.md set. Where output has a measurable quality
   and no threshold was set, measure it anyway and say what number you'd
   consider failing. Show samples, including the worst ones. A rate of
   "returned something" is not a rate of "returned the right thing".

2. **Patterns no task decided.** Find shapes several tasks share — where work
   happens (on write or on read), what gets trusted, how failure is handled.
   For each: was it decided anywhere, or inherited task to task? Would you
   choose it starting fresh?

3. **Is the rest of the plan still true?** For each remaining task, does it
   still rest on decisions that hold? Name any made stale by what this phase
   learned. Check CLAUDE.md's hard rules and SPEC.md's notes for anything
   added mid-build by the agent rather than by me — a rule the builder wrote
   for itself isn't a decision I made.

4. **Can a person use what exists?** Re-run PLAN.md's human surface table
   against the code as it is now, not as planned.

Report only. Don't fix code or edit PLAN.md. Rank findings by consequence and
end with one of: **proceed**, **fix first** (what), or **re-plan** (which
tasks). When I've decided, tick the `/checkpoint` line and write my decision
under it in one line.
