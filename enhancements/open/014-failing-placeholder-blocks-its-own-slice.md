# Enhancement: The required failing placeholder test blocks the slice that creates it

**Status: OPEN**

## Where this came from

fashion-bot build 1, 2026-10-09, task T1 (scaffold). `/plan` requires
"one placeholder test that currently fails". T1 built exactly that. Then
`verify-before-stop.sh` blocked the turn: "make check failed — this must pass
before the task is done". The agent may not skip, xfail or delete the test,
or edit `.claude/known-failing-checks`, so the only ways out were the user
editing the allowlist or starting T2 early. The user:

> *"This has happened before I thought /plan was supposed to take it into
> account"*

## The failure mode

The escape hatch exists, but nothing that runs knows about it.

- `verify-before-stop.sh` honours `.claude/known-failing-checks`, which the
  user maintains (commit `8c2a493`).
- **Only `PLAYBOOK.md` mentions that file.** Lines 58 and 68 call the
  placeholder the example case. `commands/plan.md` asks for the failing
  placeholder and never mentions the allowlist. `commands/slice.md` doesn't
  either. Nothing tells the user to add the entry before the scaffold slice
  runs.
- So every new project hits the block at its scaffold slice. This is `002`
  again: guidance in playbook prose doesn't reach the commands.

## Candidate fixes

Not prescriptive.

- **`plan.md`:** the scaffold task's verification states the expected red and
  tells the user to add `test_placeholder` to `.claude/known-failing-checks`
  before running it. The task that replaces the placeholder tells them to
  remove the entry.
- **Or drop the requirement for a test that stays failing.** The scaffold task
  shows the gate catching a failure once (paste the red output), then lands a
  trivial passing test in the same slice. That proves the gate runs without
  leaving it red across a task boundary, and the allowlist is no longer
  needed for this case.
- **Or merge the scaffold into the first real-test task**, so the placeholder
  never outlives a slice.

## Still open

- `commands/plan.md` and `commands/slice.md` are unchanged.
