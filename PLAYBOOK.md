# Build Playbook — idea to working app

A workflow for taking an idea from a half-formed thought to a solid personal
app running on `devbox` — quickly, on shared infrastructure, and built so it
doesn't quietly break a week later. Nine slash commands in `./commands/` are
the executable steps.

**The commands are the source of truth. This document explains them.** Agents
never read it — they read the command they were invoked as. Anything here
describing what *the agent* does is only true if a command file or hook makes
it so; if this file and a command disagree, the command wins and this file is
stale. What this file owns on its own is guidance for *me*: when to use the
phone, which model, when to kill a project.

**Scope:** personal apps for me and occasionally my immediate family. Nothing
is sold, nothing is external-facing, and a missed or wrong day costs little.
Every command scales its rigour to that. (The system was first written for
apps that might ship to other people; enhancement `015` is where that
changed.)

---

## Opening principle: Tailscale is the auth layer

I never write authentication. Anything another device needs to reach binds to
the tailnet (plus localhost for same-machine callers), never the LAN and never
the internet. Anyone on the tailnet is already authenticated by Tailscale.
Adding my partner is adding a device to the tailnet, not building a login
system. If something genuinely needs public access or real user accounts, it
shouldn't be self-hosted here.

## Opening principle: build on the platform

`~/projects/platform/PLATFORM.md` lists what every app shares: one way to
notify me, one way failures reach me, one way to schedule, one browser image,
one Ollama, deploy templates, a default stack. `/explore` checks it first,
`/spec` builds on it, and anything outside it needs a stated reason. That's
what stops five apps growing five schedulers.

It's a default, not a wall — a clearly better tool that needs new stack is
weighed, with the cost of keeping one more thing alive stated. And it shares
**services, not databases**: each app keeps its own data, so one bad migration
can't take every app down.

---

## Advisory vs deterministic

`CLAUDE.md` and commands are advisory: the agent usually follows them, and
"usually" does real work in that sentence once context fills up. Hooks are
deterministic: scripts that fire on a lifecycle event and can't be talked out
of running. Conventions go in `CLAUDE.md`; anything that must actually hold
goes in a hook.

Four hooks live in `hooks/`, symlinked to `~/.claude/hooks` and wired into
`~/.claude/settings.json` for every project:

- `git-guard.sh` (`PreToolUse`, `Bash`) — blocks commits that bypass hooks or
  signing, and commits of anything that looks like a secret.
- `no-skipped-tests.sh` (`PostToolUse`, `Edit|Write`) — blocks an edit that
  adds a skip/xfail/disable marker to a test, and blocks the agent editing
  `.claude/known-failing-checks`.
- `llm-call-guard.sh` (`PostToolUse`, `Edit|Write`) — blocks a new model API
  call in source unless a comment names the fuzzy judgment it requires.
- `verify-before-stop.sh` (`Stop`) — if the project has a `make check` target,
  `/build` or `/oneshot` is the most recent pipeline command, and the turn changed files, it
  runs `make check` before the turn may end and blocks with the real failure
  output if it fails. Failures matching a line in the project's
  `.claude/known-failing-checks` are let through; that file is mine, never the
  agent's.

**Never accept "it works" as evidence.** Demand the actual command output. The
failure mode isn't the agent lying — it's the agent believing itself.

**Guard against gate-gaming.** Tests may never be skipped, xfailed or deleted
to make a gate pass. Reducing coverage to go green is a failure, not a fix.

---

## Setup — once per machine

- `~/.claude/commands` → `build-system/commands`, `~/.claude/hooks` →
  `build-system/hooks` (symlinks), hooks wired in `~/.claude/settings.json`.
- The platform set up per `~/projects/platform/README.md`.
- `~/.claude/CLAUDE.md` carries machine facts and standing preferences into
  every session; a project's `CLAUDE.md` adds only its own rules.
- No plugin is required. (Superpowers was installed until 2026-10-11; its
  useful ideas now live in `/plan`, `/build`, `/checkpoint` and `/stuck`.)

Standing rules: everything in git from the first commit; config from
environment variables, never hardcoded paths or hostnames; secrets in `.env`,
never committed.

---

## The steps

| Step | Command | Writes |
|---|---|---|
| Think it through (optional) | `/discovery` | `DISCOVERY.md` |
| Decide what this build is | `/brief` | `BRIEF.md`, `ROADMAP.md` if anything is deferred |
| Check reality | `/explore` | `EXPLORE.md` |
| Write the contract | `/spec` | `SPEC.md`, project `CLAUDE.md` |
| Plan it | `/plan` (in plan mode) | `PLAN.md` |
| Build a phase | `/build` | code, `BUILD-LOG.md`, ticks |
| Judge the phase | `/checkpoint` (fresh session) | a verdict |
| When something won't give | `/stuck` | — |
| **Or, for something small: all of it in one go** | `/oneshot` | `README.md` (To do + Design), `BUILD-LOG.md` |

Commit each document once it's settled.

### `/oneshot` — the whole thing, one session, one approval

For something small enough that the steps above would be ceremony —
cclauncher's launcher was built this way, from one well-specified request.
The same rules apply (platform first, proportion, no model for enumerable
rules, evidence that tests the claim, deployed with a failure route, rulings
logged); only the separate documents and hand-offs go.

It asks at most three questions, then checks the request really is small and
recommends the full pipeline if it isn't: several builds, a bet on model
judgment, an outside product nobody has checked, or a to-do list past about
ten items. Then a design in chat, short enough for a phone — constraints
marked stated or inferred, the shape, the decisions I'd notice with defaults,
and the to-do list. One approval, then it writes README.md (`## To do` +
`## Design`) and builds straight through, ticking the list.

It writes no BRIEF, SPEC or PLAN, so the dashboard tracks it as a quick
project: progress from the README's To do list, shipped when the list is
done, something runs it, and git is clean and pushed. Running `/oneshot` in an
existing quick project adds to its list.

### `/discovery` — optional

A thinking partner, not an architect. It pushes on the idea, suggests
reframes, and asks what problem is underneath. Early on it asks whether this
already exists — searched, as two separate searches (commercial and
open source) — and what I already run that does part of it. It works out
whether this is one build or several. Skip it when I can already describe
"done" in one sentence.

It records who originated each requirement. A requirement the agent argued me
into stays visibly the agent's, because nothing downstream can recover the
difference once it's lost.

### `/brief`

Up to four targeted questions, one at a time, plus two that are always asked:
**what's the smallest version I'd actually use**, and **who looks at this and
what should using it feel like.** Scope only grows on its way to the brief,
and if nobody asks about the experience, the first screen built becomes the
design. The stakes aren't asked — they're fixed (personal).

The brief ends with a **Later** list (wanted, not now) and a **Never** list
(rejected). Cutting to the smallest version is what makes a project several
builds, so when Later isn't empty, `/brief` writes or updates `ROADMAP.md`
itself: `### Build N — <name>` per build, names being what I get, which the
dashboard shows. There's no separate roadmap step, because a separate step
was the one that never ran (`012`).

If the brief can't fit in a paragraph, the scope is wrong.

### `/explore`

The first step that touches the real world, before anything is designed.
It starts with the platform: what's already covered, and which existing
project already does something like this. Then it looks further — two
separate searches, commercial and open source — and checks what each
candidate actually does now, never from recall. A candidate that needs new
stack stays in the running with its keep-alive cost stated.

Findings are **CONFIRMED**, **WRONG**, **BLOCKED** (checkable, unchecked) or
**BET** (unknowable without building). The line between the last two is the
one that matters: needing an account or waiting a week for an export is
BLOCKED, not a bet. `/spec` refuses to write anything while something is
BLOCKED.

The failure this exists to prevent: asserting that a whole product category
can't do something standard, and inventing a subsystem to route around a
limitation that never existed (see the worked example below).

### `/spec`

Picks the shape and writes the contract. Usually there's one obvious shape on
the platform and that's a line; if there's a real choice, I pick. If anyone
sees anything, it asks about look and feel rather than inventing one.

Then `SPEC.md` — Purpose, Shape, Functional Requirements, Data Model,
Interfaces, Human Surfaces, When it breaks, Verification Gates — and the
project's `CLAUDE.md`. Proportion is the rule: every line has to change what
gets built, no invented thresholds or failure catalogues, and a one-build app
past about a dozen FRs has to say why (`011`). Requirements are
`- [ ] **FR-3 — Name.** WHEN … THE SYSTEM SHALL …`; the dashboard shows the
names. Any FR where a person does something names the screen it happens on —
a row in a database is observable and nobody can use it.

**One mark: `[ASSUMED]`** on anything I didn't say. A document is never a
source — "DESIGN.md says so" is the agent's own writing. Obvious defaults
aren't marked. At the end, every `[ASSUMED]` item is listed for me to keep
(the tag comes off) or cut. That's what's left of the old five-tag provenance
system and `/audit`: the one useful thing they did was stop a phantom
requirement becoming a schema.

It ends with **what would bite me**: the five situations most likely to go
wrong in real use, each walked through the spec to see what actually happens
to me. Five, because the cap keeps it about my life with the app rather than
the spec's wording. This is the part of the old `/audit` that earned its
place — fashion-bot's one useful finding (dedupe ignoring size) came from
exactly this question.

### `/plan`

Run with `claude --permission-mode plan` — plan mode can't edit files.

It asks first: **every decision the build will force that changes what I get
or see**, in one numbered list with a recommended answer each, so I can reply
"defaults". This is what used to happen one task at a time inside `/slice`;
asking it all up front is what lets `/build` run without stopping.
Technical choices with sensible defaults aren't asked — `/build` makes them
and logs them.

Then `PLAN.md`. **The order is the point.** An invalidating bet is proved
first with the smallest real slice of code. Then one real path end to end as
early as possible — the simplest case, real at every stage, narrow not fake.
The scaffold is part of that first task, not its own (`014`). The first phase
ends **deployed for real**: running on the platform, back by itself after a
reboot, and a failed run reaches me. The last task writes the README and
brings the docs in line with what was built. That's where `/deploy` and
`/complete` went: steps that ran after "done" never ran.

Tasks are checkboxes grouped into phases, each ending in
`- [ ] /checkpoint — <phase>`. A task carries **Fails if** only when its
output has a measurable quality, and **`⏸ STOP`** only when it holds a
decision that can't be settled until the build produces something. Most plans
have no stops.

I review the plan on my phone: how far down is the first end-to-end run, is
anything I'd care about missing from the human-surface table, and does the
ambiguity section show the spec was unclear somewhere. Fixing a plan costs
seconds; fixing code costs hours.

### `/build`

Builds a whole phase without stopping. The questions were asked at `/plan`,
and a stop that carries no decision just costs me waiting (`013`) — "the best
builds were the ones I got out of the way of".

It stops only at a `⏸ STOP` task, for something destructive,
security-sensitive or outside the project, after two failed attempts at the
same problem, or when the plan is too wrong to guess past. Everything else it
decides and logs in `BUILD-LOG.md` as
`Ruling: what — why — what it costs if wrong`. A ruling that changes what I
see takes the easiest-to-undo option and is flagged "you'd notice". The log is
also its memory across context compaction.

Per task: watch a new test fail first; never a model call for enumerable
rules; evidence has to test the claim itself (a bug is real only if reality
can produce it, an invented test input is a finding, test the reverse of
every state change); tick, commit, log.

The phase ends with a **report written for learning**: what I can do now and
how to see it, every ruling, one or two things worth understanding about how
it works, and the real `make check` output. Being involved taught me a lot;
this keeps that without making me the bottleneck.

### `/checkpoint` — fresh session

`/build` checks each task against its own gate; nothing else asks **is what
this phase built good enough to build the next one on?** — and a component
passing its gate at 33% correct can hold up everything above it for weeks
(`009`). `/checkpoint` runs the phase's output on real data and measures it,
reads the code fresh and grades each problem by what it does to me, reviews
the build's rulings, looks for patterns no task decided, and checks the rest
of the plan still holds. Fresh session, because the one that built it
inherited the assumptions it's meant to question. It recommends proceed, fix
first, or re-plan; I decide.

### `/stuck`

Root cause before any fix: read the whole error, find something similar that
works and list every difference, and find which hand-off breaks instead of
guessing. Then what was expected, what happened, two approaches, one
recommended. A third failed fix means the design is wrong, not the fix — go
back to the spec or plan rather than forcing the code to comply.

---

## Where it lives

devbox is the default. Route elsewhere when it has to be up while devbox is
off (cheap VPS), needs a public URL or real accounts (not self-hosted), or
*is* auth, payments or compliance (don't build it). Every project stays
liftable: config from `.env`, nothing devbox-specific in code or compose, state
in `./data`.

**Kill criteria:** three months unused means decommission it. An unused
container is attack surface and upkeep for nothing.

---

## Skipped steps and quick projects

`bin/build-state` (read by the cclauncher dashboard) doesn't insist on every
step:

- **A skipped step doesn't gate.** A missing doc only counts as the next step
  when no later doc exists. Gaps are listed under `skipped` in `--json`.
  `DESIGN.md` from the old pipeline is listed in `docs` but isn't a step.
- **`[ASSUMED]` gates the plan.** Unruled items stop a project at the spec
  stage until there's a PLAN.md; after that they're a warning.
- **Built means every FR in SPEC.md is ticked.** PLAN.md's ticks decide it
  only when the spec has no FRs. Built is done; a missing README is a warning.
- **Deployed** is any of: a compose file, a systemd unit or crontab line that
  runs something from the project's folder, or a workflow publishing GitHub
  Pages.
- **Quick projects** have no pipeline docs, just code and maybe a README —
  whatever `/oneshot` built, or anything started by hand. Their to-do list is a
  checklist under `## To do` in README.md. One is **done** when
  every item is ticked (or there's no list), it's deployed, and git is clean
  and pushed.

## Project layout

```
~/projects/<app>/
  README.md        what it is, how to run it, where data lives, what to back up
  CLAUDE.md        project rules and hard constraints
  BRIEF.md  EXPLORE.md  SPEC.md  PLAN.md  BUILD-LOG.md   (ROADMAP.md, DISCOVERY.md)
  compose.yml      from the platform's templates
  Dockerfile
  ops/systemd/     timer + service, for a scheduled job
  .env.example     every config key, no secrets
  Makefile         make dev / make test / make check
  src/  tests/  data/
```

`make check` is the one command that proves the app is healthy — what the
agent runs on itself and what the stop hook enforces.

---

## Phone vs desk

**Phone** for decisions: ideation, brief and spec review, answering `/plan`'s
questions, reading phase reports, kicking off `/build` on a stack the agent
knows well. **Desk** for anything that needs eyes: large diffs, a stack being
used for the first time, anything visual, confusing debugging. Don't eyeball a
real diff on a five-inch screen — it produces false confidence, not review.

## Model selection

- **Opus** for discovery, spec and plan, `/checkpoint`, and hard debugging —
  where judgment matters more than speed.
- **Sonnet** for `/build` on a settled plan — the plan carries the design.
- **Opus for `/build`** when a phase has stalled twice and `/stuck` hasn't
  resolved it.
- **Local Ollama** for bulk text in apps — classification, extraction,
  summarising — never for writing code.

## Emergency commands

| Situation | Command |
|---|---|
| Agent going down a bad path | `/clear` |
| Agent mid-action, interrupt now | `Ctrl+C` |
| Last commit was wrong | `git reset --hard HEAD~1` |
| What did the last commit change | `git diff HEAD~1` |
| Container misbehaving | `docker compose logs --tail 50` |
| Container needs a kick | `docker compose restart` |
| Rebuild after a Dockerfile change | `docker compose up -d --build` |
| Did a scheduled job fail | `systemctl --user list-timers`, then `journalctl --user -u <unit> -n 50` |
| What's listening on a port | `ss -tlnp` |
| Is Ollama using the GPU | `docker exec ollama ollama ps` |
| Switch models mid-session | `/model` |

---

## What helps and what breaks one-shotting

**Helps:** questions asked before code, one unknown per task, an end-to-end
path early, building on what already runs, verification gates that are
commands, stopping at two failed attempts, and checking what external services
actually do before designing around what they supposedly can't.

**Breaks it:** a spec at the wrong weight, horizontal layers with nothing
runnable until the end, stacking several unknowns in one task, treating a plan
as sacred, accepting "should work now" instead of output, and recording a
finding that invalidates the plan as a note instead of reordering the plan.

---

## Worked example: the phantom household

Bin collection reminder: a Telegram message the night before bin day. A
review of the spec found "must handle multiple households" — not in the
brief. It had grown out of one passing line, "my partner should get it too",
into a household data model, a settings screen and per-household scheduling,
for a feature that needed one more chat ID in an environment variable. Struck
in two minutes while it was still a sentence. This is what the `[ASSUMED]`
mark exists for: anything I didn't say is visible, and I rule on it before the
plan.

## Worked example: the nag that didn't need building

`DESIGN.md` for the task-extractor stated as fact: "no task app on any tier
does repeat-until-done nagging." It justified rejecting an architecture and
committed the build to its own scheduler, notification channel and state. It
was false — recurring reminders are standard; ClickUp does them free. The
claim came from model recall, survived three steps, and was overturned by a
passing remark. Caught, it removed a subsystem. That's why `/explore` comes
before any design and checks instead of recalling.

---

This playbook is a guide, not authority. If implementation friction says a
step is wrong, the step is wrong. Fix the command, then update this file to
explain it.
