Read BRIEF.md. Don't propose a design, pick a shape, write a spec, or code.

Scale the effort to the brief. A small personal app with an obvious shape
needs a short EXPLORE.md, not a market survey.

## 1. What do I already run?

Read `~/projects/platform/PLATFORM.md`. For each part of the brief — getting
data in, storing it, scheduling, browsing, notifying, any model call, the
screen — say which shared service or convention already covers it, and which
existing project under `~/projects` already does something like it.

This is where to start, not where to stop. The platform is the default
because every app built on it is one less thing to keep alive, not because
nothing better exists.

## 2. What else could solve this?

Name the categories of tool that could carry the job, then the two or three
leading candidates in each. Two separate searches, never one: **commercial
products**, and **GitHub / open-source projects** (PyPI, npm, archives,
datasets). Neither is a fallback for the other. For open source, star count
and last-commit date are the first filter. Don't inherit DISCOVERY.md's list
as complete.

A candidate that needs stack the platform doesn't have stays in the running.
Say what the new piece is and what it costs to keep alive — another container,
another login, another thing to update — so the trade is visible, not hidden.

## 3. What do they actually do now?

Go and look: current feature pages, API docs, pricing tiers, changelogs.
**Never answer from recall.** For each candidate that's still in the running:

- Does the capability exist, and on which tier?
- Reachable by API, or UI only? This usually decides the architecture.
- What does the cheapest usable tier really allow?
- What does the real data contain?

Mark every finding **documented** or **observed working**. Never write "no X
can do Y" without evidence — concluding a category can't do something
standard is how a build invents a subsystem to replace a checkbox.

## 4. Claims about model judgment

List anything resting on a model reliably classifying text, detecting intent,
or scoring relevance. No looking settles these — they're always BETs. For
each, name the smallest real test, and try to break the claim against one
unflattering example first.

## 5. Stop and give me the short list

Rank by consequence. Hand me only the critical few to confirm myself, each as
a specific link or action. Then wait.

## 6. Write EXPLORE.md

Four verdicts:

- **CONFIRMED** — checked. Say whether documented or observed.
- **WRONG** — I believed it, it's false. Record what's actually true.
- **BLOCKED** — checkable, unchecked. Nothing assuming the answer proceeds.
- **BET** — unknowable without building. State what being wrong costs.

Only a BET if checking is impossible, not inconvenient. Needs-an-account,
needs-a-signup, slow-to-arrive are all BLOCKED.

Per BET: survivable (note it, proceed), invalidating (the plan proves it
first, with the smallest real slice of code), or fatal and untestable (say so —
that's a decision about whether to start).

End with what this rules in and out: what the platform covers, candidates
still viable with any new stack they'd add, and each one eliminated with the
finding that killed it. /spec starts from that list.
