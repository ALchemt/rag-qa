# LlamaIndex Response Synthesis — Summary

**Source:** LlamaIndex documentation, "Response synthesis"
**URL:** https://docs.llamaindex.ai/en/stable/module_guides/querying/response_synthesizers/
**Type:** Library documentation (summary, own words)

## The problem

After retrieval you have N chunks + a question. How do you turn that into a final answer? Naively stuffing everything into a single LLM prompt works for small N, but breaks on context limits, loses quality on noisy chunks, and offers no path for refinement.

LlamaIndex abstracts this as the **response synthesizer** — a pluggable strategy for generating the final answer from retrieved nodes.

## Built-in modes

### `refine`

Process chunks one at a time. First chunk produces an initial answer. Each subsequent chunk refines it (`existing_answer + new_chunk → better_answer`).

- Pros: handles unlimited context, preserves all information.
- Cons: N LLM calls = N× latency and cost; quality degrades if later refinements are asked to "improve" an already-correct answer.
- Use when: answer quality matters more than latency; chunks vary in relevance.

### `compact`

Same as `refine`, but chunks are pre-packed into the biggest prompt that fits the model's context. Fewer LLM calls, still falls back to refinement if prompts overflow.

- Pros: fewer calls than pure `refine`, similar quality.
- Cons: still multi-pass for long documents.
- Use when: default for most production RAG.

### `tree_summarize`

Hierarchical: chunks are summarized pairwise into summaries, summaries summarized, etc., until a single answer remains.

- Pros: scales to huge N, parallelizable per level.
- Cons: summaries can lose specific facts; citation chain is muddied.
- Use when: corpus is large and the question is a summarization ("explain X in the docs").

### `simple_summarize`

Truncate retrieved chunks to fit one prompt, generate the answer in one LLM call.

- Pros: fast, cheap, one call.
- Cons: discards chunks past the context limit silently.
- Use when: k is small (e.g., top-3) and chunks are short.

### `no_text`

Return the retrieved nodes without generation. For pipelines that do their own synthesis.

### `accumulate` / `compact_accumulate`

Run the question against each chunk independently; concatenate (or compact-concatenate) the per-chunk answers. Useful when you want per-source answers ("what does each source say about X?").

## Choosing a synthesizer

| Scenario | Start with |
|---|---|
| Standard Q&A, top-5 chunks | `compact` |
| Summarize entire doc | `tree_summarize` |
| Small k, short chunks | `simple_summarize` |
| Per-source answers | `accumulate` |
| Ultra-careful refinement | `refine` |

## Custom synthesizers

Subclass `BaseSynthesizer`. The contract:
- Receive `query` + `nodes` (List[NodeWithScore]).
- Return a `Response` object (text + source nodes + metadata).

Common custom pattern: re-rank chunks by LLM relevance before synthesizing, filter out irrelevant ones, then compact-synthesize the rest.

## Interaction with retrieval

Retrieval decides *what* to feed the synthesizer. Synthesis decides *how* to collapse those chunks into one answer. Both matter:
- Bad retrieval + great synthesis = confidently wrong answer.
- Great retrieval + bad synthesis = right info, incoherent output.

Evaluate them separately when debugging quality.

## Takeaway

Response synthesis is the part of RAG that most prototypes ignore ("just stuff chunks into one prompt"). Swapping in `compact` or `tree_summarize` when you outgrow the one-shot pattern is a lightweight upgrade with real quality gains.
