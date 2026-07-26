Forget everything discussed before this message. You have no context beyond
SPEC.md in the current directory.

Read it fresh, as if seeing it for the first time. Then:

1. List every constraint you believe this system must satisfy, and for each,
   quote the exact line in SPEC.md that establishes it.

   **Quoting a line proves the requirement was written down, not that it is
   right.** A confident sentence is the easiest thing in the world to produce,
   and most of this spec was produced by a model. Treat every quote as the
   beginning of the question, not the end of it.

2. Audit the tags themselves, which is a separate job from reading them:
   - **[STATED]** claims a human raised this unprompted. If the quoted
     support is a document rather than a person's words, it is mis-tagged.
     "DESIGN.md establishes it" means nobody stated it.
   - **[AGREED]** means the model proposed it and the human said yes. For each
     one, ask directly: if this had never been suggested, would the human have
     asked for it? Say so when the answer is no.
   - **[DERIVED]** must show a chain ending in a [STATED]. Follow it. A chain
     ending in an [AGREED] or an [ASSUMED] is mis-tagged.
   - **[ASSUMED]** — check for anything inferred that carries no tag at all.

3. Flag every requirement that encodes a **prediction about how well a model
   will judge something** — that a model can reliably tell one category of
   text from another, score relevance, spot intent, or classify tone. These
   arrive disguised as architecture, and once one becomes a schema field, a
   validation rule, or a rejection reason, it gets defended as a mechanism
   instead of questioned as a guess. For each: has it been tested against a
   real example, or only written down? Name the smallest test that would
   settle it.

4. For each constraint: what would be built differently if it were removed?
   List any whose removal changes nothing — flag these as possibly redundant
   or not actually load-bearing.

5. Read the spec against itself. Quote any two passages that cannot both be
   true, or where a stated principle is contradicted by a requirement further
   down. Documents this long routinely argue with themselves, and no earlier
   step in the process ever reads one end against the other.

Do not fix anything. Just report. I'll tell you what to strike.
