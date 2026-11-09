# Enhancement: /discovery and /explore run the same existence search, and only one got 020's fixes

**Status: OPEN (fix written, unverified)** (recorded 2026-11-08). Greg asked:
*"Are the existing products/services checks in discovery and explore different
enough?"*

## The failure modes

1. **One search, written twice.** Both commands search commercial and open
   source separately, and both check what Greg already runs. Their purposes
   differ (/discovery: should this be built at all; /explore: what can carry
   the brief, verified), but nothing in the text gave them different jobs.
2. **They drift.** 020's three rules landed only in `explore.md`: search the
   job without its topic words, don't reject a candidate for lacking add-ons,
   and "nothing fits" must show its queries. /discovery is the earlier, cheaper
   place to learn something exists, and the place where the idea is reframed,
   which is when the topic-free search matters most. Going the other way,
   "tools that solve one hard part" lives only in /discovery.
3. **The handoff loses the queries.** /explore is told not to treat
   DISCOVERY.md's list as complete, but DISCOVERY.md didn't record what was
   searched. So /explore couldn't tell covered angles from missed ones, and
   redid all of it.

## Fix (2026-11-08)

- `discovery.md`: the broad search. It gained 020's topic-free search (re-run
  after any reframe), the add-ons rule, and "never 'doesn't exist' from
  topic-word searches alone". DISCOVERY.md now gets an **Existing tools**
  section: the literal searches, each marked commercial or open source, and
  every candidate with why it fits or doesn't.
- `explore.md` §2: starts from that section, runs only the missing angles,
  then goes deep (tiers, API, real data). With no DISCOVERY.md, it does the
  whole search as before.
- `oneshot.md` has no existence check either. Greg chose not to add one: quick
  projects are small enough.

## Still open

- **Verify** on the next /discovery → /explore run: does DISCOVERY.md carry
  the searches, and does /explore extend them instead of repeating?

## Evidence

- `commands/discovery.md` and `commands/explore.md` as of `819fbab`, compared
  side by side in this session.
- Related: `010` (OSS as its own search), `020` (searching the framing, not the job).
