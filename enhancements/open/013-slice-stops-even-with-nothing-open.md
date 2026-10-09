# Enhancement: `/slice` stops for approval even when nothing is open

**Status: OPEN** (revises the "always stop" decision recorded in `007`)

## Where this came from

fashion-bot build 1, 2026-10-09, task Q1: copy three saved HTML pages into
`tests/fixtures/`. The pre-build checkpoint said "Decisions this forces:
nothing open. Unknowns: none." Then it stopped and waited. The user:

> *"If this slice has literally nothing at stake that needs my input why am
> I needing to approve it"*

## The failure mode

`007` added the pre-code checkpoint so the user could catch silently settled
decisions. Its "Approval fatigue" question was resolved as **always stop**
(user-confirmed 2026-10-01), kept cheap by allowing "nothing open".

But "nothing open" plus a mandatory stop is a round trip that carries no
information. It trains exactly the reflexive approval `007` warned about.
That makes the stop less useful in the slices where it does matter. Since
`011` (fashion-bot), PLAN.md's "Leaves open" lines are mostly "none", so
most slices are this case.

## Candidate fix

The stop becomes conditional. If the checkpoint lists any open decision, a
second unknown, or a proposed split, stop and wait. If there's nothing open,
state the one-line summary and proceed in the same turn. The after-the-fact
reporting (gate output, decisions made, diff) stays unchanged, so nothing
becomes invisible.

## Still open

- `commands/slice.md` line 20 ("Then stop and wait for my go-ahead") is
  unchanged.
- `hooks/verify-before-stop.sh` was adjusted for the pause in `007`. Check
  that it still fires when code lands in the same turn as `/slice`. It did
  before `007`.
