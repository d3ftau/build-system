Read BRIEF.md and DESIGN.md (if it exists) in the current directory. Read
~/.claude/CLAUDE.md for machine and stack defaults.

Create two files in this directory and nothing else. Do not write any source
code, do not create directories, do not install anything.

1. CLAUDE.md — project-specific rules only (don't repeat the global file):
   - Tech stack for THIS project, with exact versions where they matter
   - Hard rules the agent must never break, numbered
   - Where data lives
   - What must never be installed or used

2. SPEC.md — using this exact structure. Every Functional Requirement and every
   constraint must be tagged [STATED], [DERIVED] (show the chain back to
   something stated), or [ASSUMED]:

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
