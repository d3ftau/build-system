The build is done. Bring every project doc into line with what is actually
true now, and write README.md.

Run this in the session that did the work. Use what you remember for **why**
things are the way they are — that's what makes a doc explain instead of list.
Never use it for **what** is true. Every factual claim you write, or leave
standing, gets checked against the real state: `git log`, files on disk,
running config (`docker compose config`, crontab, registered hooks, `.env.example`)
— not the doc's own claims, and not your memory of them.

1. For CLAUDE.md, DESIGN.md, SPEC.md, PLAN.md, EXPLORE.md and any other
   project doc: list every statement that is no longer true, with the evidence.
   "Not yet", "deferred", "planned" and "will" are where rot collects. Then go
   through `git log` since each doc was last touched and list what changed that
   no doc mentions.
2. Show me that list before editing anything.
3. Fix the docs. Update stale lines in place. Where a decision was reversed,
   say so and why — don't rewrite history (DESIGN.md's rejected options stay
   rejected, with what was learned).
4. Write README.md, short: what it is, how to run it, where the data lives,
   and what needs backing up — anything that can't be regenerated from git
   plus a fresh build.

Show me the diff.
