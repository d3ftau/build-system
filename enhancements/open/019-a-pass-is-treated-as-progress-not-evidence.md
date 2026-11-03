# Enhancement: "End to end early" is applied to a build that has to work first time, and a pass is treated as progress banked

**Status: OPEN** (recorded 2026-11-03). Greg: *"The stupid testing order is by
far the biggest one - you did incredibly intensive and long running tests only
to go and change things after they passed. We need to get to the heart of how
this happened rather than just writing rules around it."*

## Where this came from

backrest, Build 2 (devbox ported to the mini), reviewed after the port
finished on 2026-11-02. This is the root cause behind `018`'s modes 1 and 4.

## What happened

The expensive runs came before the changes they should have checked:

- **T12**, the full rehearsal: a fresh stick, install, 34 GB restore, data
  check and setup. About an hour, plus the build-up to it. It ended Phase 2.
  Then Phase 3 built the cutover and was re-planned, and `run-port` was
  rewritten. The final restore, services, takeover and port-check stages were
  all new. T15's test line said *"No VM rehearsal: T17 is the run."* So the
  code that changed most was never run end to end before the real port.
- **T10** measured RAM in the VM. Then the real mini had to be measured again
  anyway, and that measurement found the model was unusable (2 tok/s), which
  RAM never could.
- **Checkpoint 2:** Greg asked for less checking. The plan kept T12, already
  run, and cut the rehearsal still to come. That's exactly backwards: the cut
  test was the only one that would have run on the final code.
- **The cutover day:** the real run went first and failed. The rehearsal of
  the re-planned path ran second, after it, and filled devbox's disk.

The real run then failed at each place where the earlier tests had differed
from it:

| Real-run failure | Why the earlier test didn't meet it |
|---|---|
| `make-stick` env vars not exported | rehearsals set them from outside |
| xorriso onto a non-blank stick | rehearsals wrote an image file |
| `port.env` overwrite | the file was edited after the rehearsal |
| one-off job container | rehearsal inventory taken at a quiet moment |
| port check as greg, `Permission denied` | the rehearsal ran `--pre` as root and never reached this stage |
| Chrome caches, user `dbus` | services were held in the VM, and the reboot gate was never rehearsed |

Each difference was a sensible local ruling, made to keep the test safe or
runnable: an image instead of a stick, held services, a `--pre` mode, a
stand-in devbox, `REHEARSAL=1`. None of them was recorded as *"this pass
doesn't cover X"*.

## The heart of it

**`plan.md`'s "one real path, end to end, as early as possible" was applied
to a build it doesn't fit.** The rule assumes a build that evolves: each
version is used, failures show up in use, and the next task fixes them. An
early end-to-end run there is never wasted, because the path stays and gets
re-run as a matter of course.

This build had to work first time. The real run, the cutover, happens once.
What counts is that the rehearsal ran the *same* code and inputs the real run
would. An early end-to-end run in a build like that is only a probe for
unknowns. Treated as the proof, it went stale with the first later change.
The plan treated it as the proof. So did the re-plan: *"No VM rehearsal: T17
is the run"* is right for an evolving build, where the real run is just the
next iteration. Here it meant the final code first ran for real.

Nothing caught it going stale, because **a pass reads as progress banked.**
`build.md`'s "Finish the task" is to run the check, tick the box and log
`done`. A tick is permanent and belongs to the task, so later changes don't
un-tick it. And a passed test never says what it left out. That's how six
differences between the tests and the real run went unlisted, and why
"less testing" kept the early pass and cut the late rehearsal.

## Candidate fixes (not prescriptions)

Aim for fewer words in the commands, not more.

- **`plan.md`, Order:** the plan says which kind of build it is, from the
  brief: one that evolves (used, failing, fixed), or one whose real run
  happens once and has to work (a migration, a cutover, a run on hardware or
  data that can't be repeated). The current rule stays as it is for the
  first kind. For the second: the early end-to-end run is a cheap probe for
  unknowns. The last task before the real run is the full rehearsal, on frozen
  code with the real run's inputs. Any change after it re-runs the stages it
  touches. "Less testing" never cuts that last rehearsal.
- **`build.md`, "Finish the task":** a result is logged with what it ran on,
  and anything it set up differently from the real run, as "not covered".
  This is needed in both kinds of build, but it's what makes the second kind
  safe.

- **`checkpoint.md`, the backstop:** its opening line, *"Every task in it
  passed its own gate — that's already known and isn't the question"*, is
  this failure written down: it treats earlier passes as settled. They passed
  on the code as it was then. Step 5 ("Is the rest of the plan still
  true?") gains two questions. Which passes does the remaining plan rely on,
  and has anything they ran on changed since? And if the real run happens
  once, does the plan still end with the full rehearsal on frozen code? A
  plan, or a re-plan, that has dropped it gets a **re-plan** verdict. Here
  checkpoint 2 cut "one rehearsal in T15", and the Phase 3 re-plan wrote "T17
  is the run". Either would have been caught.

If these land, `018`'s *"a rehearsal counts only for the commit and inputs it
ran with"* and its *"real-run inputs differ from rehearsal inputs in ways
nobody listed"* are covered, and can be dropped from 018's open list.

## Evidence

- `backrest/builds/build-2/PLAN.md`: T12 ends Phase 2. T15 has *"No VM
  rehearsal: T17 is the run."* The checkpoint 2 decision line has "one
  rehearsal in T15".
- `backrest/builds/build-2/BUILD-LOG.md`: T12 Observed; the T17 Findings
  (make-stick ×2, port-env, images, rehearse broken, disk full); the
  2026-11-02 cutover entries (permission, Chrome caches, dbus).
- platform commits `74b9e9b`, `746ab14`, `8ed6997`, `d79f6a2`, `449fe73`,
  `5360137`, `6b39c2b`, `ad77280`: each a fix after a test "passed".

## Fix written (2026-11-03)

- `plan.md`, Order: "Unless the real run happens once". The plan says
  which kind of build it is. Early runs are probes, and the full rehearsal
  on frozen code comes last and is never cut.
- `build.md`: the `done` line carries `not covered: …`. A pass goes stale
  when a later change touches what it ran on, and the report lists stale
  passes.
- `checkpoint.md`: the opening no longer treats passes as settled. Step 5
  asks which passes are stale, and whether the final rehearsal is still
  planned (a re-plan without it gets **re-plan**).

Still open: seeing it work on a real build whose run happens once.
