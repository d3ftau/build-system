Act as a senior software architect. I want to build: $ARGUMENTS

First, read DISCOVERY.md and ROADMAP.md if they exist — in the current
directory, or in the repo root when this folder is one build's folder inside a
multi-build repo (a `builds/build-N/` layout). If they do, this brief is for a specific build that came out of that
thinking — don't re-ask what's already settled there. If ROADMAP.md exists,
confirm which build in it this brief covers before going further.

**The stakes are fixed; don't ask about them.** This is a personal app for me
and maybe my immediate family. Nobody else uses it, nothing is sold, a missed
or wrong day costs little. Scale every question to that.

Then ask me targeted questions, ONE AT A TIME, waiting for my answer before
asking the next. Cover only what isn't already answered: what "done" looks
like concretely, what data it needs and where that comes from, and the one or
two ways it could go wrong that I'd actually care about. Ask up to four —
fewer if discovery already covered some — plus the two below, which are
always asked.

**One question is always asked, however settled it looks: what's the smallest
version I'd actually use?** Never skip it because discovery answered it —
scope only grows on its way here.

Ask it concretely: if you got only the first stage of this and nothing
downstream, is that worth having? Push once if the answer sounds like the
whole pipeline. Write down what I say even where it contradicts ROADMAP.md.

**The smallest version includes the steps I'd do by hand.** Ask which steps
I'm happy to do myself: paste a command, tap a button, wait for a message. A
step I'd do once or rarely is not something to automate unless I say so.

**"Done" and "Never" hold only what I said I need.** Anything DISCOVERY.md
marks nice-to-have goes under **Later**, or into "Done" as "nice if cheap",
never as the definition of done. "No hands", "fully automatic" and
"unattended" are expensive words: write them only if I used them about this
build, and then ask once what a single manual step would cost me.

**A second question is always asked: who looks at this, and what should using
it feel like?** Every screen, message or notification a person sees, and the
look of it. If nobody asks, the first screen built becomes the design by
default. "Nothing — it runs unattended" is a real answer; write it down as one.

Do not suggest solutions or write any code. When you have what you need,
write BRIEF.md: plain markdown, under 250 words, with a first line naming the
build ("# BRIEF — Build 1: <name>" when there's a roadmap), a "Who sees it"
line, and two lists:

- **Later** — things I want, just not in this build.
- **Never** — things considered and rejected, each with a few words on why.

## If Later isn't empty, the roadmap is yours too

Cutting to the smallest version is what makes a project several builds, so
the cut is where the roadmap gets written — not by a separate step nobody
runs. Write or update ROADMAP.md, kept short. If one already exists in this folder or
(in a multi-build repo) at the repo root, update that one — never start a second
roadmap beside it:

- `## What this is` — two sentences.
- `## Builds` — one `### Build N — <name>` per build, the name being what I get
  in 2–5 words, not how it's built (the project dashboard shows these). This
  brief is the current build. Group the Later items into the builds after it,
  in the order they'd be worth having, one or two lines each.
- For each later build: would it still be worth using if nothing after it got
  built? If not, merge it forward.

Updating means keeping earlier builds' entries as they are and changing only
what this brief moved. A roadmap with one build is fine. Don't invent builds
for things I didn't ask for.
