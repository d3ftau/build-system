#!/usr/bin/env bash
# Stop hook. Enforces PLAYBOOK.md's rule: never accept "it works" as evidence —
# but only at the end of a /slice step, not every turn. Running the full
# `make check` (ruff + ruff format + mypy --strict + pytest) on every single
# turn measured at ~1.3s real time in file-cleanup — a fixed tax on every
# response regardless of whether a slice was involved, confirmed 2026-07-31
# to be far more than intended.
#
# Detection: the transcript's most recent *real* user turn (content is a
# plain string — synthetic tool-result feedback is always array-typed,
# confirmed empirically against this session's own transcript) must contain
# the /slice command tag Claude Code actually embeds for slash-command
# invocations (confirmed empirically, not from docs — this shape is
# undocumented).

input=$(cat)
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')
transcript=$(printf '%s' "$input" | jq -r '.transcript_path // empty')

[ -n "$cwd" ] && [ -f "$cwd/Makefile" ] || exit 0
grep -qE '^check:' "$cwd/Makefile" || exit 0

[ -n "$transcript" ] && [ -f "$transcript" ] || exit 0
last_real_user_msg=$(tac "$transcript" | jq -rs 'map(select(.type == "user" and (.message.content | type) == "string")) | .[0].message.content // empty' 2>/dev/null)
case "$last_real_user_msg" in
  *'<command-name>/slice</command-name>'*) ;;
  *) exit 0 ;;
esac

output=$(cd "$cwd" && make check 2>&1)
status=$?

if [ "$status" -ne 0 ]; then
  echo "make check failed — this must pass before the task is done:

$output" >&2
  exit 2
fi

exit 0
