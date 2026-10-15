#!/usr/bin/env bash
# Stop hook. Warns when the conversation's context passes CTX_WARN_TOKENS (default
# 200000), then again at every further +100k, so a /compact can be a choice made at a
# natural break instead of a surprise mid-task. It only warns; it never compacts or blocks.
#
# Context size = input + cache-read + cache-creation tokens of the latest main-thread
# API call in the transcript (what statusline.sh shows, and what Claude Code's own
# `used_percentage` is built from). The Stop-time transcript may lack the final call
# (hooks docs), so the number can lag by one call.
#
# Warn state lives in one tiny file per session. It resets when context falls back under
# the threshold (after /compact or /clear), so the next crossing warns again.
# Checked against Claude Code 2.1.300 (systemMessage on Stop, transcript usage fields).

input=$(cat)
transcript=$(printf '%s' "$input" | jq -r '.transcript_path // empty' 2>/dev/null)
session=$(printf '%s' "$input" | jq -r '.session_id // empty' 2>/dev/null)
[ -n "$transcript" ] && [ -f "$transcript" ] && [ -n "$session" ] || exit 0

threshold=${CTX_WARN_TOKENS:-200000}
step=100000

tokens=$(tail -n 400 "$transcript" | jq -Rn '
  [inputs | fromjson? | select(.type == "assistant" and (.isSidechain | not) and .message.usage) | .message.usage]
  | last // {}
  | (.input_tokens // 0) + (.cache_read_input_tokens // 0) + (.cache_creation_input_tokens // 0)' 2>/dev/null)
case "$tokens" in ''|*[!0-9]*) exit 0 ;; esac

state_dir="${XDG_RUNTIME_DIR:-/tmp}/claude-ctx-warn"
mkdir -p "$state_dir" 2>/dev/null || exit 0
state="$state_dir/$session"
warned=$(cat "$state" 2>/dev/null)
case "$warned" in ''|*[!0-9]*) warned=0 ;; esac

if [ "$tokens" -lt "$threshold" ]; then
  [ "$warned" -eq 0 ] || echo 0 > "$state"
  exit 0
fi

level=$(( 1 + (tokens - threshold) / step ))
[ "$level" -gt "$warned" ] || exit 0
echo "$level" > "$state"

jq -n --arg k "$(( tokens / 1000 ))" --arg t "$(( threshold / 1000 ))" '{
  systemMessage: ("Context is about \($k)k tokens (warning threshold \($t)k). Every call re-reads all of it. If you are not mid-task, /compact now at a natural break; if you are, finish first. Auto-compaction may fire on its own.")
}'
