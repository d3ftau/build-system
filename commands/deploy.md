Create a Dockerfile and docker-compose.yml for this project.

Requirements:
- Multi-stage build, minimal final image
- Port bound to the Tailscale IP ONLY, in the form "100.x.y.z:PORT:PORT".
  Never 0.0.0.0. Read the actual IP with `tailscale ip -4`.
- Persistent data on a host volume under ./data
- All config via environment variables, read from .env
- restart: unless-stopped
- A healthcheck hitting /health
- No `version:` key — obsolete in Compose V2

Then bring it up, confirm the healthcheck passes, and show me the output of
`docker ps` and `docker compose logs --tail 20`.
