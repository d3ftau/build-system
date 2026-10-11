Stop. Don't try again yet.

Find the root cause before proposing any fix:

- Read the error in full — the whole message and trace, not the first line.
- Find something similar that works — in this project, another project, or
  the library's own example — and list every difference between it and what's
  broken, however small.
- Where several pieces hand data to each other, find out at which hand-off it
  goes wrong (log what goes in and comes out at each) instead of guessing.

Then explain in plain English: what you expected to happen, what actually
happened, and what you think the root cause is, with the evidence. List two
different approaches and their tradeoffs. Recommend one and say what would
make you wrong.

If this is the third fix that hasn't worked, the problem probably isn't the
fix — it's the design. Say so, and say what you'd question.
