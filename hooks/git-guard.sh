#!/usr/bin/env bash
# PreToolUse hook (matcher: Bash). Enforces three PLAYBOOK.md standing rules:
# hooks/signing must never be bypassed, secret-like files must never be committed,
# and the agent never writes .claude/known-failing-checks (no-skipped-tests.sh
# only sees Edit/Write, so `echo x >> .claude/known-failing-checks` needs this).

input=$(cat)
command=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')

case "$command" in
  *known-failing-checks*)
    echo "Blocked: .claude/known-failing-checks tells verify-before-stop.sh which failures to ignore. Only the user edits it — adding to it is skipping a test by another route. Read it with the Read tool if you need to; fix the failure or tell the user why it should be expected." >&2
    exit 2 ;;
  *"git commit"*) ;;
  *) exit 0 ;;
esac

if printf '%s' "$command" | grep -qE -- '--no-verify|--no-gpg-sign|-c[[:space:]]+commit\.gpgsign=false'; then
  echo "Blocked: this commit bypasses hooks or signing (--no-verify / --no-gpg-sign / commit.gpgsign=false). Only do this if the user explicitly asked for it." >&2
  exit 2
fi

if [ -n "$cwd" ]; then
  staged=$(cd "$cwd" 2>/dev/null && git diff --cached --name-only 2>/dev/null)
  hit=$(printf '%s\n' "$staged" | grep -E '(^|/)\.env(\.[^.]+)?$|\.(pem|key)$|(^|/)id_(rsa|ed25519|ecdsa)$' | grep -Ev '\.env\.(example|sample|template)$' || true)
  if [ -n "$hit" ]; then
    echo "Blocked: staged file(s) look like secrets and must never be committed:
$hit" >&2
    exit 2
  fi
fi

exit 0
