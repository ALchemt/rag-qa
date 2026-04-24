# Anthropic Prompt Caching — Summary

**Source:** Anthropic docs, "Prompt caching"
**URL:** https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
**Type:** Vendor documentation (summary, own words)

## What it is

Prompt caching lets you reuse large, static prompt prefixes across multiple API calls. Anthropic caches the processed state of those prefixes for ~5 minutes; subsequent requests that match the prefix skip most of the input-token cost.

## Economics

Cached read tokens cost about **10%** of normal input tokens. Writing a cache costs about **125%** of normal input tokens (one-time premium). Break-even is after roughly the second cached hit.

Typical savings for long system prompts + context:
- 90% cheaper input tokens on cached sections.
- Noticeably faster TTFT (time to first token) because Claude skips re-processing.

## How to use it

Add a `cache_control` marker to content blocks you want cached:

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    system=[
        {
            "type": "text",
            "text": LONG_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[{"role": "user", "content": "short question"}],
)
```

You can mark up to 4 blocks in a request. Common spots:
- System prompt (instructions, persona).
- Large context (documents, retrieved chunks that don't change per query).
- Tool definitions.

## Rules

- Cache hits require **byte-identical prefixes**. Any change invalidates from that point on.
- TTL: 5 minutes (ephemeral) by default. Longer TTLs are available via extended cache.
- Minimum cacheable block size: 1024 tokens (Sonnet 4, Opus) or 2048 (Haiku).

## Response fields

The `usage` object reports:
- `cache_creation_input_tokens` — tokens written to cache this request.
- `cache_read_input_tokens` — tokens read from an existing cache.
- `input_tokens` — everything else (non-cached new input).
- `output_tokens` — generated output.

## When it pays off

- Multi-turn chats with stable system prompt.
- RAG where the same corpus chunks are re-fed across many user questions.
- Agent loops with stable tool definitions.

## When it does not

- One-shot calls (you pay the 25% write premium and never read).
- Highly dynamic prefixes (every call slightly different).
- Very small system prompts (below the minimum cacheable size).

## Gotcha: cache ordering

Caching is prefix-based. If you put dynamic content (the user's question) *before* static content, the cache never matches. Always order: [static system + tools] → [static context] → [dynamic user message].

## Takeaway

For production RAG systems with stable system prompts or repeated context, prompt caching is the single biggest cost lever available in the Anthropic API — often 5-10x cheaper at scale.
