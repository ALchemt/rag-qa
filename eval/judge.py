"""LLM-as-judge auto-scoring for eval results CSV.

Conscious v1 tradeoff: manual scoring is the gold standard per the spec,
but running judge auto-scoring lets us fill the README table without
blocking on a human rater. Results are labeled as judge-scored (not
human-validated) in the README.

Uses the same OpenAI-compatible provider selection as src/generator.py.
For v1 we use the same model as the generator — a known self-bias —
which is noted explicitly in the "What I'd do differently" section.

Usage:
    python -m eval.judge eval/results_<timestamp>.csv
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _build_client() -> tuple[OpenAI, str]:
    model_override = os.getenv("JUDGE_MODEL")
    if os.getenv("GROQ_API_KEY"):
        return (
            OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.environ["GROQ_API_KEY"]),
            model_override or "llama-3.3-70b-versatile",
        )
    if os.getenv("OPENROUTER_API_KEY"):
        return (
            OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"]),
            model_override or "openai/gpt-oss-120b:free",
        )
    raise SystemExit("No LLM provider configured.")


_client, _model = _build_client()


JUDGE_PROMPT = """You are evaluating a RAG system's answer.

Given:
- Question
- Gold answer (reference)
- System answer
- Retrieved source filenames

Score the system answer on TWO dimensions:

1. CORRECTNESS (0/1/2):
   0 = wrong, missing key facts, or contradicts the gold answer
   1 = partially correct; gets the gist but misses details or cites wrong
   2 = correct AND cites at least one relevant source from the retrieved list

2. HALLUCINATED (true/false):
   true = answer states specific facts that are not in the retrieved sources
   false = all factual claims are traceable to the retrieved sources, OR the answer correctly says "not found"

Respond with ONLY a JSON object, no prose, no markdown:
{"score": 0|1|2, "hallucinated": true|false, "explanation": "<1 sentence>"}"""


def score_row(row: dict) -> dict:
    user_msg = f"""Question: {row['question']}

Gold answer: {row['gold_answer']}

System answer: {row['answer']}

Retrieved sources: {row['retrieved_sources']}"""

    resp = _client.chat.completions.create(
        model=_model,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=250,
        temperature=0.0,
    )
    text = resp.choices[0].message.content or ""

    match = re.search(r"\{[^{}]*\"score\"[^{}]*\}", text, re.DOTALL)
    if not match:
        return {"score": None, "hallucinated": None, "explanation": f"parse_fail: {text[:100]}"}
    try:
        parsed = json.loads(match.group(0))
        return {
            "score": int(parsed.get("score", 0)),
            "hallucinated": bool(parsed.get("hallucinated", False)),
            "explanation": str(parsed.get("explanation", ""))[:200],
        }
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        return {"score": None, "hallucinated": None, "explanation": f"parse_fail: {e}"}


def run(input_csv: str):
    df = pd.read_csv(input_csv)
    print(f"Judging {len(df)} rows with {_model}...")

    scores, hallucs, explanations = [], [], []
    for i, row in df.iterrows():
        t0 = time.time()
        try:
            result = score_row(row.to_dict())
        except Exception as e:
            result = {"score": None, "hallucinated": None, "explanation": f"api_error: {e}"}
        scores.append(result["score"])
        hallucs.append(result["hallucinated"])
        explanations.append(result["explanation"])
        print(f"  {i+1}/{len(df)} {row['id']}: score={result['score']} halluc={result['hallucinated']} ({int((time.time()-t0)*1000)}ms)")

    df["score"] = scores
    df["hallucinated"] = hallucs
    df["judge_explanation"] = explanations

    output_csv = input_csv.replace(".csv", "_judged.csv")
    df.to_csv(output_csv, index=False)
    print(f"\nWrote {output_csv}")

    valid = df[df["score"].notna()]
    print("\n--- Summary ---")
    print(f"Scored: {len(valid)}/{len(df)}")
    if len(valid) > 0:
        mean_score = valid["score"].astype(float).mean()
        halluc_rate = valid["hallucinated"].astype(bool).sum() / len(valid)
        p50_lat = valid["latency_ms"].median()
        total_in = int(valid["input_tokens"].sum())
        total_out = int(valid["output_tokens"].sum())
        print(f"Mean score (/2): {mean_score:.2f}")
        print(f"Hallucination rate: {halluc_rate:.1%}")
        print(f"p50 latency: {p50_lat:.0f}ms")
        print(f"Mean tokens: in={valid['input_tokens'].mean():.0f} out={valid['output_tokens'].mean():.0f}")
        print(f"Totals: in={total_in} out={total_out}")

        # By question type
        print("\nBy type:")
        for t, g in valid.groupby("type"):
            print(f"  {t}: score={g['score'].astype(float).mean():.2f} ({len(g)} Qs)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m eval.judge <results.csv>")
        sys.exit(1)
    run(sys.argv[1])
