# Token-saving setup (ponytail, lean-ctx, batching, shell timeout): reversible

## Status (2026-10-15)
- **caveman: dropped.** Removed from the plan, along with the caveman-pause hook.
- **ponytail: done.** v5.2.0 installed as a plugin, default level full, commit `8d855ba` in `~/.claude`.
  Checked that a new session reports it active, and that disable and re-enable both work.
- **lean-ctx: tried, removed.** v3.11.4 behaves very differently from what this plan
  assumed (see below). Every change was rolled back the same day. Not installed now.
- **Batching, shell timeout: not started** (weren't part of this round).
- Undo sheet: `~/.claude/backups/pre-token-saving/UNDO.md`.

## Constraints
| Constraint | Source |
|---|---|
| Every change can be undone, one tip at a time | stated |
| ponytail is on in every session | stated |
| Use lean-ctx, not rtk | stated |
| Leave superpowers alone (you use it outside the build system) | stated |
| Batching is one line in CLAUDE.md, not a skill | stated |
| Install through the official plugin and npm routes only, never `curl \| sh` | inferred |
| Telemetry off for lean-ctx | inferred |
| Not containerised: these hook into Claude Code and the shell on this machine, so a container can't host them | inferred |

## What lean-ctx v3.11.4 actually did (2026-10-15)
The plan said `npm install` then `lean-ctx init --agent claude` makes four small changes.
In fact:
- **npm install sets itself up with no prompt.** Its post-install script runs `lean-ctx onboard`
  unless `LEAN_CTX_NO_ONBOARD=1` is set. So there is no separate step to review first.
- **Its pre-install script runs `pkill -f lean-ctx`.** That kills any process whose command line
  contains "lean-ctx", including the shell that ran the install.
- **Onboarding changed far more than four things:**
  - It denied Claude's built-in Grep and Glob tools in every session.
  - It added a Bash hook that rewrites every command and **rejects commands not on its
    allowlist**. `systemctl` was blocked, for example.
  - It added a hook that redirects file reads, and "observe" hooks on every event.
  - It replaced the status line.
  - It added its own plugin and marketplace.
  - It added two CLAUDE.md blocks. One is a "solution efficiency" ladder that duplicates ponytail.
  - It added `claude`/`codex`/`gemini` aliases to `.bashrc`/`.zshrc` and created `~/.bashenv`.
  - It registered an MCP server and started a background daemon.
- **Telemetry is on by default.** The install banner says so. The earlier research said it was off.
  It had sent nothing yet ("Last sent: never").
- Within a minute, its package folder disappeared (cause unknown, not me). Its hooks were left
  pointing at a missing binary, so it was rolled back.

### If retrying lean-ctx
- Install with `LEAN_CTX_NO_ONBOARD=1 npm install -g lean-ctx-bin`.
- Run `lean-ctx telemetry off`.
- Then pick a lighter mode explicitly. `lean-ctx init --agent claude --mode mcp --no-shell-hook`
  sounds like MCP tools only, with no command gating.
- Check what that mode changes against the snapshot before keeping it. It's untested.
- Decide whether its "solution efficiency" block should go, since ponytail covers that.

## Remaining steps (not started)
**Shell timeout.** In `~/.claude/settings.json` `env`:
- `BASH_DEFAULT_TIMEOUT_MS=300000` (5 min)
- `BASH_MAX_TIMEOUT_MS=1200000` (20 min)

**Batching.** Add one line to "How to work with me" in `~/.claude/CLAUDE.md`:
"Batch independent tool calls into a single message; only sequence calls that depend on each other's output."

## Verification still open
- Savings check: run one fixed prompt in a scratch repo with and without ponytail, and compare
  the `usage` totals in the two transcript JSONL files.
