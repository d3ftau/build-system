# Enhancement: The first end-to-end run is ordered ahead of prep the spec already says it needs

**Status: OPEN** (recorded 2026-10-19)

## Where this came from

autopantry, build 2 stage 2 (meal planner), Phase 1, T5's device run,
2026-10-19. Greg planned five recipes on his phone and tapped **Make list**.
ingredient-match then ran Qwen live for 28 ingredients it had never seen,
about 20 s each, for roughly 10 minutes. The two tasks that would have
avoided this, T15 (ingredient-match registers library recipes itself,
nightly) and T16 (slim the library, then register and price all of it), sit
in a later phase. Greg:

> *"moving the DB slimming prior to this step would've made a lot of sense.
> The plan rules say to get an end to end test in early (which we have) but
> it's been designed in a way to make it as clunky as possible"*

## The failure mode

`plan.md`'s rule "one real path, end to end, as early as possible" is applied
as "reach the path as soon as possible". It does not ask what that first run
will be like for the person using it. So prep that is cheap, depends on
nothing, and that the spec **already says the real path needs** is ordered
after the run it would have fixed.

It wasn't an unknown. The stage's own SPEC.md, FR-4, said so before planning:

> Registering from the Planner is too slow (observed 2026-10-16: a recipe with
> ingredients new to ingredient-match took up to 12 minutes …). The whole
> library, once slimmed, is registered once in advance.

The plan still put "once in advance" at T15–T16, after the first device run
(T5). Two more things follow from this:

- **A user action known at /plan time became a mid-build stop.** T16 is a
  `⏸ STOP` whose ask is "slim the recipe library first". Nothing about it
  needed the build to exist. It could have been asked at /plan, or put as the
  first task, so its result was ready before anyone touched the app.
- **"Real data" was met only in the letter.** The rule forbids stubbed stages,
  and the run was real at every stage. But the first hands-on test ran
  with a cold cache, which no later real use would ever hit, so it looked worse
  than the product will. The rule says nothing about ordering to avoid that.

## Concrete evidence

- `autopantry/builds/build-2-stage-2/PLAN.md`: Phase 1 is T1–T5. The end-to-end
  device run is in T5. T15 and T16 are in a later phase.
- `autopantry/builds/build-2-stage-2/SPEC.md`, FR-4: the 12-minute observation
  and "registered once in advance".
- `autopantry/BUILD-LOG.md`, T3 and T5: the drumsticks list needed 6 new
  product sets. Greg's 5-recipe list needed 28 (`asking Qwen for product sets
  (8 of 28)` at 09:27 on 2026-10-19).

## Candidate fixes

Not prescriptive.

- **`plan.md`, Order:** before placing the first real path, list what the spec
  says the real path depends on: caches, bulk registration, data cleanup,
  seeding. Put any of it that is independent and cheap ahead of the first
  hands-on run.
- **`plan.md`, step 1 (ask me everything first):** ask at /plan for user
  actions that need nothing built, such as "slim the library". Don't leave
  them as a `⏸ STOP` partway through the build.
- **A plan-time check:** "What will Greg's first hands-on run feel like, and
  is anything making it worse than steady state that a task already in this
  plan would fix?" If yes, move that task earlier.
- Watch the overlap with `011` (proportion). The fix is ordering, not more
  tasks.

## Still open

- `commands/plan.md` is unchanged.
