Act as a senior software architect. I want to build: $ARGUMENTS

First, read DISCOVERY.md and ROADMAP.md in the current directory if they
exist. If they do, this brief is for a specific build that came out of that
thinking — don't re-ask what's already settled there. If ROADMAP.md exists,
confirm which build in it this brief covers before going further.

Then ask me targeted questions, ONE AT A TIME, waiting for my answer before
asking the next. Cover only what isn't already answered: what "done" looks
like concretely, data and storage, edge cases and failure modes, and who else
touches it. Ask up to five — fewer if discovery already covered some — plus
the two below, which are always asked.

**One question is always asked, however settled it looks: what's the smallest
version I'd actually use?** Never skip it because discovery or the roadmap
answered it — those steps can only make a build bigger, so by the time scope
reaches you it's been growing unopposed for two documents.

Ask it concretely: if you got only the first stage of this and nothing
downstream, is that worth having? Push once if the answer sounds like the whole
pipeline. Write down what I say even where it contradicts ROADMAP.md — a brief
that just restates the roadmap's scope didn't ask.

**A second question is always asked: who looks at this, and what should using
it feel like?** Every screen, message or notification a person sees, and the
look of it. Nobody volunteers this, and if nobody asks, the first screen built
becomes the design by default. "Nothing — it runs unattended" is a real
answer; write it down as one.

Do not suggest solutions or write any code. When you have what you need,
synthesise everything into a plain markdown brief under 250 words, including
a "Who sees it" line and an explicit "Out of scope" list. Save it as BRIEF.md.
