Read BRIEF.md, EXPLORE.md and DISCOVERY.md (if they exist) in the current
directory, `~/projects/platform/PLATFORM.md`, and `~/.claude/CLAUDE.md`.

If EXPLORE.md still lists anything **BLOCKED**, stop and tell me which checks
are outstanding. Don't write the spec around a guess. Anything EXPLORE.md marks
WRONG is settled — write against what was actually found.

**Proportion.** This is a personal app; a missed or wrong day costs little.
Write the smallest spec that gets the brief built right. Every line has to
earn its place by changing what gets built. No invented thresholds, retry
schedules or failure catalogues. If a one-build app comes out past about a
dozen FRs, say why at the top of SPEC.md.

**A step I do by hand is cheap; automation of it is not.** Before an FR
automates something I could do myself, name the manual step it replaces and
how often it happens. A line I paste once costs me 30 seconds; the code that
replaces it costs build time, a test, and upkeep, and often a new secret or
permission. Write the manual step into the spec instead, unless it repeats
often or BRIEF.md names it as a must. Mark any automation of a rare manual
step `[ASSUMED]`, with what it costs.

## 1. Pick the shape

Using EXPLORE.md's findings, not recall: are there genuinely different ways to
build this — different centres of gravity, not variations? Usually there's
one obvious shape on the platform; say so in a line and move on. If there's a
real choice, give me each option in two or three lines (what it makes easy,
what it makes hard, rough size), say which you'd pick and what would change
your mind, and **wait for me to choose** before writing anything.

If BRIEF.md says a person sees anything, ask me about look and feel —
layout, tone, density, an app I like the look of. Ask; don't fill it in. If I
don't care, write that down: the first screen built sets the style and gets
shown to me before a second is built.

Model calls: any part using a model must name the fuzzy judgment that needs
one. If the rules can be enumerated, that part is code. The inverse: before
calling something enumerable, name the inputs the rules read — if one of them
is the thing being worked out, it's judgment wearing a rule's clothes. Mark
every prediction about how well a model will judge something as untested.

## 2. Write two files

Create two files in this directory and nothing else. No source code, no
directories, no installs.

**CLAUDE.md** — project-specific rules only (don't repeat the global file):
- Tech stack, with versions where they matter
- Which platform services it uses, and any stack it adds beyond them, with the
  reason
- Hard rules the agent must never break, numbered — only real ones
- Where data lives
- That no devbox-specific path, IP or hostname is written into code — it comes
  from an environment variable
- This line, verbatim: "Tests may never be skipped, xfailed, or deleted to
  make a gate pass. If a test fails, fix the code — or tell me the test is
  wrong and why. Reducing coverage to go green is a failure, not a fix. Never
  add to .claude/known-failing-checks — only the user does."

**SPEC.md**, with these sections:

### Purpose
Two sentences.

### Shape
The shape chosen, in a paragraph: what else was considered and why it lost.
Look and feel, if a person sees anything.

### Functional Requirements
Numbered checkboxes, each opening with a 2–5 word name for what I get (the
project dashboard shows these):
`- [ ] **FR-3 — Recipe import from URL.** WHEN … THE SYSTEM SHALL …`
Each independently verifiable, phrased as behaviour, not implementation. Any
FR where a person enters, sees or chooses something names the screen or
message it happens on — an FR satisfiable only server-side for something a
person needs to do is half an FR.

**Mark anything I didn't say `[ASSUMED]`.** If a requirement, constraint or
default came from you rather than from me — in the brief, discovery, or this
conversation — tag it. A document is never a source: "DESIGN.md says so" or
"EXPLORE.md implies it" is your own writing, still `[ASSUMED]`. Don't tag the
obvious: a default any sensible person would pick, that follows straight from
the goal, is just written down.

### Data Model
Tables and fields with types. Only what something reads.

### Interfaces
Routes, message formats, anything crossing between programs. Omit if none.

### Human Surfaces
Every screen, form, message or notification a person uses: who, what they do
there, which FRs it serves. Every table a person's data goes into needs a way
in that isn't SQL. If nothing is human-facing, write "None — " and why.

### When it breaks
What I see when it fails, not a catalogue of how it could. Usually one or two
lines: what counts as a failed run, and that it reaches me through the
platform's failure route. Name anything that would fail *silently* — wrong
output that looks right — because that's the kind I won't notice.

### Verification Gates
Exact shell commands that must exit 0. Commands, not adjectives. Include one
that proves it's deployed and comes back after a reboot.

## 3. What would bite me

Name the **five** situations most likely to go wrong for me in real use —
realistic days with this app, not exotic edge cases. A restock in a new size,
a week of devbox being off, a duplicate arriving twice. For each, walk it
through the spec and say what actually happens to me.

Where the spec does the wrong thing and the fix follows from the goal, fix the
spec. Where it's a genuine choice, it goes on the list below. Five, not more:
the cap is what keeps this about my life with the app, not the spec's wording.

## 4. Stop and show me

Show me both files, then list every `[ASSUMED]` item in one place, one line
each, with what it costs to build. I'll keep or cut each. A kept one loses its
tag — it's now my decision. A cut one comes out of the spec.
