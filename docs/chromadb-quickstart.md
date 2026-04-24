# ChromaDB Quickstart — Summary

**Source:** Chroma documentation, "Getting started"
**URL:** https://docs.trychroma.com/
**Type:** Library documentation (summary, own words)

## What Chroma is

ChromaDB is an open-source, embedded vector database. "Embedded" meaning it runs in-process like SQLite — no separate server needed for dev/demo work. A client-server mode exists for production.

## Three core concepts

- **Client.** The entry point (`chromadb.Client()` for in-memory or `chromadb.PersistentClient(path=...)` for on-disk).
- **Collection.** A named group of vectors + metadata. Think of it as a table.
- **Item.** A vector + optional text + metadata, keyed by a string id.

## Minimal example

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
col = client.get_or_create_collection("my_docs")

col.add(
    documents=["RAG retrieves chunks then generates.", "MMR reranks for diversity."],
    metadatas=[{"source": "rag-paper.md"}, {"source": "mmr-notes.md"}],
    ids=["doc_1", "doc_2"],
)

results = col.query(query_texts=["how does RAG work?"], n_results=2)
```

## Embedding handling

Chroma can embed documents automatically (default model: `all-MiniLM-L6-v2`) OR accept pre-computed vectors via the `embeddings=[...]` argument on `add`/`query`. Pass pre-computed vectors when you want to control the embedding model externally — e.g., in LlamaIndex pipelines where `Settings.embed_model` is already configured.

## Persistence

`PersistentClient(path=...)` stores everything under that directory:
- SQLite metadata DB.
- Vector segments.
- HNSW indexes per collection.

The directory is portable — copy it, zip it, deploy it with your app. On HF Spaces, checking in the chroma_db folder is a valid pattern for static demo corpora.

## Metadata filtering

Queries support `where` clauses on metadata:
```python
col.query(
    query_texts=["RAG"],
    n_results=5,
    where={"source": "rag-paper.md"},
)
```

Operators: `$eq`, `$ne`, `$gt`, `$lt`, `$in`, `$nin`, `$and`, `$or`. Combine with full-text search via `where_document`.

## Collections vs. one big table

Use multiple collections when:
- Different corpora need different embedding models or chunking strategies.
- You want hard isolation (multi-tenant, different permissions).

Otherwise, one collection with metadata filters is simpler.

## Scaling notes

- HNSW index in memory: fast, but memory grows with corpus size.
- For >1M vectors: consider Chroma Cloud, or switch to Qdrant / pgvector with HNSW on disk.
- Chroma's in-process mode is wonderful for < 100k-vector demos; less wonderful for production-scale serving.

## Gotchas

- `add` vs `upsert`: `add` errors if an id exists. Use `upsert` or `update` for idempotent pipelines.
- Deleting a collection and recreating with the same name requires a fresh client in some versions — restart if you see stale caches.
- LlamaIndex's Chroma integration expects the collection to be created before binding — see the indexer example in this repo.

## Why it is a good portfolio choice

- Zero infrastructure to demo (single `PersistentClient`).
- One-line deploy on HF Spaces (check in the db directory).
- Same code upgrades to production by swapping `PersistentClient` for `HttpClient`.
- Recognizable to recruiters without explanation.
