"""Run evaluation on eval/test_set.jsonl and write results CSV.

Manual scoring convention (fill scores after run):
    0 = wrong or hallucinated
    1 = partial
    2 = correct + correctly cited

Usage:
    python -m eval.run_eval
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd

from src.generator import answer as generate_answer
from src.retriever import retrieve

TEST_SET = Path(__file__).parent / "test_set.jsonl"
RESULTS = Path(__file__).parent / f"results_{int(time.time())}.csv"


def run():
    rows = []
    with TEST_SET.open() as f:
        tests = [json.loads(line) for line in f if line.strip()]

    for t in tests:
        t0 = time.time()
        chunks = retrieve(t["question"])
        result = generate_answer(t["question"], chunks)
        latency_ms = int((time.time() - t0) * 1000)

        rows.append(
            {
                "id": t["id"],
                "question": t["question"],
                "type": t["type"],
                "gold_answer": t["gold_answer"],
                "expected_source": t.get("expected_source", ""),
                "answer": result.text,
                "retrieved_sources": ";".join(s.source for s in chunks),
                "latency_ms": latency_ms,
                "input_tokens": result.input_tokens,
                "output_tokens": result.output_tokens,
                "cached_tokens": result.cached_tokens,
                "score": "",
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv(RESULTS, index=False)
    print(f"Wrote {len(rows)} results to {RESULTS}")
    print("Next: open the CSV, fill the `score` column (0/1/2), rerun summary.")


if __name__ == "__main__":
    run()
