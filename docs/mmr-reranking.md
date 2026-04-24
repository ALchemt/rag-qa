# MMR Reranking — Method Notes

**Source:** Carbonell & Goldstein 1998, "The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries"
**URL:** https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf
**Type:** Foundational method (summary, own words)

## Problem MMR solves

Pure top-k similarity retrieval often returns near-duplicates. If your corpus has 5 chunks that paraphrase the same fact, top-5 retrieval returns all 5 — and you've wasted 4 slots that could have held complementary information.

**MMR (Maximal Marginal Relevance)** re-ranks candidates to balance:
- Relevance: how close a chunk is to the query.
- Diversity: how different a chunk is from already-selected chunks.

## The formula

At each step, select the document `d` that maximizes:

```
MMR(d) = λ · Sim1(d, query) − (1 − λ) · max_{d' ∈ selected} Sim2(d, d')
```

- `λ = 1` → pure relevance (ignores diversity), equivalent to top-k.
- `λ = 0` → pure diversity (ignores relevance), selects maximally different docs with no regard for the question.
- `λ = 0.5` → balanced, common default.

## Algorithm

```
selected = []
candidates = top_n_by_similarity(query, n=20)   # n > k
while len(selected) < k:
    best = argmax_{d in candidates} MMR(d)
    selected.append(best)
    candidates.remove(best)
return selected
```

Note: you need a **larger candidate pool** than `k` — MMR is reranking, not initial retrieval. Typical: retrieve top-20, MMR-rerank to top-5.

## Where it helps

- Corpora with redundant content (FAQs, product docs with cross-referenced sections).
- Summarization-style tasks where you want *coverage* not *depth*.
- Multi-faceted questions ("compare X vs Y vs Z") where top-k by relevance returns all-X.

## Where it hurts

- Narrow technical queries where all top chunks are necessarily about the same topic — MMR may inject irrelevant diversity.
- Small k (k=2 or 3). The diversity term dominates; you lose a relevant chunk to gain a tangential one.
- Corpora with no duplication. Nothing to deduplicate; MMR is pure overhead.

## LlamaIndex implementation

```python
from llama_index.core.vector_stores.types import VectorStoreQueryMode
retriever = index.as_retriever(
    similarity_top_k=5,
    vector_store_query_mode=VectorStoreQueryMode.MMR,
    vector_store_kwargs={"mmr_threshold": 0.5},  # this is lambda
)
```

Note: LlamaIndex's `mmr_threshold` = λ from the formula. Higher threshold = more relevance, less diversity.

## ChromaDB implementation

Chroma supports MMR via the `query` method with `include` and post-processing, or through integrations like LlamaIndex's wrapper.

## Tuning λ

- Start at 0.5.
- If retrieved chunks feel too repetitive → lower λ (e.g., 0.3).
- If retrieved chunks feel off-topic → raise λ (e.g., 0.7).
- Tune on your eval set, not by feel.

## MMR vs. other rerankers

- **MMR:** classical, deterministic, no extra model. Cheap.
- **Cross-encoder reranker** (e.g., BGE reranker): neural, treats each query-doc pair with a strong classifier. Much better quality, ~100ms per pair.
- **LLM reranker:** ask an LLM to rank candidates. Highest quality, highest cost. Overkill for most.

MMR is the right default for free/low-infra demos. Upgrade to cross-encoder reranking when you have the latency budget and quality ceiling to justify it.

## Takeaway

MMR is a cheap, boring classical method that makes top-k retrieval visibly less stupid on redundant corpora. For a portfolio project, MMR is a compact signal that you understand retrieval is not just "embed and sort" — it has structure and tradeoffs.
