# Enhancement: /explore searches the project's framing, not the job, and "nothing fits" licenses a build

**Status: OPEN** (recorded 2026-11-07). Greg: *"How did explore miss this? It's
literally the entire point of the step"*, then *"Yes this is a bad failing"*.

## Where this came from

shortlister, Build 1 (research a purchase, reply with tiered picks). Explore
ran on 2026-11-06. Phase 1 was built and reported on 2026-11-07. Greg then
rejected its results, and after a day redesigning the research loop, said it
looked like a solved problem and asked why we were inventing it from scratch.

## What happened

`EXPLORE.md` said "Off-the-shelf open source: nothing fits". The searches behind it:

- Web: `AI shopping research assistant`
- GitHub: `shopping agent`, `product research agent`, `ozbargain`

"Deep research" was never searched. The first `gh search repos "deep research
agent"` on 2026-11-07 returned Alibaba-NLP/DeepResearch (20k stars) and
dzhng/deep-research (19.9k), and related searches found
langchain-ai/open_deep_research (12.7k) and jordan-gibbs/hyperresearch. Local
Deep Research reports results on Qwen on one GPU, close to Greg's hardware.
Hermes, already running on his VPS, ships a `grounded-citations` skill that does
the quote check I had just proposed building.

Hermes itself was assessed only as a front door and as the home of the context
files, never as a research engine, though it was already doing this kind of job.

So the build wrote its own gatherer and evidence pipeline. That was then
redesigned in conversation, step by step, into something these tools already are.

## The failure modes

1. **The search terms inherit the project's framing.** The rule says to name the
   categories of tool that could carry the job, but the categories came from the
   brief's vocabulary (shopping). The generic job underneath ("research a question
   across many web sources and write a cited report") was never stated, so its
   whole category stayed invisible. `010` made OSS its own search, and this run
   obeyed it: two searches, wrong words. Following the rule didn't help.
2. **Whole-job rejection.** Candidates were eliminated for lacking the
   domain-specific parts (OzBargain, cashback, context files). Nobody asked
   whether a general tool could do the core and take those parts as add-ons. The
   comparison that matters is the cost of adding the missing piece against the
   cost of building everything else.
3. **The verdict outlives its evidence.** "Nothing fits" reads as a finding about
   the world. It was only a finding about three queries. /spec and /plan built on
   it, and nothing downstream prompted anyone to reopen it.
4. **Tools already in use aren't assessed for the job itself.** /explore step 1
   maps the brief's parts onto existing projects, so Hermes got slotted in by part.
   Nothing asked "is something I already run doing this whole job?"
5. **Late signal, no re-check.** Nothing in /build or /checkpoint asks "does this
   already exist?" again when a build's core starts being redesigned.

## Cost

Phase 1's research pipeline and a day of redesign. The OzBargain archive and
harvest are unaffected, because none of these tools has that data.

## Candidate fixes (not prescriptions)

- **/explore:** state the job in one sentence with the domain removed, and search
  that as well as the domain version. Record both.
- **/explore:** for each elimination, ask whether the missing part could be added,
  and whether that's cheaper than building the rest.
- **/explore:** a "nothing fits" verdict lists its literal queries beside it and
  names the most general one tried. If that query contains the project's domain
  words, the verdict isn't allowed yet.
- **/explore step 1:** ask whether anything already running does the whole job,
  not only which piece covers which part.
- **/stuck or /checkpoint:** when the core approach is being redesigned, re-run the
  existence search with the new understanding of the job.

## Evidence

- `~/projects/shortlister/EXPLORE.md`, section 2–3 and "Eliminated" (corrected
  2026-11-07; the original is in git, commit `775323f`).
- Session transcript: `~/.claude/projects/-home-greg-projects-shortlister/6b127423-2f5a-4db5-a8d6-49aec70a9ef0.jsonl`.
- Related: `010` (OSS as its own search: the same family, one level up) and `017`
  (each snag adds machinery instead of questioning the goal).
