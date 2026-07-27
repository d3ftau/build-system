Forget everything discussed before this message. You have no context beyond
SPEC.md in the current directory.

Read it fresh, as if seeing it for the first time. Then:

1. List every constraint you believe this system must satisfy, and for each,
   quote the exact line in SPEC.md that establishes it. **A quote proves the
   requirement was written down, not that it's right** — most of this spec was
   written by a model. Treat each quote as the start of the question.

2. Audit the tags, which is a different job from reading them:
   - **[STATED]** claims a human raised it unprompted. If the support is a
     document rather than a person's words it's mis-tagged — "DESIGN.md
     establishes it" means nobody stated it.
   - **[AGREED]** means the model proposed it and the human agreed. For each:
     if it had never been suggested, would they have asked for it?
   - **[DERIVED]** must chain back to a [STATED]. Follow it. A chain ending in
     [AGREED] or [ASSUMED] is mis-tagged.
   - **[ASSUMED]** — find anything inferred that carries no tag at all.

3. Flag every requirement encoding a **prediction about model judgment** —
   that it can classify text, score relevance, spot intent. Once one becomes a
   schema field or a rejection reason it gets defended as a mechanism instead
   of questioned as a guess. Tested against a real example, or only written
   down? Name the smallest test that would settle it.

4. For each constraint: what would be built differently if it were removed?
   Flag any whose removal changes nothing as possibly not load-bearing.

5. Read the spec against itself. Quote any two passages that can't both be
   true, or a stated principle contradicted by a requirement further down.

Do not fix anything. Just report. I'll tell you what to strike.
