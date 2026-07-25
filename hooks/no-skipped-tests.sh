#!/usr/bin/env bash
# PostToolUse hook (matcher: Edit|Write). Enforces PLAYBOOK.md's gate-gaming guard:
# tests may never be skipped or xfailed to make a gate pass.

input=$(cat)
file_path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')

case "$file_path" in
  *test*|*spec*|*__tests__*) ;;
  *) exit 0 ;;
esac

new_text=$(printf '%s' "$input" | jq -r '.tool_input.new_string // .tool_input.content // empty')
[ -n "$new_text" ] || exit 0

if printf '%s' "$new_text" | grep -qE '@pytest\.mark\.(skip|xfail)|pytest\.mark\.(skip|xfail)|\.skip\(|\bxit\(|\bxdescribe\(|it\.skip|describe\.skip|test\.skip|@Disabled|@Ignore|#\[ignore\]|\[Ignore\]|Skip[[:space:]]*=|t\.Skip\('; then
  echo "Blocked: this edit to $file_path adds a skip/xfail/disable marker. PLAYBOOK.md rule: tests may never be skipped, xfailed, or deleted to make a gate pass. Fix the underlying code, or tell the user the test is wrong and why." >&2
  exit 2
fi

exit 0
