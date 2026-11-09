# Enhancement: model-judgment tests are designed even when no result could change the build

**Status: OPEN** (recorded 2026-11-09, deal-hunter Build 1 /build, T1). Greg: *"There's been
multiple times where you've designed test after test of LLM performance. It's only relevant for
using cheap models - otherwise you're just scoring your own ability which is a waste of tokens."*
And on T1's match test: *"Don't judge it at all. Its the best model I'm going to use and it's better
than not using an LLM at all so how it performs isn't going to change anything."*

## What happened

`/explore` §4 says every claim that rests on a model's judgment is "always a BET", to be given "the
smallest real test". deal-hunter's EXPLORE.md marked "Claude can tell a store page is the approved
variant" as an **invalidating** BET. `/plan` put it first (T1) with a measured **Fails if** (a miss
rate, plus "any wrong match", which I invented) and a `⏸ STOP` asking Greg to judge a ~160-row table.

In /build that turned into:
- several full runs and re-scores of ~160 real pages, each with Claude calls;
- me (Opus, the build agent) reading every scored row and judging the matches by hand, which
  duplicated the model's own judging. Greg: "Doesn't that mean I'll pay twice?";
- a plan to have Greg judge the table on his phone.

None of it could change the build. Claude was the best model Greg would use, there was no
code-only alternative that a bad score would have switched to, and Greg had already said a
let-through mistake beats a miss. A bad result would have meant "keep the model call", the same as a
good one.

## The failure modes

1. **"Always a BET" has no "so what" test.** A BET is worth testing only when a bad answer would
   change what gets built. `/explore` asks what being wrong *costs*, never whether any outcome would
   change the decision. With the strongest model and no alternative, every outcome leads to the same
   build.
2. **The real case for testing goes unnamed.** Measuring model judgment pays off when choosing a
   *cheap* model (llmbox's Qwen, Haiku) over a stronger one, or when deciding between a model and
   code (or nothing). Neither was the case here, and nothing in the commands asks.
3. **The agent grades its own model family.** When the build agent hand-judges a Claude model's
   outputs, it's scoring itself with no independent signal, at Opus prices.
4. **"Invalidating" plus a measured Fails if makes the test unskippable.** Once /plan writes a
   number, /build is told "below it, the task isn't done", so it keeps measuring.

## Candidate fixes

- `explore.md` §4: a model-judgment claim is a BET only if **some result would change the design**,
  typically (a) the plan uses a cheap or local model and a stronger one is the fallback, or (b)
  code-only or no-feature is a real alternative. Otherwise record it as "model call, not tested:
  no result changes the build" and move on.
- `plan.md`: no **Fails if** on model accuracy, and no `⏸ STOP` to judge model output, unless the
  explore verdict names which decision the number feeds.
- `build.md`: the build agent doesn't hand-judge a model's outputs in bulk. If a measure is genuinely
  needed, the user's verdicts are the measure; the agent only counts them.
- `spec.md` line "Mark every prediction about how well a model will judge something as untested":
  keep the tag, but say it's a label, not a test to schedule.
- Check other projects for the same shape (Greg says it has happened several times; other instances
  aren't gathered here).
