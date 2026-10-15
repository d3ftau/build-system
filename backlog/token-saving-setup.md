# Token-saving setup (ponytail, lean-ctx, batching, shell timeout): reversible

## Status (2026-10-15)
- **caveman: dropped.** Removed from the plan, along with the caveman-pause hook.
- **ponytail: done.** v5.2.0 installed as a plugin, default level full, commit `8d855ba` in `~/.claude`.
  Checked that a new session reports it active, and that disable and re-enable both work.
- **Where the tokens go (measured 2026-10-15, `bin/token-audit.py`, last 14 days, ~$478 API-equivalent):**
  - **A few marathon sessions dominate.** 9 sessions that peaked above 300k of context are 77% of usage.
    27 small sessions are 3%. Auto-compact defaults to about 967K on 1M-window models (model-config docs),
    so sessions almost never compact.
  - **Cost by token type:** cache writes 44%, cache reads 38%, output 18%.
  - **Opus 5.5 is 87% of spend**, despite `opusplan`. 23 of 53 sessions never touched Sonnet. The cause is not found.
    Sonnet 5.5 is exactly half the price of Opus 5.5 in every column.
  - **Calls after >1h idle are 23% of spend** (cache rebuilds). Almost all cache writes use the 1-hour TTL, so the
    Reddit "5-minute cache" story doesn't apply here.
  - **Shell output is small.** Bash results are about 6% of everything written to cache, so even a perfect
    shell-output compressor (lean-ctx, rtk) is worth about 3-4% at most.
- **What would save at least 15%, replayed on real history** (baseline replay matched actual spend):

  | Change | Saving | Notes |
  |---|---|---|
  | Compact at 150k (`autoCompactWindow`) | 28% | 23% with 50k re-read per compaction, 18% with 100k |
  | Move 25% of Opus work to Sonnet | 11% | 50% of it: 22%. Quality cost not measured |
  | Fresh start after >1h idle | 29% | Fragile: ~0% if each fresh start needs 100k of re-reading |
  | All three (50k re-read) | 28% | Fresh start and compaction overlap |

  Open: why sessions stay on Opus under `opusplan`. Not yet changed: `autoCompactWindow` in settings.json.
- **Recommendation changed: don't install lean-ctx.** Independent tests (JetBrains, 80+ paired tasks per tool) found
  caveman -8.5% output tokens and rtk +7.6% cost; ponytail -10.3% cost (the only significant saver). The block below
  is kept only in case that changes.
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
  It **did send** one batch at 00:29:41 to `api.leanctx.com`, about a minute after install. The batch held
  an anonymous install ID, the version and OS, and usage counters. An earlier "Last sent: never"
  reading came before that send.
- Within a minute, its package folder disappeared (cause unknown, not me). Its hooks were left
  pointing at a missing binary, so it was rolled back.

### Sandbox findings (2026-10-15, lean-ctx 3.11.4, nothing installed for real)
Tested with the release binary in a fake home folder and in `claude -p` runs pointed at sandbox folders.
- **`init` and `onboard` can't be used safely.** Every `init --agent claude` variant, including
  `--mode mcp --no-shell-hook`, installs:
  - the command-rewrite hook and the file-read redirect hook
  - "observe" hooks on every event
  - a status line, a skill, and a CLAUDE.md block (the CLAUDE.md block still says "Replace Mode")
  - MCP tools set to `alwaysLoad` with 59 tools auto-approved

  Run inside a repo, `init` also writes `AGENTS.md`, `LEAN-CTX.md`, `.claude/settings.local.json` and
  `hooks/lean-ctx-*` into that repo. `--mode` only changes whether Grep/Glob are denied.
- **Its rewrite hook answers "allow" for every command.** Per code.claude.com/docs/en/hooks (PreToolUse),
  "allow" skips the permission prompt. A block still wins ("deny > defer > ask > allow"), so git-guard keeps working.
- **A rewrite without "allow" keeps permissions intact.** Tested: a hook that only returned
  `updatedInput` was applied, and a rewrite to `touch` was denied by the normal permission check.
- **Three default blocks would break real work.** Both are off switches in `config.toml`:
  - The command allowlist blocks `docker` (exit 126) and `systemctl`. Off: `shell_security = "off"`.
  - The path jail blocks paths outside the project and outside home, and blocks home dot-folders such
    as `~/.config`. Off: `path_jail = false`.
- **Compression needs `LEAN_CTX_AGENT=1`.** Without it, output passes through unchanged.
  - `git log --stat -10`: 9182 → 874 bytes
  - `git log -20`: 13841 → 1551 bytes
  - `ls -la /usr/bin`: 110745 → 37183 bytes
  - `docker ps` and `git diff`: unchanged

  When it compresses, the full output is kept for 24h in a "tee" log file.
- **Correctness checks passed:**
  - exit codes and error output are preserved
  - the working folder carries over between commands
  - heredocs and quoting pass through intact
  - redirects, pipes, `tee` and `$(…)` get the exact original bytes; only what Claude reads is compressed
- **Side effects:**
  - It starts a background daemon on demand. Its pid and socket always go in `~/.local/share/lean-ctx`.
  - Some output is reformatted: `head` gets line numbers and a header.
  - Shell permission prompts show `lean-ctx -c '…'`, so allow-rules like `Bash(git status:*)` stop
    matching. There are none in settings.json today.

### Recommended install (tested in the sandbox, not yet done for real)
Shell-output compression only. No `npm`, `init`, `onboard`, MCP server, read redirect, CLAUDE.md block,
status line or shell aliases.
1. Download the binary with `gh release download v3.11.4 -R yvgude/lean-ctx` and check it against
   `SHA256SUMS`. Install it to `~/.local/bin/lean-ctx`. Keep this as a pinned script in this repo.
2. Create `~/.config/lean-ctx/config.toml` with `shell_security = "off"` and `path_jail = false`.
   Then run `lean-ctx telemetry off`.
3. In settings.json `env`, set `LEAN_CTX_AGENT=1`, `DO_NOT_TRACK=1`, `LEAN_CTX_TELEMETRY=off` and
   `LEAN_CTX_NO_UPDATE_CHECK=1`.
4. Add a new hook, `hooks/lean-ctx-compress.sh`, registered as PreToolUse/Bash after git-guard. It runs
   `lean-ctx hook rewrite`, keeps only the rewritten command (and any deny), and drops the "allow".
   If the binary is missing or fails, it does nothing and the command runs unchanged. The tested draft
   is below.
5. Undo, in order:
   - Remove the hook entry and the env lines (`git revert`).
   - Delete `~/.local/bin/lean-ctx`, `~/.config/lean-ctx`, `~/.local/share/lean-ctx` and `~/.local/state/lean-ctx`.
   - Kill switch without reverting anything: delete the binary.

Optional later: file-read compression through its MCP `ctx_read`. Only worth it after measuring
the shell part. It would need the MCP server registered by hand, without `alwaysLoad` or auto-approve.

```bash
#!/bin/bash
# PreToolUse(Bash): route commands through lean-ctx so their output comes back compressed,
# while keeping Claude Code's normal permission checks.
# lean-ctx's own hook answers "allow" for every command, which skips the permission prompt.
# This keeps only its rewritten command (and any "deny"). If lean-ctx is missing or fails,
# the command runs unchanged. Checked against lean-ctx 3.11.4.
LC="${LEAN_CTX_BIN:-$HOME/.local/bin/lean-ctx}"
[ -x "$LC" ] || exit 0
out=$("$LC" hook rewrite 2>/dev/null) || exit 0
[ -n "$out" ] || exit 0
jq -c '.hookSpecificOutput // empty
  | if .permissionDecision == "deny" then {hookSpecificOutput: .}
    elif .updatedInput then {hookSpecificOutput: {hookEventName: "PreToolUse", updatedInput: .updatedInput}}
    else empty end' <<<"$out" 2>/dev/null || exit 0
```

## Remaining steps (not started)
**Shell timeout.** In `~/.claude/settings.json` `env`:
- `BASH_DEFAULT_TIMEOUT_MS=300000` (5 min)
- `BASH_MAX_TIMEOUT_MS=1200000` (20 min)

**Batching.** Add one line to "How to work with me" in `~/.claude/CLAUDE.md`:
"Batch independent tool calls into a single message; only sequence calls that depend on each other's output."

## Verification still open
- Savings check: run one fixed prompt in a scratch repo with and without ponytail, and compare
  the `usage` totals in the two transcript JSONL files.
