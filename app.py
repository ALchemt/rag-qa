"""Streamlit entrypoint for RAG Document Q&A.

Hugging Face Spaces convention: `app.py` at repo root.

Run locally:
    streamlit run app.py
"""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="RAG Document Q&A", page_icon="📚", layout="wide")


@st.cache_resource(show_spinner="Building index (one-time, ~30s)...")
def ensure_index():
    """Build ChromaDB index on first launch if not present.

    HF Spaces starts from a clean checkout without chroma_db/; this builds
    once at startup and caches the resource for the container's lifetime.
    """
    chroma_path = Path(os.getenv("CHROMA_PATH", "./chroma_db"))
    if not chroma_path.exists() or not any(chroma_path.iterdir()):
        from src.indexer import build_index
        build_index()
    return True


ensure_index()

from src.generator import answer as generate_answer
from src.retriever import retrieve

st.title("📚 RAG Document Q&A")
st.caption(
    "Ask questions about AI engineering. Answers grounded in a curated corpus "
    "of foundational papers + practical cookbooks. "
    "[Source & eval on GitHub](https://github.com/ALchemt)"
)

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        - **Stack:** LlamaIndex · ChromaDB · Claude API · Streamlit
        - **Corpus:** ~25 curated docs (RAG/ReAct/Anthropic docs/Karpathy)
        - **Eval:** see README for accuracy/latency/cost table
        """
    )
    st.markdown("---")
    st.caption("Portfolio project by Andrey Ovsyannikov")

question = st.text_input(
    "Question",
    placeholder="What is RAG and when should I use it?",
    key="q",
)

if st.button("Ask", type="primary") or question:
    if not question.strip():
        st.info("Type a question above.")
        st.stop()

    with st.spinner("Retrieving..."):
        chunks = retrieve(question)

    if not chunks:
        st.warning("No chunks retrieved. Is the index built? Run `python -m src.indexer`.")
        st.stop()

    with st.spinner("Generating..."):
        result = generate_answer(question, chunks)

    st.markdown("### Answer")
    st.markdown(result.text)

    col1, col2, col3 = st.columns(3)
    col1.metric("Input tokens", result.input_tokens)
    col2.metric("Output tokens", result.output_tokens)
    col3.metric("Cached tokens", result.cached_tokens)

    with st.expander(f"Sources ({len(chunks)})"):
        for i, c in enumerate(chunks, start=1):
            st.markdown(f"**{i}. {c.source}** — score {c.score:.3f}")
            st.text(c.text[:500] + ("..." if len(c.text) > 500 else ""))
            st.markdown("---")
