# Enhancement: claims are accepted without checking they are the kind of claim that can be true

**Status: DONE** — all four candidate fixes in `commands/slice.md`; general form in `~/.claude/CLAUDE.md`.

## Where this came from

Autopantry Build 1. Four instances across the build, which only look like one
failure mode once they are next to each other.

**1. An enumerability claim that needed the thing it was replacing.**
`PLAN.md` specified an "implausibility check" to catch bad shelf-life estimates
and justified it as code rather than a model call: *"Implausibility is
enumerable — perishable terms against a long shelf life, a chilled item in a
dry location — so it is code."* The user: *"who is deciding that yoghurt in the
pantry looks wrong?"* The rule needs to already know yoghurt belongs in the
fridge, which is precisely what the model call exists to determine. The same
file's `enrichment.ts` carried an `LLM-JUSTIFIED` comment stating those rules
are *not* enumerable across a supermarket's catalogue. Both claims were written
by the same agent, in the same build, and could not both hold.

**2. A bug reported from a repro that could not occur.** A "significant, real
bug" was reported — the pantry going stale after a post-migration order
revision — evidenced by a live test calling the RPC with a manufactured
timeline. The user: *"how is this even a bug? you can't amend an order after
it's been picked up and migration happens after collection time."* The test
proved the *code* would permit the call, not that the *retailer* could ever
produce it. Withdrawn.

**3. A test input that had to be fabricated.** The `UNKNOWN` substitution
outcome had no reachable case in any of seven real Coles fixture emails; a
synthetic input was constructed to cover it. It was eventually deleted as a
parser failure recorded as if it were a data value — the fabrication was the
evidence, and it was read as a coverage task instead.

**4. Verification that only exercised the intended direction.** Moving a pantry
item fridge → freezer was built, tested, and reported working. Freezer → fridge
returned a 500 on a check constraint, and a location change recomputed dates
from the original delivery reference so thawing produced a use-by already in
the past. Both were found only because the reverse was tried later.

## The general failure mode

The tracker's README already names the thread for `001`/`002`/`003`: *"the
system trusts its own prose. A claim becomes true by being written down
confidently in a document with an authoritative title."* This is the same
thread one level in — **a claim becomes true by being asserted confidently
within a session, and the evidence gathered for it tests something adjacent to
what the claim actually says.**

In each case evidence *was* produced. That is what makes it hard to catch:

| Claim | Evidence produced | What it actually established |
|---|---|---|
| "this rule is enumerable" | a plausible list of rules | that rules could be written, not that their inputs were available |
| "this is a real bug" | a passing repro | that the code permits the call, not that reality produces it |
| "this branch is covered" | a green test | that a fabricated input works, not that any real one reaches it |
| "the move works" | a passing manual run | that one direction works |

Each is a substitution of a checkable proxy for the actual claim, and each
proxy is close enough to pass unexamined. The existing `/explore` step has
exactly the right instinct for this at the *research* stage — "never write 'no
X can do Y' without evidence", the CONFIRMED/WRONG/BLOCKED/BET verdicts, "only
a BET if checking is impossible, not inconvenient" — but nothing carries that
discipline into implementation and verification, where the same substitutions
recur.

Note also the asymmetry in the standing rule this violates. `~/.claude/CLAUDE.md`
says *never use an LLM for work that code can do*, with a stated test ("can I
enumerate the rules?"). There is no inverse — nothing warns against claiming
code can do work that needs the model — and the inverse error is the more
dangerous one, because it sounds like the disciplined answer and so survives
review.

## Candidate fixes

- **Extend the enumerability test to be two-directional.** Before writing that
  something is enumerable, name the inputs the rule reads and check that none
  of them is the thing being inferred. Where a check genuinely needs judgment,
  the honest options are a *narrow* enumerable subset or an internal-consistency
  test needing no outside knowledge — never a second model call auditing the
  first, since the auditor has no better information than the original.
- **Before reporting a failure, state the precondition and where it was
  checked** — against the real upstream system, not against the code. A repro
  demonstrates permissibility; reachability is a separate claim needing
  separate evidence.
- **Treat a fabricated test input as a finding.** If no real input produces the
  state, the default hypothesis is that the branch models something that cannot
  happen. Write that down instead of writing the synthetic test.
- **Verification should exercise the inverse of any state change**, not just
  the direction the task was written in.

## Open, not resolved here

- Where any of this binds. `/slice` is the obvious host for the verification
  items, but the enumerability rule belongs next to its existing half in
  `~/.claude/CLAUDE.md`, and the reachability rule may be a hook on the
  reporting step rather than prose anywhere.
- Whether the existing `llm-call-guard.sh` hook — which already forces a
  written justification above every model call — could be inverted to demand
  the same for a claim of enumerability. It would need something to trigger on,
  and "code that was written instead of a model call" is not detectable.
- Whether this and `001` are ultimately one enhancement. They are the same
  shape at different scopes, and `001`'s note that provenance-tagging failures
  are "probably one fix" may extend here.

## Still open

- Nothing has changed in any command, hook, or CLAUDE.md.
- All four instances were caught by the user, not by the system.

## Implementation status (2026-10-01)

- **Two-directional enumerability** — `commands/slice.md`, `commands/design.md`,
  `commands/contract.md`: name the inputs a rule reads; if one is the thing
  being inferred, it isn't enumerable.
- **Reachability before reporting a bug**, **an invented input is a finding**,
  **test the reverse of every state change** — `commands/slice.md` "While
  building".
- `~/.claude/CLAUDE.md` (user-approved, 2026-10-01) — the inverse of "never use
  an LLM for work code can do", plus an "Evidence must test the claim itself"
  section that also covers `009`'s second instance: a rule the agent wrote
  earlier in the session is not authority. That's the only place that reaches
  conversational work outside the pipeline. It's outside this repo, so it
  isn't in git here.
- **Not done, deliberately:** no hook. "Code written instead of a model call"
  and "a bug report" have nothing for a hook to trigger on.
