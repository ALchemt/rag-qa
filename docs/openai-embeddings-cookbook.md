# OpenAI Embeddings — Cookbook Summary

**Source:** OpenAI Cookbook, "Get embeddings" / "Question answering using embeddings"
**URL:** https://cookbook.openai.com/examples/question_answering_using_embeddings
**Type:** Vendor cookbook (summary, own words)

## Why embeddings

Embeddings turn text into vectors where semantic similarity becomes geometric proximity. Two pieces of text with similar meaning are close in vector space; unrelated texts are far apart. This is the substrate of every retrieval system built on dense search.

## OpenAI's embedding models

| Model | Dim | Note |
|---|---|---|
| `text-embedding-3-large` | up to 3072 | best quality, highest cost |
| `text-embedding-3-small` | up to 1536 | good quality, cheap |
| `text-embedding-ada-002` | 1536 | legacy; avoid for new work |

`text-embedding-3-*` support a `dimensions` parameter — truncate the vector with near-linear quality loss to save storage and speed up search.

## Typical pipeline

1. **Chunk.** Break documents into 200–500 token pieces. Paragraph-aware splitters work better than fixed-window.
2. **Embed.** Call the embeddings endpoint on each chunk; store the vector + chunk text + metadata.
3. **Index.** Put vectors into a vector DB (ChromaDB, pgvector, Pinecone, Qdrant, Weaviate).
4. **Query.** Embed the user's question; retrieve top-k closest chunks.
5. **Generate.** Pass retrieved chunks + the question to an LLM.

## Chunking tips from the cookbook

- Use a tokenizer, not a character count, to control chunk size.
- Keep a small overlap (50–100 tokens) so facts split across a chunk boundary aren't lost.
- Preserve metadata (source, section, URL) — you will need it for citations.

## Similarity metric

Cosine similarity is standard. OpenAI embeddings are already L2-normalized, so cosine == dot product. This means:
- No need to normalize again in your code.
- You can use the simpler/faster inner-product search mode in FAISS, Chroma, etc.

## Batch embedding

Send batches (e.g., 100 texts per call) to reduce request overhead. The endpoint supports batching natively — send an array of strings.

## Cost math

`text-embedding-3-small` is extremely cheap (~$0.02 per 1M tokens). For a 10M-token corpus, embedding costs are dollars, not hundreds. The cost side of RAG is almost always the generator, not the embeddings.

## Alternatives for free / local setups

- `sentence-transformers/all-MiniLM-L6-v2` — 384-dim, runs on CPU in a venv, zero cost. Quality is lower than OpenAI 3-large but adequate for most portfolio and prototype work.
- `BAAI/bge-base-en-v1.5` — MTEB-top open-source encoder, 768-dim, also CPU-runnable.

## Takeaway

Embeddings are a commodity input: choose dimensions and model based on cost/quality, and spend your attention on chunking strategy, reranking, and generation quality — those are where real RAG systems win or lose.
