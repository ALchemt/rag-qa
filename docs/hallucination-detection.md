# Hallucination Detection — Methods

**Source:** Practitioner synthesis; see Ji et al. "Survey of Hallucination in Natural Language Generation" for deeper references
**URL:** https://arxiv.org/abs/2202.03629
**Type:** Methods overview (summary, own words)

## Definition

A hallucination is output that is not supported by the input context or is factually wrong despite being fluent. Two flavors:
- **Intrinsic:** the output contradicts the source material provided to the model.
- **Extrinsic:** the output introduces facts not present in the source. May be right, may be wrong; impossible to verify from the input alone.

In RAG systems, the hallucination you care about most is *extrinsic facts not found in any retrieved chunk*.

## Why LLMs hallucinate

- Pretraining optimizes fluency, not truth.
- The model has no knob for "I don't know" — it always generates something.
- Retrieval can provide unrelated or incomplete context, and the model fills gaps from its prior.

## Detection methods

### 1. Grounding check (deterministic)

For each factual claim in the answer, check whether a substring / entailment exists in the retrieved chunks.

- **Exact substring match:** brittle, easy to evade (paraphrases count as hallucination incorrectly).
- **Semantic match:** embed each claim + each chunk sentence; check cosine similarity. Threshold-based.
- **NLI-based:** natural language inference model (RoBERTa-MNLI, DeBERTa) classifies each claim as entailed / contradicted / neutral given the retrieved context. Strong baseline.

### 2. LLM-as-judge faithfulness

Prompt a strong model: "Given this question, this answer, and these sources, does the answer contain any claim not supported by the sources? Respond with yes/no and the unsupported claim."

- Pros: flexible, handles paraphrase.
- Cons: biased by the judge's prior knowledge, costs another LLM call.

### 3. Self-consistency

Sample N answers to the same question. Claims that appear in all N are more likely grounded; claims that appear in one are more likely hallucinated.

- Works especially well with temperature > 0 and chain-of-thought prompting.
- Expensive (N× cost); rarely worth it in production unless accuracy is life-or-death.

### 4. Uncertainty signals from the model

- **Token-level log probabilities.** Low-probability tokens in the answer often mark hallucinated content. Requires logprobs API access.
- **Perplexity of answer given context.** High perplexity on an answer that *should* follow from context suggests the model went off-source.

### 5. Source-citation audits

Force the model to cite sources inline, then post-process:
- Parse citations, look them up in the corpus.
- If any citation refers to a non-existent source or a source that does not contain the claim, flag as hallucinated.

Anthropic's Citations API bypasses manual parsing: server-side enforcement guarantees citations point at real spans.

## Prevention (better than detection)

- **Stronger retrieval.** The single biggest lever. If the right passage is in context, the model usually uses it.
- **"Not found" prompts.** Instruct the model to respond "I cannot find this in the provided context" for unsupported questions. Effective for well-aligned models (Claude, GPT-4).
- **Short, grounded outputs.** Longer generations drift. Bullet points + citations structure reduces drift.
- **Lower temperature.** Temperature 0 reduces creative embellishment. Default for RAG synthesis.

## Metrics to track

- **Hallucination rate:** fraction of answers containing ≥ 1 unsupported claim.
- **Coverage:** fraction of "not answerable from corpus" questions where the model correctly refused vs. invented.
- **Precision of citations:** fraction of cited claims actually supported by the cited source.

## Takeaway

Hallucination detection is not a solved problem. In practice, production RAG systems combine *prevention* (better retrieval + grounded prompting) with *detection* (NLI or LLM-judge on a sample of outputs, plus user-visible source citations) and *user feedback loops* (thumbs-down + follow-up audits).
