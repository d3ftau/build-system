# Token-saving setup (caveman, ponytail, lean-ctx, batching, shell timeout): reversible

## Context
You found Reddit tips for cutting Claude Code token use and want them applied in a way you can undo:
1. caveman and ponytail on in every session (always on, not on demand)
2. lean-ctx, an alternative to rtk, to compress shell and file output
3. batched tool calls
4. a longer wait time for shell commands

You also said caveman should stay off during conversational steps like /discovery.

## Constraints
| Constraint | Source |
|---|---|
| Every change can be undone, one tip at a time | stated |
| caveman and ponytail are on in every session | stated |
| caveman is off for conversational build-system commands | stated |
| Use lean-ctx, not rtk | stated |
| Leave superpowers alone (you use it outside the build system) | stated |
| Batching is one line in CLAUDE.md, not a skill | stated |
| caveman's default level is **lite**, not full, because of your plain-language preference | inferred (you didn't pick one; strike this to use full) |
| Install through the official plugin and npm routes only, never `curl \| sh` | inferred |
| Turn telemetry off for caveman and lean-ctx (`DO_NOT_TRACK=1`) | inferred |
| Not containerised: these hook into Claude Code and the shell on this machine, so a container can't host them | inferred |

## What the research found (checked against each project's own repo)
- **caveman** (JuliusBrussee/caveman, v3.1.0): a Claude Code plugin. A SessionStart hook loads its rules, and a UserPromptSubmit hook repeats a reminder on every turn. Default level is set by `CAVEMAN_DEFAULT_MODE`. It keeps per-session state in `~/.claude/.caveman-sessions/<session_id>.mode`, and writing the literal `off` there turns it off for that session for good. It has no built-in way to switch off for particular commands, but its hook ignores other commands' `<command-name>` wrappers, so a hook of our own can do the switching.
- **ponytail** (DietrichGebert/ponytail, v4.12.0): a plugin with lifecycle hooks. It pushes me toward the simplest, least code. Levels lite/full/ultra/off. JetBrains measured about 10% lower cost, against the advertised 20%.
- **lean-ctx** (yvgude/lean-ctx, v3.10.5): `lean-ctx init --agent claude` makes four changes:
  - registers an MCP server in `~/.claude.json`
  - adds a marked `<!-- lean-ctx -->` block to `~/.claude/CLAUDE.md`
  - adds a skill at `~/.claude/skills/lean-ctx/`
  - installs a shell hook (`init --global`) that edits your shell startup file

  Telemetry is off by default in the release. `lean-ctx uninstall --dry-run` and `uninstall` remove only what it added.
- **Shell timeout**: from the Claude Code env-vars docs, `BASH_DEFAULT_TIMEOUT_MS` (default 120000, 2 min) and `BASH_MAX_TIMEOUT_MS` (default 600000, 10 min), both set under `env` in settings.json.
- **Existing hooks are safe.** `git-guard.sh` matches on the text `git commit` appearing anywhere in a command, so a command lean-ctx has rewritten still gets caught. `verify-before-stop.sh` runs `make check` itself, so lean-ctx never compresses its output.

## Steps
Each step gets its own commit in the `~/.claude` git repo, so any one tip can be reverted alone.

**0. Snapshot**
- Commit the current uncommitted `CLAUDE.md`/`settings.json` in `~/.claude` as a baseline.
- Copy `~/.claude.json`, `~/.bashrc` and `~/.profile` to `~/.claude/backups/pre-token-saving/`.

**1. Shell timeout.** In `~/.claude/settings.json` `env`, set:
- `BASH_DEFAULT_TIMEOUT_MS=300000` (5 min)
- `BASH_MAX_TIMEOUT_MS=1200000` (20 min)
- `DO_NOT_TRACK=1`

**2. Batching.** Add one line to the "How to work with me" section of `~/.claude/CLAUDE.md`: "Batch independent tool calls into a single message; only sequence calls that depend on each other's output."

**3. ponytail**
- `claude plugin marketplace add DietrichGebert/ponytail`
- `claude plugin install ponytail@ponytail`
- Default level (full).

**4. caveman**
- `claude plugin marketplace add JuliusBrussee/caveman`
- `claude plugin install caveman@caveman`
- Plugin only. Not the all-agents `install.sh`, which also touches other tools and adds a statusline.
- Add `CAVEMAN_DEFAULT_MODE=lite` to settings `env`.

**5. caveman off for conversational commands**
- New hook `~/projects/build-system/hooks/caveman-pause.sh`, registered under UserPromptSubmit in settings.json.
- It reads the prompt and looks for `<command-name>/(discovery|brief|design|stuck)</command-name>`. The list is one variable at the top of the file, so you can edit it.
- When it finds a match, it writes `off` to caveman's session file for that session and adds a line to the context: "Caveman mode is off for this session: write normal, plain prose; disregard earlier caveman instructions." That second part is needed because the rules caveman loaded at session start are already in the context.
- Any other prompt: no output, exit 0.
- `/caveman lite` turns it back on mid-session if you want.
- The header comment says that this depends on caveman's session-file format, and which caveman version that format was checked against.
- Commit in the build-system repo.

**6. lean-ctx**
- `npm install -g lean-ctx-bin`, which goes into `~/.npm-global` along with the other npm tools.
- Run `lean-ctx init --agent claude`.
- Then `lean-ctx doctor` and `lean-ctx telemetry status`, which should say off.
- Commit the CLAUDE.md block it adds as its own commit.

**7. Undo sheet.** Write `~/.claude/backups/pre-token-saving/UNDO.md` with the exact commands to reverse each step:
- `claude plugin uninstall caveman@caveman` / `ponytail@ponytail`, plus `marketplace remove`
- `lean-ctx uninstall` (followed by `npm uninstall -g lean-ctx-bin`)
- `git revert <sha>` for each settings or CLAUDE.md commit
- remove the caveman-pause hook entry

## Verification
1. Run `claude plugin list`: caveman and ponytail are enabled.
2. Start a new session with `claude -p "say hi"`: the reply is terse (caveman on).
3. Run `claude -p "/discovery test idea"`, then check that the session file reads `off` and that the reply is in normal prose. **Reverse direction:** in the same session, `/caveman lite` brings caveman back.
4. Run `claude -p "/slice"` in a non-project directory: caveman stays on, because only the listed commands switch it off.
5. lean-ctx:
   - `lean-ctx doctor` passes.
   - `claude mcp list` shows lean-ctx.
   - A `git status` run through Claude comes back compressed.
   - A `git commit --no-verify` attempt is still blocked by git-guard.
6. Timeout: `claude -p` runs `sleep 150 && echo done` and it finishes (it would have timed out at the old 2 min default).
7. Undo test: run `lean-ctx uninstall --dry-run` and confirm it lists only lean-ctx's own changes.
8. Optional savings check: run one fixed prompt in a scratch repo before step 3 and after step 6, and compare the `usage` totals in the two transcript JSONL files. This tests whether tokens actually went down, rather than trusting the Reddit claim.
