"""Fill the score / hallucinated columns for rows the automated judge
could not score (ran out of OpenRouter free-tier quota at row 13).

Scores for q13-q30 were assigned by the session-level assistant
(Claude Opus 4.7 acting as a second judge). Rubric identical to
`eval/judge.py`:
    0 = wrong / contradicts gold
    1 = partially correct; or missing inline citation
    2 = correct AND cites at least one relevant retrieved source
"""

import sys

import pandas as pd

# (id, score, hallucinated, explanation)
MANUAL = [
    ("q13", 2, False, "Correct: angle, L2-normalized, dot-product equivalence, FAISS/Chroma. Cites [source: openai-embeddings-cookbook.md]."),
    ("q14", 2, False, "Correct: server-side, document blocks, character-level citation spans. Cites anthropic-citations.md."),
    ("q15", 2, False, "Correct MMR definition with formula and lambda tradeoff. Cites mmr-reranking.md with section refs."),
    ("q16", 1, False, "Correct formula and algorithm. Citation not in expected [source] format; partial."),
    ("q17", 1, False, "Correct: cache_control, ephemeral, 4 blocks, 1024/2048 tokens. No inline citation format."),
    ("q18", 1, False, "Correct tool-use flow with code example. Missing inline [source] citation."),
    ("q19", 2, False, "Correct: PersistentClient(path=...), SQLite + vector segments. Cites chromadb-quickstart.md."),
    ("q20", 1, False, "Correct deploy steps. Missing inline [source] citation."),
    ("q21", 2, False, "Correct ReAct loop: Thought/Action/Observation/Finish. Cites react-paper.md."),
    ("q22", 2, False, "Correct: thinking={'type':'enabled', 'budget_tokens':N}, budget < max_tokens. Cites anthropic-extended-thinking.md."),
    ("q23", 2, False, "Correct: grounding, NLI, LLM-judge, self-consistency. Cites hallucination-detection.md."),
    ("q24", 2, False, "Correct LlamaIndex MMR config with mmr_threshold semantics. Cites llamaindex-retriever-modes.md."),
    ("q25", 1, False, "Correct hybrid retrieval code. Missing inline [source] citation on key claims."),
    ("q26", 2, False, "Correct distinction tool-use vs extended-thinking. Cites both anthropic-tool-use and anthropic-extended-thinking."),
    ("q27", 1, False, "Correct LangChain vs LlamaIndex comparison table. Missing inline [source] citation."),
    ("q28", 1, False, "Correct refine vs tree_summarize tradeoffs. Missing inline [source] citation."),
    ("q29", 2, False, "Correct RAG vs fine-tuning guidance per Eugene Yan. Cites eugene-yan-rag-patterns.md."),
    ("q30", 1, False, "Correct MMR vs cross-encoder tradeoff table. Missing inline [source] citation."),
]


def main(csv_path: str):
    df = pd.read_csv(csv_path)
    applied = 0
    for qid, score, halluc, expl in MANUAL:
        mask = df["id"] == qid
        if not mask.any():
            print(f"warn: {qid} not in CSV")
            continue
        df.loc[mask, "score"] = score
        df.loc[mask, "hallucinated"] = halluc
        df.loc[mask, "judge_explanation"] = f"opus-as-judge: {expl}"
        applied += 1
    df.to_csv(csv_path, index=False)
    print(f"Filled {applied} rows in {csv_path}")

    valid = df[df["score"].notna()]
    print(f"\nTotal scored: {len(valid)}/{len(df)}")
    mean = valid["score"].astype(float).mean()
    halluc_rate = valid["hallucinated"].astype(bool).sum() / len(valid)
    print(f"Mean score: {mean:.2f}/2")
    print(f"Hallucination rate: {halluc_rate:.1%}")
    print(f"p50 latency: {valid['latency_ms'].median():.0f}ms")
    print(f"Mean tokens: in={valid['input_tokens'].mean():.0f} out={valid['output_tokens'].mean():.0f}")
    print()
    print("By type:")
    for t, g in valid.groupby("type"):
        print(f"  {t}: {g['score'].astype(float).mean():.2f} ({len(g)} Qs)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "eval/results_1776961397_judged.csv")
