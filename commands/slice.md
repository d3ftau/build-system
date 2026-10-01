Implement the next unstarted task from PLAN.md. Only that task. $ARGUMENTS

If the next unticked item is a `/checkpoint` line, build nothing. Tell me the
phase is complete and that /checkpoint runs in a brand-new session, then stop.

## Before writing any code

Tell me, briefly — a checkpoint, not a design document:
- Which task, in one line.
- What will change: files, schema, interfaces, anything added to `make check`.
- **Every decision this task forces that PLAN.md and SPEC.md don't settle.**
  Start from the task's "Leaves open" line, then add what you find. The ones
  that get reversed are rarely the thing the task names — they're the adjacent
  choice nobody asked for: a policy, a prohibition, a schema, a flagging tier,
  an extra check. If you'd build anything the task didn't ask for, it's on
  this list. If there's nothing, say "nothing open".
- If the task carries more than one unknown — a new API, a new library, a new
  pattern — say so and propose a split.

Then stop and wait for my go-ahead. No edits until I give it.

## While building

Never implement a model call for work whose rules can be enumerated. If the
task reads as a decision tree, write the logic. If PLAN.md specifies a model
call for something enumerable, stop and say so rather than building it. The
inverse holds too: before writing rules *instead* of a model call, name the
inputs they read — if one of them is the thing being worked out, the rules
can't be written and you should say so.

Evidence has to test the claim itself, not something next to it:
- **A bug is real only if reality can produce it.** Before reporting one,
  state the precondition and where you confirmed the real upstream system
  can reach it. A passing repro proves the code permits it, nothing more.
- **An invented test input is a finding.** If no real input reaches a branch
  and you'd have to fabricate one, stop and tell me — the branch probably
  models something that can't happen.
- **Test the reverse of every state change**, not just the direction the
  task was written in.
- If the task has a **Fails if** threshold, measure it on real data and
  report the number. Below the threshold, the task isn't done.

If a second attempt at the same problem fails, don't make a third. Stop and
tell me what you expected, what actually happened, and what you think the
root cause is — the same as /stuck.

## When done

1. Run `make check` (if the Makefile has a `check` target yet) plus any test
   PLAN.md names for this specific task, and paste the real terminal output —
   not a summary. Only run SPEC.md's full Verification Gates script if PLAN.md
   marks this task as a phase-assembly or final-gate task — most tasks aren't,
   and a gate that depends on a later phase's artifact (deploy tooling, a
   coverage floor, anything needing infra that doesn't exist yet) will fail
   for reasons that have nothing to do with what this task built.
2. Tick the task in PLAN.md and the FR checkboxes in SPEC.md it satisfies.
3. List every decision you made that wasn't on the list I approved.
4. Show me the diff.
5. Stop. Do not start the next task.
