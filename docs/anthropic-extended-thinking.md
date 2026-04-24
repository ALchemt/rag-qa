# Anthropic Extended Thinking — Summary

**Source:** Anthropic docs, "Extended thinking"
**URL:** https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
**Type:** Vendor documentation (summary, own words)

## What it is

Extended thinking lets Claude spend a configurable number of tokens on internal reasoning before producing its visible response. The reasoning is returned as a `thinking` content block in the response — visible to you, the developer, but not part of the prior conversation unless you pass it back.

## Why it exists

Some tasks benefit from more "thinking time":
- Multi-step math.
- Complex code review with many constraints.
- Ambiguous requirements that need decomposition before answering.

Prior to extended thinking, the only lever was chain-of-thought prompting in the visible output, which wastes user-visible tokens and breaks formatting.

## How to use it

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 8000},
    messages=[{"role": "user", "content": "hard reasoning question"}],
)
```

- `budget_tokens` — max tokens for internal reasoning. Must be less than `max_tokens`.
- The model may use less than the budget if it finishes sooner.

## Response structure

Content blocks arrive in order:
1. `thinking` block(s) — the reasoning.
2. `text` block(s) — the final answer.

Both are charged as output tokens.

## Costs

Thinking tokens are billed at the normal output rate. Budget wisely — a 32k thinking budget on a task that does not need it doubles cost for no benefit.

## Interaction with tool use

Extended thinking can be combined with tool use. The thinking block often appears before a `tool_use` block, letting you see the plan Claude formed before calling the tool. Useful for debugging agent behaviors.

## Interaction with prompt caching

Thinking blocks are part of output, not input, so they do not interact with input caching. However, if you pass prior thinking blocks back into a multi-turn conversation, they become cacheable input like any other content.

## When to enable

Reach for extended thinking when:
- Your eval shows the model failing on multi-step reasoning.
- Latency is acceptable to trade for quality.
- The task decomposes poorly into multiple smaller LLM calls.

Do NOT enable when:
- The task is fact lookup (RAG) — the bottleneck is retrieval, not reasoning.
- You need predictable latency (thinking variance is high).
- A smaller model without thinking already meets your accuracy bar.

## Tool use vs. extended thinking

- **Tool use:** model takes actions — calls APIs, queries DBs, retrieves docs. Necessary when the answer depends on information the model doesn't have.
- **Extended thinking:** model reasons more deeply with information it already has (including retrieved context). Necessary when the question is hard to answer even with all facts in front of you.

These are complementary, not alternatives. Best agents use both.
