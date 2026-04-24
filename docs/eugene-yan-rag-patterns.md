# Eugene Yan — RAG Patterns & Pitfalls

**Source:** Eugene Yan, "Patterns for Building LLM-based Systems & Products"
**URL:** https://eugeneyan.com/writing/llm-patterns/
**Type:** Blog summary (own words, based on Eugene's public writing)

## The seven practical patterns

Eugene Yan's influential post groups the techniques for building LLM systems into seven patterns. Four of them are directly relevant to RAG.

### 1. Evals

Before anything else, build an eval harness. See separate notes on `hamel-husain-evals.md` and `evaluating-llms-overview.md` in this corpus. Eugene's framing: **"You can't improve what you can't measure."**

### 2. RAG

Retrieval-Augmented Generation is the default pattern for letting an LLM answer over your private data. Key design decisions Eugene highlights:

- **Chunking.** 200–500 tokens with overlap is the common starting point. Better: chunk by structure (sections, functions, Q&A pairs) not by fixed size.
- **Retrieval.** Hybrid (BM25 + dense) beats pure dense for technical content. Reranking (cross-encoder) adds 5–15% quality at small cost.
- **Generation.** Use a stable system prompt — helps downstream caching and debugging. Instruct the model to cite sources; use citations API if available.

### 3. Fine-tuning

Three variants:
- **Full fine-tuning** — rarely worth it, mostly eaten by RAG or LoRA.
- **LoRA / PEFT** — cheap, targeted, good for style adaptation.
- **Instruction fine-tuning** — teach the model to follow a specific output format. Useful when prompt engineering stops scaling.

Eugene's guidance: *do RAG first*. Fine-tuning is for teaching the model *how* to behave. RAG is for *what* to know. Most teams need the "what," not the "how."

### 4. Caching

- **Prompt caching** (e.g., Anthropic's): reuse large static prefixes across calls.
- **Embedding caching**: memoize expensive embedding calls for repeat queries.
- **Answer caching**: exact-match lookup for frequently-asked questions.

Caching is the highest-ROI production optimization — 5–10× cost reduction is common.

## Eugene's pitfalls (RAG edition)

- **"Just stuff everything in context."** Works until context limits, then falls over silently.
- **Relevance ≠ accuracy.** Retrieved chunks can be relevant but not answer-bearing. MMR + reranking help; eval catches this.
- **Underestimating latency.** Embedding + retrieval + generation → easily 2–5 seconds end-to-end. Streaming UI hides this; pure API use cases cannot.
- **Over-engineering early.** A pure top-k dense retriever + one-shot Claude call is enough for 80% of use cases. Prove you need fancier before adding it.
- **Ignoring failure modes.** What happens when retrieval returns empty? When the model hallucinates despite good context? Production readiness = explicit plan for each.

## The "write it down" discipline

Eugene strongly advocates for writing decisions down as you build: why you chose chunk size X, why k=5, why hybrid vs. dense. Future-you (or a teammate) cannot reproduce the reasoning from git history alone. A single `design.md` per system is the cheapest and most-skipped tool.

## For a portfolio RAG demo

Takeaways specific to a resume project:

- **Show your eval.** A filled evaluation table in README is worth more than a glossy demo video. Recruiters who know RAG look for it.
- **Name the tradeoffs.** In `What I'd do differently`, list what you deliberately *did not* build (reranker, hybrid, multi-turn). Shows judgment, not just feature count.
- **Keep it small.** 25 docs, 30 questions, one retriever, one generator. A tight demo with measured numbers beats a sprawling one with TBDs.

## Takeaway

RAG is no longer novel; *rigor* is. The practitioners Eugene writes for have built production RAG — they want to see you've thought about chunking, evaluation, caching, and failure modes, not that you've stacked five frameworks.
