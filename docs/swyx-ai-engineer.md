# Swyx — The Rise of the AI Engineer

**Source:** Shawn "swyx" Wang, "The Rise of the AI Engineer"
**URL:** https://www.latent.space/p/ai-engineer
**Type:** Blog summary (own words, based on swyx's public writing)

## The thesis

A new role has emerged that is neither "ML researcher" nor "software engineer":

- **ML Researcher** — trains and fine-tunes models. Works in research orgs. PhD-tier math, lots of GPU time.
- **AI Engineer** — builds products *on top of* foundation models. Works at product companies. Stack: API calls, RAG, prompt engineering, evals, tool use, deployment.
- **Software Engineer** — writes traditional code. Does not wake up thinking about tokens per second.

Swyx's point: the middle category barely existed before 2023 and is now one of the fastest-growing roles in tech, because:
1. Foundation models became good enough to ship products on via API.
2. You don't need a PhD to be productive — you need systems thinking, product sense, and engineering discipline.
3. The work is fundamentally different from training models *or* writing CRUD apps.

## What an AI engineer actually does

- **Ship LLM-powered features into products.** Chat, Q&A, extraction, summarization, generation.
- **Design prompt pipelines.** System prompts, few-shot, tool descriptions, output parsing.
- **Build RAG systems.** Corpus, chunking, retrieval, reranking, generation, citations.
- **Write evals.** Test sets, LLM-as-judge, offline + production monitoring.
- **Orchestrate agents.** Tool use, planning, error recovery, multi-agent coordination.
- **Optimize cost and latency.** Caching, model selection, streaming, batching.
- **Handle AI-specific failure modes.** Hallucination, prompt injection, unsafe content, rate limits.

## Skills that differentiate

- **API fluency.** Anthropic, OpenAI, Google, Cohere SDKs. Knowing what each provider does well (pricing, context, caching, tool use quirks).
- **Retrieval intuition.** When dense beats sparse, when to rerank, when chunking is the bug.
- **Eval discipline.** Not treating eval as an afterthought.
- **Product judgment.** When the LLM is the wrong solution. Not everything benefits from AI.

## Skills that *don't* differentiate (anymore)

- Using LangChain or LlamaIndex. These are commodities now.
- Running a demo on Hugging Face Spaces. Zero-infrastructure demos are table stakes.
- "I built a chatbot." Everyone has.

## Where the role sits org-wise

- Between data/ML teams and product engineering.
- Reports into engineering or product, not research.
- Work output: shipped features, not papers.
- Performance measured in user metrics (retention, task completion) and system metrics (latency, cost, accuracy), not benchmark numbers.

## Hiring signals swyx calls out

- A public portfolio with *working* demos, not just code.
- Evidence of eval thinking — not just "I built X" but "here's how I measured X."
- Understanding of model economics — tokens, caching, batching.
- A take on tradeoffs ("I'd do X differently next time") rather than uncritical hype.

## For junior candidates

Three things to build into portfolio:
1. **A working RAG system** with eval numbers in the README. (This project.)
2. **An agent or tool-using system** that does something non-trivial.
3. **An eval-focused project** — take an existing LLM system and write a rigorous eval harness around it.

Bonus: write about your decisions. Public blog posts or even good README sections signal AI engineer thinking more clearly than code alone.

## Takeaway

"AI engineer" is not a watered-down ML engineer. It is a distinct role defined by shipping products, not training models. The job market is increasingly hiring for this specific pattern — look for the job title, but more importantly, for the JD that describes RAG, prompt pipelines, evals, and shipping. Those are the real signals.
