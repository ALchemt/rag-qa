# Toolformer — Summary

**Source:** Schick et al. 2023, "Toolformer: Language Models Can Teach Themselves to Use Tools"
**URL:** https://arxiv.org/abs/2302.04761
**Type:** Foundational paper (summary, own words)

## Idea

Instead of hand-engineering tool use via prompting, fine-tune the model on data where tool calls are inserted at positions that reduce next-token loss. The model learns *when* and *how* to call tools from self-generated training data.

## Tools used

Calculator, Q&A system, Wikipedia search, machine translation, calendar. Small, general utilities.

## Self-supervised pipeline

1. Sample raw text.
2. Prompt the base LM to propose candidate tool-call positions + arguments.
3. Execute each candidate call, collect the result.
4. Keep only calls that lower perplexity on the subsequent tokens — i.e., calls that were useful.
5. Interleave these calls into the original text, producing annotated training data.
6. Fine-tune the base LM on the annotated text.

At inference, the fine-tuned model emits `<API>tool(args)</API>` during decoding; a controller intercepts it, runs the tool, substitutes the result, and continues generation.

## Why it matters

- Shows that tool use can be *learned*, not just *prompted*. This is the research ancestor of native function calling in Claude, GPT-4, Gemini.
- The self-supervised signal (does the tool call reduce loss?) is elegant — no human annotation needed.
- Fine-tuned 6.7B Toolformer beats much larger zero-shot baselines on math, QA, and multilingual tasks.

## Limits

- Each tool is called in isolation — no chaining, no loops.
- Static insertion: the model does not decide mid-sentence to revise its tool choice.
- Paper does not release weights or public code.

## Evolution

- **ReAct (2022):** prompting-based, supports chains.
- **OpenAI / Anthropic function calling (2023–):** trained-in, JSON-structured, looped inside chat.
- **Gorilla, ToolBench, ToolLLM (2023–2024):** scale the idea to thousands of APIs.

## Connection to RAG

Toolformer is the conceptual bridge between "retrieval as a fixed preprocessing step" (original RAG) and "retrieval as a tool the model decides to invoke" (agentic RAG). The LLM owns the decision of *when* to retrieve — a query rewrite, a second search, a calculator check — instead of it being pipelined outside the model.
