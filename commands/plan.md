Read CLAUDE.md and SPEC.md in full. Inspect the current directory.

Write PLAN.md containing:
1. An ordered task list, each task small enough to complete and verify
   independently. Task 1 must be the scaffold: a Makefile with `dev`/`test`/
   `check` targets, `.env.example`, `.gitignore`, and one placeholder test
   that currently fails — before any business logic. Every later task's
   verification step depends on `make check` existing and being fast; skipping
   this leaves nothing scoped to check against until the whole build is done.
2. The exact files each task creates or modifies
3. Which FR from SPEC.md each task satisfies
4. The dependencies you'll install and why each is needed
5. Anything in the spec that's ambiguous or that you'd do differently, stated
   plainly

Do not create or modify any source files. If you are not already in
plan/read-only mode, treat this instruction as binding: no edits, plan only.
