# Anthropic Citations — Summary

**Source:** Anthropic docs, "Citations"
**URL:** https://docs.anthropic.com/en/docs/build-with-claude/citations
**Type:** Vendor documentation (summary, own words)

## What it is

Citations is a server-side feature that makes Claude cite the exact source chunks that support each claim in its answer. You pass documents as structured content; Claude's response contains `citation` blocks that reference specific character spans in those documents.

## How to enable

Mark document content blocks with `citations: {enabled: true}`:

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {"type": "text", "media_type": "text/plain", "data": long_text},
                    "title": "RAG paper",
                    "context": "Lewis et al. 2020",
                    "citations": {"enabled": True},
                },
                {"type": "text", "text": "What is RAG?"},
            ],
        }
    ],
)
```

## Response shape

Each `text` block in the response may carry `citations`: an array of objects pointing at the source document by index + character range.

```json
{
  "type": "text",
  "text": "RAG retrieves relevant passages...",
  "citations": [
    {
      "type": "char_location",
      "document_index": 0,
      "document_title": "RAG paper",
      "start_char_index": 420,
      "end_char_index": 512,
      "cited_text": "...retrieves relevant passages..."
    }
  ]
}
```

## Why it matters

Three things an honest RAG system needs:
1. **Answer.**
2. **Sources it used.**
3. **Evidence that *that* specific claim came from *that* specific passage.**

Most RAG systems do 1 and 2. Citations does 3 — and does it with character-level precision, not whole-document.

## Supported document types

- Plain text.
- PDFs (multi-page).
- Custom content blocks (array of text blocks with indices).

## Cost

Enabling citations adds small overhead in output tokens (the citation markers). No input-side premium.

## Limits

- Only works when documents are passed as `document` content blocks — not when you manually stuff chunks into a user message.
- Citation granularity follows how you chunked: if you pass whole documents, citations span paragraphs; if you pass sentence-level chunks, citations are tight.

## Practical pattern for portfolio RAG

If your retrieval already chunks into 200–500 token pieces, pass each chunk as its own document block with citations enabled. Claude's answer then has tight, auditable pointers — much better story to tell a recruiter than ad-hoc `[source]` markers in the output string.

## Comparison to manual citation prompting

- **Manual:** "Cite sources as [filename]. " — the model complies, sometimes. Hallucinated citations are common.
- **Citations API:** server-side, Claude cannot cite a range that does not exist in the provided documents. This is the structural guarantee manual prompting cannot offer.
