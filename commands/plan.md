Read CLAUDE.md, SPEC.md, and EXPLORE.md (if it exists) in full. Inspect the
current directory.

Write PLAN.md containing:
1. **Open questions — as the first numbered tasks, not a note.** Anything
   BLOCKED in EXPLORE.md, or tagged [BET] or [ASSUMED] in SPEC.md, where being
   wrong would invalidate work rather than just adjust it.

   - **BLOCKED items come first, always.** These are checkable and unchecked —
     mostly minutes and no code: request the export, open the file, read the
     feature page. Nothing that assumes the answer gets planned after them; it
     gets planned *behind* them.
   - **A BET that would invalidate the build gets proved by the smallest
     possible slice of real code**, with everything around it faked — before
     any work depends on it being true. If the answer only shows up once real
     data flows end to end, then a thin end-to-end path is the first thing
     built, not the last. Never sequence a build so an invalidating answer
     arrives at task 40.

   If this produces a build order that looks wrong to you, order it this way
   regardless and say why you disagree. A recommendation to do something early,
   attached to a task numbered late, is not an ordering — /slice follows the
   numbers, and prose never overrides them. Do not talk yourself out of
   reordering on the grounds that the dependency is slow to arrive; slow is the
   argument for starting it first, not for building against a guess meanwhile.
2. Then the scaffold: a Makefile with `dev`/`test`/`check` targets,
   `.env.example`, `.gitignore`, and one placeholder test that currently fails
   — before any business logic. Every later task's verification depends on
   `make check` existing and being fast; skipping it leaves nothing scoped to
   check against until the whole build is done.
3. Then the ordered task list, each task small enough to complete and verify
   independently. **Sequence it so one real path runs end to end as early as
   possible** — narrow, not faked. Pick the single simplest case the app exists
   to handle, and make every stage of it real for that one case, even if it
   handles that case badly. One real input, through real code at every step, to
   one real output. Then widen.

   Narrow means *fewer cases*, not *pretend data*. A pipeline that runs end to
   end on stubbed responses and sample rows proves the wiring and nothing else
   — every stage still gets its first contact with reality later, all at once,
   which is the failure this ordering exists to prevent. Fake a stage only when
   the real thing is genuinely unavailable at that point in the build — an
   export that hasn't arrived, an API that costs money per call — and when you
   do, say in the task which stage is faked and which task makes it real.

   Do not build each layer fully in dependency order — all the models, then all
   the services, then all the routes. Discovering at task 30 that nothing has
   ever run together is the outcome that ordering produces.
4. The exact files each task creates or modifies
5. Which FR from SPEC.md each task satisfies
6. The dependencies you'll install and why each is needed
7. Anything in the spec that's ambiguous or that you'd do differently, stated
   plainly

Do not create or modify any source files. If you are not already in
plan/read-only mode, treat this instruction as binding: no edits, plan only.
