Read BRIEF.md. Don't propose a design, pick a shape, write a spec, or code.

Scale the effort to the brief. A small personal app with an obvious shape
needs a short EXPLORE.md, not a market survey.

## 1. What do I already run?

Read `~/projects/platform/PLATFORM.md`. For each part of the brief — getting
data in, storing it, scheduling, browsing, notifying, any model call, the
screen — say which shared service or convention already covers it, and which
existing project under `~/projects` already does something like it.

Then ask it whole: is anything I already run, here or on another box, doing
this entire job, even under another name? Mapping parts onto pieces hides a
tool that already does all of them.

This is where to start, not where to stop. The platform is the default
because every app built on it is one less thing to keep alive, not because
nothing better exists.

## 2. What else could solve this?

If DISCOVERY.md has an **Existing tools** section, start from it: its
searches and candidates are already done. Read its searches against the rules
below and run only what's missing: an angle not taken, a category not
searched, the topic-free version if every search used the brief's words, or
anything that changed with a reframe since. Then carry its live candidates
into section 3. With no such section, do the whole search here.

First write the job in one sentence with the brief's domain taken out
("research a question across many web sources and write a cited report", not
"find the best vacuum deal"). Search both: the domain version and the generic
one. The brief's vocabulary hides any category it doesn't use.

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

A candidate that lacks the domain-specific parts isn't out for that alone.
Ask whether it could do the core with those parts added, and compare the cost
of adding them against the cost of building everything else.

A "nothing fits" verdict lists, beside it, the literal queries it rests on and
names the most general one. If every query uses the brief's own domain words,
the verdict isn't allowed yet: run the generic one first.

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
