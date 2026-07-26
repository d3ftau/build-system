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
   independently. Sequence it so something runs end to end as early as
   possible, with the hard parts faked — a stubbed API response, three rows of
   sample data — rather than building each layer fully in dependency order.
   Replacing a fake is a small verifiable change; discovering at task 30 that
   nothing has ever run together is not.
4. The exact files each task creates or modifies
5. Which FR from SPEC.md each task satisfies
6. The dependencies you'll install and why each is needed
7. Anything in the spec that's ambiguous or that you'd do differently, stated
   plainly

Do not create or modify any source files. If you are not already in
plan/read-only mode, treat this instruction as binding: no edits, plan only.
