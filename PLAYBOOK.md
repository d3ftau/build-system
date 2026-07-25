# Build Playbook — idea to working app

A spec-driven workflow for taking an idea from a half-formed thought to a
running, deployed app on `devbox`. Ten slash commands in `./commands/` are
the executable steps behind each phase below — this document explains what
they're for and how to sequence them; the commands themselves are the source
of truth for exact wording.

**Scope:** personal tools and proofs-of-concept, for me and occasionally my
partner. Nothing external-facing.

---

## Opening principle: Tailscale is the auth layer

I never write authentication. Every app binds to the tailnet, not the LAN
and not the internet. Anyone on the tailnet is already authenticated by
Tailscale; anyone not on it cannot reach the service at all. Adding my
partner is adding a device to the tailnet, not building a login system.

If a project genuinely needs public access or real user accounts, that's
the signal it shouldn't be self-hosted here. Don't bolt auth on. Move it
somewhere that's built for it.

---

## Advisory vs deterministic

`CLAUDE.md` and skills are advisory. The agent reads them and usually
follows them — but "usually" is doing real work in that sentence,
especially once context fills up. Hooks are deterministic: scripts that
fire on a lifecycle event and cannot be talked out of running.

Use `CLAUDE.md` for conventions and preferences. Use hooks for anything
that must actually hold — typechecks, tests, lint, secret scanning.

**Never accept "it works" as evidence.** Demand the actual command output,
not a summary of it. The failure mode isn't the agent lying — it's the
agent believing itself.

**Guard against gate-gaming.** Tests may never be skipped, xfailed, or
deleted to make a gate pass. If a test fails, fix the code — or say the
test is wrong and why. Reducing coverage to go green is a failure, not a
fix.

---

## Phase 0 — one-time setup

Done once per machine, not once per project.

- **Install a spec-driven plugin.** Either Superpowers
  (`/plugin install superpowers@claude-plugins-official`) or GitHub Spec Kit
  as the more structured alternative, if neither is already installed. This
  playbook's commands assume one of them is available.
- **`~/.claude/CLAUDE.md` is inherited global context.** It carries machine
  facts and standing preferences into every project's session automatically —
  project `CLAUDE.md` (Phase 2) adds project-specific rules on top of it, it
  never needs to restate it.
- **Standing rules, no exceptions:**
  - Everything lives in git from the first commit.
  - Config via environment variables only — never hardcoded paths or
    hostnames.
  - No hardcoded paths — a devbox-specific path baked into code breaks the
    escape hatch (Phase 5) later, when it's expensive to fix.
  - Secrets live in `.env`, never committed.
  - Every project gets an Uptime Kuma monitor before it counts as done (see
    the Phase 5 checklist).

---

## Phase 0.5 — Discovery (optional)

**Command:** `/discovery <whatever you've got, however half-formed>`

Unstructured and conversational — a thinking partner, not an architect.
Divergent on purpose: it pushes on the idea, suggests reframes, and asks
what problem is actually underneath it, rather than narrowing toward a
spec. Best done walking. Skip it when I can already describe "done" in one
sentence and I'm confident it's the right thing.

One thing discovery should always surface: is this one build, or a product
with several pieces? If it's a product, run `/roadmap` next.

**Command:** `/roadmap`

Reads the discovery conversation and writes `ROADMAP.md`: the spine (the
one capability everything else hangs off), the builds in order, and why
that order. The test applied to every build in the roadmap: **would I use
this if nothing after it ever got built?** If no, that build is scoped
wrong — not too small, too dependent on something that doesn't exist yet.
Re-scope it or merge it forward until the answer is yes. If the idea
genuinely doesn't decompose, the roadmap should say so honestly rather than
manufacture a fake incremental plan.

---

## Phase 1 — Brief

**Command:** `/brief <one sentence description>`

First checks for `DISCOVERY.md` and `ROADMAP.md` in the current directory.
If they exist, this brief is for a specific build that came out of that
thinking, so it doesn't re-ask what's already settled — and if `ROADMAP.md`
exists, it confirms which build in it this brief covers before going
further.

Then up to five targeted questions, one at a time, waiting for an answer
before asking the next — covering only what isn't already answered: what
"done" looks like concretely, the smallest version I'd actually use, data
and storage, edge cases and failure modes, and who else touches it. Fewer
than five if discovery already covered some. No solutions, no code. Once it
has what it needs, it synthesises everything into a plain markdown brief
under 200 words, with an explicit "Out of scope" list, saved as `BRIEF.md`.

If the brief can't fit in a paragraph, the scope is wrong. Cut it.

**Commit:** `BRIEF.md` once synthesised.

---

## Phase 1.5 — Design

**Command:** `/design`

Reads `BRIEF.md` and identifies the genuinely distinct ways this could be
built — not variations on one idea, different shapes with different
centres of gravity. However many actually exist: two, five, or honestly
just one, with an explanation of why the obvious alternatives don't hold
up. No padding a list to make it look fuller.

For each option: what it fundamentally is, what it makes easy or hard or
forecloses, what it'd be good at in a year that the others wouldn't, and
roughly how much work v1 is. It recommends one and says what would change
its mind.

I pick one option or a hybrid. `DESIGN.md` records all the options
considered, what was picked, and why — including what was rejected and
why. That record is what stops me re-litigating the same decision in three
months when I'm tempted to rebuild.

**Commit:** `DESIGN.md` once the choice is recorded.

---

## Phase 2 — Contract

**Command:** `/contract`

Reads `BRIEF.md`, `DESIGN.md` (if it exists), and `~/.claude/CLAUDE.md` for
machine and stack defaults, then writes two files and nothing else — no
source code, no directories, no installs.

**`CLAUDE.md`** — project-specific rules only: tech stack for this project
with exact versions where they matter, hard rules the agent must never
break, where data lives, what must never be installed or used. It also
carries the gate-gaming guard verbatim (see above).

**`SPEC.md`** — Purpose, Functional Requirements, Out of Scope, Data
Model, Interfaces, External Dependencies, Failure Modes, Verification
Gates. Every FR is a numbered, independently verifiable checkbox phrased as
"WHEN `<trigger>` THE SYSTEM SHALL `<observable behaviour>`" — "search
should be fast" is untestable, "WHEN the user types in the search box THE
SYSTEM SHALL filter the visible list within 200ms" is testable. Every FR
and every constraint is tagged:

- `[STATED]` — I said this, verbatim or close to it
- `[DERIVED]` — follows necessarily from something stated (chain shown)
- `[ASSUMED]` — the agent filled a gap

Verification gates are exact shell commands that must exit 0 — `make check`
exits 0, `pytest` passes with no skipped tests, `curl -s localhost:PORT/health`
returns 200. Commands, not adjectives.

**Commit:** `CLAUDE.md` and `SPEC.md` once written — before starting the
audit, so the pre-audit spec is a distinct commit from the post-audit one.

---

## Phase 2.5 — Audit

**Command:** `/audit`, run in a **fresh session with no prior context.**

This matters — the point is removing the conversation history that made an
invented constraint feel natural. The agent reads only `SPEC.md`, as if
seeing it for the first time, and:

1. Lists every constraint it believes the system must satisfy, quoting the
   exact line in `SPEC.md` that establishes it
2. Separately lists anything it's inferring rather than reading directly
   (these should already be tagged `[ASSUMED]` — it checks for any that
   aren't)
3. For each constraint, asks what would be built differently if it were
   removed, flagging any whose removal changes nothing as possibly
   redundant or not load-bearing

This catches two failure modes: a phantom constraint invented from a
passing remark, and a silent choice made among several valid readings that
was never flagged at all. The second is worse — a phantom usually leaves a
trace, a silent choice leaves nothing to find. Nothing tagged `[ASSUMED]`
proceeds to Phase 3 unresolved.

**Commit:** `SPEC.md` once every `[ASSUMED]` tag is resolved. This is the
checkpoint that matters most — everything from Phase 3 onward builds
against this spec, so the audited version needs to be the one in git, not
just the one open in the editor.

---

## Phase 3 — Plan

**Setup:** `claude --permission-mode plan`, then `/plan`

Plan Mode is a permission mode where the agent cannot edit files — an
enforced constraint, not a polite request. `/plan` reads `CLAUDE.md` and
`SPEC.md` in full, inspects the current directory, and writes `PLAN.md`:
an ordered task list where each task is small enough to complete and
verify independently, the exact files each task touches, which FR each
task satisfies, the dependencies it'll install and why, and anything in
the spec that's ambiguous or that it would do differently.

I review `PLAN.md` on my phone, watching for wrong technology choices,
missing FRs, tasks that are secretly four tasks, unnecessary dependencies,
and — the most valuable part — the ambiguity section. If the agent found
something unclear, the spec was unclear.

Fixing a wrong plan costs ten seconds — edit a text file. Fixing wrong code
costs hours. That asymmetry is the entire point of this phase.

**Commit:** `PLAN.md` once reviewed and approved.

---

## Phase 4 — Build

**Scaffold first, always.** Before any business logic: directory
structure, dependency install, a Makefile with dev/test/check targets,
`.env.example`, `.gitignore`, a `/health` endpoint returning 200, and one
placeholder test that currently fails. No business logic yet. Verify it
actually runs — `make check`, real output — and commit it before touching
logic. This separates environment problems (dependency conflicts, port
collisions, container networking) from logic problems; debugging both at
once is where builds die.

**Command (repeated):** `/slice`

Implements the next unstarted task from `PLAN.md` — only that task. When
done: run every verification gate in `SPEC.md` and paste the real terminal
output, tick the FR checkboxes that task satisfies, show the diff, then
stop without starting the next task. Review and commit between slices.

**Vertical slices, not horizontal layers.** Build one complete path from
input to output — even handling a single case badly — then widen it.
Never build all the models, then all the services, then all the routes:
nothing works until the very end and there's no way to verify along the
way.

**Fake the hard parts first.** Hardcode the external API response, stub
the LLM call, use three rows of sample data. Get the whole pipe working,
then replace fakes one at a time — each replacement a small verifiable
change instead of a big-bang integration.

**One unknown at a time.** A new API and a new library and a new pattern
in one slice is how one-shots fail. Sequence them. If a slice has two
unknowns, split it.

**Command:** `/stuck`

If two attempts at the same slice fail, stop iterating and change
approach. The agent explains in plain English what it expected, what
actually happened, and what it thinks the root cause is, then lists two
different approaches with tradeoffs and recommends one, stating what would
make it wrong. Still stuck after that? The spec or plan is wrong — go fix
it rather than forcing the implementation to comply.

---

## Phase 5 — Deploy

### Where does it live?

Devbox is the default. Route elsewhere when:

| Situation | Where it lives instead |
|---|---|
| Needs to be up while devbox is down or I'm gaming | Cheap VPS |
| Needs a public URL or real user accounts | Not self-hosted at all |
| Sends email at volume | Managed sending service |
| Outgrows SQLite or needs real concurrency | Managed Postgres |
| Large file storage | Object storage |
| It IS auth, payments, or compliance | Don't build it |

Cloudflare Tunnel is the middle ground for genuine public access without
leaving devbox — but it moves the service outside the tailnet boundary, so
the "anyone who can reach it is already authenticated" assumption (see
Opening principle) stops holding. Anything tunneled needs its own auth.

**Command:** `/deploy`

Creates a Dockerfile and `docker-compose.yml`: multi-stage build, minimal
final image, port bound to the Tailscale IP only in the form
`100.x.y.z:PORT:PORT` — **never `0.0.0.0`** — read with `tailscale ip -4`,
persistent data on a host volume under `./data`, config via environment
variables from `.env`, `restart: unless-stopped`, a healthcheck hitting
`/health`, no obsolete `version:` key. Then it brings the stack up,
confirms the healthcheck passes, and shows `docker ps` and
`docker compose logs --tail 20`.

Before calling it done:

- [ ] `docker compose up -d --build` succeeds from cold
- [ ] `docker ps` shows the tailnet IP in PORTS, not `0.0.0.0`
- [ ] Reachable from phone over Tailscale
- [ ] Stack visible in Dockge
- [ ] Uptime Kuma monitor added, hitting `/health`
- [ ] **Reboot test** — the box (or at least the container) survives a
      restart and comes back up on its own. Wi-Fi associates slowly on
      cold boot on this machine; this is not optional.

### Escape hatch

Anything that ever goes external won't be self-hosted, so every project
must stay liftable — off devbox and onto a VPS, someone else's box, or
anywhere else — without a rewrite:

- Config via environment variables only, nothing devbox-specific baked
  into code.
- No devbox-specific paths, IPs, or hostnames hardcoded anywhere.
- `docker-compose.yml` would run unmodified on a different host — the
  only per-machine input is `.env`.
- State lives in a volume or a database, not scattered across the
  filesystem in ad hoc locations.

If lifting a project would be painful, that's a design smell — fix it now,
while the project is small, not after it's grown around the assumption.

---

## Phase 6 — Operate

Every project gets a `README.md` in three sentences: what it is, how to
run it, where the data lives. Anything irreplaceable — state that can't be
regenerated from git plus a fresh build — gets backed up; everything else
is disposable by design, since the whole point is `git pull && docker
compose up` recovery.

**Kill criteria:** if a project goes three months without being used,
that's the signal to decommission it, not to keep it running out of
inertia. An unused container is not a free asset — it's attack surface and
maintenance debt for zero return.

---

## Default stack

Pre-decided so no build re-litigates them. Deviate only with a stated
reason.

| Need | Default | Notes |
|---|---|---|
| Headless automation, scraping, pipelines | Python + `uv` | |
| API | FastAPI | |
| UI — app-shaped | Next.js + TypeScript + Tailwind | Heavily represented in training data; models write it well |
| UI — dashboard-shaped | Streamlit | When it's a readout, not an app. Ugly is fine. |
| State | SQLite | Postgres only when concurrency or size demands it |
| Scheduling | APScheduler in-process, or a systemd timer | |
| Notifications | Telegram bot | One bot, many apps, separate threads |
| Local inference | Ollama on the tailnet IP | Bulk text, classification, extraction — not code generation |
| Cloud inference | API via env var | Reasoning-heavy or quality-sensitive |
| Packaging | Docker Compose, one file per project | |
| Access | Tailscale | Never `0.0.0.0` |

**Open question, deliberately unresolved:** Next.js vs a no-build-chain
stack (FastAPI + HTMX). Next.js one-shots better because models know it
cold. HTMX is lower-maintenance and has no `node_modules`. Build one UI
each way before deciding, and note which was used in each project's
README.

---

## Project layout

```
~/projects/<app-name>/
  README.md              what this is, in three sentences
  CLAUDE.md              project rules and hard constraints
  SPEC.md                the contract — requirements + verification gates
  PLAN.md                written by Claude Code in Plan Mode, reviewed by me
  DESIGN.md              options considered, choice made, and why
  docker-compose.yml
  Dockerfile
  .env.example           every config key, no secrets
  .gitignore
  src/
  tests/
  Makefile               make dev / make test / make check
```

`make check` is the single command that proves the app is healthy — what
the agent runs to verify itself, what a hook enforces, and what Uptime
Kuma effectively asks in production.

---

## Phone vs desk

**Phone** is for decisions: ideation, spec review, approving plans, running
the slice loop on a stack the agent already knows well, kicking off long
background work to check on later.

**Desk** is for anything that genuinely needs eyes: large diffs, a stack
being used for the first time, anything visual (UI, layout, rendered
output), confusing debugging where state matters, or reviewing more than
about 50 lines of code at once. Don't try to eyeball a real diff on a
five-inch screen — it produces false confidence, not review.

---

## Model selection

- **Opus in chat** for ideation, architecture decisions, and hard
  debugging where reasoning quality matters more than speed.
- **Sonnet in Claude Code** for most building — the slice loop, scaffolding,
  routine implementation.
- **Opus in Claude Code** when a slice has stalled twice and `/stuck`
  hasn't resolved it — a bigger model for a genuinely hard problem, not a
  first resort.
- **Local Ollama** for bulk text — classification, extraction,
  summarisation — never for code generation. An 8B local model writing
  code is a false economy; the debugging time erases whatever was saved.

---

## Emergency commands

| Situation | Command |
|---|---|
| Agent going down a bad path mid-conversation | `/clear` |
| Agent mid-action, need to interrupt now | `Ctrl+C` |
| Last commit was wrong | `git reset --hard HEAD~1` |
| Check what the last commit actually changed | `git diff HEAD~1` |
| Container misbehaving | `docker compose logs --tail 50` |
| Container needs a kick | `docker compose restart` |
| Rebuild after a Dockerfile/dependency change | `docker compose up -d --build` |
| What's listening on a port | `ss -tlnp` |
| Is Ollama actually using the GPU | `docker exec ollama ollama ps` |
| Switch models mid-session | `/model` |

---

## What helps and what breaks one-shotting

**Helps:** a spec with tagged provenance, verification gates that are
commands rather than adjectives, one unknown per slice, faking the hard
integration first, stopping at two failed attempts instead of thrashing, a
scaffold that runs before any logic exists.

**Breaks it:** vague requirements papered over with an agent's best guess,
horizontal-layer builds with nothing runnable until the end, stacking a
new API and a new library and a new pattern into one slice, treating a
plan as sacred once written, and accepting "should work now" instead of
pasted command output.

---

## Worked example: bin collection reminder

Discovery: a Telegram message the night before bin collection. Brief:
done means a message arrives by 8pm the night before, only for the bins
actually due, no web UI needed. Design: single shape — no genuinely
distinct alternative, a cron-triggered script beats anything more
elaborate for this scope.

`/audit`, run cold on `SPEC.md` alone, flagged a constraint that wasn't
actually in the brief: "must handle multiple households." It had crept in
from a single passing line in the brief — "my partner should get it too" —
which the contract step had generalised into multi-household support
nobody asked for. Struck in two minutes once flagged. Left unstruck, it
would have meant a household data model, a settings UI, and per-household
scheduling logic for a feature that needed exactly one Telegram chat ID in
an environment variable — hours of build time for a capability nothing in
the brief required. This is the audit step earning its place in the
workflow: catching a phantom requirement while it's still a sentence to
delete, not a schema to unwind.

---

## Phase summary

| Phase | Command(s) | Output |
|---|---|---|
| 0 Setup (once per machine) | plugin install | Spec-driven plugin, standing rules in place |
| 0.5 Discovery | `/discovery`, `/roadmap` | `DISCOVERY.md`, `ROADMAP.md` (optional) |
| 1 Brief | `/brief` | `BRIEF.md` |
| 1.5 Design | `/design` | `DESIGN.md` |
| 2 Contract | `/contract` | `CLAUDE.md`, `SPEC.md` |
| 2.5 Audit | `/audit` (fresh session) | Resolved `[ASSUMED]` tags |
| 3 Plan | `claude --permission-mode plan`, `/plan` | `PLAN.md` |
| 4 Build | scaffold, then `/slice` (repeat), `/stuck` if blocked | Working, verified, committed code |
| 5 Deploy | `/deploy` | Running container on the tailnet |
| 6 Operate | — | README, backups, kill criteria |

---

This playbook is a guide, not authority. If implementation friction says a
step is wrong, the step is wrong. Update this file.
