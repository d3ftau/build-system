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
   constraint must be tagged [STATED], [DERIVED] (show the chain back to
   something stated), [ASSUMED], or [BET] (rests on a BET in EXPLORE.md — name
   which claim, and what this requirement costs if it turns out false):

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
