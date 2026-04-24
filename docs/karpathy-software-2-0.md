# Karpathy: Software 2.0 — Summary

**Source:** Andrej Karpathy, "Software 2.0" blog post (2017)
**URL:** https://karpathy.medium.com/software-2-0-a64152b37c35
**Type:** Conceptual essay (summary, own words)

## The claim

Software is bifurcating into two stacks:
- **Software 1.0:** code written by humans. Python, C, JavaScript — instructions executed literally by a CPU.
- **Software 2.0:** code written by *optimization* — neural net weights, learned from data. The CPU-equivalent is matrix multiplications on a GPU.

You do not *write* Software 2.0. You specify a dataset, a loss function, and an architecture; gradient descent writes the code.

## Properties that differ

| Property | Software 1.0 | Software 2.0 |
|---|---|---|
| How written | By programmers | By optimization from data |
| Source form | Source files | Weights |
| Runtime | CPU instructions | GPU / NPU tensor ops |
| Debugging | Step through code | Probe representations, dataset audits |
| Reproducibility | Deterministic | Seed-dependent, hardware-dependent |
| Version control | Git | Weight checkpoints + dataset versioning |
| Refactoring | Rename, restructure | Re-train, distill |

## Why it matters for AI engineers

Large parts of what used to be explicit code are being replaced by neural net components:
- Image recognition: no more hand-written filters — train a CNN.
- Translation: no more grammar rules — train a seq2seq.
- Speech: no more phoneme pipelines — train end-to-end.
- Now: LLMs consume whole categories of business logic (classification, extraction, routing) that used to be `if/elif` trees.

## Implications for RAG engineers

- The retrieval layer is 1.0 (indexes, filters, BM25). The generation layer is 2.0 (LLM weights).
- When your RAG system misbehaves, ask: is this a 1.0 bug (wrong chunk retrieved, bad metadata) or a 2.0 problem (the model interprets context oddly)? Fix accordingly.
- Eval is the 2.0 equivalent of unit tests. Without eval, you cannot ship 2.0 safely.

## Karpathy's broader prediction

The "compile target" of more and more human effort is shifting from code to *datasets and evals*. The programmer of 2030 may spend most of the day curating data, designing evals, and writing one-pagers that steer model behavior — not typing `for` loops.

This is already visible in AI engineer job descriptions: dataset curation, eval design, and prompt engineering are growing line items.

## Caveats

- 1.0 is not going away. Security, systems, OS, compilers, databases remain human-written for good reasons.
- 2.0 does not literally generalize. A model trained on dataset X fails in distribution Y — this is a 1.0-free problem but it *is* a problem.
- Pure 2.0 solutions are opaque. Hybrid 1.0+2.0 (symbolic + learned) is often more debuggable and often wins in production.

## Takeaway for a portfolio

RAG systems are canonical hybrids: 1.0 retrieval (explicit, debuggable, cheap) + 2.0 generation (learned, powerful, expensive). Understanding where each half lives — and which kind of bug you are chasing — is what senior AI engineers are paid to do.
