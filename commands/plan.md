Read CLAUDE.md, SPEC.md, EXPLORE.md (if it exists) and
`~/projects/platform/PLATFORM.md` in full. Inspect the current directory.

Do not create or modify any source files. If you are not already in
plan/read-only mode, treat this instruction as binding: no edits, plan only.

**Proportion.** A personal app. The plan is as long as the build needs and no
longer — a small app is one or two phases. Size each task as the smallest
unit with its own test that's worth checking separately: fold setup, config
and docs into the task whose deliverable needs them, and only split where one
half could be wrong while the other is right.

## 1. Ask me everything first

/build runs without stopping, so the questions it would have stopped for get
asked now, in one go.

List every decision this build will force that **changes what I get or see**
and that neither SPEC.md nor an obvious default settles: a policy, what
happens in a case nobody named, what a message says, what gets kept or thrown
away. Number them, and give each your recommended answer, so I can reply
"defaults" or change two. Then wait.

Leave off anything technical with a sensible default — library choice, file
layout, config names, lint rules. /build decides those and reports them; you
don't ask about them and don't list them.

**Then weigh each piece of automation: effort against time saved.**
Automation is the goal, and one that costs a line or two of code is simply
done. The test is the return. On one side: the time to build it, test it and
keep it working, plus any new problem it creates (a secret to carry, a
permission, a cross-machine link, a mode, a rehearsal rig), each of which
needs effort of its own. On the other: the time it saves me, which is how
long the step takes by hand times how often it happens over the thing's
whole life. Spending more to automate a step than a lifetime of doing it by
hand would cost is a poor return. For any piece whose cost is more than a
task, give me one line: the step it removes, how often, and what it adds. A
nice-to-have in DISCOVERY.md whose cost outweighs its saving is a question
for me, with that line, not a task.

## 2. Write PLAN.md

First line: `# PLAN — <build name from BRIEF.md>`.

**Order.**
- **An invalidating BET goes first**, proved by the smallest possible slice of
  real code with everything around it faked. Never sequence a build so an
  invalidating answer arrives late.
- **Then one real path, end to end, as early as possible.** The single
  simplest case the app exists to handle, real at every stage, from real input
  to real output, even if it handles that case badly. Narrow means fewer cases,
  not pretend data: a pipeline running on stubbed responses proves only the
  wiring. Fake a stage only when the real thing is genuinely unavailable yet,
  and say which task makes it real.
- **The scaffold is part of that first task**, not a task of its own: Makefile
  with `dev`/`test`/`check`, `.env.example`, `.gitignore`, the platform's
  deploy template, and a first real test. No placeholder test that's meant to
  fail.
- **The first phase ends deployed for real**: running on the platform, back
  by itself after a reboot, and a failed run reaches me through the platform's
  failure route. That's part of the build, not a step after it.
- Then widen, case by case. Never build layer by layer (all models, then all
  services, then all routes).
- **One unknown per task.** A new API, library or pattern each get their own
  task.
- **The last task** writes README.md (what it is, how to run it, where data
  lives, what to back up) and brings CLAUDE.md and SPEC.md in line with what
  was actually built.

**Phases.** Group tasks into phases, each ending with its own checkbox line
`- [ ] /checkpoint — <phase name>`, roughly every 8–12 tasks and always after
anything later tasks depend on for quality.

**Each task** is a checkbox line, `- [ ] **T3 — <what it delivers>.**`, then:
- the files it creates or changes
- the FR(s) it satisfies
- **Fails if:** only when its output has a measurable quality (a match rate,
  an accuracy) — the number, measured on real data, below which it isn't good
  enough to build on
- **`⏸ STOP`** on the checkbox line itself, only when the task carries a
  decision that step 1 couldn't settle because it needs something the build
  hasn't produced yet (seeing real output first, say), or proves an
  invalidating BET. Say what I'll be asked. Most plans have none.

## 3. Then, after the tasks

- **Human surface check** — a short table. Every FR: which task builds the
  part a person touches, or "server-only" and why that's enough. Every table
  holding a person's data: which task gives a way in that isn't SQL. Any empty
  cell is a missing task — add it.
- **New dependencies**, each with why, and whether the platform already
  covers it.
- **Anything in the spec that's ambiguous or that you'd do differently**,
  stated plainly.
