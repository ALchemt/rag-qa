# RAGAS — Framework Notes

**Source:** Shahul Es et al., "RAGAS: Automated Evaluation of Retrieval Augmented Generation"
**URL:** https://arxiv.org/abs/2309.15217 and https://docs.ragas.io/
**Type:** Framework notes (summary, own words)

## What RAGAS is

RAGAS is a Python library for evaluating RAG systems using LLM-as-judge. It operationalizes four canonical RAG metrics as composable evaluators, so you can point it at a test set + your RAG pipeline and get a scorecard.

## The four core metrics

### Faithfulness

*Does the answer stay grounded in the retrieved context?*

1. Decompose the generated answer into atomic claims.
2. For each claim, check via LLM whether the retrieved context supports it.
3. Score = (supported claims) / (total claims).

Low faithfulness = hallucination. This is the metric RAG teams track most closely.

### Answer Relevance

*Does the answer actually address the question?*

1. Generate N candidate questions from the answer alone (via LLM).
2. Embed the original question + each generated question.
3. Score = mean cosine similarity.

Low answer relevance = answer is off-topic, padded, or avoids the question.

### Context Precision

*Are the retrieved chunks useful, and ranked well?*

1. For each retrieved chunk, LLM-judge whether it is relevant to the question.
2. Weight by position (earlier relevant chunks count more).
3. Score reflects whether the retrieval ranker is surfacing useful results at the top.

Low context precision = retrieval is returning noise or bad ordering.

### Context Recall

*Did retrieval capture all the information needed to answer?*

1. From the ground-truth answer, decompose into claims.
2. For each claim, check via LLM whether it is present in the retrieved context.
3. Score = (claims present in context) / (total claims).

Low context recall = retrieval missed passages that would have been needed.

## Why this matrix is powerful

The four metrics form a 2×2:

|  | Retrieval | Generation |
|---|---|---|
| Precision-like | Context Precision | Faithfulness |
| Recall-like | Context Recall | Answer Relevance |

You can diagnose where your system breaks:
- Faithfulness low, Context Precision high → generator is hallucinating despite good context. Prompt issue, or model too weak.
- Faithfulness high, Context Recall low → answers are grounded but incomplete. Improve retrieval k, chunking, or query rewriting.
- Answer Relevance low, Faithfulness high → answers are technically grounded but off-topic. System prompt issue, answer formatting issue.

This decomposition beats single-number accuracy for debugging.

## How to use it

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

dataset = ... # HF Datasets with question, answer, contexts, ground_truth
result = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])
print(result)
```

## Cost and caveats

- LLM-as-judge under the hood — every metric is another LLM call per example. 100 examples × 4 metrics = 400 judge calls.
- Judge choice matters. GPT-4 / Claude as judge is strong; smaller models drift.
- Bootstrap confidence intervals on the scores; variance between judge runs is non-trivial.

## Alternatives

- **LlamaIndex Evaluation module** — similar metrics, native integration if you already use LlamaIndex.
- **DeepEval** — pytest-style, integrates with CI naturally.
- **Trulens** — observability + eval, strong on tracing.

## When to adopt RAGAS

- You have >30 eval examples and manual scoring is painful.
- You need a shared vocabulary with stakeholders ("our faithfulness is 0.89, last week it was 0.76").
- You want metrics that are comparable across changes to your retrieval or generator.

Do not adopt if:
- You have <20 examples. Score manually. The signal is stronger, the vocabulary is your own.
- Your task is not classical RAG (e.g., agentic multi-hop, tool-heavy). RAGAS metrics assume one-shot retrieval.
