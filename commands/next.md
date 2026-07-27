Inspect the current directory (not build-system itself — this is for a project
directory under ~/projects/<app-name>/) to work out how far this project has
got, and tell me. Do not run the next command, do not create, edit, or scaffold
anything. This is a read-only status check.

Check for these files, in order:

- No BRIEF.md yet → nothing started. Suggest /discovery if the idea is still
  half-formed, or /brief directly if "done" can already be described in one
  sentence.
- BRIEF.md exists, no EXPLORE.md → run /explore. What the candidate tools
  actually do hasn't been established, and design shouldn't start without it.
- EXPLORE.md exists, no DESIGN.md → run /design, unless anything is still
  marked BLOCKED. If it is, say so and stop: those are checkable-but-unchecked,
  and a design built on them rules options in or out for reasons nobody
  verified. Name the outstanding checks as the next action.
- DESIGN.md exists, no SPEC.md → run /contract — same BLOCKED check first.
- SPEC.md contains any [ASSUMED] tag → the audit isn't resolved. Say
  explicitly: run /audit in a **brand-new `claude` session** in this directory,
  never the current one — continuing defeats the fresh-eyes read.
- SPEC.md has no [ASSUMED] tags left, no PLAN.md → say explicitly: restart with
  `claude --permission-mode plan`, then run /plan — not just /plan here.
- PLAN.md exists → count ticked vs. total task checkboxes, report "N/M tasks
  done", and name the next unstarted task rather than a phase. If there's no
  Makefile, src/, or scaffold yet, say scaffolding comes before the first
  /slice.
- Scaffold exists, every PLAN.md task ticked, no docker-compose.yml → /deploy.
- docker-compose.yml exists → nothing left to run. Operate, backups, kill
  criteria.

Whenever a SPEC.md exists, count the **[AGREED]** tags and report the number.
They aren't blocking, but they're the requirements I never asked for and the
cheapest scope to be wrong about. Say so out loud if [AGREED] outnumbers
[STATED].

Check whether the furthest-reached artifact is actually committed (`git
status`, `git log -1 -- <file>`). Each artifact gets committed before the next
step starts; if it isn't, say so before moving on.

This can't detect two failed /slice attempts — that's conversational state, not
a file. If stuck, mention /stuck exists; don't try to trigger it.

Report where it's got to, the commit status, and the exact next command, then
stop.
