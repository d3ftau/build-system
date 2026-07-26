# Enhancements

Process failures found in this build system, recorded when they're diagnosed
and fixed in dedicated sessions later. Each file records **where it came from,
the general failure mode, concrete evidence, and candidate fixes** — deliberately
not a prescribed patch, because scoping the fix to the exact symptom is how you
get a system full of narrow special cases.

## Layout

```
enhancements/
  README.md    this index — the status table below is the source of truth
  open/        diagnosed, not fixed (or only partly fixed)
  done/        fully implemented; the fix is in a command file or a hook
```

A file moves to `done/` only when every item in its own "Still open" or
"Candidate fixes" section has landed **somewhere binding**. Partially-fixed
work stays in `open/` — `002` is the current example.

**Binding means a command file, a hook, or a generated project `CLAUDE.md`.**
An edit to `PLAYBOOK.md` alone does not close an enhancement. That is `002`'s
entire thesis, and applying it to this tracker is the point: the playbook is
documentation, the command files are the program.

## Status

| # | Title | Status | Fix binds in | Verified |
|---|---|---|---|---|
| [001](open/001-pipeline-over-trusts-prior-output.md) | The pipeline over-trusts its own earlier output | **OPEN** | nothing yet — `commands/audit.md` untouched since `333c972` | 2026-07-26 |
| [002](open/002-principles-dont-reach-commands.md) | Principles in PLAYBOOK.md prose don't reach the commands | **PARTIAL** | `commands/plan.md` (`165da12`) — 3 items still open | 2026-07-26 |
| [003](open/003-scope-only-ratchets-up.md) | Scope can grow but never shrink; agent-argued requirements recorded as the user's | **OPEN** | nothing yet | 2026-07-26 |

## Open items in detail

**001 — over-trusting prior output.** Nothing implemented. `[STATED]` still
conflates "the user decided this" with "an earlier document asserted this."
`/audit` still asks for a quoted source line, which rewards traceability rather
than correctness. `/explore` (`d1511c6`, `f0a0b3f`) landed nearby but addresses
the externally-checkable class of claim — which is the case this file records as
having *self-corrected fine*. The unfixed core is claims about model judgment.

**002 — playbook prose doesn't bind.** The vertical-slice principle now lives in
`commands/plan.md`. Still open:
- *"One unknown at a time"* remains orphaned — confirmed absent from `commands/`
  and `hooks/` as of 2026-07-26; it exists only in `PLAYBOOK.md:355`.
- `file-cleanup/PLAN.md` has not been regenerated — still 41 tasks, first
  end-to-end run at ~31.
- No mechanism prevents recurrence. Both fixes so far were "someone noticed and
  edited a file."

**003 — scope only ratchets up.** Nothing implemented. `/roadmap`'s test
("would this be worth using if nothing after it got built?") can only detect a
build that is too small, and PLAYBOOK.md:122 gives growing it as the only
remedy. No command can make a build smaller. Separately, a requirement the agent
argued for and the user assented to gets recorded as `[STATED]`, identical to
one the user raised unprompted.

## Common thread

All three are the same shape: **the system trusts its own prose.** A claim
becomes true by being written down confidently in a document with an
authoritative title, and every later stage's job is to honour the previous
document rather than test it. `001` and `003` are both provenance-tagging
failures and are probably one fix; `002` is why any fix has to land in a
command file to exist at all.

## Adding one

Number it next in sequence, drop it in `open/`, add a row to the table above
with what would have to bind for it to close. Record the diagnosis and evidence
now while it's fresh; leave the fix to a dedicated session with a clear head.
