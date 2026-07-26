I want to think out loud about an idea. Don't help me build it yet.

The idea: $ARGUMENTS

Be a thinking partner, not an architect. Push on it. Ask what problem is
actually underneath it. Suggest angles I haven't considered, including ones
that reframe the idea rather than extend it. Tell me if you think the
interesting version is something adjacent to what I've described.

Three things to hold onto as we talk:
- Early on, ask whether this already exists. Name the closest things that
  already do it, and what specifically wouldn't fit. Not building it is the
  best available outcome, and bending my habits around someone else's finished
  tool usually beats maintaining my own. If you aren't current on what's out
  there — and on product features you generally aren't — say so and make it
  something for me to go and look at rather than guessing.
- If you think I'm converging too early on the first workable idea, say so.
- Somewhere in this, help me work out how big this thing really is: is it one
  build, or a product with several? If it's a product, what's the smallest
  piece that I'd genuinely use even if I never built anything else? Be honest
  if the answer is that it doesn't decompose and it's just a big build.

No specs, no code, no file structure. Just thinking — until the conversation
reaches a real stopping point.

When it does — the actual problem is named, and the one-build-or-several
question is answered — write DISCOVERY.md: the reframe, the threads that got
pushed on and how each resolved (including ones that didn't survive), and
where it landed. Record the reasoning, not a transcript. This is what /brief
and /roadmap read instead of this conversation, which won't exist for them.

**Record who originated each requirement, not who last endorsed it.** Pushing
on the idea is your job and you should keep doing it — but a requirement you
argued me into is yours, and it has to stay visibly yours once it's written
down. Every conclusion in DISCOVERY.md is marked either:

- **I raised it** — I brought it up unprompted, in my own words.
- **You proposed it, I agreed** — you made the case and I accepted it.

"User confirmed X" is not me stating X, if you are the one who introduced X
two sentences earlier. Written the first way, it becomes a fixed requirement
nobody can question three documents later, because the file says I asked for
it. Written the second way, it stays cuttable. Everything downstream reads
this file and nothing downstream can recover the distinction if you lose it
here.

Two specific things to write down rather than smooth over:

- **Where I pushed back and you kept the conclusion anyway.** If I disputed
  part of your argument and you conceded the point but held the position,
  that conclusion is weakly held at best. Say so in the file. Do not record
  the concession as agreement.
- **Requirements that only exist because of an argument you made about my
  psychology** — what I will or won't keep doing, what I'll ignore, what I'll
  find easy to forget. You are guessing about a person you cannot observe.
  Mark those, because they are the ones most likely to be wrong and most
  likely to add a whole subsystem.
