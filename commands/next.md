Read ~/projects/build-system/PLAYBOOK.md's Phase summary table. Then inspect
the current directory (not build-system itself — this is for a project
directory under ~/projects/<app-name>/) to work out which phase this project
has reached, and tell me. Do not run the next command, do not create, edit,
or scaffold anything. This is a read-only status check.

Check for these files, in the order the playbook defines:

- No BRIEF.md yet → nothing started. Suggest /discovery if the idea is still
  half-formed, or /brief directly if "done" can already be described in one
  sentence.
- BRIEF.md exists, no DESIGN.md → Phase 1.5, run /design.
- DESIGN.md exists, no EXPLORE.md → Phase 1.75, run /explore. The external
  claims the design rests on haven't been checked against the real thing yet.
- EXPLORE.md exists, no SPEC.md → Phase 2, run /contract — but first check for
  anything still marked BLOCKED. If there is, say so and stop: those are
  checkable-but-unchecked, and /contract won't spec around them. Name the
  outstanding checks as the actual next action instead.
- SPEC.md exists and contains any [ASSUMED] tag → Phase 2.5 Audit isn't
  resolved yet. Say explicitly: run /audit in a **brand-new `claude`
  session** in this directory — never continue the current session for
  this step, that defeats the point of the fresh-eyes read.
- SPEC.md has no [ASSUMED] tags left, no PLAN.md → Phase 3. Say explicitly:
  restart with `claude --permission-mode plan`, then run /plan — not just
  /plan in this session.
- PLAN.md exists → Phase 4. Count ticked vs. total task checkboxes, report
  "N/M tasks done", and name the next unstarted task instead of a phase
  name. If there's no Makefile, src/, or scaffold yet, say scaffolding comes
  before the first /slice.
- Scaffold exists and every PLAN.md task is ticked, no docker-compose.yml →
  Phase 5, run /deploy.
- docker-compose.yml exists → Phase 6. No more commands — operate, backups,
  kill criteria.

Also check whether the furthest-reached artifact is actually committed
(`git status`, `git log -1 -- <file>`). If it isn't, say so and point at
this playbook's commit-checkpoint line for that phase before moving on.

Note: this can't detect two failed /slice attempts — that's conversational
state, not a file. If stuck, mention /stuck exists; don't try to trigger it.

Report the phase, the commit status, and the exact next command, then stop.
