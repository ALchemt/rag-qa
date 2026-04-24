# Evaluating LLMs — Overview

**Source:** Composite of practitioner write-ups (Hamel Husain, Eugene Yan, Anthropic, OpenAI)
**URL:** Multiple — see individual blog posts in this corpus
**Type:** Overview / own synthesis

## Why eval matters

Without eval, there is no engineering — only vibes. The single biggest difference between a demo and a production LLM system is that the production one has an eval harness telling you whether changes are improvements or regressions.

Quote from Hamel Husain that practitioners repeat: *"Your eval is your test suite for the LLM era."*

## Three eval paradigms

### 1. Reference-based

You have a gold-standard answer. Compare model output to it.
- **Metrics:** BLEU, ROUGE, exact match, F1 token overlap.
- **Use when:** deterministic tasks (translation, extraction).
- **Breaks on:** open-ended generation where there are many valid answers.

### 2. Reference-free / rubric-based

Score output against a rubric — correctness, relevance, style, faithfulness.
- **Human scoring:** gold standard, slow, expensive, non-scalable.
- **LLM-as-judge:** ask a strong model to score with a defined rubric. Cheap and scalable, but inherits the judge's biases.
- **Hybrid:** human-score a small gold set, auto-score the rest with a judge, spot-check.

### 3. Behavioral / adversarial

- **Red teaming:** deliberately craft inputs that break the model (jailbreaks, confusing queries, edge cases).
- **Regression suites:** known-bad inputs from past failures; every release must still handle them.

## RAG-specific metrics

RAG breaks into two subsystems; evaluate each separately.

**Retrieval metrics:**
- **Recall@k** — does the top-k contain the ground-truth passage?
- **MRR (Mean Reciprocal Rank)** — how high up in top-k is the relevant passage?
- **nDCG** — graded relevance, for multi-level judgments.

**Generation metrics:**
- **Faithfulness** — does the answer contain only facts supported by retrieved context?
- **Relevance** — does the answer address the question?
- **Correctness** — is the answer right (compared to a gold answer)?

Faithfulness is the RAG-specific metric that catches hallucinations. A high correctness / low faithfulness score means the model happened to know the right answer without help from retrieval — a red flag for deployment.

## Frameworks

- **RAGAS** — Python library implementing the faithfulness / relevance / context-recall triad with LLM-as-judge.
- **LlamaIndex Evaluation** — built-in `FaithfulnessEvaluator`, `RelevancyEvaluator`, `CorrectnessEvaluator`.
- **DeepEval** — pytest-like framework for LLM tests.
- **Custom pandas CSV + rubric + spreadsheet** — underrated baseline. For < 100 test cases, a pandas DataFrame and a human scoring pass beats any framework.

## Practical workflow

1. **Write eval before the code.** Even 10 examples.
2. **Score baseline.** Run current system on the 10 examples. See what breaks.
3. **Ship a fix, rerun eval.** If numbers get worse, reject the change.
4. **Grow the set slowly.** When you find a real-world failure, add it to the eval as a regression test.
5. **LLM-as-judge cautiously.** Validate the judge on the subset humans have scored. Judges drift; re-validate every few months.

## Anti-patterns

- Eval on training-distribution-only data. You will be shocked in production.
- Single-metric evals. Accuracy alone hides hallucinations. Always pair with faithfulness.
- Skipping latency and cost. A system that is 5% more accurate but 3× slower may be a regression in practice.

## Takeaway

Eval is the real work of building a RAG system. Chunking, model choice, reranking — all knobs whose settings only matter if you can measure their effect. Start with 30 examples and a rubric; grow from there.
