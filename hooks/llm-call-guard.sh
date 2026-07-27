#!/usr/bin/env bash
# PostToolUse hook (matcher: Edit|Write). Standing rule: never use an LLM for
# work that code can do. This cannot judge whether a call is warranted — it
# forces the decision to be explicit and leaves a greppable trace.

input=$(cat)
file_path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')

# Source files only. Docs, prompts and config may mention these freely.
case "$file_path" in
  *.py|*.js|*.ts|*.tsx|*.jsx|*.go|*.rb|*.rs|*.java|*.sh) ;;
  *) exit 0 ;;
esac

new_text=$(printf '%s' "$input" | jq -r '.tool_input.new_string // .tool_input.content // empty')
old_text=$(printf '%s' "$input" | jq -r '.tool_input.old_string // empty')
[ -n "$new_text" ] || exit 0

pattern='anthropic\.Anthropic\(|new[[:space:]]+Anthropic\(|\.messages\.create\(|openai\.OpenAI\(|new[[:space:]]+OpenAI\(|chat\.completions\.create\(|ollama\.(chat|generate)\(|api\.(anthropic|openai)\.com|/v1/(messages|chat/completions)'

printf '%s' "$new_text" | grep -qE "$pattern" || exit 0

# Present before this edit too — not newly introduced.
if [ -n "$old_text" ] && printf '%s' "$old_text" | grep -qE "$pattern"; then
  exit 0
fi

printf '%s' "$new_text" | grep -q 'LLM-JUSTIFIED:' && exit 0

cat >&2 <<'MSG'
Blocked: this edit introduces a model API call.

Standing rule: never use an LLM for work that code can do. A model earns its
place only when the task is genuinely fuzzy and code would give a noticeably
worse result — not when writing a prompt is faster than thinking.

The test: can the decision rules be enumerated? If they can be written down,
write the logic instead.

If the call is genuinely warranted, name the fuzzy judgment that requires it in
a comment on the line above:

    # LLM-JUSTIFIED: classifies free-text intent; rules are not enumerable
MSG
exit 2
