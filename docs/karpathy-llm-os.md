# Karpathy: LLM OS — Summary

**Source:** Andrej Karpathy, "Intro to Large Language Models" talk / "LLM OS" concept
**URL:** https://www.youtube.com/watch?v=zjkBMFhNj_g
**Type:** Conceptual framing by Karpathy (summary, own words)

## The mental model

Karpathy proposes thinking of a modern LLM as the CPU of an emerging "LLM OS" — an operating system built around language-model-powered computation instead of traditional CPUs.

The analogy:

| Traditional OS | LLM OS |
|---|---|
| CPU | LLM |
| RAM (fast, small) | Context window |
| Disk (slow, large) | File storage + embeddings index |
| Peripherals | Tools (calculator, browser, code interpreter) |
| Kernel scheduler | Agent loop / planner |
| Processes | Parallel agent calls |
| Security model | System prompts + tool-use guardrails |

## Why it matters

The framing clarifies why certain research directions matter:
- **Longer context** = more RAM — lets the model hold more in "working memory" without paging.
- **Retrieval** = disk access — load what is needed when it is needed.
- **Tool use** = peripherals — expand what the system can *do* beyond text output.
- **Agents** = processes — run multiple cognitive tasks that coordinate toward a goal.

## Implications for RAG

RAG is "disk access" in the LLM OS. The corpus is long-term memory; the context window is RAM; the retrieval step is the page-in. Thinking this way suggests:
- You do not need to fit everything in context. Design the retrieval so the model can page in what it needs, when it needs it.
- Hierarchical retrieval (summary → detail) is analogous to CPU cache levels.
- Caching (prompt caching, KV cache) is analogous to CPU cache — re-use hot state.

## Limits of the analogy

- LLMs are stateless between calls; traditional CPUs are not.
- "Execution" is soft / probabilistic — no deterministic instruction set.
- No clear equivalent of interrupts, memory protection, or real-time scheduling (yet).

## Why it shows up in a portfolio corpus

Karpathy's framing has become the de facto vocabulary among senior AI engineers. Interviewers use terms like "LLM OS," "context as RAM," "retrieval as paging" casually. Knowing the reference is table stakes for AI engineer roles.

## Connection to agents

If the LLM is the CPU, then agents are processes. A well-designed agent system has:
- A scheduler (who runs next).
- Shared memory (common state, message bus).
- Isolation (sub-agents don't trample each other's context).
- IPC (tool calls between agents, structured message passing).

These are standard OS concepts. The LLM OS frame says: solve agent architecture problems by borrowing solutions from 50 years of OS research, not by reinventing them.
