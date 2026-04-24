"""Generate answer via an OpenAI-compatible LLM provider.

Supported providers (auto-detected from env in priority order):
  1. GROQ_API_KEY       -> Groq Cloud (Llama 3.3 70B, high free rate limit)
  2. OPENROUTER_API_KEY -> OpenRouter (gpt-oss-120b:free default, 200/day free)
  3. HF_TOKEN           -> Hugging Face Inference Providers (legacy)

Models are OpenAI-compatible — same client, different base_url.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI

from src.retriever import Chunk

load_dotenv()


def _build_client() -> tuple[OpenAI, str]:
    """Return (client, default_model) based on which API key is configured."""
    model_override = os.getenv("LLM_MODEL")

    if os.getenv("GROQ_API_KEY"):
        client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ["GROQ_API_KEY"],
        )
        return client, model_override or "llama-3.3-70b-versatile"

    if os.getenv("OPENROUTER_API_KEY"):
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )
        return client, model_override or "openai/gpt-oss-120b:free"

    if os.getenv("HF_TOKEN"):
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.environ["HF_TOKEN"],
        )
        return client, model_override or "meta-llama/Llama-3.3-70B-Instruct:together"

    return None, ""


_client, _model = _build_client()


SYSTEM_PROMPT = """You answer questions about AI engineering using ONLY the provided context chunks.

Rules:
1. If the answer is not in the context, say "Not found in the indexed corpus." Do not speculate.
2. Cite sources inline using [source_filename] after each claim.
3. Be concise. Prefer bullet points for procedural questions.
4. If multiple sources agree, cite all of them. If they disagree, note the disagreement.

You are a helpful technical assistant for a junior AI engineer ramping up."""


@dataclass
class Answer:
    text: str
    sources: list[str]
    input_tokens: int
    output_tokens: int
    cached_tokens: int


def _format_context(chunks: list[Chunk]) -> str:
    parts = []
    for i, c in enumerate(chunks, start=1):
        parts.append(f"[chunk {i} | source: {c.source} | score: {c.score:.3f}]\n{c.text}\n")
    return "\n---\n".join(parts)


def answer(question: str, chunks: list[Chunk]) -> Answer:
    if _client is None:
        raise RuntimeError(
            "No LLM provider configured. Set one of GROQ_API_KEY, "
            "OPENROUTER_API_KEY, or HF_TOKEN in .env."
        )

    context_block = _format_context(chunks)
    user_msg = f"Context:\n\n{context_block}\n\nQuestion: {question}"

    resp = _client.chat.completions.create(
        model=_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=1024,
        temperature=0.0,
    )

    text = resp.choices[0].message.content or ""
    sources = sorted({c.source for c in chunks})
    usage = resp.usage

    return Answer(
        text=text,
        sources=sources,
        input_tokens=getattr(usage, "prompt_tokens", 0) or 0,
        output_tokens=getattr(usage, "completion_tokens", 0) or 0,
        cached_tokens=0,
    )
