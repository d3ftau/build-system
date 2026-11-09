# Enhancement: the /checkpoint report can't be acted on from a phone

**Status: OPEN (fix written, unverified)** (recorded 2026-11-08). Greg: *"Checkpoint
command gives too much detail to address at once, with inconsistent numbering
which makes it hard to address. I'm often unclear what I need to decide on as
some findings are presented as facts with no ask for decision even though they
appear to need one. Findings are written in tech speak … The step is coming up
with a lot of really useful information but then often only says a couple of
tiny changes are required, after calling out numerous deficiencies."*

## The failure modes

1. **Numbering collides.** Sections are numbered and findings are numbered
   inside them. the-wolf Phase 3: section "2. Code review" held findings 1 and
   2, and Greg replied "2. Do this". shortlister Phases 1–2: findings 1–8 were
   numbered, 7 minor items weren't, so they couldn't be pointed at.
2. **Decisions are filed as facts.** shortlister: "Hunts 3–6 are stuck" (Greg
   had to say "kill all current hunts"), "Lucy (FR-1) gets no reply" (a broken
   requirement, filed as minor), "I'd decide T29–T30 at the Phase 3 checkpoint"
   (a deferral nobody asked for), the archive that stopped growing. None asked
   anything.
3. **Written for the builder.** `review.uncited()`, `corpus._never`,
   `walk_nodes`, `_google_refused`, `log_cursors`, "process groups".
4. **The verdict undersells the findings.** shortlister: "Two small fixes
   before T25. Everything else holds", over 8 ranked findings. Greg read them
   and called a re-plan. The command's three grades gave "worth fixing" and
   "minor" no fate, and the verdict counted only the top grade.

## Fix (in `commands/checkpoint.md`, 2026-11-08)

- Every finding gets a fate: Fix `F`, Decision `D`, Later `L` (named task),
  Note `N`. Those labels are the report's only numbering. A fact that implies
  an action is a decision. Anything that changes what Greg gets is never a note.
- Items are written in plain words, starting with what he'd notice, with no
  code names.
- The verdict comes first and counts every fate. Any fix means at least "fix first".
- The full evidence goes in a committed `CHECKPOINT.md`, sent to the phone.
  `/plan` reads it, which also keeps it past a window clear (`021`).
- Decisions are asked through AskUserQuestion (a tap-to-answer survey), with
  the recommendation first and the verdict as the last question.

## /build's phase report had the same failures

Read on 2026-11-08: the-wolf Phase 3's report, and Greg's replies to all 21
phase reports in 9 projects.
- **A question buried in the text:** "The three commits aren't pushed. Say if
  you want them pushed."
- **Rulings with no ask:** each ends "If wrong: …", such as a hold lasting up
  to 5 hours too long, but nothing asks whether to keep it.
- **An untested path with no action:** "Not tried for real: no real reading
  has reached 90%." It took /checkpoint to say the drill should be re-run.
- **The next step not clear:** "Should I run checkpoint?" (cart-fill), "Is
  checkpoint next?" (fashion-bot).
- **Gaps in understanding:** "Explain what health checks does?" (backrest),
  "Is the fix then re-run a two phase approval process with taps for each?"
  (the-wolf).
- **Numbered sections**, and 3,000–6,800 characters on a phone.

Fix in `commands/build.md`, 2026-11-08, with Greg's choices from a survey:
- Items are labelled `W` (works now), `R` (ruling) and `U` (not tested for
  real), with no numbered sections.
- **Every ruling is asked keep-or-change in a survey** (Greg chose "ask on
  all" over only the ones he'd feel). A changed ruling is made, checked and
  logged before the handoff.
- Other asks (push, costs, manual steps) go in the survey too.
- Checks are one line in chat. The raw `make check` tail goes in
  BUILD-LOG.md, and failures are shown in full.
- The last line is exactly what to type next.
- `/checkpoint` step 3 follows up `U` items that are still untested.
- 021's write-down step went into the same edit.

## Still open

- **Verify** on the next real /build phase end and /checkpoint: are the
  labels used consistently, is every action-implying fact asked, and do the
  survey answers come through over remote control?

## Evidence

- `~/.claude/projects/-home-greg-projects-shortlister/935658dd-4adb-4fe1-ab61-93c9a2e03ef3.jsonl`
- `~/.claude/projects/-home-greg-projects-the-wolf/320b3bbd-e759-4143-aaed-b02ddf89f45b.jsonl`

## It wasn't only these two commands (2026-11-09)

deal-hunter's /spec reply had a "Five things that would bite you" list
numbered 1–5, then "My assumptions: keep or cut each" numbered 1–15. The one
real choice ("This is the one that really needs your call") came at #15, after
14 items costing "none". Then came 3 unnumbered CLAUDE.md items to strike.
usecasebot's last reply buried a "Decision for you" at the end of the text.
Greg: *"This problem is repeating everywhere."*

The general rule now lives in `~/.claude/CLAUDE.md`, "How to work with me",
so every session gets it, inside the pipeline or not:
- **Anything to answer goes in AskUserQuestion**, real choices first; plain
  defaults are grouped into one keep-all question.
- **One labelling scheme per message**, with letter prefixes, and no numbered
  headings.

Commands that told the agent to write a numbered list for Greg to answer now
say survey instead:
- `spec.md` §4: B/A labels, real choices first, defaults in one question;
- `plan.md` §1: decisions asked as a survey, not "reply defaults";
- `oneshot.md`: rulings and push asked as a survey;
- `stuck.md`: the choice between the two approaches;
- `brief.md`: a survey where the answer has options you can name.
