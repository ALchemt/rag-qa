# LlamaIndex Retriever Modes — Summary

**Source:** LlamaIndex documentation, "Retrieval"
**URL:** https://docs.llamaindex.ai/en/stable/module_guides/querying/retriever/
**Type:** Library documentation (summary, own words)

## What a retriever is

In LlamaIndex, a retriever takes a query and returns a list of `NodeWithScore` objects from an index. It is the R in RAG — the part that decides which chunks to send to the generator.

## Built-in retriever modes

### Vector retriever (default)

Embed the query, do dense similarity search against the vector store, return top-k. Fast, simple, good baseline.

```python
retriever = index.as_retriever(similarity_top_k=5)
```

### BM25 retriever

Classic sparse keyword search over the corpus. Strong for exact matches (API names, error codes, IDs) where dense embeddings under-perform.

```python
from llama_index.retrievers.bm25 import BM25Retriever
retriever = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=5)
```

### MMR (Maximal Marginal Relevance)

Re-ranks dense results to trade off relevance vs. diversity. Useful when top-k contains near-duplicates.

```python
from llama_index.core.vector_stores.types import VectorStoreQueryMode
retriever = index.as_retriever(
    similarity_top_k=5,
    vector_store_query_mode=VectorStoreQueryMode.MMR,
    vector_store_kwargs={"mmr_threshold": 0.5},  # lambda in the MMR formula
)
```

`mmr_threshold` closer to 1.0 = pure relevance; closer to 0.0 = pure diversity. 0.5 is a common default.

### Hybrid retriever

Combines dense + sparse (BM25) and fuses the scores. Typically via Reciprocal Rank Fusion (RRF).

```python
from llama_index.core.retrievers import QueryFusionRetriever
retriever = QueryFusionRetriever(
    [vector_retriever, bm25_retriever],
    similarity_top_k=5,
    num_queries=1,
    mode="reciprocal_rerank",
)
```

Hybrid is the single highest-ROI upgrade over pure-dense for most production RAG systems.

### Auto-merging retriever

Works with hierarchical node structures: retrieves leaf nodes but merges neighbors back into parent chunks when enough of a parent is relevant. Good for long-form documents where context is split across chunks.

### Recursive retriever

For complex index structures (index of indices). Retrieval returns summary nodes that point to deeper indices; the retriever recursively descends. Useful in multi-document, multi-collection setups.

## Rerankers (post-retrieval)

Retrievers return candidates; rerankers refine them. LlamaIndex supports plug-in rerankers via the `node_postprocessors` list on the query engine:
- `SentenceTransformerRerank` — cross-encoder, local, slow but accurate.
- `CohereRerank` — hosted, fast, API-based.
- `LLMRerank` — ask an LLM to rank candidates; expensive, highest quality.

## Choosing a retriever

| Scenario | Start with |
|---|---|
| Generic semantic Q&A | vector + MMR |
| Codebase / exact identifiers | hybrid (BM25 + dense) |
| Long documents, summarization | auto-merging |
| Multi-corpus (product docs + tickets + blog) | recursive |
| Quality above all, latency OK | vector → top-20 → cross-encoder rerank → top-5 |

## Anti-patterns

- Tuning `similarity_top_k` to huge numbers (50+) without a reranker — wastes context budget.
- Using MMR when you already have diverse data — just use top-k.
- Skipping BM25 for technical corpora. Dense embeddings are bad at exact-string recall.
