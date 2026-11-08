# Enhancement: /checkpoint is suggested before what the session learned is written down, and clearing the window loses it

**Status: OPEN (fix written, unverified; the measurement is still open)**
(recorded 2026-11-08). Fixed in the same edit as `022`:
- `/build` writes down what was decided in chat before its phase report, and
  ends with "safe to clear".
- `/checkpoint` step 3 checks that Greg's quoted decisions show in SPEC.md.

The replay measurement below hasn't been done. Greg: *"checkpoint shouldn't be suggested
until this check is done. I usually clear the current window to do checkpoint as
it is much easier than opening a second session. I wonder how much undocumented
knowledge I am losing."*

## Where this came from

shortlister, Build 1, end of Phase 2 (T22). I told Greg the next step was
`/checkpoint` in a fresh session, twice. Only when he asked *"Before I clear, is
there any documentation needed that would benefit from the current context"* did
I look, and a good deal existed only in the conversation.

## What happened

What I found and wrote down only because he asked:

- **The spec was out of date on what he gets.** FR-4 still said answers are split
  into 4,096-character Telegram messages. Greg had changed it to a summary plus a
  link to a findings page. FR-14 still described "a ranking"; Greg had replaced it
  with a full buyer's guide ("Let the model actually tell me what it read") and
  approved the result ("superb. This shape works").
- **CLAUDE.md didn't list a new service.** A Caddy page server on port 8096 was
  built and deployed this session. PLATFORM.md had its port row, but the
  project's own "what this adds, and why" list didn't, and its data section
  didn't name `data/pages/` or `data/review-<hunt>/`.
- **PLAN.md's next task didn't know the work existed.** T25 (wire the review into
  the bot) didn't mention the page and summary code, now run by hand from a script.
- **Preferences that apply beyond this repo.** Trial models at their highest
  reasoning effort from the first call. The output of deep research should carry
  everything it found. How to read the 5-hour quota meter, and what a hunt costs
  in it. None of these had a home until I saved them as memories.

BUILD-LOG.md did hold the rulings and measurements, because /build requires them
as they're made. What it doesn't capture is **the documents drifting from what
the user decided in conversation**, and the knowledge that isn't a ruling:
- what was tried and dropped, and why;
- the user's stated preferences;
- operational gotchas found along the way. This session's: code is baked into the
  image, so a running container needs `docker compose cp` or a rebuild; `uv` isn't
  on a non-login shell's PATH; a `pgrep -f` wait loop matches its own command line
  and never ends.

## The failure modes

1. **The handoff has no write-down step.** /build's phase report ends with "the
   next step is /checkpoint in a fresh session", and nothing before that asks what
   the session knows that the repo doesn't. The cold reader is the point of
   /checkpoint, so whatever isn't in the repo is invisible to it by design.
2. **The real workflow is clear-and-reuse, not a second session.** Greg works from
   his phone and clears the window to run /checkpoint. Anything that lived only in
   the conversation is gone for good from that moment. The .jsonl transcript
   survives on disk, but nothing reads it.
3. **Conversation decisions don't flow back into SPEC.md.** /build logs rulings
   it makes itself. A decision the user makes mid-build in chat ("send a summary
   and a link") changes what they get, but nothing requires the FR to be
   rewritten. So /checkpoint would judge the build against a spec the user has
   already overruled.
4. **The agent decides when to stop, but the user notices the loss.** It took
   Greg's question to trigger the check, the same shape as `020`, where the user
   noticed what the process should have.

## Cost

Unknown, which is Greg's point. This session's catch was a spec contradicting
two of his decisions and a missing service. A /checkpoint that read the old
FR-4 would have flagged the summary-and-link reply as a deviation from spec, or
judged T25 against the wrong target. The transcripts of past builds are on disk
(`~/.claude/projects/*/*.jsonl`), so the loss could be measured: replay a phase's
transcript against the docs at its checkpoint commit and count what was decided
or learned in chat but never written down.

## Candidate fixes (not prescriptions)

- **/build, before the phase report:** a write-down step. List what was decided or
  learned in conversation this phase and isn't in the repo, then put each item
  where it belongs:
  - a user decision that changes what they get goes in SPEC.md, with their quote;
  - a new service, port or data folder goes in CLAUDE.md;
  - anything a later task needs goes in PLAN.md;
  - what was tried and dropped goes in BUILD-LOG.md;
  - cross-project preferences go in memory.
  Only then say /checkpoint is next. The report says what was written down.
- **/build, the "next step" line:** written for clearing this window, not opening a
  second session. Say the write-down is done and it's safe to clear.
- **/checkpoint, step 3:** besides the `Ruling:` lines, check that each user
  decision quoted in BUILD-LOG.md appears in SPEC.md where it applies. A
  contradiction is a finding.
- **Write facts and quotes, not conclusions.** A write-down made by the agent
  that built the work is that agent's prose (`001`), so it records what the user
  said and what was measured, not the agent's verdict on its own work.
- **Measure it once:** replay one past phase's transcript against its checkpoint
  commit, to learn how much is usually lost and whether the step above catches it.

## Evidence

- Session transcript: `~/.claude/projects/-home-greg-projects-shortlister/6b127423-2f5a-4db5-a8d6-49aec70a9ef0.jsonl`
  (2026-11-08, from "What's next" to "Before I clear").
- shortlister commit `01f516d` ("Docs: findings pages and the guide shape in
  CLAUDE.md, SPEC FR-4/FR-14, PLAN T25"): everything that was missing before Greg asked.
- `commands/build.md` lines 22–23 and 103: the two places /checkpoint is suggested.
- Related: `001` (the system trusts its own prose), `020` (the user noticed what
  the process should have).
