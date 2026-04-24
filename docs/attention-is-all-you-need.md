# Attention Is All You Need — Summary

**Source:** Vaswani et al. 2017, "Attention Is All You Need" (NeurIPS)
**URL:** https://arxiv.org/abs/1706.03762
**Type:** Foundational paper (summary, own words)

## Core idea

The Transformer architecture replaces recurrence (RNN) and convolution entirely with attention mechanisms. Input sequences are processed in parallel, not step-by-step, which makes training dramatically faster on GPUs.

## Architecture

- **Encoder-decoder stack.** Both are stacks of 6 identical layers.
- **Encoder layer:** multi-head self-attention + feed-forward network, each wrapped in a residual connection + layer norm.
- **Decoder layer:** same, plus a masked self-attention sublayer and an encoder-decoder attention sublayer.
- **Multi-head attention:** attention is computed h times in parallel with different learned projections, then concatenated. h=8 in the base model.

## Scaled dot-product attention

`Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V`

- Q (query), K (key), V (value) are linear projections of the input.
- Dividing by `sqrt(d_k)` keeps gradients stable as dimensions grow.

## Positional encoding

Since the model has no recurrence, position is injected via sinusoidal encodings added to the input embeddings. The paper also notes that learned positional embeddings work comparably.

## Why it matters for RAG

- Attention is the primitive behind today's LLMs (GPT, Claude, Llama).
- Retrieval-augmented systems depend on embedding models derived from Transformer encoders (e.g., BERT, sentence-transformers).
- Long-context models (100k+ tokens) are engineering extensions of this same architecture — understanding the O(n^2) attention cost explains why retrieval is needed in the first place.

## Key numbers

- Base model: 65M parameters, trained on WMT 2014 EN-DE (~4.5M sentence pairs).
- BLEU 28.4 on EN-DE, 41.0 on EN-FR — state of the art at the time, for a fraction of the training cost of prior sequence-to-sequence models.

## Takeaway

The Transformer's contribution is not a specific model but a design pattern: stacked attention layers with residual connections. Every modern LLM, every embedding model used in RAG, and every reranker inherits from this blueprint.
