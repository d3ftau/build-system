# Enhancement: the pipeline has no concept of a human surface

**Status: DONE** — all three candidate fixes landed.

## Where this came from

Autopantry Build 1, 2026-08-06, around task 17. After eight tasks had been
built against `PLAN.md`, the user asked: *"I've just gone through the plan and
it looks like we're building only a tiny portion of the actual UI for the app.
is the idea that we are completing pantry management only and everything else
comes after?"*

It wasn't. Checking every FR against the task list found **four requirements
whose server half was assigned a task and whose input half was assigned
nothing**:

| Requirement | What the plan assigned | What was missing |
|---|---|---|
| FR-7 / FR-17 household identity | nothing | the household's `email_token` — the address order emails must be forwarded to — was displayed nowhere; it could only be read out of Postgres by hand |
| FR-21 allergy roster | `household_members` table + allergen filter | no screen; allergies could only be entered by writing SQL |
| FR-23 managed vs BYOK | server-side routing (task 28) | no chooser; the client half (task 24) was the Gemini *call*, not a settings surface |
| FR-22 spend cap | server-side enforcement (task 27) | no display; a household hitting a cap had no way to see it |

A second, related finding in the same session: **no step in the chain had ever
asked what the thing should look like.** Confirmed by grep across
`BRIEF/DISCOVERY/ROADMAP/EXPLORE/DESIGN/SPEC/CLAUDE` — zero hits for look and
feel, visual, palette, typography, theme. The user: *"building a whole UI based
on a few mostly functional paragraphs is a bit opaque, do I get a say in the
look and feel of the app?"* Every visual decision in the built app was the
agent's own, unasked and unreviewed, and the first screen built had silently
become the design language.

## The general failure mode

**The document format cannot represent the gap, so reading the document cannot
find it.** Three mechanisms compound:

1. **`/contract`'s SPEC.md template has no slot for a screen.** Its
   `## Interfaces` section is defined as "signatures, routes, message formats —
   anything crossing a boundary," and in practice held only HTTP routes and
   payloads. A missing screen is not an omission the document can express.
2. **`THE SYSTEM SHALL` is satisfiable server-side by construction.** The
   mandated FR phrasing asks for "observable behaviour" without asking
   *observable by whom* — a row in Postgres qualifies. FR-21's "never suggest a
   recipe containing that trigger" is satisfied by a filter function with no
   caller. So FR checkboxes went green while the product stayed unusable
   without SQL.
3. **`/brief`'s five questions are all functional** — done criteria, data and
   storage, edge cases, failure modes, who else touches it. The last is the
   closest and reads as *access*, not *experience*. Nothing asks who looks at
   this or what using it should feel like.

This is `001`'s shape — trusting earlier output rather than testing it — but
with a sharper edge: here there was nothing to distrust. The spec was accurate,
internally consistent, and complete *as a description of a backend*. The
existing `AUDIT.md` step checks provenance, tag correctness and
self-contradiction — all **truthfulness** properties. Nothing anywhere checks
**completeness as a product**.

Worth recording separately: the plan's own header documents catching one
instance of this and fixing it locally — the first draft deferred all UI to
task 31 behind ~24 backend tasks, and was corrected to put an app shell at task
7 — without ever asking whether the same blindness applied elsewhere. It did.
A local fix to a systemic blindness reads as resolution and prevents the
general question being asked.

## Candidate fixes

Deliberately three, at different stages, because a single check at one stage
would be the narrow special case the tracker's README warns about:

- **`/contract`** — split `## Interfaces` into machine interfaces and human
  surfaces, with the rule that any FR using *let*, *show*, *review* or *choose*
  must name the surface it lives on. This is the structural one: it makes the
  gap unwritable rather than merely detectable.
- **`/brief`** — a second always-asked question alongside the mandatory
  smallest-version one: who looks at this, and what should it feel like to use.
  Always-asked for the same reason: by the time scope reaches `/brief` it has
  been growing unopposed, and nobody volunteers the experience question.
- **A new completeness audit between `/plan` and `/slice`** — every FR, which
  task delivers the part a person touches; every table, is there a non-SQL path
  to get data in; first run, can someone get from install to the core loop
  unaided; is there a design language or is it about to be set by default.

The table check is the sharpest and generalises best — `households`,
`household_members` and `household_api_keys` all failed it.

## Open, not resolved here

- Does the human-surface rule belong in `/contract` (a spec section) or
  `/plan` (a task must exist)? Putting it only in the spec risks a named
  surface nobody schedules; only in the plan risks the requirement never being
  written down.
- Whether the completeness audit is a new command or an extension of the
  existing `audit.md`. `004` already proposes a *post-build* doc audit; this is
  pre-build and checks a different property, but two audit commands may be one
  too many.
- The look-and-feel question has no obvious artefact. `/design` produces
  architectural options, not visual ones. What the answer gets written *into*
  is undecided — DESIGN.md has no section for it.

## Still open

- No command file has changed. All three fixes are proposals.
- Nothing prevents recurrence — this was found because the user read the plan
  and asked, which is the same "someone noticed" pattern as `002`.
- The four Autopantry gaps were patched in that project's `PLAN.md` (tasks
  18b, 21b, 28b) but that is a project-level fix, not a binding one.

## Implementation status (2026-10-01)

- `commands/contract.md` — `## Interfaces` split into **Machine Interfaces**
  and **Human Surfaces**; any FR where a person enters, sees, reviews or
  chooses something must name its surface; every table holding a person's
  data needs a non-SQL way in. "Observable by whom?" stated explicitly.
- `commands/brief.md` — second always-asked question: who looks at this, and
  what should using it feel like. BRIEF.md gets a "Who sees it" line.
- `commands/plan.md` item 5 — **human surface check** table (every FR → task
  building the part a person touches; every user-data table → non-SQL entry
  task; first run → task). Empty cell = missing task.
- `commands/checkpoint.md` item 4 re-runs that table against the code as built.
- **Open questions, decided:** the rule lives in *both* `/contract` (written
  down) and `/plan` (scheduled) — each alone fails the way the original note
  predicted. The completeness audit is a required table in `/plan` plus a
  re-check in `/checkpoint`, not a third audit command. Look and feel goes in
  a **Look and feel** section of DESIGN.md (`commands/design.md`), asked not
  filled; if the user doesn't care, the first screen sets the style and is
  shown before a second is built.
