This runs in a brand-new session. If this conversation has history above this
message, stop and tell me to start a fresh one — the point is a reader who
didn't build it and hasn't inherited its assumptions.

Read PLAN.md, SPEC.md and CLAUDE.md, and BUILD-LOG.md and DESIGN.md if they exist.
A build started before 2026-10-11 has no BUILD-LOG.md; its decisions are in the
plan's and spec's own notes, and you read those instead.
The phase being checked is everything above the first unticked `/checkpoint`
line in PLAN.md, back to the previous checkpoint. Every task in it passed its
own gate on the code as it was then; step 5 asks whether that still holds.
The question is
**whether what this phase built is good enough to build the next phase on.**

Scale this to the app. A personal app gets judged on whether it does the job
for me, not on production polish.

1. **Real output.** For each thing the phase built that produces output, run
   it on real data — the project's actual inputs, not test fixtures — and look
   at what comes out. Measure every **Fails if** threshold PLAN.md set. Where
   output has a measurable quality and no threshold was set, measure it anyway
   and say what number you'd consider failing. Show samples, including the
   worst ones. A rate of "returned something" is not a rate of "returned the
   right thing".

2. **Read the code fresh.** Review this phase's diff (`git log` and
   `git diff` from the previous checkpoint) as a reviewer who didn't write
   it. Grade every problem by what it does to me using the app — not by
   whether the spec mentions the case. A spec's silence isn't permission for
   something to break in a way any reasonable person would expect to work.
   Grade each as **breaks it for me**, **worth fixing** or **minor**. The
   grade sets its fate in the report: anything that breaks it is a fix or a
   decision, never a note.

3. **The rulings.** Read BUILD-LOG.md's `Ruling:` lines for this phase (or,
   for an older build, the decisions recorded in PLAN.md and SPEC.md notes). Any
   you'd have decided differently, or that quietly changed what I get, name
   them. Each decision of mine quoted in BUILD-LOG.md should show in SPEC.md
   where it applies; a SPEC.md that still says otherwise is a finding. So is
   a `U` item (not tested for real) from /build's report that is still
   untested.

4. **Patterns no task decided.** Shapes several tasks share — where work
   happens, what gets trusted, how failure is handled. Decided anywhere, or
   inherited task to task? Would you choose it starting fresh?

5. **Is the rest of the plan still true?** For each remaining task, does it
   still rest on decisions that hold? Which earlier passes does it rely on,
   and has anything they ran on changed since? If the real run happens once,
   does the plan still end with the full rehearsal on frozen code? A plan or
   re-plan without it is **re-plan**. Check CLAUDE.md's hard rules for
   anything added mid-build by the agent rather than by me.
   If this phase redesigned the build's core approach, re-run /explore's
   existence search (domain and generic, commercial and open source) with the
   new understanding of the job. A redesign often lands on something that
   already exists.

6. **Is it still worth it?** A challenge, every checkpoint, to what's built
   and what's still to come, limited to the expensive automation: the pieces
   that brought a new secret, permission, cross-machine link, mode or
   rehearsal rig, or that exist to fix a problem another piece created.
   Ordinary code isn't weighed. For each, the effort it has taken and will
   take (building, testing, upkeep, and the problems it caused that needed
   solving in turn) against what it saves me over its life (the manual
   step's length times how often it happens) or the mistakes it prevents.
   The chain of fixes is the warning sign. If the remaining plan rests on
   one, the verdict is **re-plan**, not proceed with trims. If I've asked
   whether this is over-engineered, answer from this step and say plainly
   what was over-built, before what to keep.

7. **Can a person use what exists?** Re-run PLAN.md's human surface table
   against the code as it is now. If this phase was meant to end deployed,
   check it's running, comes back after a restart, and that a failed run
   would reach me.

## The report

Report only. Don't fix code or edit PLAN.md. I read and answer this on my
phone, so the work above is thorough and the report is short.

**Every finding gets a fate**, and the report is sorted by fate, not by step:
- **Fix** (`F1`, `F2`…): you recommend fixing it before the next phase.
- **Decision** (`D1`, `D2`…): it needs me. That covers a real choice, anything
  that changes what I get, and any fact that implies an action (stale records
  to clear, a stalled job, a requirement that's quietly broken). If you'd
  write "I'd decide this later", that's a decision now: ask whether to defer.
- **Later** (`L1`…): belongs to a named later task. Name it.
- **Note** (`N1`…): true, and nothing to do. If a note suggests an action,
  it's a decision instead.

A finding that changes what I get, or what a later task needs, is never a
note. These labels are the only numbering in the report. Sections and
headings carry no numbers, so a reply like "F2 skip" can't be misread.

**Write each item for someone who didn't build it.** Start with what I'd
notice using the app, then the cause in plain words. No function, variable or
file names in the item itself; when a term is unavoidable, explain it in a
clause the first time. One to three sentences each.

**The verdict comes first and counts everything**: proceed, fix first, or
re-plan (which tasks), then "N fixes, N decisions, N later, N notes". It
follows from the items. Any fix means at least fix first. If decisions could
change the plan's shape, say so in the verdict, not after.

**Detail goes in a file.** Write the full evidence (measurements, samples,
worst cases, the code review, rulings, what wasn't checked) to `CHECKPOINT.md`
in the project, replacing the previous one, and commit it. Organise it under
the same labels so "more on D2" has one place to look. Send it to me with
SendUserFile if that tool is available. The chat message holds only the
verdict and the items.

**Then ask the decisions as a survey** with AskUserQuestion, after the
message:
- One question per decision, with my options and your recommendation first,
  marked "(Recommended)". Each question stands alone: say what it's about
  in it, because the dialog may hide the report.
- One question for the fixes: "Fix F1–F3 before the next phase?", with
  options all / none / let me pick. If I pick, ask which, multi-select.
- At most 4 questions a call. Ask the rest in further calls.
- The verdict is the last question: proceed, fix first or re-plan, with
  your verdict first.

When I've answered, tick the `/checkpoint` line and write my decision under it
in one line, with the item labels I approved.
