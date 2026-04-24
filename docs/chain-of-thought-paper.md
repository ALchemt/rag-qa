# Chain-of-Thought Prompting — Summary

**Source:** Wei et al. 2022, "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (NeurIPS)
**URL:** https://arxiv.org/abs/2201.11903
**Type:** Foundational paper (summary, own words)

## Core finding

Adding intermediate reasoning steps into few-shot exemplars dramatically improves LLM performance on multi-step problems — **only for models above ~62B parameters**.

## The prompt pattern

Standard few-shot:
```
Q: Roger has 5 tennis balls. He buys 2 cans. Each can has 3 balls. How many balls?
A: 11.
```

Chain-of-thought:
```
Q: Roger has 5 tennis balls. He buys 2 cans. Each can has 3 balls. How many balls?
A: Roger starts with 5 balls. 2 cans × 3 balls = 6 balls. 5 + 6 = 11. The answer is 11.
```

The model, given enough scale, imitates the reasoning pattern on new questions.

## Where it helps

- **Arithmetic:** GSM8K solve rate jumps from ~18% to ~57% on PaLM-540B.
- **Commonsense:** StrategyQA, Date Understanding gain significantly.
- **Symbolic:** last-letter concatenation, coin flip tracking.

## Where it does not

- Tasks under the emergence threshold — smaller models often get *worse* with CoT.
- Tasks that do not decompose into steps (sentiment, simple classification).

## Emergence

CoT is the canonical example of an "emergent" ability: the behavior does not appear in smaller models and cannot be extrapolated from their scaling curves. It shows up around 60B+ parameters.

## Zero-shot CoT

Kojima et al. 2022 showed that appending "Let's think step by step." to a zero-shot prompt produces CoT-like reasoning without exemplars — less effective than few-shot CoT but a free win.

## Self-consistency

Wang et al. 2022: sample multiple CoT chains, take the majority answer. Boosts accuracy further at the cost of N× inference.

## Practical use today

- Modern frontier LLMs (Claude, GPT-4, Gemini) do CoT implicitly — extended thinking / reasoning modes are productized CoT.
- For production RAG: CoT is still useful in the synthesis step ("first list the relevant facts from context, then answer").
- CoT is a prerequisite for ReAct (reasoning + acting).

## Takeaway

CoT was the first clear demonstration that *how you prompt* matters more than you think — the same model can be dumb or smart depending on whether you surface its reasoning. It seeded the entire "prompt engineering" discipline.
