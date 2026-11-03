# Enhancement: A nice-to-have becomes the build's spine, and every snag after that adds machinery instead of questioning it

**Status: OPEN, fix written, not yet seen working** (recorded 2026-11-01). Greg: "one of your biggest failures yet."

## Where this came from

backrest, Build 2 ("Rebuild without fiddling"): moving devbox's Linux side to
the mini. Phase 3, during /build of T13–T16, 2026-11-01. In discovery the
port was *"a fresh Ubuntu install, the setup script, a restic restore, then
`git pull && compose up`"*. Greg asked whether a scripted run was possible,
as a nice-to-have. By the brief it had become the definition of done: "no
hands from power-on", with "hands-on install steps" under **Never**. Every
later stage honoured that line, and the build grew around it:

- an unattended-install USB stick carrying every secret;
- a timed cutover (`CUTOVER_AT`) that waits on the mini;
- a forced-command SSH key so the mini can drive devbox;
- a passwordless-sudo root helper installed on devbox;
- a mode for "devbox unreachable", from the latest snapshot;
- a stand-in devbox container so a VM could rehearse the whole cutover;
- a monthly-rewritten "kept stick" with its secrets, plus a reminder timer.

The last step was this question from Claude: a "24-hour wipe guard" so the
kept stick wouldn't wipe the server if left plugged in through a reboot. It
was marked "(Recommended)". Greg:

> *"What sort of crazy recommended solution is this. … you are still trying
> way too hard to save a tiny amount of work. This is supposed to be an
> extremely straightforward migration and [I've] spent about 15% of weekly
> quota building what seems to be a ridiculously convoluted solution. I asked
> if a scripted run was possible as a nice to have and now we're building
> doomsday keys that wipe any machine they are plugged into."*

Asked to review the plan, Claude found the simple shape in one pass. The
cutover is two pasted commands: one on devbox (stop, final backup, power off,
with sudo typed by hand) and one on the mini (final restore from OneDrive,
the Tailscale takeover, start, check). The boxes never need to talk to each
other, because the final restore comes from OneDrive and not from devbox.
Nothing in the shape was new. It was available at /plan, and at both
checkpoints.

Greg, afterwards, putting it at its sharpest:

> *"The build system asks for the smallest slice I would use yet you don't
> ask yourself if what you're building is making things 100x more complex to
> save me entering one line in a terminal."*

The pipeline applies "smallest version" to the *product* at /brief. It never
applies it to the *mechanism* during the build. There, each piece of
machinery was judged on whether it worked, never on what it saved Greg. Here
it saved him pasting about two lines, once.

It also took Greg two challenges to get the failure admitted in full:

> *"It also took two challenges from me for you to fully admit it."*

**The first challenge was at checkpoint 2, before any Phase 3 code existed.**
Greg asked directly (2026-11-01, 10:25 UTC):

> *"Can I double check the aim to 'not notice I'm on a new machine' doesn't
> have us massively over engineering everything? A prompt out to all repos
> after the move to check they are working is easy and probably solves every
> glitch."*

Claude answered "partly yes", then mostly defended the plan. It listed what
a prompt "can't do" and cut only *checking*: the daily timer checker, the
hourly Deco nag, a second rehearsal, a live undo test. Everything that made
the build complex stayed: the automated, timed cutover, devbox driven over
SSH, the kept disaster stick and its monthly reminder. The reply also read
FR-12 ("the same stick rebuilds the server") as something Greg had stated,
which made it look like a constraint. And one argument for keeping the
machinery rested on something false, "two fashion-bots would both answer
Telegram"; fashion-bot doesn't use Telegram, which Greg had to correct. The
reply never asked the question the build was really facing: is any of this
worth more than Greg pasting two lines at the cutover? So Phase 3 was built
on the over-built plan he had just asked about. That is the expensive half
of this failure.

**The second challenge** was his "crazy recommended solution" message,
mid-build. That reply conceded, then got straight back to selling. It led
with what was "built and working" and "tested today", and offered the cut as
a new proposal. It didn't say the question had already been put at
checkpoint 2 and answered wrongly. Defending earlier work while appearing to
concede is the same sunk-cost pull that built the machinery in the first
place.

And the cost in Greg's time, not just quota:

> *"The real irony is - I spent hours yesterday afternoon interacting with you
> about this build for you to save me literally 30 seconds or so of work. This
> needs a widespread fix across the whole build system as it seems
> extraordinarily avoidable."*

The automation was meant to save his attention. It used hours of it, in
questions, stops and reviews, to save about 30 seconds of pasting.

## The failure modes

0. **"Smallest" is asked about scope, never about mechanism.** Nothing makes
   the agent price new machinery against the human step it replaces, in
   lines typed and times done. One line pasted once is almost free. A key,
   a sudo rule, a timed wait and a rehearsal rig are not.

1. **Provenance lost on the way in (`003` again).** A "would be nice" in
   discovery became the brief's *Done* line and a **Never**. After that no
   stage could tell it was optional, so no stage weighed its cost. `003` is
   marked DONE, so its fix doesn't cover a requirement that hardens while it
   is being restated, not only when it is added.
2. **Complications are solved, never priced.** Each snag (root over SSH, the
   SSH key, the cutover timing, the rehearsal touching real jobs, a stick
   that can wipe) got more machinery. Claude never asked "this goal now costs
   X; is it still worth it?". The `/build` rules make this worse. "Rulings,
   not stalls" and "take the choice that's easiest to undo" both push toward
   adding code, never toward cutting scope. The stop list has "a plan so wrong
   that every way forward is a guess", but nothing for "a plan whose cost has
   outgrown what it buys".
3. **Checkpoints check quality, not proportion.** Checkpoint 2 cut some
   checking, but kept the automated cutover, the disaster stick and the
   rehearsal. It asked "is this good enough to build on?", never "is this
   still the simplest thing that does the job?". `011` (proportion at
   spec/plan) is DONE, but it doesn't reach checkpoints or a running build.
4. **Recommending the most elaborate option.** When Claude did ask, the
   recommended answer was the one with the most new mechanism. "Drop the kept
   stick" wasn't offered at all. The real choice behind the question, whether
   this feature should exist, was never put to Greg.

## Concrete evidence

- `backrest/DISCOVERY.md`, "Where it landed", item 5: the port as install +
  setup script + restore + compose up.
- `backrest/builds/build-2/BRIEF.md`: *Done* = "runs with no hands"; *Never*
  = "Hands-on install steps".
- `backrest/builds/build-2/PLAN.md`: 18 tasks. T13 (forced-command key, sudo
  helper), T15 (CUTOVER_AT, with/without-devbox modes, a VM rehearsal with a
  stand-in devbox), T16 (the monthly reminder, a wipe guard due before it).
- `backrest/builds/build-2/BUILD-LOG.md`, T13–T14 rulings; platform commits
  `923ce19`, `dfa10ca`, and T15's uncommitted work (15 files).
- Cost: by Greg's estimate about 15% of a week's quota, on a migration that
  needs perhaps a third of what was built.

## Candidate fixes

Not prescriptive.

- **A trade test for any automation, at /plan and in /build:** name the
  human step it removes and how often it happens. "Greg pastes one line,
  once" is the bar the code has to beat. If the code needs a new secret, a
  permission, a mode or a rehearsal to beat it, the human step wins by
  default.

- **Every requirement keeps its strength from discovery onward:** must /
  should / nice-to-have, with who said it. The brief's *Done* line and its
  **Never** list may hold only "must"s. A nice-to-have that a later stage
  wants to make load-bearing goes back to Greg as a question, with its cost.
- **`plan.md`:** before ordering tasks, write the smallest plan that meets
  only the "must"s. Then price each nice-to-have as extra tasks, and let Greg
  choose.
- **`build.md`:** a stop for growth. When a task needs new machinery that the
  plan didn't name to keep a goal alive (a new key, permission, mode,
  rehearsal rig or guard), stop and ask whether the goal is worth it. Don't
  rule on it. "Easiest to undo" isn't the test. "Smallest" is.
- **`checkpoint.md`:** add "what would you cut?" Re-derive the simplest
  version of the whole remaining plan, and compare its size with the plan
  as written.
- **"Is this over-engineered?" from Greg is a re-plan trigger, not a review
  item.** The answer starts from the smallest version that meets the
  "must"s, re-derived from scratch, and compares it with the plan. It doesn't
  start from the plan and trim around the edges. Any argument for keeping a
  piece has to name the requirement and who stated it, and checking a fact
  it rests on (Telegram) comes before using it.
- **When challenged on over-building:** the first reply states the failure
  plainly: what was never asked, and since when. Only then does it list what
  survives, and it doesn't defend the earlier work in the same breath.
- **Recommended options:** a question about adding a mechanism must also
  offer "don't have this feature", and recommend the smallest option unless
  there's a stated reason not to.

## Fix written (2026-11-01, same session; revised the same day)

The first fix (`323bf3d`) swung too far: "a manual step is cheap; automating
it must beat it", spread across seven commands. Greg:

> *"you have swung too far the other way. If automating a rare and simple
> manual step only takes a line or two of code itself that is fine. The
> question is about effort vs time saved. Automation is the goal here but
> spending more time automating than would be saved in a lifetime of
> automations is a poor return on effort, even worse if it is creating new
> sets of problems which in turn need more effort to solve."*

So the rule is a return test, not a bias toward manual: **the effort to build
and keep a piece of automation, plus the problems it creates, against the
time it saves over its whole life.** Cheap automation is simply done.
Brief, spec and oneshot are rolled back to before `323bf3d`; build has a narrower stop.

- `discovery.md` (kept from the first fix): each requirement records its
  strength, must or nice-to-have, beside who raised it.
- `plan.md`, `build.md` and `checkpoint.md`: the return test (effort to
  build and keep, against time saved over its life or mistakes prevented)
  fires only on expensive automation: a new secret, permission,
  cross-machine link, mode or rehearsal rig, or a piece that fixes another
  piece's problem (the chain, the clearest warning). Ordinary code is never
  weighed, so the rule adds no overhead to normal work (Greg: "code by
  definition is automation").
  - `/plan`: one line per piece that fires; if the saving doesn't clearly
    win, it goes to Greg as a question.
  - `/build`: a ruling that adds such a piece unweighed is a stop, not a
    ruling. Most of Build 2's machinery grew here, mid-phase.
  - `/checkpoint` step 6, "Is it still worth it?": re-weighs those pieces,
    built and planned, every phase. A chain under the remaining plan means
    re-plan; it's also where "is this over-engineered?" is answered.

Still open: seeing it work in a real /plan and /checkpoint. Whether the
challenge-response rule belongs in `~/.claude/CLAUDE.md` is Greg's call
(proposed, not applied).

Also (2026-11-03, review): `build.md`'s "take the choice that's easiest to
undo" is now "the smallest choice (between equals, the one easier to undo)".
That was the second `/build` rule named in failure mode 2.
