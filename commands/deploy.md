Create a Dockerfile and docker-compose.yml for this project.

First, classify it. Read SPEC.md's Machine Interfaces and Human Surfaces and
tell me which of these it is, with the evidence, before writing anything:

- **Reached from other devices** — my phone or another tailnet machine calls it.
- **Local only** — only things on this box call it: Claude Code sessions,
  other containers, cron.
- **Not a service** — a CLI or a scheduled job; nothing listens.

If it's none of these, or a mix, stop and say what it is.

Every shape:
- Multi-stage build, minimal final image
- Persistent data on a host volume under ./data
- All config via environment variables, read from .env — nothing
  devbox-specific (IPs, paths, hostnames) written into the compose file
- No `version:` key — obsolete in Compose V2

**Reached from other devices:**
- Ports bound to localhost *and* the Tailscale IP — never 0.0.0.0:
  `"127.0.0.1:PORT:PORT"` and `"${TAILSCALE_IP}:PORT:PORT"`, with
  `TAILSCALE_IP` in .env, read from `tailscale ip -4`. Same-machine callers use
  localhost; Tailscale is only for other devices.
- `restart: unless-stopped`, and a healthcheck hitting `/health`

**Local only:**
- Ports bound to `127.0.0.1` only — or none at all, if only other containers
  call it (put them on a shared Docker network instead).
- `restart: unless-stopped`
- A healthcheck using whatever the service already answers — an existing
  endpoint or a CLI probe. Don't add an HTTP server just to have `/health`.

**Not a service:**
- No ports, no healthcheck.
- If it's scheduled, say how it gets triggered (host cron running
  `docker compose run --rm`, or a scheduler container) and **where a failed run
  shows up** — a job that fails silently is worse than no job. Ask me if
  that's not already settled.

Then bring it up and verify it for its shape — healthcheck passing, or for a
non-service one real run with its output and exit code. Show me `docker ps`
and `docker compose logs --tail 20`.

Finally, give me the checklist I still have to do by hand, for this shape only:
the reboot test always (Wi-Fi is slow on cold boot here, so check it comes back
by itself); phone reachability and an Uptime Kuma monitor only if it's reached
from other devices — for a local-only service, ask whether anything I rely on
would break silently if it were down, and only then suggest a monitor.
