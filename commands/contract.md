Read BRIEF.md, DESIGN.md, and EXPLORE.md (if they exist) in the current
directory. Read ~/.claude/CLAUDE.md for machine and stack defaults.

Anything EXPLORE.md marks WRONG is settled — write the spec against what was
actually found, not what DESIGN.md assumed.

If EXPLORE.md still lists anything **BLOCKED**, stop and tell me. Don't write
the spec around it, don't write it twice for both outcomes, don't note it and
carry on. A blocked item is checkable and unchecked; a data model written
against a guess is how a spec ends up with requirements resting on nothing.
Say which checks are outstanding and wait.

Create two files in this directory and nothing else. Do not write any source
code, do not create directories, do not install anything.

1. CLAUDE.md — project-specific rules only (don't repeat the global file):
   - Tech stack for THIS project, with exact versions where they matter
   - Hard rules the agent must never break, numbered
   - Where data lives
   - What must never be installed or used

2. SPEC.md — using this exact structure. Every Functional Requirement and every
   constraint carries one of these tags:

   - **[STATED]** — I raised this myself, unprompted, in my own words. Quote
     them. Not "confirmed", not "agreed" — said, first, without being asked.
   - **[AGREED]** — you proposed it and I said yes. Still yours, not mine.
   - **[DERIVED]** — follows necessarily from a [STATED]. Show the chain. A
     chain that bottoms out in an [AGREED] or an [ASSUMED] is not [DERIVED];
     tag it as whatever it actually rests on.
   - **[ASSUMED]** — you filled a gap and I never ruled on it.
   - **[BET]** — rests on a BET in EXPLORE.md. Name which claim, and what this
     requirement costs if it turns out false.

   **A document is never a source.** "DESIGN.md says so" is not provenance —
   DESIGN.md is your writing, and an earlier document asserting something
   confidently is not evidence that anyone decided it. If the only thing
   behind a requirement is a sentence in a document you wrote, it is
   [ASSUMED], however settled the prose reads. Trace to a human or tag it
   as yours.

   **[AGREED] is not a lesser [STATED] — it is the scope you should cut
   first.** When I ask why the build is this big, list the [AGREED] items
   before anything else, because those are the ones I never asked for.

   ## Purpose
   Two sentences.

   ## Functional Requirements
   Numbered FR-1, FR-2... each an unchecked markdown checkbox, each
   independently verifiable, each tagged. Phrase them as
   "WHEN <trigger> THE SYSTEM SHALL <observable behaviour>". An FR states
   behaviour, not implementation — if it's only restating a field list, a hash
   formula, or a schema detail that belongs in Data Model, put it there instead
   and have the FR reference it rather than repeat it.

   ## Out of Scope (v1)
   ## Data Model
   Tables/entities, fields, actual types.
   ## Interfaces
   Signatures, routes, message formats — anything crossing a boundary.
   ## External Dependencies
   Note which already exist on this machine.
   ## Failure Modes
   Network down, API 429/500, malformed input, disk full. Mandatory for
   anything scheduled or unattended.
   ## Verification Gates
   Exact shell commands that must exit 0. Not descriptions — commands.

Add this line verbatim to CLAUDE.md: "Tests may never be skipped, xfailed, or
deleted to make a gate pass. If a test fails, fix the code — or tell me the
test is wrong and why. Reducing coverage to go green is a failure, not a fix."

Then stop and show me both files.
