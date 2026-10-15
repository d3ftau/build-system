#!/usr/bin/env bash
# Status line: model, folder, and context size. Turns red with a warning marker once
# context passes CTX_WARN_TOKENS (default 200000; same variable as context-warn.sh).
# Context = input + cache-read + cache-creation tokens of the latest API call
# (docs: statusline "context window fields"). It is null right after /compact or /clear
# until the next API call, shown as a dash.

input=$(cat)
threshold=${CTX_WARN_TOKENS:-200000}

model=$(printf '%s' "$input" | jq -r '.model.display_name // "?"')
dir=$(printf '%s' "$input" | jq -r '.workspace.current_dir // .cwd // ""')
tokens=$(printf '%s' "$input" | jq -r '
  .context_window.current_usage // null
  | if . == null then "" else ((.input_tokens // 0) + (.cache_read_input_tokens // 0) + (.cache_creation_input_tokens // 0)) end')

if ! [[ "$tokens" =~ ^[0-9]+$ ]]; then
  ctx="ctx -"
elif [ "$tokens" -ge "$threshold" ]; then
  ctx=$(printf '\033[1;31mctx %dk ⚠ over %dk\033[0m' $(( tokens / 1000 )) $(( threshold / 1000 )))
else
  ctx="ctx $(( tokens / 1000 ))k"
fi

echo "[$model] ${dir##*/} | $ctx"
