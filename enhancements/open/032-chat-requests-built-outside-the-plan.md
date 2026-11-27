# Enhancement: changes asked for in chat are built straight away, outside the plan

**Status: OPEN** (recorded 2026-11-27, deal-hunter Build 1, whole-build review). Greg, 23 Nov: *"inserting tasks
into an existing plan is dangerous"*.

## What happened

- **150 of 300 commits carry no task ID.** Most are log and doc commits. A rough count puts about 45 of them as
  features and design changes built from chat between phases:
  - a new browser library (Patchright, after a 403);
  - delivery read through a store's cart, which changed hard rule 1 ("Cart, postcode only", 15 Nov);
  - rules for two apps sharing one Chrome (P1–P4);
  - hourly OzBargain alerts and Claude call logging;
  - a per-site request safeguard (26 Nov);
  - store pages read in Chrome only (27 Nov).
- **T43 (the web app) became a chain of chat requests:** photos, a Research tab, charts with a script,
  per-variant Best, stock, all-time low, pinned tabs.
- **Phase 7 took a second product mid-phase** ("Fold it into Phase 7"). The full re-read after its tasks were
  inserted found contradictions across the plan's shared rules.
- None of this went through /plan's checks (expensive automation, order rules, the human surface), and none of it
  counted toward phase size.

## The failure modes

1. **/build has a route for a task but none for a request.** The fastest path is to build it.
2. **Inserting a task leaves the plan's shared rules unchecked:** its settings, tables and order.
3. **Out-of-plan work is invisible to the checkpoint as scope.** Phase size and the worth-it step can't see it.

## Candidate fixes (not prescriptions)

- **P1: A chat request in /build becomes a written task** (or a next-build item, per `029`) before any code. A
  one-line fix to the current task stays inside that task.
- **P2: Inserting a task runs /plan's checks on it,** plus a re-read of the plan's shared rules in the same step.
- **P3: The checkpoint counts commits with no task ID** and lists what they changed in behaviour.

## Evidence

- deal-hunter: `git log --format=%s | grep -cvE '^T[0-9]'` (150 of 300).
- BUILD-LOG.md: chat features after Phase 4, the contention design, Bing Lee 403 and Patchright, "Cart, postcode
  only", T43, the 23 Nov re-read, 26–27 Nov.
- Related: `029` (scope), `007` (open decisions settled silently).
