# RAG Document Q&A — Spec

**Project:** `rag-qa`
**Status:** Phase A — Spec
**Author:** Andrey Ovsyannikov (ALchemt)
**Target role signal:** Junior AI Engineer / Generative AI Specialist / AI Automation Developer

## Problem

Recruiters scanning GitHub for Junior AI candidates see dozens of "upload a PDF, get an answer" clones. None of them ship evaluation, production-grade deploy, or a focused knowledge domain. This project is a working, public RAG system over a curated **AI Engineering knowledge base** (foundational papers + practical cookbooks) with a measured accuracy baseline.

It is a portfolio artifact, not a product — judged on clarity, evaluation rigor, and deploy quality.

## User

Hypothetical: a junior dev ramping up on AI engineering who wants to query "what is RAG?", "how does reranking work?", "when use Claude tool use vs function calling?" and get a grounded answer with citations.

Real: the recruiter reading the README in under 5 minutes.

## Scope

### In

- Corpus of 20–30 curated documents (papers + practical guides, all freely available)
- Chunk → embed → store (ChromaDB, local)
- Retrieve top-k with MMR reranking
- Generate answer with Claude API (+ prompt caching on system prompt)
- Citations with source link + chunk preview
- Streamlit UI: ask box + answer + expandable sources
- Eval harness: 30 Q&A test set, metrics in README
- Deploy: Hugging Face Spaces (free tier)

### Out

- Multi-tenant / user auth
- Document upload UI (static corpus only — simpler story, more focused)
- Fine-tuning / embedding training
- Agentic retrieval (planned as separate portfolio project #2–4)

## Architecture

```
 ┌──────────────┐     ┌──────────────┐     ┌─────────────────┐
 │ Corpus (/docs)│ ──▶ │ Chunker      │ ──▶ │ ChromaDB        │
 │ 20-30 .md/.txt│     │ LlamaIndex   │     │ (persisted)     │
 └──────────────┘     │ SentenceSplit│     └────────┬────────┘
                      └──────────────┘              │
                                                    ▼
 ┌──────────────┐     ┌──────────────────┐   ┌─────────────┐
 │ Streamlit UI │ ──▶ │ Query pipeline   │──▶│ Retriever   │
 │ ask box +    │     │ - embed question │   │ top-k=5     │
 │ sources      │     │ - MMR rerank     │   │ + MMR       │
 └──────┬───────┘     │ - Claude call    │   └──────┬──────┘
        │             │   (w/ caching)   │          │
        │             └────────┬─────────┘          ▼
        │                      │              ┌─────────────┐
        │                      ▼              │ Chunks +    │
        │             ┌────────────────┐      │ metadata    │
        └────────────▶│ Answer + cites │◀─────┤ (source,URL)│
                      └────────────────┘      └─────────────┘
```

## Tech choices

| Layer | Choice | Why |
|---|---|---|
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` | free, local, good enough baseline; swap-in OpenAI showcased in eval |
| Vector store | ChromaDB (local, persisted) | zero-infra, HF Spaces-friendly, easy to show in repo |
| Chunking | LlamaIndex SentenceSplitter, 512 tokens, 50 overlap | conservative baseline, easily tunable |
| Retrieval | top-k=5 with MMR reranking (lambda 0.5) | diversity vs relevance shown in eval |
| LLM | Claude Sonnet 4.6 (`claude-sonnet-4-6`) | default; haiku 4.5 tested in eval for cost/quality tradeoff |
| Prompt caching | Anthropic prompt caching on system prompt + corpus context | demonstrates API feature awareness, real cost saving |
| UI | Streamlit | fastest path, HF Spaces native |
| Deploy | Hugging Face Spaces (streamlit template) | free, public URL, git-based deploy |
| Eval | 30 Q&A test set, pandas, mlflow-lite csv | accuracy (manual rubric 0/1/2), latency, token cost |

## Corpus (v1, ~25 docs)

Foundational / reference:
1. "Attention Is All You Need" (excerpt: architecture section)
2. RAG paper (Lewis et al. 2020) abstract + method
3. ReAct paper — reasoning + acting
4. Chain-of-Thought paper excerpt
5. Toolformer paper excerpt

Practical / cookbooks:
6. Anthropic docs: prompt caching
7. Anthropic docs: tool use
8. Anthropic docs: extended thinking
9. Anthropic docs: citations
10. OpenAI cookbook: embeddings basics
11. LlamaIndex docs: retriever modes
12. LlamaIndex docs: response synthesis
13. ChromaDB quickstart
14. LangChain vs LlamaIndex comparison note
15. HF Spaces deploy guide

Karpathy / opinionated:
16. Karpathy "LLM OS" thread
17. Karpathy "Software 2.0"
18. Karpathy "State of GPT" talk notes

Evaluation / ops:
19. Evaluating LLMs — overview
20. Hallucination detection methods
21. RAGAS framework notes

Extras:
22-25. 3-5 recent AI-engineering blog posts (Hamel Husain, Eugene Yan, Swyx)

All sources: public, attribution in README, license-respecting excerpts (<500 words per doc where fair use applies).

## Evaluation plan

- **30 questions** in `eval/test_set.jsonl`: 15 "what is X" (factoid), 10 "how do I" (procedural), 5 "compare X vs Y" (reasoning).
- For each: manual gold answer + expected citation source.
- Rubric (per Q, scored by me, not LLM-as-judge for v1):
  - 0 = wrong or hallucinated
  - 1 = partially correct
  - 2 = correct + correctly cited
- Report in README:

| Config | Accuracy (mean score /2) | Hallucination rate | p50 latency | $/query |
|---|---|---|---|---|
| baseline (k=5, MMR 0.5, sonnet-4-6) | TBD | TBD | TBD | TBD |
| k=3 no MMR | TBD | TBD | TBD | TBD |
| haiku-4-5 | TBD | TBD | TBD | TBD |

- Hallucination = answer contains fact not in any retrieved chunk.
- Cost measured via Anthropic usage.input_tokens / output_tokens.

## Milestones

| Phase | Deliverable | Time budget |
|---|---|---|
| A Spec (done) | this file | 30 min |
| B MVP | repo scaffold, hello-world indexer + query, local streamlit run | 2 h |
| B' Deploy | HF Spaces live URL, minimal UI | 1 h |
| C Corpus + ingestion | 25 docs in /docs, index built, queries work | 1.5 h |
| C' Eval | 30 Q&A set, baseline table filled | 2 h |
| D Polish | README final, GIF demo, badges | 1 h |

Total: ~8 h over 2–3 sessions.

## Success criteria

- HF Spaces URL returns a working demo in <10 s cold start
- 5 example queries work end-to-end with citations
- README contains a filled evaluation table (not TBD)
- Repo passes `ruff check` and has a 1-command local run instructions

## What I'd do differently (filled in README at Phase D)

Placeholder — filled honestly after shipping. Likely candidates: add reranker model, LLM-as-judge for scalability, separate retrieval/generation eval, try hybrid BM25+dense.

## Out of scope for v1 (maybe v2)

- User-uploaded docs
- Multi-turn conversation memory
- Agentic retrieval (plan → search → synthesize loop)
- Self-hosted embedding server
- Advanced reranking (Cohere rerank, cross-encoder)
