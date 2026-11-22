# Enhancement: build sessions may spend subscription usage on steps code could do; nothing measures it

**Status: OPEN, undiagnosed: measure first** (recorded 2026-11-22, from /discovery in
`~/projects/llm-test`). Claude proposed it while looking for work to move off the Claude
subscription; Greg chose to file it here rather than fold it into that project.

## What prompted it

Greg's goal in llm-test is to free up his Claude subscription for work that needs it. Measuring
where the usage goes (`~/.claude/projects/*/*.jsonl`, 149 sessions over 20 KB, Oct–Nov 2026):

- **About 70% of Claude Code tokens are in sessions that run /build or work on PLAN.md**
  (input + cache writes + output; cache reads not counted; not weighted by model; the /build match
  is a loose regex).
- Of 139M tokens in total, by project: deal-hunter 20%, autopantry 13.5%, backrest 10%.

llm-test asks which of that work a *local model* could do. This enhancement asks a cheaper
question first: **how much of a build session is steps whose rules can be written down**
(bookkeeping in BUILD-LOG/PLAN.md, ticking checklists, reading `make check` output to see
pass/fail, re-reading the same project docs at the start of each task), which by
`~/.claude/CLAUDE.md`'s "never use an LLM for work that code can do" should be code, not a model
of any size.

## The failure mode, if it's real

The pipeline has no measure of what a build session spends its tokens *on*. So a recurring step
that code could do never shows up as a cost, and nothing proposes moving it into `bin/`, a hook,
or `bin/build-state`.

## Evidence so far

Only the session-level share above. **There's no per-step breakdown yet**, so this is a hypothesis
and not a diagnosis. Specifically unknown:
- how much of a /build session's tokens are re-reading context, versus tool output, versus writing
  code;
- whether any single enumerable step is big enough to matter.

## Candidate fixes (for a dedicated session)

1. **Measure:** attribute tokens in a few real /build transcripts to the tool calls and phases that
   caused them (doc reads, test output, BUILD-LOG writes, code edits).
2. For any enumerable step that shows up large, move it to a script or hook the command calls,
   following the "advisory vs deterministic" rule in PLAYBOOK.md.
3. If nothing enumerable is large, close this as "not a problem", with the measurement attached.
