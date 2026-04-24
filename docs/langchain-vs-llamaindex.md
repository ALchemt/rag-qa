# LangChain vs LlamaIndex — Comparison

**Source:** Own comparison based on both libraries' docs and practical use
**URL:** https://docs.langchain.com/ and https://docs.llamaindex.ai/
**Type:** Opinion / comparison note

## Short version

- **LlamaIndex** is a data / retrieval framework that also does orchestration.
- **LangChain** is an orchestration framework that also does retrieval.

For pure RAG over your own documents, LlamaIndex has the shorter path. For general LLM application wiring (chains, agents, tools, memory, callbacks), LangChain has the broader surface.

## Where they overlap

Both provide:
- Document loaders (PDF, HTML, Notion, Slack, etc.).
- Text splitters / chunkers.
- Vector store integrations (Chroma, Pinecone, Qdrant, etc.).
- Embedding model wrappers.
- LLM wrappers.
- Retriever → generator pipelines.

If you only use these overlapping pieces, either library gets the job done. Choose by which API you prefer.

## Where LlamaIndex wins

- **Index structures.** First-class support for vector indexes, keyword indexes, summary indexes, tree indexes, composable indexes of indexes. Useful for complex corpora (e.g., "search docs first, then tickets, then blog").
- **Retrieval modes.** More built-in retriever variations (MMR, auto-merging, recursive) than LangChain ships.
- **Response synthesizers.** `refine`, `compact`, `tree_summarize` as first-class objects with tuning knobs. LangChain's equivalent (`stuff`, `map_reduce`, `refine`) exists but feels older.
- **Evaluation utilities.** `llama_index.core.evaluation` has ready-made faithfulness, relevance, and correctness evaluators with LLM-as-judge built in.
- **Observability.** LlamaIndex Observability + llama-cloud give structured traces out of the box.

## Where LangChain wins

- **Tool ecosystem.** Hundreds of ready-made integrations — every API, every vendor, every obscure database.
- **LangGraph.** Explicit state-machine-based agent orchestration. Cleaner than LlamaIndex's agent classes once you have >3 nodes.
- **LCEL (LangChain Expression Language).** Concise pipe-style composition of chains (`prompt | llm | parser`). Either you love it or you don't.
- **Community size.** More tutorials, more Stack Overflow answers, more third-party tools (LangSmith, LangServe, LangFuse).
- **Non-RAG agent workflows.** Multi-tool agents, deep tool-calling loops, async streaming chains are better paved in LangChain.

## Anti-patterns to avoid

- Using both in the same project. Each brings its own abstractions for retrievers, prompts, chains; mixing them creates two sources of truth.
- Choosing by vibe. If your task is "RAG over a static corpus," LlamaIndex; if it is "agent with 5 tools + retrieval," LangChain. Don't over-think it.

## Portfolio choice

For a focused RAG Q&A demo (this project), LlamaIndex + ChromaDB is the shortest, cleanest path:
- `SimpleDirectoryReader` → `SentenceSplitter` → `ChromaVectorStore` → `VectorStoreIndex` is 4 method calls.
- Retriever modes (MMR, top-k) are parameters, not new classes.
- No chain plumbing boilerplate.

For an agent portfolio project with tool use + multi-step planning, LangChain + LangGraph would be the right pick.

## Caveat

Both libraries iterate fast. APIs change between minor versions. Pin versions in your requirements.txt, and treat blog posts older than 6 months as historical — they may not compile.
