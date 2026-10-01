#!/usr/bin/env bash
# Stop hook. Enforces PLAYBOOK.md's rule: never accept "it works" as evidence —
# but only at the end of a /slice step, not every turn. Running the full
# `make check` (ruff + ruff format + mypy --strict + pytest) on every single
# turn measured at ~1.3s real time in file-cleanup — a fixed tax on every
# response regardless of whether a slice was involved, confirmed 2026-07-31
# to be far more than intended.
#
# Detection, two conditions, both read from the transcript:
#
# 1. /slice is the most recent *pipeline* command (any file in commands/
#    except /stuck, which happens inside a slice). Not "the latest message is
#    /slice": /slice stops for approval before writing code, so the code is
#    written in the turn answering my "go ahead" — a plain message.
# 2. This turn — everything after the latest real user message — used a tool
#    that can change files. Bash counts — edits made through sed would
#    otherwise skip the gate — so an approval pause that read files through
#    Bash pays ~1s for a check that passes on the clean tree it started from.
#
# A real user message has string content; tool results are always
# array-typed. Slash commands embed <command-name>/x</command-name>. Both
# shapes confirmed empirically against real transcripts, not from docs.

input=$(cat)
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')
transcript=$(printf '%s' "$input" | jq -r '.transcript_path // empty')

[ -n "$cwd" ] && [ -f "$cwd/Makefile" ] || exit 0
grep -qE '^check:' "$cwd/Makefile" || exit 0

[ -n "$transcript" ] && [ -f "$transcript" ] || exit 0

commands_dir="$(dirname "$(readlink -f "$0")")/../commands"
pipeline=$(find "$commands_dir" -maxdepth 1 -name '*.md' ! -name 'stuck.md' -printf '%f\n' 2>/dev/null | sed 's/\.md$//' | paste -sd'|')
[ -n "$pipeline" ] || exit 0

verdict=$(jq -rs --arg cmds "$pipeline" '
  to_entries as $e
  | [ $e[] | select(.value.type == "user" and (.value.message.content | type) == "string") ] as $real
  | ($real | last | .key // -1) as $turn_start
  | ([ $real[].value.message.content
       | capture("<command-name>/(?<c>[A-Za-z0-9_-]+)</command-name>")? | .c
       | select(test("^(" + $cmds + ")$")) ] | last) as $cmd
  | ([ $e[] | select(.key > $turn_start and .value.type == "assistant")
       | .value.message.content[]? | select(.type == "tool_use") | .name ]
     | any(. == "Edit" or . == "Write" or . == "MultiEdit" or . == "NotebookEdit" or . == "Bash")) as $changed
  | if $cmd == "slice" and $changed then "run" else "skip" end
' "$transcript" 2>/dev/null)
[ "$verdict" = "run" ] || exit 0

output=$(cd "$cwd" && make check 2>&1)
status=$?

if [ "$status" -ne 0 ]; then
  # A project can declare known-intentionally-failing checks (e.g. the
  # scaffold's placeholder test, which proves the gate itself runs). This
  # never touches the test — it only tells this gate the red is expected.
  # The list is mine to edit, not the agent's: no-skipped-tests.sh blocks
  # agent writes to it, or it would be a skip marker with extra steps.
  allowlist="$cwd/.claude/known-failing-checks"
  if [ -f "$allowlist" ]; then
    failure_lines=$(printf '%s\n' "$output" | grep -E 'FAIL|✗|×|AssertionError|Error:')
    patterns=$(grep -vE '^[[:space:]]*(#|$)' "$allowlist")
    if [ -n "$failure_lines" ] && [ -n "$patterns" ]; then
      unexplained=$(printf '%s\n' "$failure_lines" | grep -vF -- "$patterns")
      if [ -z "$unexplained" ]; then
        echo "make check failed, but every failure line matched an entry in $allowlist — treating as expected." >&2
        exit 0
      fi
    fi
  fi

  echo "make check failed — this must pass before the task is done:

$output" >&2
  exit 2
fi

exit 0
