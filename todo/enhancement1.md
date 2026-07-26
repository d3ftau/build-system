# Enhancement: the pipeline over-trusts its own earlier output

## Where this came from

Session on `task-extractor` (personal decision-mining tool). Ran the full
chain: `/discovery` → `/roadmap` → `/brief` → `/design` → `/contract`, then
iterated on the resulting SPEC.md directly with Greg over several turns. Two
significant design errors surfaced only during that iteration — not during
`/design`, not during `/contract`, not on request — and both required Greg to
push back explicitly, in one case twice, before I actually dropped the flawed
mechanism rather than patching around it.

Greg's framing, verbatim: the process was "leaning far too hard on prior
documents as sources of truth," and this iteration step is "the first place
those become real" — which is exactly when a bad decision made two skills ago
finally gets checked, and by then it's had two documents' worth of confident
prose reinforcing it.

## The general failure mode

1. An earlier stage (`/design`, sometimes `/roadmap`) produces prose reasoning
   about how something will behave — often a prediction about model
   judgment, not a fact about the world.
2. That reasoning reads as settled analysis, because it's written in
   declarative sentences in a document titled DESIGN.md.
3. A later stage (`/contract`) formalizes it into structure — a schema field,
   a matching rule, a gate — and tags it `[STATED]` because it's traceable to
   that document.
4. The tagging system rewards traceability, not correctness. "Cites a source"
   and "is actually right" get treated as the same property.
5. Once the claim is structural (a field with a `CHECK` constraint, a
   validation rule, a table), there's now sunk cost in defending the
   mechanism, not just the idea. When challenged, the instinct is to patch
   the mechanism (add a new case, a new enum value) rather than ask whether
   the mechanism should exist at all.
6. The actual test — does this hold up against a concrete example — doesn't
   happen until a human reads the formalized requirement and tries to picture
   it working. That's often several documents and a fair amount of writing
   later.

## Concrete example 1: the evidence-span requirement

`/design` produced, in DESIGN.md's "hard part" section:

> "The load-bearing signal is user-turn endorsement of a specific, actionable
> course of action... every candidate must carry the evidence span that
> justifies it."

This is a *prediction about what a classification signal looks like in chat
transcripts* — dressed as an architectural conclusion. It was never tested
against a real example before being written down.

`/contract` then turned it into a hard requirement: every candidate needed a
`evidence` field that was a **verbatim substring** of a user turn, checked
with a literal string match, with a dedicated rejection reason
(`evidence_not_in_user_turn`) for anything that didn't match.

Greg's first pushback: a conversation about quilt types that clearly implies
"go buy a quilt" has no sentence anywhere that states that decision. I
responded by adding an `endorsed` / `inferred` split — two categories, one of
which relaxed the evidence requirement. This **kept the flawed mechanism
alive** by giving it an escape hatch, rather than questioning whether
"evidence must be a verbatim span" was the right idea at all.

Greg's second, more direct pushback: real endorsement is carried by
*trajectory across a sequence of turns* — a comparative question ("what's the
best way to fix a patchy lawn") giving way to an operational one ("how much
ground prep before laying turf"), an option silently dropped, a procurement
question ("hire or buy a rotovator"). None of that is a substring anyone
said. Only at this point did the verbatim-match idea get retired entirely,
replaced by turn-index citations with a bounds check instead of a text match.

**The gap:** between the quilt example and the trajectory explanation, I had
a full turn where I built out structure (a `basis` enum, a differentiated
matching rule per basis, a dropped-candidate reason called
`basis_mismatch`) in service of an idea that was still wrong. The first
counterexample should have been enough to question the mechanism itself, not
prompt a patch to it.

## Concrete example 2: the ClickUp nag capability (contrast case)

Separately, DESIGN.md asserted: "no task app on any tier does repeat-until-done
nagging... ClickUp['s]... notifications are pull, not nag." I repeated this
claim uncritically in conversation and carried it into a spec rewrite.

Greg corrected it in one line: "ClickUp supports push nag features - which
was a miss on your part." I searched, confirmed ClickUp does support
recurring reminders (available on the free plan, can recur forever, push to
mobile), found the actual limitation (no API access to reminders — the real
constraint, just not the one DESIGN had claimed), and corrected both DESIGN.md
and SPEC.md within the same turn, with no back-and-forth needed.

**Why this one didn't repeat the pattern:** it was an external, checkable
fact. "Let me go verify a claim about a third-party product" doesn't touch
anything I'd reasoned into or built. The quilt-example correction was
different in kind — it was a claim about how well a model can classify
ambiguous text, which is not independently checkable the same way, and which
I had personally elaborated into schema and validation logic. I corrected the
verifiable external fact immediately and defended the unverifiable internal
judgment call until pushed twice.

## What this suggests, without prescribing the fix

Greg explicitly did not want the fix scoped to "add this exact check for this
exact failure" — the deeper issue is generalizable and he wants to design the
skill update deliberately, in its own session. Some observations that might
be useful raw material for that session, not proposals:

- The three tags (`[STATED]`, `[DERIVED]`, `[ASSUMED]`) currently collapse two
  different things under `[STATED]`: "the user explicitly decided this" and
  "an earlier document asserted this while reasoning toward something else."
  Those have very different reliability, especially when the assertion is a
  prediction about model behavior rather than a fact about the world or an
  explicit human choice.
- `/audit` already exists as a fresh-eyes review pass, and its current
  instruction — "quote the exact line in SPEC.md that establishes it" — is
  precisely the traceability-as-correctness pattern. It would quote the
  evidence-span requirement as "established" by DESIGN.md and move on,
  because DESIGN.md does contain a sentence that establishes it. Whatever the
  fix is, `/audit` is a candidate place for it, since its whole purpose is to
  catch what earlier stages missed.
- The self-correction asymmetry (fast on checkable facts, slow on judgment
  calls I'd built structure around) is probably not fixable by a single
  instruction added to one skill. It might be more about how much structure
  gets built *before* a design claim about model behavior is deliberately
  marked as unverified and cheap to discard, versus quietly folded in as
  settled.
- Any fix probably needs to survive being applied by a fresh session with no
  memory of this incident — i.e., it needs to change what the skill actually
  asks for, not just be a lesson Greg or I personally remember.

## Where this lives for now

Recorded as project-scoped memory on `task-extractor`
(`~/.claude/projects/-home-greg-projects-file-cleanup/memory/feedback_spec_process_over_deference.md`)
so it isn't lost, pending the dedicated skill-update session.
