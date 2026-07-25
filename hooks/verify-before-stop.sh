#!/usr/bin/env bash
# Stop hook. Enforces PLAYBOOK.md's rule: never accept "it works" as evidence.
# If this project defines `make check`, it must actually pass before the turn ends.

input=$(cat)
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')

[ -n "$cwd" ] && [ -f "$cwd/Makefile" ] || exit 0
grep -qE '^check:' "$cwd/Makefile" || exit 0

output=$(cd "$cwd" && make check 2>&1)
status=$?

if [ "$status" -ne 0 ]; then
  echo "make check failed — this must pass before the task is done:

$output" >&2
  exit 2
fi

exit 0
