# Enhancement: Spec and plan complexity doesn't scale to the size of the solution

**Status: DONE** (2026-10-11, via `015`) — `spec.md` sets proportion and replaces the failure catalogue with "When it breaks"; `plan.md` asks only decisions that change what the user gets or sees; `audit.md` is gone, its useful part now the five-situation walk at the end of `/spec`.

## Where this came from

fashion-bot build 1, 2026-10-09: a personal app that emails one person a daily
list of cheap Country Road outlet menswear in their sizes. During `/audit`
and `/plan` the user said:

> *"Why are you obsessed with this no longer available edge case? If I can't
> buy it, you don't send it. This is the third time it's been brought up"*

> *"I feel like the more effort I put into planning just goes towards you
> trying to find bizarre and completely irrelevant edge cases to think
> decisions need to be made on instead of focusing on the goal of the app"*

> *"This isn't a nuclear launch sequence, I'm just trying to find cheap
> clothes to buy"*

> *"complexity of specs and plan needs to match the needs of the solution.
> Seems like even the most basic of projects is coming out with 30+ FRs and
> overly complex thinking around failure modes"*

## Evidence

**fashion-bot (one retailer, one recipient, one email a day):**
- **SPEC.md:** 23 FRs, 481 lines, 8 SQLite tables.
  - The `observation` table has 17 columns, kept per item per run, and
    nothing ever reads its history.
  - A `fibre_seen` table exists only to feed autocomplete suggestions.
- **Failure Modes table:** 13 rows of invented thresholds, none of which the
  user asked for:
  - 60 s timeout, then one retry after 60 s
  - more than 10% malformed tiles fails the run
  - more than half of product pages failing fails the run
  - "100% of product pages, and at least 5, lack a composition"
  - SMTP retries at 1, 5 and 15 minutes
  - a "disk full" row
  - The table's own preface contradicts four of its rows. The model then
    spent audit effort reporting those contradictions back to the user.
- **First PLAN.md:** 39 tasks plus 5 open-question tasks, with ~40 "Leaves
  open" items. Nearly all of them had obvious answers or didn't affect the
  user. Examples:
  - ruff rule selection
  - `shm_size` value
  - `EMAIL_FROM` display name
  - whether `/healthz` ever returns non-200
  - whether the run lock is held during SMTP backoff
  - how to test a disk-full error
- **The rewrite after the feedback:** 15 tasks in 3 phases, every "Leaves
  open" settled by default. The same FRs are still covered.
- **The "no longer available" case** was raised three times (audit,
  plan, audit correction) for a rule the user considered self-evident.

**Other projects (`grep` of each SPEC.md, 2026-10-09):**

| Project | FRs | SPEC lines | Failure-mode rows |
|---|---|---|---|
| autopantry build 1 | 35 | 939 | — |
| autopantry build 2 | 69 | 3097 | — |
| usecasebot | 17 | 655 | ~25 |
| fashion-bot | 23 | 481 | 13 |
| work-flow | 14 | 113 | 0 |
| file-cleanup | 13 | 132 | 0 |

The "30+ FRs on basic projects" claim holds literally only for autopantry.
The weight pattern holds more broadly. Per row:
- **usecasebot:** 655 lines.
- **fashion-bot:** 23 FRs and a failure matrix for a single daily email.
- **work-flow and file-cleanup:** look proportionate.

## `/audit` specifically

Feedback from the user after fashion-bot's audit:

> *"The audit step in general seems largely pointless - checking if tags are
> correct and being ultra pedantic about wording isn't adding any value. It
> picked up literally one useful detail: the size/item name uniqueness"*

The tally from that audit:
- **Roughly 40 findings**, sorted into:
  - tag mis-assignments (for example "FR-13 is [DERIVED], not [STATED]")
  - quote provenance
  - untagged numeric constants
  - ten "contradictions", mostly wording, such as a preface saying "every
    case" over rows that don't
- **One changed the build:** dedupe was keyed on the item and ignored size, so
  a restock in a newly stocked size would never be emailed. The user
  replied "Dedupe should include size."
- **That finding came from reading the spec for behaviour against the goal**
  ("what would actually happen to me in this case?"), not from any tag,
  provenance or wording check.
- **Two findings were wrong** and had to be retracted once EXPLORE.md was
  read: the "gone item" branch being hypothetical, and colour "needing
  vision". This happened because the command insists on SPEC.md alone.

What it suggests: the value is in walking realistic scenarios through the
spec's behaviour. The provenance-tag audit (the bulk of the command, from
`001`/`003`) produced no build-changing output here. Options range from
cutting `/audit` down to a scenario walk-through, to folding that
walk-through into `/contract` and dropping the step. `001` and `003` closed
partly through `audit.md`, so removing it means checking that their fixes
still bind somewhere.

## The general failure mode

**Every command asks for completeness, and none asks for proportion.** Each
stage is rewarded for finding more, and nothing pushes back:

- **`contract.md`** says Failure Modes are "Network down, API 429/500,
  malformed input, disk full. Mandatory for anything scheduled or
  unattended." That's a checklist, so it gets filled in full, with invented
  numbers, whatever the stakes. fashion-bot's "disk full" row comes straight
  from this line.
- **`plan.md`** (added by `007`): "Leaves open: each decision the task will
  force… anything you leave off gets decided silently." The penalty sits
  entirely on omission, so the model lists every micro-decision to be safe.
  `007` fixed silent consequential decisions by making all decisions loud.
- **`audit.md`**: "List every constraint", "find anything inferred that
  carries no tag", "quote any two passages that can't both be true". Every
  item it finds becomes a question back to the user, even when the answer is
  obvious from the goal. Its one pruning step ("what would be built
  differently if it were removed?") reports and never removes.
- **Nothing in the pipeline states the stakes of the solution.** Without that
  stake ("personal app; a missed day costs nothing"), the model defaults to
  production-service rigour. Retries, thresholds and contradiction-hunting
  are all reasonable for a payments system and noise for a clothes email.

This is the inverse of `003` (scope only ratchets up). That was about
features. This is about rigour, which also only ratchets up, because every
stage adds and none subtracts.

## Candidate fixes

Not prescriptive.

- **A stakes line**, set once at `/brief` from the user's words and inherited
  by every later command. For example: "personal; a missed or wrong day costs
  nothing" vs "money moves". Each command scales its rigour to it.
- **Failure Modes in `contract.md`** become "what the user sees when it
  breaks" rather than a mandatory catalogue. For low-stakes unattended jobs
  that's often one line: any error, then one retry, then a failed email.
- **`plan.md`'s Leaves open** gets a materiality filter: only decisions that
  change what the user gets or sees. Obvious defaults are taken silently and
  listed nowhere. This needs reconciling with `007`, which is why it isn't a
  one-line edit.
- **`audit.md`** gets a "decide it yourself" rule: a finding whose answer
  follows from the stated goal is resolved in the report, not raised as a
  question.
- **A size budget** proportional to the brief (FR count, plan task count),
  where going over it has to be justified.

## Interim

fashion-bot's project `CLAUDE.md` has a "Proportion" section, and its
PLAN.md was rewritten from 39 tasks to 15. Both are project-level fixes, not
binding, and they don't reach any other build.

## Still open

- `commands/contract.md`, `commands/plan.md`, `commands/audit.md` are
  unchanged.
- Whether `/audit` survives as a scenario walk-through, or is folded into
  `/contract` and removed.
- How to reconcile a materiality filter with `007` without bringing back
  silent consequential decisions.
