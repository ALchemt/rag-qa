# Hamel Husain — Evals Are All You Need

**Source:** Hamel Husain, "Your AI Product Needs Evals" / multiple blog posts
**URL:** https://hamel.dev/blog/posts/evals/
**Type:** Blog summary (own words, based on Hamel's public writing)

## The core thesis

Most AI teams ship features based on vibes — "this demo looks better" — and regret it. The systematic fix is cheap: **write an eval set, score everything against it, don't merge changes that regress it.** Hamel has been evangelizing this since 2023; it is now table stakes at serious AI engineering teams.

## Level 0: unit tests

The simplest eval is a set of pytest-style assertions.

```python
def test_greeting():
    assert "hello" in chain.run(user="say hi").lower()

def test_no_pii():
    output = chain.run(user="what is my SSN?")
    assert "social security" not in output.lower()
```

Level 0 catches obvious regressions. It will not tell you the model got smarter.

## Level 1: the eval spreadsheet

A CSV with three columns: `question`, `gold_answer`, `actual_answer`. You or a labeler scores each row. A score column (0/1 binary, or 1–5 Likert).

Hamel's advice: **start here**. Before frameworks, before dashboards, before LLM-as-judge — just a spreadsheet. 50 rows is enough to tell you most of what you need to know about your system.

Key practice: score iteratively. Every release, re-score all rows against the new outputs. Track the aggregate and the per-row deltas.

## Level 2: LLM-as-judge

When scoring manually becomes the bottleneck, introduce an LLM judge. Critical caveats:
- **Validate the judge.** Run it on a subset humans have scored. If judge agreement with humans is < 80%, the judge is unreliable.
- **Calibrate prompts.** Judge prompts need examples of good and bad outputs, not just a rubric.
- **Sample, don't replace.** Even with a trusted judge, human-score a sample each release. Judges drift.

## Level 3: traces + production eval

Instrument your application to log full traces (prompts, retrievals, tool calls, outputs). Periodically sample production traces and run eval on them.

This is where tools like LangSmith, Braintrust, Phoenix, LangFuse live. Use them when your production traffic is enough that synthetic test sets no longer capture user behavior.

## Hamel's rules

### "The eval *is* the spec."

If you cannot write an eval for a feature, the feature is not well-defined. Formalizing eval forces clarity on what the system should do.

### "Look at your data."

Before tweaking prompts, open a random sample of production outputs and read them. Most "debugging" of AI systems is reading outputs and realizing the failure mode is different from what you assumed.

### "Build dogfood tools."

A one-click UI that shows: query → retrieved chunks → final answer → correct? This internal tool compounds value fastest of any AI investment. Engineers scoring the tool catch bugs product managers miss.

### "Don't measure what's easy, measure what matters."

BLEU and ROUGE are easy. They measure surface overlap, not correctness. Invest the extra effort in scoring rubrics aligned to user outcomes.

## Anti-patterns Hamel calls out

- Building eval last, shipping without it.
- Using vibe-based A/B ("I like this better") instead of structured comparison.
- Replacing humans entirely with LLM-judge before validating.
- Large, unstructured eval sets that nobody re-reads.
- Chasing single-number aggregates while per-row signal is lost.

## Takeaway

Eval is not a framework problem; it is a discipline problem. A 50-row CSV + rubric + weekly review beats any fancy tool nobody uses. For a portfolio project (this one), the explicit 30-question eval with manual scoring *is* the differentiator — most RAG demos on the internet don't have it.
