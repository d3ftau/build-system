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
work stays in `open/`.

**Binding means a command file, a hook, or a generated project `CLAUDE.md`.**
An edit to `PLAYBOOK.md` alone does not close an enhancement. The commands are
the source of truth; the playbook explains them (`002`). The exception is
guidance aimed at the user rather than the agent, which the playbook owns.

## Status

| # | Title | Status | Fix binds in | Verified |
|---|---|---|---|---|
| [001](done/001-pipeline-over-trusts-prior-output.md) | The pipeline over-trusts its own earlier output | **DONE** | `contract.md`, `audit.md` (`9b0d2dd`, `d381b32`) | 2026-07-27 |
| [002](done/002-principles-dont-reach-commands.md) | Principles in PLAYBOOK.md prose don't reach the commands | **DONE** | `plan.md`, `slice.md`, `contract.md`, PLAYBOOK.md redefined as explanation (`165da12`, 2026-10-01) | 2026-10-01 |
| [003](done/003-scope-only-ratchets-up.md) | Scope can grow but never shrink; agent-argued requirements recorded as the user's | **DONE** | `roadmap.md`, `brief.md`, `discovery.md` (`9b0d2dd`, `d381b32`) | 2026-07-27 |
| [004](done/004-no-post-build-doc-audit.md) | Nothing performs a post-build doc-reality audit; `CLAUDE.md`/`DESIGN.md` drift silently, no `README.md` ever gets written | **DONE** | `complete.md` (new), `bin/build-state` | 2026-10-01 |
| [005](done/005-deploy-assumes-one-project-shape.md) | `/deploy` assumes every project is a reachable web service | **DONE** | `deploy.md` | 2026-10-01 |
| [006](done/006-pipeline-has-no-concept-of-a-human-surface.md) | The pipeline has no concept of a human surface; FRs go green with no UI and nothing ever asks what it should look like | **DONE** | `brief.md`, `design.md`, `contract.md`, `plan.md`, `checkpoint.md` | 2026-10-01 |
| [007](done/007-slice-settles-open-decisions-silently.md) | `/slice` settles the plan's open decisions silently, mid-build, and surfaces them only after the code exists | **DONE** | `slice.md`, `plan.md`, `hooks/verify-before-stop.sh` | 2026-10-01 |
| [008](done/008-claims-accepted-without-checking-they-can-be-true.md) | Claims are accepted on evidence that tests something adjacent to what the claim says | **DONE** | `slice.md`, `design.md`, `contract.md` (+ `~/.claude/CLAUDE.md`, outside this repo) | 2026-10-01 |
| [009](done/009-slice-is-too-small-a-unit-for-a-large-build.md) | `/slice`'s per-task lens can't see output quality, cross-task patterns, or a stale plan — and a 61-task build has no checkpoint that can | **DONE** | `checkpoint.md` (new), `plan.md`, `slice.md`, `bin/build-state` | 2026-10-01 |
| [010](done/010-existence-checks-skip-oss.md) | "Does this exist" checks default to commercial alternatives and skip GitHub/OSS as its own search category | **DONE** | `discovery.md`, `explore.md` | 2026-10-01 |

## Open items in detail

None open as of 2026-10-01.

## Common thread

The first three are the same shape: **the system trusts its own prose.** A
claim becomes true by being written down confidently in a document with an
authoritative title, and every later stage's job is to honour the previous
document rather than test it. `001` and `003` are both provenance-tagging
failures and are probably one fix; `002` is why any fix has to land in a
command file to exist at all.

`008` is that thread one level in — the same substitution of a confident
assertion for a checked one, but *within* a session rather than across
documents, and with evidence actually produced that tests something adjacent
to the claim. It may ultimately be one fix with `001`.

`006` is a different shape and worth keeping distinct: there was nothing to
distrust. The spec was accurate, internally consistent, and complete as a
description of a backend. The failure was that the document format could not
represent what was missing, so no amount of reading it carefully would have
found the gap — which is also why the existing `audit.md`, which checks
truthfulness, cannot catch it.

`009` is `006`'s shape rather than the first thread's: again nothing was
untrue. Task 12's build note recorded its real measured hit rate accurately.
The failure was that **no stage owns the question "is this good enough to build
on"** — `/slice` verifies one task against its own gate, `/audit` checks
documents against reality at the end, and the gap between them is where a
33.6%-correct component sat for two days holding up nutrition *and* allergy
filtering. It also has a scale term the others don't: the same pipeline that
was adequate at 35 tasks is visibly not at 61, which makes it the first
enhancement whose severity is a function of `003` staying open.

## Adding one

Number it next in sequence, drop it in `open/`, add a row to the table above
with what would have to bind for it to close. Record the diagnosis and evidence
now while it's fresh; leave the fix to a dedicated session with a clear head.
