# ReAct: Reasoning + Acting — Summary

**Source:** Yao et al. 2022, "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023)
**URL:** https://arxiv.org/abs/2210.03629
**Type:** Foundational paper (summary, own words)

## Problem

Two capabilities were developed in isolation:
- **Reasoning:** chain-of-thought prompting lets models think step by step — but they cannot look anything up or affect the world.
- **Acting:** agents that call tools (search, APIs) — but they lack explicit reasoning between actions.

ReAct combines them.

## The ReAct loop

At each step the model produces one of:
- **Thought:** free-text reasoning about what to do next.
- **Action:** a structured call to an external tool (e.g., `Search[Colorado orogeny]`).
- **Observation:** the result of the action, fed back into the prompt.

The model then produces the next Thought/Action, continuing until it emits a final Answer.

Example trace:
```
Thought: I need to find the elevation range of the area.
Action: Search[Colorado orogeny]
Observation: The Colorado orogeny was an episode of mountain building...
Thought: It does not mention the eastern sector. I'll search for that.
Action: Search[eastern sector Colorado orogeny]
...
Thought: So the answer is 1,800 to 7,000 ft.
Action: Finish[1,800 to 7,000 ft]
```

## Why this works

- **Interpretable:** you can read the chain of thoughts and see why the agent did what it did.
- **Error-correcting:** if a search returns garbage, the next thought can re-plan.
- **Grounded:** acting on real tools prevents hallucination of facts that can be checked.

## Results

- HotpotQA, FEVER: ReAct beats reasoning-only (CoT) and acting-only (WebGPT-style) baselines.
- ALFWorld, WebShop: interactive decision-making tasks, ReAct outperforms imitation + RL baselines with far fewer in-context examples.

## Implementation notes

- Tools are described in the system prompt with their syntax.
- Observations are often truncated or summarized — raw HTML breaks context budgets.
- Stopping criterion: emit `Finish[answer]` or hit a step limit.

## ReAct vs. function calling today

Modern function calling (Anthropic tool use, OpenAI tools) is ReAct with structured outputs:
- Thought → assistant message
- Action → `tool_use` block with JSON args
- Observation → `tool_result` block

The loop is the same; the serialization is cleaner.

## When to use

Reach for ReAct-style agents when:
- The answer requires multi-step lookups across tools.
- You need an audit trail (compliance, debugging).
- The task space is open — a single retrieval pass is insufficient.

Do NOT use when:
- A one-shot RAG retrieval is enough. Extra loops add latency + cost without adding quality.
