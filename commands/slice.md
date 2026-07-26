Implement the next unstarted task from PLAN.md. Only that task. $ARGUMENTS

When done:
1. Run `make check` (if the Makefile has a `check` target yet) plus any test
   PLAN.md names for this specific task, and paste the real terminal output —
   not a summary. Only run SPEC.md's full Verification Gates script if PLAN.md
   marks this task as a phase-assembly or final-gate task — most tasks aren't,
   and a gate that depends on a later phase's artifact (deploy tooling, a
   coverage floor, anything needing infra that doesn't exist yet) will fail
   for reasons that have nothing to do with what this task built.
2. Tick the FR checkboxes in SPEC.md that this task satisfies
3. Show me the diff
4. Stop. Do not start the next task.
