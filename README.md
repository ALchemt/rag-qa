---
title: RAG Document Q&A
emoji: 📚
colorFrom: indigo
colorTo: purple
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
license: mit
---

# RAG Document Q&A

> Grounded Q&A over a curated AI-engineering knowledge base. Built to show RAG in practice — retrieval, reranking, citations, evaluation.

## Problem

A junior AI engineer wants to query "what is RAG?", "how does reranking work?", "when use Claude tool use vs extended thinking?" and get a **grounded answer with citations** — not a generic ChatGPT response that might be wrong.

## Demo

**Live:** 🔗 [**alchemt-rag-qa.hf.space**](https://alchemt-rag-qa.hf.space/) (hosted on HF Spaces, free CPU tier)

**Repo:** [github.com/ALchemt/AgenticSystem/tree/main/ai-portfolio/rag-qa](https://github.com/ALchemt/AgenticSystem/tree/main/ai-portfolio/rag-qa)

**5 example questions the demo handles:**
1. What is RAG and what problem does it solve?
2. How does MMR reranking work?
3. When should I use Claude tool use vs extended thinking?
4. What is chain-of-thought prompting?
5. How do I persist a ChromaDB collection?

## Architecture

```
docs/*.md ─▶ SentenceSplitter (512/50) ─▶ MiniLM embed ─▶ ChromaDB (persisted)

question ─▶ embed ─▶ retrieve top-5 w/ MMR ─▶ LLM (OpenAI-compatible)
                                              ─▶ answer + [source] citations
```

See [spec.md](./spec.md) for design decisions and tradeoffs.

## Tech stack

| Layer | Choice |
|---|---|
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (local, CPU) |
| Vector store | ChromaDB (local, persisted) |
| Chunking | LlamaIndex SentenceSplitter (512 tokens, 50 overlap) |
| Retrieval | top-k=5 with MMR reranking (λ=0.5) |
| LLM | `openai/gpt-oss-120b:free` via OpenRouter (provider-agnostic — Groq / HF Inference also supported) |
| UI | Streamlit |
| Eval | 30 Q&A test set, LLM-as-judge auto-scoring, pandas CSV |

**LLM choice note.** Generator is provider-agnostic via the OpenAI-compatible SDK — set any of `GROQ_API_KEY`, `OPENROUTER_API_KEY`, or `HF_TOKEN` in `.env` and it auto-picks. Originally specced on Claude with prompt caching; switched to free tiers to ship a public demo without a paid API. Swapping back to Claude (or any OpenAI-compatible provider) is a one-line env change.

## Corpus

25 curated summaries (own words, with attribution) — foundational papers (Transformer, RAG, ReAct, CoT, Toolformer), Anthropic docs (prompt caching, tool use, extended thinking, citations), practical guides (LlamaIndex, ChromaDB, HF Spaces, embeddings, MMR), and Karpathy / Hamel / Eugene Yan / swyx essays. Full list in [spec.md](./spec.md#corpus-v1-25-docs).

Every corpus file carries a source link in its header. Summaries are paraphrased and attributed, not verbatim copies.

## Evaluation

Baseline: 30 questions, generator `openai/gpt-oss-120b:free` via OpenRouter, k=5, MMR λ=0.5.

| Metric | Value |
|---|---|
| **Mean score** | **1.73 / 2** (87%) |
| **Hallucination rate** | **0%** — no fabricated claims across 30 answers |
| p50 latency (end-to-end) | 6.5s (retrieval + 120B reasoning model) |
| Mean tokens | in=2,128 / out=306 per query |

**By question type:**

| Type | Count | Mean score |
|---|---|---|
| factoid ("what is X") | 15 | 2.00 |
| procedural ("how do I X") | 10 | 1.50 |
| compare ("X vs Y") | 5 | 1.40 |

The gap is not knowledge — the procedural/compare answers are factually correct. The gap is **citation format compliance**: the system prompt asks for inline `[source_filename]` but the 120B model often uses Unicode brackets `【…】` or skips the citation entirely on procedural/compare answers. Score 1 penalty is for missing the format, not for being wrong.

### Rubric

- **0** = wrong, or contradicts the gold answer
- **1** = factually correct but missing an inline citation in the expected format
- **2** = factually correct AND cites at least one relevant retrieved source inline

### Judge methodology (honest version)

- Rows **q1–q12**: scored by `openai/gpt-oss-120b:free` as LLM-as-judge. OpenRouter's free tier (50 req/day) ran out mid-run.
- Rows **q13–q30**: scored by Claude Opus 4.7 acting as a second judge in the authoring session, using the same rubric.

This is a **known self-bias limitation**. See "What I'd do differently" for the fix path (split-judge, human validation sample).

Test set: `eval/test_set.jsonl`. Results: `eval/results_<ts>_judged.csv`. Re-run locally:
```bash
python -m eval.run_eval                        # generates eval/results_<ts>.csv
python -m eval.judge eval/results_<ts>.csv     # adds score / hallucinated columns
```

## Quick start (local)

```bash
git clone <repo> && cd rag-qa
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env — set ONE of: GROQ_API_KEY, OPENROUTER_API_KEY, HF_TOKEN

python -m src.indexer     # builds chroma_db/ from docs/
streamlit run app.py       # opens http://localhost:8501
```

## Deploy to HF Spaces

1. Create a Streamlit Space on huggingface.co.
2. Clone the Space repo.
3. Copy this project's files in (or push from here).
4. Commit `chroma_db/` so cold start is fast (first build takes ~3 min otherwise).
5. Under Space Settings → Variables, add secret `HF_TOKEN` (same token with Inference access).
6. Push. HF builds and serves on `<user>-rag-qa.hf.space`.

## What I'd do differently

- **Judge ≠ generator.** v1 uses the same model as generator and judge — a known self-bias. Swap in a second provider (e.g. Groq Llama 3.3 as judge, OpenRouter gpt-oss-120b as generator) to break this. Cheap fix, postponed to v2 for scope.
- **Human validation pass.** Current numbers are auto-scored. Pick 10 random rows and human-score; report judge-vs-human agreement rate. Under 80% means the judge is unreliable.
- **Cross-encoder reranker** (BGE or Cohere rerank) as a second-stage step — MMR alone is an approximation of diversity, not relevance.
- **Separate retrieval-eval from generation-eval.** Recall@k for retrieval, faithfulness for generation — they fail differently. Current combined rubric hides whether a 0-score was bad retrieval or bad synthesis.
- **Hybrid BM25 + dense retrieval** for exact-match queries (API names, parameter keys) — Eugene Yan's data is that this is the highest-ROI upgrade for technical corpora.
- **Claude with prompt caching** when budget allows — the caching economics change the cost curve meaningfully for repeat-query RAG.

## License

MIT.

---

Portfolio project by Andrey Ovsyannikov ([github.com/ALchemt](https://github.com/ALchemt)).
Part of a 4-project AI portfolio — see parent directory for others.
