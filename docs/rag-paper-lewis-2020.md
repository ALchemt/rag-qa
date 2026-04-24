# RAG: Retrieval-Augmented Generation — Summary

**Source:** Lewis et al. 2020, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (NeurIPS)
**URL:** https://arxiv.org/abs/2005.11401
**Type:** Foundational paper (summary, own words)

## Problem

Pretrained language models store facts in their parameters, but:
- Knowledge is frozen at training time.
- Updating the model is expensive.
- Facts are hard to attribute — the model cannot say *where* a claim came from.

## Solution

RAG couples a pretrained seq2seq generator (BART) with a non-parametric memory (a dense vector index of Wikipedia passages). At inference time:

1. Encode the question into a query vector.
2. Retrieve top-k passages from the index (Maximum Inner Product Search via FAISS).
3. Condition the generator on the question + retrieved passages.
4. Generate the answer.

## Two variants

- **RAG-Sequence:** one set of passages retrieved, used for the whole output sequence.
- **RAG-Token:** different passages can drive different output tokens — more flexible, marginally better for long answers.

## What they retrieve

Wikipedia, chunked into 100-word passages, embedded with DPR (Dense Passage Retriever — a dual-encoder BERT model fine-tuned on QA).

## Training

The generator and the query encoder are fine-tuned jointly; the passage encoder is frozen. This avoids re-indexing Wikipedia every training step.

## Results

- Beats closed-book models (T5, BART) on Natural Questions, TriviaQA, WebQuestions.
- Competitive with extractive QA models while being generative.
- Critically: answers can be traced back to retrieved passages — a huge usability win.

## Why it matters

RAG is the pattern behind almost every LLM-over-private-data application today. The specific model choices (BART, DPR) are dated, but the architectural blueprint — **retrieve, then generate** — is unchanged. Modern systems swap in:
- Instruction-tuned LLMs (Claude, GPT-4) instead of BART.
- Sentence-transformers / text-embedding-3 / Cohere embeddings instead of DPR.
- Hybrid retrieval (BM25 + dense) and cross-encoder reranking.

## Limits the paper acknowledges

- Retrieval quality bounds generation quality — garbage in, garbage out.
- Latency overhead (embedding + search before generation).
- Fixed k means you cannot adaptively decide how much evidence to fetch.

These limits motivated later work: agentic retrieval, query rewriting, Self-RAG, RAG-Fusion.
