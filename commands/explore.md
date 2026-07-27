Read BRIEF.md. Don't propose a design, pick a shape, write a spec, or code.

## 1. What kinds of tool could solve this?

From the brief, name the categories that could carry the job — task managers,
note apps, schedulers, whatever fits — including ones I probably won't pick.
Then the two or three leading candidates in each.

## 2. What do they actually do now?

Go and look: current feature pages, API docs, pricing tiers, changelogs.

**Never answer from recall.** If you're writing what a product does without
having just looked, stop and look.

For each candidate:
- Does the capability exist, and on which tier?
- Reachable by API, or UI only? This usually decides the architecture.
- What does the cheapest usable tier really allow?
- What does the real data contain?

Mark every finding **documented** or **observed working**.

Never write "no X can do Y" without evidence. Concluding a category can't do
something standard is how a build invents a subsystem to replace a checkbox.

## 3. Claims about model judgment

List anything resting on a model reliably classifying text, detecting intent,
or scoring relevance. No looking settles these — they're always BETs. For
each, name the smallest real test, and try to break the claim against one
unflattering example first. If it breaks, ask whether the mechanism should
exist, not what special case would patch it.

## 4. Stop and give me the short list

Rank by consequence. Hand me only the critical few to confirm myself, each as
a specific link or action — not the whole list. Then wait.

## 5. Write EXPLORE.md

Four verdicts:

- **CONFIRMED** — checked. Say whether documented or observed.
- **WRONG** — I believed it, it's false. Record what's actually true.
- **BLOCKED** — checkable, unchecked. Nothing assuming the answer proceeds.
- **BET** — unknowable without building. State what being wrong costs.

Only a BET if checking is impossible, not inconvenient. Needs-an-account,
needs-a-signup, slow-to-arrive are all BLOCKED. Writing a justification for
assuming a checkable thing is itself the error.

Per BET: survivable (note it, proceed), invalidating (smallest test built
first, everything else faked), or fatal and untestable (say so — that's a
decision about whether to start).

End with what this rules in and out: candidates still viable, and each one
eliminated with the finding that killed it. /design starts from that list;
/contract and /plan also read this file.
