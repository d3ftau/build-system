Build this in one go: $ARGUMENTS

For something small enough that the full pipeline (/brief → /explore → /spec →
/plan → /build) would be ceremony. Same rules, one session, one approval.

This is a personal app — me, maybe immediate family; a missed or wrong day
costs little. Scale everything to that.

## 1. Understand, then check it's really small

Read `~/projects/platform/PLATFORM.md`, `~/.claude/CLAUDE.md`, and anything
already in the current directory. If README.md here already has a `## To do`
list, this is a change to an existing quick project: work out what the
request adds to it.

Ask me only what you can't settle from the request and a sensible default —
at most three questions, one at a time. Always ask who sees this and what
using it should feel like, unless the request already says.

**Then decide whether this belongs here.** Recommend the full pipeline
instead, and stop, if any of these hold:
- it's several builds — the smallest version I'd use still leaves a list of
  things I want next
- it rests on a model reliably judging something (classifying, spotting
  intent, scoring relevance) — that's a bet worth testing before building
- it depends on an outside product or API doing something you haven't just
  checked — check it now if it's a quick look; if it needs an account,
  signup or wait, that's the pipeline's /explore
- the to-do list below comes out longer than about ten items

## 2. Show me the design, in chat

Short — a screen on my phone, not a document:

- **What it does**, in two sentences.
- **Constraints**, each marked **stated** (I said it) or **inferred** (you did),
  so I can strike the inferred ones.
- **Manual steps kept manual**: what I'll do by hand (paste a line, press a
  button). Automate one only if it repeats often or I asked. One line I paste
  once beats any code that replaces it.
- **Shape**: what it's built from, and which platform services it uses. Any
  stack beyond the platform gets one line on why. A model call names the fuzzy
  judgment that needs it; anything with enumerable rules is code.
- **Decisions I'd notice** — what it says, what it keeps or throws away, what
  happens in the case nobody named — each with your recommended answer, so I
  can reply "defaults".
- **The to-do list**: the checklist you'll build from. One real path working
  end to end first. Deploying on the platform — running, back by itself after
  a reboot, a failure reaching me — is an item, not an afterthought.

Then stop and wait. My reply is the one approval this gets.

## 3. Write it down

Create or update README.md — this is what the project dashboard reads, so the
format matters:

- A first paragraph saying what it is.
- `## To do` — the approved list as `- [ ] …` checkboxes. Progress and
  "shipped" are read from this list; never put anything else under it.
- `## Design` — the constraints (stated / inferred), the shape, and the
  decisions I approved, each in a line. This is the record that stops me
  re-arguing it in three months.

Don't create BRIEF.md, SPEC.md, PLAN.md or the other pipeline docs: their
presence moves the project onto the pipeline track. If the project needs hard
rules a future session must not break, put them in a short CLAUDE.md, with
this line verbatim: "Tests may never be skipped, xfailed, or deleted to make a
gate pass. If a test fails, fix the code — or tell me the test is wrong and
why."

Commit.

## 4. Build it without stopping

Work down the to-do list without checking in. Stop only for something
destructive or irreversible, something security-sensitive, something outside
this project I didn't approve (pushing, another repo, system config beyond the
platform's own steps), two failed attempts at the same problem (then tell me
what you expected, what happened and the likely root cause), or a design so
wrong that every way forward is a guess.

Everything else you decide, and log in `BUILD-LOG.md` as
`Ruling: <what> — <why> — <what it costs if wrong>`. A ruling that changes
what I'd see takes the option that's easiest to undo and is marked
`(you'd notice)`.

For each item:
- Watch a new test fail before writing the code that passes it.
- Evidence tests the claim itself: a bug is real only if the real upstream
  system can produce it; a test input you had to invent to reach a branch is a
  finding; test the reverse of every state change.
- Run `make check` once it exists and read the output.
- Tick the item in README.md, commit, and log it.

If an item turns out bigger than it looked, add items rather than stretching
one. If the list passes about ten, stop and tell me — it's outgrown a one-shot.

## 5. Finish

When every item is ticked:
1. Bring README.md in line with what was actually built: how to run it, where
   data lives, what to back up. Check every fact against the real state, not
   memory.
2. Report: what I can do now and how to see it, every ruling ("you'd notice"
   first), one or two things worth understanding about how it works, and the
   real `make check` output.
3. Ask whether to push. The dashboard calls a quick project shipped when the
   list is done, something runs it, and git is clean and pushed.
