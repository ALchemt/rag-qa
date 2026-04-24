# Anthropic Tool Use — Summary

**Source:** Anthropic docs, "Tool use"
**URL:** https://docs.anthropic.com/en/docs/build-with-claude/tool-use
**Type:** Vendor documentation (summary, own words)

## What it is

Tool use is Anthropic's function-calling implementation. You describe functions Claude may invoke, and Claude emits structured JSON calls when it decides one is needed. Your code runs the call and returns the result, and Claude continues the conversation.

## Request structure

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    }
]

response = client.messages.create(
    model="claude-sonnet-4-6",
    tools=tools,
    messages=[{"role": "user", "content": "Weather in Tbilisi?"}],
)
```

## Response shapes

Claude's response contains content blocks. Key types:
- `text` — normal assistant prose.
- `tool_use` — a structured call: `{name, input, id}`.
- The `stop_reason` is `"tool_use"` when Claude expects you to run a tool.

## The loop

1. User sends a question.
2. Claude responds with `tool_use` block(s).
3. Your code executes the tool and sends a `tool_result` block back in a new user message, referencing the `tool_use_id`.
4. Claude either issues more tool calls or returns a final text response.

Continue until `stop_reason != "tool_use"`.

## Parallel tool use

Claude can emit multiple `tool_use` blocks in one response. Run them in parallel and return all results in a single user message. Enabled by default on modern Claude models.

## Tool choice

The `tool_choice` parameter:
- `{"type": "auto"}` — default, Claude decides.
- `{"type": "any"}` — force Claude to use *some* tool (but not which one).
- `{"type": "tool", "name": "..."}` — force a specific tool.
- `{"type": "none"}` — disable tools for this turn.

## Best practices

- **Descriptions matter more than schemas.** Write tool descriptions like you are describing it to a new engineer — inputs, outputs, edge cases.
- **Validate on your side.** Claude's JSON is usually correct but never assume — JSON-schema-validate before executing.
- **Keep tool results short.** Long results eat context. Summarize or paginate.
- **Version your tools.** Changing a tool's schema mid-conversation confuses the model; start a new conversation.

## Error handling

If a tool call fails, return a `tool_result` with `is_error: true` and an explanation. Claude will usually adapt (retry with different args, ask the user, give up gracefully).

## Connection to RAG

Retrieval itself can be a tool. Two patterns:
- **Static RAG:** retrieve before calling Claude, pass chunks in context. Simple, one LLM call.
- **Agentic RAG:** expose `search_docs` as a tool. Claude decides *whether* and *how many times* to retrieve. More flexible, more latency, harder to evaluate.
