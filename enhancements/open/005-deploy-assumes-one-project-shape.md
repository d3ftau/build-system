# Enhancement: `/deploy` assumes every project is a reachable web service

**Status: OPEN** — diagnosed, not built. Leave the actual rewrite to a
dedicated session.

## Where this came from

Same `file-cleanup` completion-check session as `004`, 2026-08-01. Checking
which Playbook phases had actually been run against this project surfaced
that `/deploy` (Phase 5) had never been invoked. On inspection, it's not
obvious it should be — `deploy.md`'s entire requirement list assumes a
project shape this one isn't:

- "Port bound to the Tailscale IP ONLY... reachable from phone over
  Tailscale" — file-cleanup's services (Qdrant, the embed service) are
  deliberately `127.0.0.1`-only. Nothing outside devbox itself is meant to
  reach them; they're called by Claude Code sessions running on the same
  box, not by another device on the tailnet. Binding them to the Tailscale
  IP would be the wrong call, not a missing step (see the corrected
  Tailscale-vs-localhost principle in `~/.claude/CLAUDE.md`, written earlier
  in this same build after a related mistake).
- "A healthcheck hitting `/health`" — there's no HTTP surface to this
  project in the sense Phase 5 assumes; the containers involved don't have
  a health endpoint because nothing calls them that way.
- Phase 5's checklist — "reachable from phone," "Uptime Kuma monitor,"
  "stack visible in Dockge" — is written entirely in terms of a service
  someone checks on remotely. None of it maps cleanly onto local-only
  ingestion infrastructure.

## The general failure mode

`/deploy` was written with one concrete project shape in mind — a
network-reachable app — and never given the "identify genuinely distinct
shapes, not variations on one idea" treatment that `/design` explicitly
applies to build options. It doesn't classify or ask; it has a single
template and assumes every project fits it. This is a narrower instance of
the same shape as `002`/`003`: a document (here, `deploy.md` plus Phase 5's
prose) encodes an assumption as if it were universal, and nothing checks
whether the current project actually matches it before applying it.

## Candidate fix

`/deploy` classifies the project first — network-reachable service (current
behavior, unchanged) vs. local-only infrastructure — and branches its
requirements and end-of-phase checklist accordingly, rather than one
template applied unconditionally.

## Open, not resolved here

What the local-only branch should actually require is a real design
question, not assumed:
- Does local-only infrastructure still want a healthcheck of some kind
  (e.g. `docker compose ps` reporting healthy, or a Qdrant `/collections`
  check) even without phone-reachability being the point?
- Does a service nothing outside the box calls still deserve an Uptime Kuma
  monitor for basic "did this crash" detection, or is that meaningless for
  something with no external consumer to notice an outage on its behalf?
- Are there other project shapes beyond these two (e.g. a CLI tool with no
  running service at all) that also don't fit either branch?

## Still open

- `/deploy` itself is unchanged.
- No mechanism would catch the next project that's the wrong shape for
  `/deploy`'s current assumptions — same "someone noticed" pattern as `002`.
