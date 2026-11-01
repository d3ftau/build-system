Build the current phase of PLAN.md. $ARGUMENTS

Read PLAN.md, SPEC.md, CLAUDE.md and `~/projects/platform/PLATFORM.md`. Start
at the first unticked item.

`$ARGUMENTS` can change this, in plain words:
- **A path** — "builds/build-2/PLAN.md" — when the plan isn't in the current
  directory (a repo holding several builds keeps one folder per build; BUILD-LOG.md
  goes next to that plan).
- **"one task"** or **"stop after each task"** — build one task, run its checks,
  report, and stop, the way the old per-task approval worked. For a risky build
  or one I want to follow closely.

**Older plans** (written before 2026-10-11) differ: tasks may be `### Task N —`
headings marked done with ✅ instead of checkboxes — mark them done the way the
plan already does, and don't convert it. They have no `⏸ STOP` marks and were
written when every task stopped for approval, so a "Leaves open" line there is a
decision the plan didn't settle: make it a logged ruling if it's cheap to undo,
and stop and ask if it's expensive to undo or changes what I'd see in a way I
haven't been shown. If the plan carries no such lines, nothing was left open.

If it's a `/checkpoint` line, build nothing. Tell me the phase is complete and
that /checkpoint runs in a brand-new session, then stop.

## Run the phase without stopping

Work task after task until the next `/checkpoint` line. An older plan may have
none: then stop at the next phase heading, and if it has no phases either,
after about ten tasks — report and stop, so a long plan never runs to its end
in one go. Don't check in between
tasks — the questions were asked at /plan, and every round trip that carries
no decision just costs me waiting time.

Only these stop you:
- **A `⏸ STOP` task.** Ask what it says, with your recommended answer, and
  wait. Carry on after I answer.
- **Something destructive or irreversible** — deleting data, dropping a table,
  overwriting something not in git.
- **Something security-sensitive** — secrets, exposing a port beyond what
  PLATFORM.md allows, permissions.
- **Something outside this project** the plan doesn't name — pushing, another
  repo, system config. What the plan names (deploying on the platform,
  installing its systemd unit) is in scope.
- **Two failed attempts at the same problem.** Don't make a third. Stop and
  tell me what you expected, what happened, and what you think the root cause
  is — the same as /stuck.
- **A plan so wrong that every way forward is a guess.**

## Rulings, not stalls

Everything else that neither PLAN.md nor SPEC.md settles, you decide. Log
each decision in `BUILD-LOG.md` in the project root as it's made:

`T4: Ruling: <what you decided> — <why> — <what it costs if wrong>`

Deviating from the plan without a logged ruling is a decision made in secret.

If a ruling **changes what I get or see** — a question /plan should have asked
and didn't — take the choice that's easiest to undo and log it as
`T4: Ruling (you'd notice): …`. If the choice would be expensive to undo,
it's a stop instead.

BUILD-LOG.md is also your memory. After a context compaction, trust it, the
ticks in PLAN.md and `git log` over your recollection, and never redo a task
the log marks done.

## Each task

- **Watch a new test fail before writing the code that passes it**, and know
  which break it catches. A test that passes first time proves nothing.
- **Never implement a model call for work whose rules can be enumerated.** If
  the plan specifies one for something enumerable, that's a ruling — build the
  code and log it. The inverse: before writing rules instead of a model call,
  name the inputs they read; if one is the thing being worked out, the rules
  can't be written — stop and say so.
- **Evidence tests the claim itself.** A bug is real only if the real upstream
  system can produce it — state the precondition and where you confirmed it.
  A test input you had to invent to reach a branch is a finding: the branch
  probably models something that can't happen; log it. Test the reverse of
  every state change. Measure any **Fails if** on real data; below it, the
  task isn't done.
- **Finish the task:** run `make check` (once it exists) plus any test the plan
  names, and read the output. Tick the task in PLAN.md and the FRs in SPEC.md
  it satisfies. Commit, message starting with the task id. Append
  `T4: done — <commit> — make check: <result>` to BUILD-LOG.md in the same
  step.

## At the end of the phase: report

Write it for someone learning, in plain language, no jargon left unexplained:

1. **What you can do now** — what works, from my side, and how to see it
   (a URL, a command, the email that'll arrive).
2. **Rulings** — every one from this phase, "you'd notice" first, each with
   what it costs if wrong.
3. **Worth understanding** — one or two things about how this works or why it
   was built this way, that would help me next time. Pick what's genuinely
   useful, not a tour.
4. **The real `make check` output** — the tail, not a summary.

Then stop: the next step is /checkpoint in a fresh session.
