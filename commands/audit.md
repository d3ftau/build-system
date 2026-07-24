Forget everything discussed before this message. You have no context beyond
SPEC.md in the current directory.

Read it fresh, as if seeing it for the first time. Then:

1. List every constraint you believe this system must satisfy, and for each,
   quote the exact line in SPEC.md that establishes it.
2. Separately list anything you're inferring rather than reading directly —
   these should already be tagged [ASSUMED], but check for any that aren't.
3. For each constraint: what would be built differently if it were removed?
   List any whose removal changes nothing — flag these as possibly redundant
   or not actually load-bearing.

Do not fix anything. Just report. I'll tell you what to strike.
