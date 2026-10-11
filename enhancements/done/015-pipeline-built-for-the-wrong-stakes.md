# Enhancement: The pipeline is built for shipping to strangers, and doesn't know shared infrastructure exists

**Status: DONE** (2026-10-11) — commands rewritten (build-system `6838696`), build-state and stop hook updated, cclauncher follows (`7a9efc2`), platform built (`~/projects/platform`, `dd2b7fb`), playbook rewritten, superpowers uninstalled, autopantry's local Supabase stopped. Remaining migrations of existing apps onto the platform are tracked in `~/projects/platform/README.md` under To do.

## Where this came from

End-to-end review of the build system, 2026-10-11. It began with a question
about superpowers' context cost and became a review of every command, the
playbook, the open enhancements (011–014), all 14 superpowers skills, and every
project under `~/projects` plus what is actually running on devbox.

The user's goal, restated in that session:

> *"I am not building production software for customers (build-system
> originally had the idea that I would ship apps to more than just myself or
> immediate family, I've moved on from that). I want a system to gets me to
> solid personal task solving apps quickly but also in a manner that means
> they don't break after a week and don't create a bunch of different
> solutions to the same problem - they should be running on as much shared
> backend infrastructure as possible"*

Also from the user: `/deploy` and `/complete` have never been used, and `/audit`
in its current form is of low worth (already recorded in `011`). On `/slice`:

> *"it was put in to prevent token waste on bad build that a couple of
> questions up front could've prevented but is only really useful for truly
> complex builds. I'd rather being those decisions forward into plan and just
> get the thing built as 90% of the time I'm just typing slice then waiting.
> Although it is nice being involved in the process - I've learnt a lot."*

> *"the best builds were the ones I just got the fuck out of the way of"*

## Evidence

### Weight

- 13 commands and up to 9 documents per build. `/slice` was typed 53 times
  across all transcripts, more than every other command combined.
- `discovery.md` still asks whether an improvement "is actually sellable
  against that product's own user base". The playbook's escape hatch is
  justified by "anything that ever goes external".
- Spec sizes: see the table in `011`. fashion-bot (one email a day) got 23
  FRs; autopantry build 2 has 3097 SPEC lines.
- `/deploy` and `/complete` never ran on any project. A step that is always
  skipped is a wrong step, not a discipline problem.

### Shared infrastructure (inventory of 11 projects, 2026-10-11)

| Need | What the projects actually do |
|---|---|
| Notifications | fashion-bot and file-cleanup send mail through the host's msmtp; house-bot uses Telegram via Hermes on a VPS. The playbook's default says Telegram. |
| Storage | SQLite per app (fashion-bot, usecasebot, EchoMuse, house-bot); autopantry on hosted Supabase, with an 11-container local Supabase stack running for its tests, published on `0.0.0.0`. |
| Scheduling | Five mechanisms: APScheduler in a container (fashion-bot), systemd user timers (usecasebot, free-time), a system unit (autopantry-price-sweep), cron (file-cleanup), an always-on worker container. |
| Browser | fashion-bot bakes its own headed Chrome + Xvfb into its image. |
| Local models | One shared Ollama — but `~/projects/ollama` is not a git repo. |
| Monitoring | The playbook requires Uptime Kuma and Dockge. Neither is installed. |

`~/projects/platform` holds a July design for a shared platform (model gateway,
Redis queue, notifier service, cashback browser). None of it was built.

### Superpowers

- Its `SessionStart` hook ran in 141 of 162 sessions; a superpowers skill was
  invoked in 10.
- `skillOverrides` in `~/.claude/settings.json` sets `superpowers:brainstorming`
  to `off`, yet brainstorming was invoked on 2026-10-03 and was still listed
  as available on 2026-10-11. The overrides don't take effect for this
  plugin's skills.
- Its brainstorming skill pushes "when in doubt, take the heavier path" and
  competes with `/discovery` → `/brief`.

## The general failure modes

1. **Rigour is set for the wrong stakes.** The pipeline was written when apps
   might ship to other people and still runs at that weight. `011` is the
   symptom inside `/contract`, `/plan` and `/audit`; this is the cause.
2. **No stage knows what already runs.** `/explore` searches the world for
   tools but never asks what devbox already has, and no command reads the
   playbook's default stack (`002` again). Each build chooses its plumbing
   from scratch, so five apps have five schedulers.
3. **"Doesn't break" lives in steps that don't run.** The reboot test and the
   monitor were in `/deploy`; nothing replaced them. No running app has a
   route for telling the user it failed except the ones that happened to
   build one (fashion-bot's "failed" email).
4. **The per-task stop costs more than it buys.** `007`'s stop exists so
   consequential decisions are made before code. Those decisions can all be
   asked in one sitting at `/plan`; the per-task stop mostly carries "nothing
   open" (`013`).

## Fixes (decided 2026-10-11)

Commands, 13 → 7 steps plus `/stuck`:

- **`/discovery`**: drop the "sellable" line; ask what already runs that does
  part of this.
- **`/roadmap` merges into `/brief`**: the brief ends with a Later list, and
  writes or updates ROADMAP.md when it isn't empty. Closes `012`.
- **`/explore`**: the existing stack and the platform first, without stopping
  there. A clearly better tool that needs new stack is weighed, with the cost
  of the new piece stated.
- **`/design` + `/contract` → `/spec`**: options considered become a
  paragraph; size proportionate to the brief; failure modes become "what I
  see when it breaks"; the five provenance tags become one mark, `[ASSUMED]`,
  on anything the user didn't say; stack outside the platform needs a reason.
- **`/audit` is replaced** by the end of `/spec`: the five situations most
  likely to bite the user, walked through the spec (superpowers'
  writing-plans "Review Focus", capped at five). `001`/`003` survive as the
  `[ASSUMED]` mark and the ruling on it.
- **`/plan`**: scaffold folds into the first real task (closes `014`); every
  decision the user would see is asked up front; "Leaves open" only for
  decisions that change what the user gets or sees (`011`); tasks carrying an
  open decision or an invalidating bet are marked `⏸ STOP`; the first
  end-to-end task includes deployed, survives a reboot, and a failed run
  reaches the user.
- **`/slice` → `/build`**: runs a whole phase continuously, stopping only at
  `⏸ STOP` tasks or for something destructive, security-sensitive or outside
  the project (superpowers' executing-plans "rulings, not stalls"). Each call
  it makes is logged as `Ruling: what — why — cost if wrong`. The phase ends
  with a plain-language report written for learning. Closes `013`.
- **`/checkpoint`** gains a fresh-eyes code review graded by effect on the
  person using it.
- **`/stuck`** gains root cause first, compare against a working example,
  and question the design after three failed fixes (superpowers'
  systematic-debugging).
- **`/deploy` and `/complete` are deleted**: deployment is a plan task; the
  README is the build's last task.
- `hooks/verify-before-stop.sh`, `bin/build-state` and cclauncher's stage list
  follow the new names.

Platform:

- `~/projects/platform` becomes a small real repo: `PLATFORM.md` plus a
  compose file. Shared: notifications (msmtp mail), Ollama, one headed-Chrome
  container, one scheduling convention, a deploy template, one failure route.
  The July design is archived.
- **Share services, not databases.** Each app keeps its own SQLite file; one
  shared database means one bad migration takes every app down.
- Failure visibility through cclauncher, not Uptime Kuma.

Cleanup: playbook rewritten to match; superpowers uninstalled and the dead
`skillOverrides` removed; autopantry's local Supabase stopped (`supabase stop`,
data kept).

Not taken from superpowers: test-first "delete your code", worktrees and
branch finishing, a subagent per task, brainstorming's heavier-path ratchet.

## Still open

Nothing in build-system. Moving existing apps onto the platform (usecasebot's
own failure unit, fashion-bot's own Chrome layer) is tracked in
`~/projects/platform/README.md` under To do.

## Corrections found while landing it

- PLATFORM.md's first draft said containers reach Ollama via
  `host.docker.internal`. Tested: they can't — Ollama isn't bound to the Docker
  bridge. Fixed with a shared `platform` Docker network (`http://ollama:11434`).
- cclauncher already flagged failed timer runs and down containers, so the
  "failure visibility through cclauncher" item needed a convention (schedule
  with systemd timers), not new code.
