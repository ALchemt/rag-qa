# Karpathy: State of GPT — Summary

**Source:** Andrej Karpathy, "State of GPT" talk (Microsoft Build 2023, updated lectures 2024)
**URL:** https://www.youtube.com/watch?v=bZQun8Y4L2A
**Type:** Technical talk (summary, own words)

## The 4-stage training pipeline

Karpathy breaks LLM training into four stages. Each has a clear purpose and distinct data requirements.

### 1. Pretraining

- Raw text from the internet, trillions of tokens.
- Objective: next-token prediction.
- Produces a **base model** — knows a lot, but responds like a text completer, not a helpful assistant.
- Expensive: $1M–$100M for frontier-scale runs.

### 2. Supervised Fine-Tuning (SFT)

- Hand-curated prompt → ideal-response pairs, maybe 10k–1M examples.
- Objective: same next-token prediction, but on clean, high-quality demonstrations of desired behavior.
- Produces a **SFT model** — responds helpfully to instructions.
- Cheap relative to pretraining (single-digit GPU-hours to days).

### 3. Reward Modeling

- Collect human comparisons: given a prompt and N candidate responses, rank them.
- Train a reward model to predict the human ranking.
- Produces a **reward model** — a proxy for human preferences.

### 4. Reinforcement Learning from Human Feedback (RLHF) / DPO

- Use the reward model to fine-tune the SFT model via policy-gradient RL (PPO) or direct preference optimization (DPO).
- Objective: generate responses that score highly on the reward model.
- Produces the **RLHF model** — the one you actually ship (ChatGPT, Claude, Gemini).

## Key observations

### Base vs. RLHF models behave very differently

- Base model: completes text. "The capital of France is" → "Paris, with a population..."
- RLHF model: responds as an assistant. Same prompt → "The capital of France is Paris."

For most API work you want the RLHF model. Base models are useful for: scientific probing, in-context learning experiments, generating diverse completions.

### RLHF is narrow

Alignment via RLHF is a thin coat of paint over a much larger pretrained distribution. The base model still "knows" how to be unsafe; RLHF discourages it. Jailbreaks exploit this asymmetry.

### Emergent abilities come from scale + pretraining

Chain-of-thought, few-shot learning, arithmetic — none of these are SFT targets. They emerge from pretraining scale. SFT + RLHF shape *how* the model responds, not *what* it knows.

## Practical implications

- **Prompt engineering ≈ exploiting what pretraining encoded.** You cannot prompt a base model into answering questions it was never exposed to.
- **Fine-tuning ≈ SFT on your specific task.** Works well for changing style, tone, output format. Less effective at injecting *new* knowledge — for that, use RAG.
- **RAG ≈ dynamic fine-tuning at inference time.** You do not change weights; you change context. Cheaper, faster, more auditable.

## Why RAG beats fine-tuning for most use cases

Knowledge that changes (docs, tickets, prices) should live outside the model, not inside. Fine-tuning bakes knowledge in — a one-way door, expensive to update. RAG makes knowledge swappable with a re-index.

## Takeaway

Understanding the 4-stage pipeline changes how you read every LLM headline. "New model X beats Claude on benchmark Y" — which stage is responsible? Is it better pretraining (fundamental capability gain), better SFT (better at following instructions), better RLHF (better at *seeming* helpful)? The answer changes what the result means for your application.
